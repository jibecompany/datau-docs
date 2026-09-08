#!/usr/bin/env python3
"""Pad a screenshot clear of its device frame's notch, then frame it in black.

The `frames` CLI pastes a screenshot into a device bezel at a fixed offset. On
notched devices the bezel's notch is opaque and sits *over* the top of the
screenshot, hiding whatever is up there — a page title, a toast, a nav bar.

This script measures the notch from the frame asset itself (no hardcoded
numbers), shifts the screenshot's content down far enough to clear it, and then
calls `frames`. The shift is paid for by deleting the same number of rows from a
band of single-colour dead space further down, so the image keeps its original
resolution -- `frames` matches devices by exact pixel size, so changing the
height would stop it detecting the device.

Inputs are never modified; the padded image is written to a temp file unless
--keep-padded is given.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required:  pip install Pillow")

# Frame colours that read as black, best first. Devices without colour variants
# ignore --color, so passing it is always safe.
BLACK_PREFERENCE = ("Black", "Space Black", "Midnight", "Dark", "Graphite")

SAMPLE_STEP = 13   # px between sampled columns; exact-match work stays cheap
TOLERANCE = 8      # per-channel slack when deciding "same as the top row"
ALPHA_OPAQUE = 200


# --------------------------------------------------------------------------- #
# frames CLI

def frames_json(*args: str) -> dict:
    proc = subprocess.run(
        ["frames", "--json", *args], capture_output=True, text=True
    )
    if proc.returncode != 0:
        sys.exit(f"frames {' '.join(args)} failed:\n{proc.stderr or proc.stdout}")
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        sys.exit(f"frames {' '.join(args)} gave non-JSON output:\n{proc.stdout}")


def assets_dir() -> Path:
    return Path(frames_json("doctor")["assets_path"])


def frame_asset(device: str, assets: Path) -> Path | None:
    """The bezel PNG for a device. Colour variants are '<device> <Colour>.png'."""
    exact = assets / f"{device}.png"
    if exact.exists():
        return exact
    variants = sorted(
        p for p in assets.glob(f"{device}*.png") if not p.stem.endswith("_mask")
    )
    return variants[0] if variants else None


def pick_black(colors: list[str]) -> str:
    """Darkest available colour name, or 'Black' as a harmless default."""
    for want in BLACK_PREFERENCE:
        for c in colors:
            if c.lower() == want.lower():
                return c
    for c in colors:                       # e.g. "Aluminum Jet Black + ..."
        if "black" in c.lower():
            return c
    return "Black"


# --------------------------------------------------------------------------- #
# measurement

def notch_depth(asset: Path, screen_y: int) -> int:
    """How far the bezel intrudes below the top of the screen, in px.

    Walks down the frame's centre column from the screen's top edge for as long
    as the frame is opaque. Returns 0 for frames with no notch.
    """
    frame = Image.open(asset).convert("RGBA")
    width, height = frame.size
    px = frame.load()
    x = width // 2
    y = max(screen_y, 0)
    while y < height and px[x, y][3] > ALPHA_OPAQUE:
        y += 1
    return y - screen_y


def clear_top_rows(im: Image.Image) -> int:
    """Leading rows that look like the very top row.

    Works for a flat top and for a horizontal gradient alike: each row is
    compared against row 0 column by column, so only a *vertical* change counts
    as content.
    """
    rgb = im.convert("RGB")
    width, height = rgb.size
    px = rgb.load()
    xs = range(0, width, SAMPLE_STEP)
    ref = [px[x, 0] for x in xs]
    for y in range(height):
        for x, want in zip(xs, ref):
            got = px[x, y]
            if any(abs(a - b) > TOLERANCE for a, b in zip(got, want)):
                return y
    return height


def uniform_bands(im: Image.Image, min_len: int, below: int = 0):
    """Runs of rows that are all one flat colour, as (start, end, length).

    A row must be flat left-to-right *and* match the colour the band started
    with. Without that second test a run could straddle a colour boundary --
    two flat regions of different colours -- and cutting rows there would
    delete a real edge rather than dead space.
    """
    rgb = im.convert("RGB")
    width, height = rgb.size
    px = rgb.load()
    xs = list(range(SAMPLE_STEP, max(width - SAMPLE_STEP, SAMPLE_STEP + 1), SAMPLE_STEP))
    bands, start, band_color = [], None, None

    def close(run_end):
        if start is not None and run_end - start >= min_len:
            bands.append((start, run_end, run_end - start))

    for y in range(below, height):
        first = px[xs[0], y]
        flat = all(px[x, y] == first for x in xs)
        if flat and start is None:
            start, band_color = y, first
        elif start is not None and not (flat and first == band_color):
            close(y)
            # this row may itself begin a new band
            start, band_color = (y, first) if flat else (None, None)
    close(height)
    return sorted(bands, key=lambda b: b[2], reverse=True)


# --------------------------------------------------------------------------- #
# the shift

def shift_down(im: Image.Image, amount: int, band_start: int) -> Image.Image:
    """Move content down by `amount`, reclaiming the rows from `band_start`."""
    width, height = im.size
    filler = im.crop((0, 0, width, 1)).resize((width, amount), Image.NEAREST)
    out = Image.new(im.mode, (width, height))
    out.paste(filler, (0, 0))
    out.paste(im.crop((0, 0, width, band_start)), (0, amount))
    out.paste(im.crop((0, band_start + amount, width, height)), (0, amount + band_start))
    return out


def grow_top(im: Image.Image, amount: int) -> Image.Image:
    """Fallback: prepend rows. Changes the height, so `frames` may not match."""
    width, height = im.size
    filler = im.crop((0, 0, width, 1)).resize((width, amount), Image.NEAREST)
    out = Image.new(im.mode, (width, height + amount))
    out.paste(filler, (0, 0))
    out.paste(im, (0, amount))
    return out


# --------------------------------------------------------------------------- #

def process(path: Path, args, tmp: Path) -> bool:
    info = frames_json("info", str(path))
    device = info.get("device") or info.get("primary_match")
    if not device:
        print(f"  ! {path.name}: frames could not match a device "
              f"({info.get('width')}x{info.get('height')})")
        return False

    screen_y = int(info.get("y") or 0)
    colors = info.get("colors") or []
    color = pick_black(colors)
    print(f"  device      {device}  ({info['width']}x{info['height']}, "
          f"screen y={screen_y})")
    print(f"  colour      {color}" + ("" if colors else "  (device has no variants)"))

    asset = frame_asset(device, args.assets)
    if asset is None:
        print(f"  ! no frame asset found for {device!r}; framing without padding")
        depth = 0
    else:
        depth = notch_depth(asset, screen_y)
    print(f"  notch       {depth}px" + ("" if depth else "  (no notch)"))

    src = Image.open(path)
    to_frame, padded_path = path, None

    if depth:
        wanted = depth + args.clearance
        have = clear_top_rows(src)
        need = wanted - have
        print(f"  clear top   {have}px  (want {wanted} = {depth} + {args.clearance})")

        if need <= 0:
            print("  padding     not needed")
        else:
            bands = uniform_bands(src, need + args.band_margin, below=have)
            if bands:
                start, _end, length = bands[0]
                out = shift_down(src, need, start)
                print(f"  padding     +{need}px, taken from the {length}px band "
                      f"at y={start}  (size unchanged {out.size[0]}x{out.size[1]})")
            elif args.allow_resize:
                out = grow_top(src, need)
                print(f"  padding     +{need}px appended — NO dead space found, so "
                      f"the size changed to {out.size[0]}x{out.size[1]}; "
                      f"frames may no longer match the device")
            else:
                print(f"  ! need {need}px but found no dead band of "
                      f"{need + args.band_margin}px+. Skipped. Re-run with "
                      f"--allow-resize to append rows instead.")
                return False

            if args.dry_run:
                print("  (dry run — nothing written)")
                return True
            padded_path = (path.parent if args.keep_padded else tmp) / f"{path.stem}__padded.png"
            out.save(padded_path, optimize=True)
            to_frame = padded_path
            if args.keep_padded:
                print(f"  padded ->   {padded_path}")

    if args.dry_run:
        print("  (dry run — nothing written)")
        return True

    outdir = args.output or path.parent
    outdir.mkdir(parents=True, exist_ok=True)
    result = frames_json("frame", "--color", color, "--output", str(outdir), str(to_frame))
    produced = Path(result["output"])

    # frames names its output after the file it was given; restore the plain name
    final = produced
    if padded_path is not None:
        final = produced.with_name(f"{path.stem}_framed{produced.suffix}")
        produced.replace(final)
        if not args.keep_padded:
            padded_path.unlink(missing_ok=True)

    print(f"  framed ->   {final}  ({result['frame_size']}, colour={result['color']})")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Pad a screenshot clear of the device notch, then frame it in black.",
    )
    ap.add_argument("images", nargs="+", type=Path, help="screenshot files")
    ap.add_argument("-o", "--output", type=Path,
                    help="output directory (default: next to each input)")
    ap.add_argument("--clearance", type=int, default=24,
                    help="extra px between the notch and the content (default: 24)")
    ap.add_argument("--band-margin", type=int, default=40,
                    help="dead band must exceed the need by this much (default: 40)")
    ap.add_argument("--keep-padded", action="store_true",
                    help="keep the intermediate padded image next to the input")
    ap.add_argument("--allow-resize", action="store_true",
                    help="if there is no dead space, append rows and change the height")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would happen, write nothing")
    args = ap.parse_args()
    args.assets = assets_dir()

    ok = True
    for path in args.images:
        if not path.exists():
            print(f"{path}: not found")
            ok = False
            continue
        print(path.name)
        ok = process(path, args, Path(tempfile.gettempdir())) and ok
        print()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
