# DataU Documentation (`public-docs`)

Public user & developer documentation for the **DataU platform** and the **SPOON toolset**,
built with [MkDocs](https://www.mkdocs.org/) + [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

The site has two audiences:

- **End Users / Data Subjects** — how to use DashboardU and the SPOON connected apps
  (SPOON Dashboard, Questionnaire Tool, Data Lake, Personal Data Wallet).
- **Developers / Data Processors** — how to build apps on DataU with the ProxyU Java client (SDK).

## Local development

```bash
# From the repo root
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

mkdocs serve                       # live preview at http://127.0.0.1:8000
mkdocs build --strict              # production build into ./site (fails on broken links)
```

## Project layout

```
docs/
├── index.md                       # landing page
├── data-subjects/                 # End Users section
│   ├── dashboardu.md
│   └── connected-apps/spoon/      # SPOON app guides
└── developers/                    # Developers section
    └── proxyu-java-sdk/           # ProxyU Java SDK guide
```

Navigation is defined explicitly in [`mkdocs.yml`](./mkdocs.yml).

## Deployment (GitHub Pages)

Deployment is **opt-in** — nothing publishes until you push this repo and enable Pages.

**Option A — GitHub Actions (recommended).** The workflow at
[`.github/workflows/deploy.yml`](./.github/workflows/deploy.yml) builds and publishes the site.
It runs on push to `main` and can also be triggered manually from the Actions tab
(*Run workflow* / `workflow_dispatch`). One-time setup: in **Settings → Pages**, set
**Source = GitHub Actions**.

**Option B — one-shot from your machine.**

```bash
source .venv/bin/activate 
mkdocs gh-deploy --strict   # builds and pushes to the gh-pages branch
```

The published site URL is `https://jibecompany.github.io/datau-docs/` (see `site_url` in `mkdocs.yml`).
