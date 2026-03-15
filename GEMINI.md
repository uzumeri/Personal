<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

# VicPersonalBlog — Gemini Context

This repo is the **drafting and staging environment** for Vic Uzumeri's personal writing, published to **Substack** and distributed via **LinkedIn**, **Facebook**, and **Bluesky**.

---

## Publication Channels

| Channel | Format | Purpose | Method |
| --- | --- | --- | --- |
| **Substack** (`vicuzumeri.substack.com`) | Rich text (paste from rendered HTML) | Canonical home for all personal writing | Manual copy-paste |
| **LinkedIn feed post** | Plain text (400–500 words) | Professional teaser driving traffic to Substack | Manual copy-paste |
| **Facebook feed post** | Plain text (150–250 words) | Personal/casual teaser with direct link | Manual copy-paste |
| **Bluesky post** | Plain text (≤280 chars) | Short teaser with link card | Script (`post_bluesky.py`) |

**Substack is the single publication target.** All other platforms are distribution channels — teasers that point back to the canonical Substack article.

---

## Content Firewall

This repo is for **personal, independent writing** — professional reflections, opinions, and analysis that Vic would write regardless of whether DeeperPoint existed.

**Rules:**

- **No DeeperPoint marketing.** You may reference DeeperPoint work as context ("in my work on marketplace design…") but the article must stand on its own merits.
- **No links to deeperpoint.com** unless genuinely relevant to the reader's interest — and even then, sparingly.
- **Personal voice.** First person. Opinions welcome. The tone is "practitioner reflecting," not "project promoting."
- **No cross-posting.** Substack content does not appear on deeperpoint.com. DeeperPoint blog content does not appear on Substack.

---

## Repository Structure

```text
VicPersonalBlog/
├── GEMINI.md                              ← this file
├── .agent/workflows/
│   ├── substack-post.md                   ← /substack-post workflow
│   ├── linkedin-post.md                   ← /linkedin-post (teaser → Substack)
│   └── rewrite-post.md                    ← /rewrite-post (regenerate derivatives)
├── scripts/
│   ├── preview.py                         ← render markdown → HTML → browser
│   └── post_bluesky.py                    ← post to Bluesky via AT Protocol
├── drafts/                                ← working drafts (iterative, messy)
├── published/                             ← final versions with derivatives
│   ├── YYYY-MM-DD-slug.md                 ← source of truth
│   ├── YYYY-MM-DD-slug-substack.md        ← Substack-ready version
│   ├── YYYY-MM-DD-slug-linkedin-post.txt  ← LinkedIn feed teaser
│   ├── YYYY-MM-DD-slug-facebook-post.txt  ← Facebook feed teaser
│   └── YYYY-MM-DD-slug-bluesky-post.txt   ← Bluesky post (≤280 chars)
├── .env                                   ← Bluesky credentials (gitignored)
└── README.md
```

### `drafts/` — Working Space

Place rough drafts, outlines, notes, and half-finished ideas here. Files in `drafts/` are not expected to be complete or polished. Use any naming convention that helps you find things.

### `published/` — Final Versions

When a draft is approved, move it to `published/` with the standard naming convention. Running `/substack-post` generates the derivative files here.

---

## Drafting Workflow — 4-Step Process

### Step 1 — Draft in Markdown

Write posts as `.md` files in `drafts/`. Include a YAML frontmatter header:

```yaml
---
title: Your Post Title
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
summary: One-sentence summary of the post.
estimated-read: X min read
---
```

Write the body in standard Markdown:

- `##` for section headings (H2 — Substack renders these well)
- `**bold**` for key terms
- `*italic*` for emphasis
- Unordered and ordered lists
- Block quotes (`>`) for emphasis or attribution
- `---` for thematic breaks

Review and edit the draft. This is the iterative phase — take your time.

### Step 2 — Generate All Derivatives

When the draft is ready, run `/substack-post <slug>`. This:

1. Moves the draft to `published/` (if not already there)
2. Generates a Substack-ready version (`-substack.md`)
3. Generates a LinkedIn feed post teaser (`-linkedin-post.txt`)
4. Generates a Facebook feed post (`-facebook-post.txt`)
5. Generates a Bluesky post (`-bluesky-post.txt`)

### Step 3 — Publish and Distribute

1. **Substack:** Run `python scripts/preview.py published/YYYY-MM-DD-slug-substack.md`, then select-all → copy → paste into Substack's editor. Review, add cover image if desired, publish.
2. **LinkedIn:** Copy the published Substack URL. Paste the LinkedIn teaser as a feed post. Put the Substack URL in the **first comment** (not the post body).
3. **Facebook:** Paste the Facebook teaser as a personal post. The Substack URL is already in the text.
4. **Bluesky:** Run `python scripts/post_bluesky.py published/YYYY-MM-DD-slug-bluesky-post.txt` — or paste manually at bsky.app.

### Step 4 — Commit and Push

Commit the source draft and all derivative files together.

---

## Triggering the Workflow

| Command | When to use |
| --- | --- |
| `/substack-post <slug>` | Approved draft ready → generate Substack + all social teasers |
| `/linkedin-post <slug>` | Regenerate only the LinkedIn teaser from a published post |
| `/rewrite-post <slug>` | Edited the source → regenerate all derivative files |

Pass either the bare slug or the full filename. Date prefix is optional.

---

## Substack Formatting Rules

Substack's editor accepts rich-text paste from rendered HTML. It supports:

- ✅ Headings (H2, H3)
- ✅ Bold, italic, strikethrough
- ✅ Ordered and unordered lists
- ✅ Block quotes
- ✅ Horizontal rules
- ✅ Links (absolute URLs only)
- ✅ Images (add manually in Substack editor)
- ❌ Tables (convert to bullet lists or descriptive text)
- ❌ Code blocks with syntax highlighting (use plain text formatting)
- ❌ HTML entities (use Unicode: em-dash `—`, curly quotes `""`)

The `-substack.md` derivative should follow these constraints.

---

## Social Post Rules

### LinkedIn (`-linkedin-post.txt`)

A **stand-alone plain-text post** (400–500 words):

- **No markdown** — LinkedIn feed does not render markdown
- **Opening hook:** First 2 lines shown before "see more" — make them count
- **5–8 short paragraphs** separated by blank lines
- **Optional emoji** — 1–2 maximum, used purposefully
- **No Substack URL in the post body** — LinkedIn's algorithm suppresses posts with external links
- **End with:** "Full article on my Substack → link in the first comment" or similar
- **Hashtags:** 3–5 at the end (`#Opinion #AI #Strategy` etc.)

### Facebook (`-facebook-post.txt`)

A **shorter, warmer plain-text post** (150–250 words):

- **No markdown** — Facebook renders plain text only
- **Slightly more conversational** than LinkedIn — this is a personal account
- **Opening hook** in the first 2 lines
- **3–5 short paragraphs** separated by blank lines
- **Optional emoji** — 1–2 maximum
- **Include the Substack URL directly in the post body** — Facebook is less punitive about links
- **No hashtags** — they are ineffective on Facebook

### Bluesky (`-bluesky-post.txt`)

A **very short plain-text post** (≤280 characters):

- 1–2 sentences capturing the core insight
- **Include the Substack URL** — Bluesky generates a link card preview
- No hashtags
- Every character counts — be punchy and direct

---

## Style and Voice

- **Audience:** Broadly professional — colleagues, peers, people in adjacent fields. Not specific to thin market theory or DeeperPoint.
- **Voice:** First-person, conversational, grounded in specific experience. Thoughtful but not academic. Opinions are welcome.
- **Length:** 400–800 words for articles. Shorter is better if the idea is clear.
- **Tone:** Personal. Reflective. Honest. May reference DeeperPoint work where genuinely relevant, but should not read as marketing.

---

## Content Tags

Use consistent tags to track post categories:

`reflection` · `market-design` · `ai` · `trade` · `craft` · `leadership` · `strategy` · `canada` · `technology` · `education` · `case-study` · `opinion`

---

## Copyright

Insert the following at the top of every markdown file:

```text
<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->
```

For plain text files, omit the comment syntax — just begin with the content.
