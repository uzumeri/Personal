<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->

# VicPersonalBlog — Gemini Context

This repo is the **drafting and staging environment** for Vic Uzumeri's personal writing, published to **Substack** and promoted via **LinkedIn**.

---

## Publication Channels

| Channel | Format | Purpose |
|---|---|---|
| **Substack** (`substack.com/@vicuzumeri`) | Rich text (paste from rendered HTML) | Canonical home for all personal writing |
| **LinkedIn feed post** | Plain text | Teaser post driving traffic to the Substack article |

**Substack is the single publication target.** LinkedIn Pulse articles are not used — Substack provides superior formatting (tables, code, images) and builds a direct subscriber relationship.

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

```
VicPersonalBlog/
├── GEMINI.md                              ← this file
├── .agent/workflows/
│   ├── substack-post.md                   ← /substack-post workflow
│   ├── linkedin-post.md                   ← /linkedin-post (teaser → Substack)
│   └── rewrite-post.md                    ← /rewrite-post (regenerate derivatives)
├── scripts/
│   └── preview.py                         ← render markdown → HTML → browser
├── drafts/                                ← working drafts (iterative, messy)
├── published/                             ← final versions with derivatives
│   ├── YYYY-MM-DD-slug.md                 ← source of truth
│   ├── YYYY-MM-DD-slug-substack.md        ← Substack-ready version
│   └── YYYY-MM-DD-slug-linkedin-post.txt  ← LinkedIn feed teaser
└── README.md
```

### `drafts/` — Working Space

Place rough drafts, outlines, notes, and half-finished ideas here. Files in `drafts/` are not expected to be complete or polished. Use any naming convention that helps you find things.

### `published/` — Final Versions

When a draft is approved, move it to `published/` with the standard naming convention. Running `/substack-post` generates the derivative files here.

---

## Drafting Workflow — 3-Step Process

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

### Step 2 — Generate Substack + LinkedIn Files

When the draft is ready, run `/substack-post <slug>`. This:

1. Moves the draft to `published/` (if not already there)
2. Generates a Substack-ready version (`-substack.md`)
3. Generates a LinkedIn feed post teaser (`-linkedin-post.txt`)

### Step 3 — Publish

1. Run `python scripts/preview.py published/YYYY-MM-DD-slug-substack.md`
2. The rendered HTML opens in your browser
3. Select all → Copy → Paste into Substack's editor
4. Review formatting in Substack, add cover image if desired, publish
5. Copy the published Substack URL
6. Post the LinkedIn teaser, putting the Substack URL in the **first comment** (not the post body — LinkedIn suppresses posts with external links)

### Step 4 — Commit and Push

Commit the source draft and all derivative files together.

---

## Triggering the Workflow

| Command | When to use |
|---|---|
| `/substack-post <slug>` | Approved draft ready → generate Substack + LinkedIn files |
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

## LinkedIn Feed Post Rules

The LinkedIn teaser (`-linkedin-post.txt`) is a **stand-alone plain-text post** (150–250 words):

- **No markdown** — LinkedIn feed does not render markdown
- **Opening hook:** First 2 lines shown before "see more" — make them count
- **3–5 short paragraphs** separated by blank lines
- **Optional emoji** — 1–2 maximum, used purposefully
- **No Substack URL in the post body** — LinkedIn's algorithm suppresses posts with external links
- **End with:** "Full article on my Substack → link in the first comment" or similar
- **Hashtags:** 3–5 at the end (`#Opinion #AI #Strategy` etc.)

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

```
<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->
```

For plain text files, omit the comment syntax — just begin with the content.
