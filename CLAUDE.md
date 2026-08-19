# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A documentation-only site (no application code, no tests) for the **DataU platform** and the
**ProxyU Java client SDK**, built with MkDocs + Material for MkDocs. Two audiences: data subjects
(end users of DashboardU) and data processors (developers integrating ProxyU).

## Commands

```bash
source .venv/bin/activate          # venv already exists at ./.venv
pip install -r requirements.txt    # mkdocs-material, pinned

mkdocs serve                       # live preview at http://127.0.0.1:8000
mkdocs build --strict              # what CI runs — broken internal links fail the build
```

Always verify with `mkdocs build --strict` before considering a change done; the GitHub Actions
workflow (`.github/workflows/deploy.yml`, on push to `main`) builds with `--strict` and publishes
`site/` to GitHub Pages. `site/` is gitignored build output — never commit it or hand-edit it.

## Architecture

**Navigation is explicit.** Every page must be listed in the `nav:` block of `mkdocs.yml`. A new
`.md` file that isn't added there is built but unreachable.

**The landing page is a Jinja template, not Markdown.** `docs/index.md` is frontmatter only
(`template: home.html`); all hero/feature/CTA content lives in `overrides/home.html`, which extends
Material's `main.html` and overrides three blocks:

- `{% block tabs %}` — calls `{{ super() }}`, then appends the full-bleed landing sections
- `{% block content %}` — emptied, so the normal page body doesn't render
- `{% block footer %}` — a slimmed footer (copyright + social, no prev/next nav)

Inside that template, links must go through Material's URL filter with a trailing slash —
`{{ 'developers/' | url }}`, not a relative `.md` path. Icons are inlined with
`{% include ".icons/material/<name>.svg" %}` so CSS can control their `fill`. Regular Markdown pages
use ordinary relative `.md` links, which MkDocs rewrites.

**Styling lives in `docs/stylesheets/extra.css`** (registered via `extra_css`), in three parts:

1. Brand palette — `mkdocs.yml` sets `primary: custom` / `accent: custom`, and the actual colors are
   defined here under `[data-md-color-primary="custom"]` / `[data-md-color-accent="custom"]`.
2. Header overrides — the header and tabs are forced light in *both* schemes so the full-color DataU
   wordmark stays legible; in `slate` the logo gets a white pill background. The redundant site-name
   text next to the logo is hidden.
3. Landing-page rules, all prefixed `dx-` (`dx-hero`, `dx-band`, `dx-features`, `dx-cards`, `dx-cta`)
   matching the classes in `home.html`. Changing landing copy means editing `home.html`; changing its
   look means editing these `dx-` rules.

**Diagrams are Mermaid, not images.** `pymdownx.superfences` declares a `mermaid` custom fence, so
sequence/flow diagrams live in ```mermaid blocks inside the Markdown — theme-aware and diffable.
Material pulls mermaid.js from the unpkg CDN at page load, so diagrams need network access to render
in the browser (the build itself stays offline). Screenshots remain PNGs in `docs/assets/`.

**Content conventions in Markdown pages:** Material grid cards
(`<div class="grid cards" markdown>` with `-   :material-icon: **Title**` items), `!!!`
admonitions, and `===` tabbed blocks (`pymdownx.tabbed`) for alternative integration approaches.
Images go in `docs/assets/`.

Note: the "Project layout" tree in `README.md` lists a `data-subjects/connected-apps/spoon/`
directory that does not exist yet — trust `mkdocs.yml` and the filesystem over that tree.
