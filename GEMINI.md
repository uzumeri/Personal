# VicPersonalBlog — Gemini Context

This repo is the **drafting and staging environment** for Vic Uzumeri's personal LinkedIn articles and posts.

Unlike DeeperPointBlogging, there is no associated website. All content is published directly to LinkedIn.

---

## Publication Channels

| Output | Format | Purpose |
|---|---|---|
| `YYYY-MM-DD-slug-linkedin.md` | Markdown | LinkedIn Pulse native article (copy-paste into LinkedIn editor) |
| `YYYY-MM-DD-slug-linkedin-post.txt` | Plain text | LinkedIn feed post teaser (copy-paste into LinkedIn status update) |

There is no Step 2 HTML publishing step. The workflow is two steps only:

1. **Draft** — write the source `.md` in this repo
2. **LinkedIn** — generate Article + feed post for distribution

---

## Drafting Workflow — 2-Step Process

### File Naming Convention

```
YYYY-MM-DD-post-slug.md                ← Step 1: source draft (this repo)
YYYY-MM-DD-post-slug-linkedin.md       ← Step 2: LinkedIn Article (Pulse format)
YYYY-MM-DD-post-slug-linkedin-post.txt ← Step 2: LinkedIn feed post (plain text teaser)
```

---

### Step 1 — Draft in Markdown (this repo)

Write posts as `.md` files in the root of this repo. Include a YAML-style front matter header:

```yaml
---
title: Your Post Title
date: YYYY-MM-DD
tags: [tag1, tag2, tag3]
summary: One-sentence summary of the post.
estimated-read: X min read
hero-image: images/hero-slug.jpg   ← optional; omit if no cover image
hero-caption: Caption text         ← optional
---
```

Write the body in standard Markdown:
- `##` for section headings
- `**bold**` for key terms
- `*italic*` for emphasis
- Unordered and ordered lists as needed
- `---` for a thematic break before a closing note or signature

Review and edit the `.md` draft before proceeding to Step 2.

---

### Step 2 — LinkedIn Distribution

Generate two LinkedIn files from the approved draft.

#### 2a — LinkedIn Article (`-linkedin.md`)

A version of the post formatted for **LinkedIn Pulse** (native articles):

- **Header:** Same YAML header as the draft, plus `linkedin-cover: images/hero-slug.jpg` if a cover image was specified.
- **Length:** Same as the draft, or slightly condensed (trim 10–20% if needed).
- **H2 headings:** Keep them — LinkedIn Pulse renders headings.
- **No HTML entities:** Use plain Unicode (em-dashes `—`, curly quotes `""`).
- **Body images:** Note as `[IMAGE: filename — Caption]` placeholder; add manually in the LinkedIn editor.
- **No relative links:** There is no personal website, so remove or replace all relative links with context-appropriate full URLs (e.g., a DeeperPoint link → `https://deeperpoint.com/`). If a link is purely internal with no appropriate external destination, remove it.
- **End with a CTA:** Close with 2–3 sentences inviting engagement ("What's your experience with X?", "I'd be glad to hear your thoughts.").

Filename: `YYYY-MM-DD-slug-linkedin.md`

#### 2b — LinkedIn Feed Post (`-linkedin-post.txt`)

A **stand-alone plain-text social post** (150–250 words):

- **No markdown** — LinkedIn feed does not render markdown.
- **Opening hook:** First 2 lines shown before "see more" — make them count.
- **3–5 short paragraphs** separated by blank lines.
- **Optional emoji** — 1–2 maximum, used purposefully.
- **End with a CTA + hashtags:** 3–5 hashtags. If the full article is on LinkedIn Pulse, end with a note directing readers to it. Otherwise, end with a question to prompt discussion.
- **No external URLs are required** since there is no personal website. Link to the LinkedIn Article if publishing one; otherwise end with hashtags only.

Filename: `YYYY-MM-DD-slug-linkedin-post.txt`

---

### Step 3 — Commit and Push

Commit both the source draft and all LinkedIn output files together so versions stay in sync.

---

## Triggering the Workflow

Use slash commands in chat to trigger each step:

| Command | When to use |
|---|---|
| `/linkedin-post <slug>` | Approved draft ready → generate LinkedIn Article + feed post |
| `/rewrite-post <slug>` | Edited the source draft → regenerate LinkedIn files |

Pass either the bare slug or the full filename. Date prefix is optional.

---

## Style and Voice

- **Audience:** Broadly professional — colleagues, peers, people in adjacent fields. Not specific to thin market theory or DeeperPoint (use DeeperPointBlogging for that content).
- **Voice:** First-person, conversational, grounded in specific experience. Thoughtful but not academic. Opinions are welcome.
- **Length:** 400–800 words for articles. Shorter is better if the idea is clear.
- **Tone:** Personal posts may reference DeeperPoint work where genuinely relevant, but should not read as marketing.

---

## Content Tags

Use consistent tags to track post categories:

`reflection` · `market-design` · `ai` · `trade` · `craft` · `leadership` · `strategy` · `canada` · `technology` · `education` · `case-study` · `opinion`

---

## Copyright

Insert the following at the top of every file:

```
<!--Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.-->
```

For plain text files, omit the comment syntax — just begin with the content.
