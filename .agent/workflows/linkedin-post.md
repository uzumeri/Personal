---
description: Generate LinkedIn feed post from an approved blog post draft
---

## /linkedin-post — Generate LinkedIn Teaser for a Published Substack Article

Use this workflow to generate (or regenerate) only the LinkedIn feed post teaser for a post that has already been published to Substack.

### How to invoke

In chat, say one of these:

> `/linkedin-post my-post-slug`
> `/linkedin-post 2026-03-07-my-post-slug`

You may pass either the bare slug or the full filename. The date prefix is optional.

---

### What the agent will do

1. **Locate the source draft** in `published/` using the slug or filename provided. If not found in `published/`, check `drafts/`.

2. **Generate a LinkedIn Feed Post** (`YYYY-MM-DD-slug-linkedin-post.txt` in `published/`):
   - Plain text only — no markdown, no HTML.
   - 150–250 words.
   - Opening hook in the first 2 lines (shown before LinkedIn's "see more" cut).
   - 3–5 short paragraphs separated by blank lines.
   - Maximum 1–2 emoji, used purposefully.
   - **Do NOT put the Substack URL in the post body** — LinkedIn's algorithm suppresses posts with external links.
   - End with: "Full article on my Substack → link in the first comment" or similar phrasing.
   - 3–5 hashtags at the end.

3. **Confirm** the file is written and display the full feed post `.txt` for quick review.

---

### Notes

- If `-linkedin-post.txt` already exists for this slug, ask the user whether to overwrite or skip.
- The teaser should work as a standalone read — valuable even if the reader never clicks through.
- Personal voice: first-person, conversational, reflective. This is Vic's independent writing, not DeeperPoint marketing.
