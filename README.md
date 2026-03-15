<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

# VicPersonalBlog

Drafting and staging environment for Vic Uzumeri's personal writing, published to [Substack](https://substack.com/@vicuzumeri).

## Workflow

1. **Draft** — write markdown in `drafts/`
2. **Generate** — run `/substack-post <slug>` to produce Substack-ready article + LinkedIn teaser
3. **Preview** — run `python scripts/preview.py published/YYYY-MM-DD-slug-substack.md`
4. **Publish** — copy-paste from browser preview into Substack's editor
5. **Promote** — post LinkedIn teaser with Substack URL in the first comment

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install markdown
```

## Content Firewall

This repo is for **personal, independent writing** only. DeeperPoint content belongs in the [DeeperPointBlogging](https://github.com/DeeperPoint/DeeperPointBlogging) repo and publishes to [deeperpoint.com/blog](https://deeperpoint.com/blog/).
