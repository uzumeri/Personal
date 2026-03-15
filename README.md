<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

# VicPersonalBlog

Drafting and staging environment for personal writing published on **Substack** and distributed via **LinkedIn**, **Facebook**, and **Bluesky**.

## Quick Start

```bash
# Set up the Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install markdown

# Preview a draft as styled HTML (for copy-paste into Substack)
python scripts/preview.py published/YYYY-MM-DD-slug-substack.md
```

## Bluesky Setup (optional)

1. Go to [bsky.app/settings/app-passwords](https://bsky.app/settings/app-passwords)
2. Create a new App Password (do NOT use your main password)
3. Create a `.env` file in the repo root:

```bash
BLUESKY_HANDLE=your-handle.bsky.social
BLUESKY_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

4. Post from the command line:

```bash
python scripts/post_bluesky.py published/YYYY-MM-DD-slug-bluesky-post.txt
```

## Workflow

| Command | What it does |
| --- | --- |
| `/substack-post <slug>` | Generate Substack article + LinkedIn, Facebook, Bluesky teasers |
| `/linkedin-post <slug>` | Regenerate LinkedIn teaser only |
| `/rewrite-post <slug>` | Regenerate all derivatives after editing the source |

## Distribution Channels

| Platform | Method | Details |
| --- | --- | --- |
| **Substack** | Copy-paste from preview | Canonical publication home |
| **LinkedIn** | Copy-paste text, URL in first comment | Professional teaser |
| **Facebook** | Copy-paste text (URL in body) | Personal/casual teaser |
| **Bluesky** | Script (`post_bluesky.py`) or manual | Short post with link card |

See [GEMINI.md](GEMINI.md) for full workflow details, formatting rules, and content guidelines.
