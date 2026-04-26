<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

# uzumeri.com — Personal Site

Personal website and blog drafting environment for **Mustafa (Vic) Uzumeri**, hosted via GitHub Pages at [uzumeri.com](https://uzumeri.com).

## What This Repo Contains

### Website (GitHub Pages)

The site is a static HTML/CSS/JS site — no build step, no framework. Push to `main` and GitHub Pages deploys automatically.

| Page | File | Purpose |
|---|---|---|
| **Home** | `index.html` | Landing page with bio, contact links, and active project cards |
| **History** | `history.html` | Integrated professional timeline (1974–2026) with expandable entries |
| **Blog** | `blog.html` | Index of published Substack articles with tags and summaries |

### Blog Drafting Pipeline

This repo also serves as the drafting and staging environment for personal writing published on **Substack** and distributed via **LinkedIn**, **Facebook**, and **Bluesky**.

```
drafts/              ← working drafts (iterative, messy)
published/           ← final versions with derivative files
  YYYY-MM-DD-slug.md              ← source of truth
  YYYY-MM-DD-slug-substack.md     ← Substack-ready version
  YYYY-MM-DD-slug-linkedin-post.txt
  YYYY-MM-DD-slug-facebook-post.txt
  YYYY-MM-DD-slug-bluesky-post.txt
```

## Directory Structure

```
Personal/
├── index.html              ← Home / About page
├── history.html            ← Professional history timeline
├── blog.html               ← Substack article listing
├── styles.css              ← Design system (DeeperPoint aesthetic)
├── reveal.js               ← Scroll-reveal animations
├── nav-mobile.js           ← Mobile navigation toggle
├── images/about/           ← Timeline images (49 assets)
├── CNAME                   ← uzumeri.com domain config
├── GEMINI.md               ← AI context and workflow rules
├── drafts/                 ← Blog working drafts
├── published/              ← Final posts + derivative files
├── scripts/
│   ├── preview.py          ← Render markdown → HTML for Substack paste
│   └── post_bluesky.py     ← Post to Bluesky via AT Protocol
└── .agent/workflows/       ← AI workflow definitions
```

## Local Development

Preview the site locally with any static HTTP server:

```bash
# Python (built-in)
python -m http.server 8080

# Then open http://localhost:8080
```

Preview a blog draft for Substack paste:

```bash
python scripts/preview.py published/YYYY-MM-DD-slug-substack.md
```

## Blog Workflows

| Command | What it does |
|---|---|
| `/substack-post <slug>` | Generate Substack article + LinkedIn, Facebook, Bluesky teasers |
| `/hero-image <slug>` | Generate or regenerate the hero image for a post |
| `/linkedin-post <slug>` | Regenerate LinkedIn teaser only |
| `/rewrite-post <slug>` | Regenerate all derivatives after editing the source |

## Distribution Channels

| Platform | Method | Details |
|---|---|---|
| **Substack** | Copy-paste from preview | Canonical publication home |
| **LinkedIn** | Copy-paste text, URL in first comment | Professional teaser |
| **Facebook** | Copy-paste text (URL in body) | Personal/casual teaser |
| **Bluesky** | Script (`post_bluesky.py`) or manual | Short post with link card |

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

## Design System

The site uses the **DeeperPoint design system** — dark glassmorphism aesthetic with animated background orbs, glass-panel cards, and the Outfit/Inter typeface stack. The CSS is shared with [deeperpoint.com](https://deeperpoint.com) for visual consistency across Vic's professional presence.

## History Timeline

The history page merges content from two sources into a single chronological timeline:

- **[deeperpoint.com/history.html](https://deeperpoint.com/history.html)** — DeeperPoint professional history
- **[EduOpsLab/lineage.html](https://uzumeri.github.io/EduOpsLab/lineage.html)** — Education and learning science lineage

Four career eras are represented: **Origins** (1974–1989), **Academic** (1987–2012), **iPOV** (1997–2014), and **Recent** (2011–2026).

## Related Projects

| Project | URL | Description |
|---|---|---|
| **DeeperPoint** | [deeperpoint.com](https://deeperpoint.com) | AI marketplace framework for thin markets |
| **EduOpsLab** | [uzumeri.github.io/EduOpsLab](https://uzumeri.github.io/EduOpsLab/) | Operations management applied to education |
| **MarketForge** | [deeperpoint.com/marketforge](https://deeperpoint.com/marketforge.html) | Open-source Cosolvent harness and AI tools |

---

See [GEMINI.md](GEMINI.md) for full AI context, workflow details, formatting rules, and content guidelines.
