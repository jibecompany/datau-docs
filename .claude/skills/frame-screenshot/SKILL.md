---
name: frame-screenshot
description: Wrap a screenshot in a black Apple device bezel using the installed `frames` CLI, first shifting its content clear of the frame's notch if the notch would cover the header. Use when asked to frame a screenshot, add a device frame or bezel, mock up a screenshot, or when a framed screenshot's title/toast/nav bar is hidden behind the notch.
---

# Frame a screenshot

Screenshots in `docs/assets/` are shown in device bezels, produced by the
`frames` CLI (`frames --help`). `frames` pastes the screenshot into a bezel PNG
at a fixed offset — and on notched devices the notch is **opaque and sits over
the top of the screenshot**, hiding whatever is up there: a page title, a
success toast, an app nav bar.

Fixing that by hand means measuring the notch and nudging the content down.
This skill does both, then frames the result.

## Use it

```bash
python3 .claude/skills/frame-screenshot/pad_and_frame.py <image>...
```

Common forms:

```bash
# frame in place (writes <name>_framed.png next to the input)
python3 .claude/skills/frame-screenshot/pad_and_frame.py ~/Downloads/shot.png

# straight into the docs assets
python3 .claude/skills/frame-screenshot/pad_and_frame.py -o docs/assets ~/Downloads/*.png

# report what it would do, write nothing
python3 .claude/skills/frame-screenshot/pad_and_frame.py --dry-run shot.png
```

Requires Pillow. This repo's venv has it: `source .venv/bin/activate` first.

**Always run `--dry-run` first** and read the numbers back to the user before
writing — the shift is judged from pixel heuristics, and the dry run is how you
catch a bad device match or a missing dead band cheaply.

## What it does, per image

1. **Detects the device** — `frames --json info <file>`, which also reports the
   screen's offset inside the bezel. `frames` matches on exact pixel
   dimensions.
2. **Measures the notch** from the bezel PNG in the assets directory
   (`frames --json doctor` → `assets_path`), by walking down the frame's centre
   column from the screen's top edge for as long as the frame is opaque. Nothing
   is hardcoded, so each device gets its own number — an iPhone 12–13 Pro Max
   notch is 100px, a MacBook Pro M5 14 is 63px. Frames with no notch measure 0
   and skip straight to framing.
3. **Decides whether padding is needed.** It counts the leading rows that look
   like row 0 (compared column by column, so a horizontal gradient header still
   counts as empty — only a *vertical* change is content). If that already
   exceeds notch + clearance, nothing is shifted.
4. **Shifts the content down** by the shortfall, and pays for it by deleting the
   same number of rows from the largest band of dead space — a run of rows that
   are all one flat colour. **This keeps the original pixel dimensions**, which
   matters: `frames` identifies devices by exact size, so growing the image
   would break detection.
5. **Frames it** — `frames frame --color <black> --output <dir>`.

## Black frames

The frame colour is always the darkest the device offers, preferring
`Black`, then `Space Black`, `Midnight`, `Dark`, `Graphite`, then any name
containing "black". Devices with no colour variants (iPhone 12–13 Pro Max, for
one) ignore `--color` and report `colour=None` in the output — their bezel is
already black, so that is correct and not an error.

## Flags

| Flag | Default | Purpose |
| --- | --- | --- |
| `-o, --output DIR` | next to the input | where the framed PNG goes |
| `--clearance N` | 24 | extra px between notch and content |
| `--band-margin N` | 40 | dead band must exceed the need by this much |
| `--keep-padded` | off | keep the intermediate shifted image |
| `--allow-resize` | off | if there is no dead space, append rows instead |
| `--dry-run` | off | report only |

## Worth knowing

- **It is idempotent.** Re-running on an already-shifted image reports
  `padding not needed`, because the top is already clear. Safe to re-run over a
  whole folder.
- **Inputs are never modified.** The shifted intermediate goes to a temp file
  and is deleted, unless `--keep-padded`.
- **No dead space is a hard stop.** If the image has no flat band big enough,
  it skips the file and says so rather than guessing. `--allow-resize` appends
  rows instead, but that changes the height and `frames` may then fail to match
  the device — the message says as much.
- **Filling the new top rows** stretches the source's row 0 downward. Seamless
  for a flat top, and for the DashboardU header gradient too, whose vertical
  variation over ~100px is only a few RGB units.
- **Output naming** is `<stem>_framed.png`, matching the existing assets.

## Checking the result

The clearance is a heuristic, so look at what came out — crop the top of the
framed PNG and confirm nothing is hidden:

```python
from PIL import Image
im = Image.open("out/shot_framed.png")
bg = Image.new("RGB", im.size, (255, 255, 255))
bg.paste(im, (0, 0), im)          # flatten; the bezel is transparent outside
bg.crop((0, 0, im.size[0], 440)).save("/tmp/check.png")
```

Then read `/tmp/check.png`. If the header is still clipped, raise
`--clearance`.
