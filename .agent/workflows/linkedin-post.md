---
description: Generate LinkedIn Article and feed post from an approved personal blog draft
---

## /linkedin-post — Step 1 → Step 2

Use this workflow when you have a reviewed and approved Step 1 draft and want to generate the two LinkedIn distribution files.

### How to invoke

In chat, say one of these:

> `/linkedin-post my-post-slug`
> `/linkedin-post 2026-03-07-my-post-slug`

You may pass either the bare slug or the full filename. The date prefix is optional.

---

### What the agent will do

1. **Locate the source draft** in `VicPersonalBlog/` using the slug or filename provided.

2. **Generate a LinkedIn Article** (`YYYY-MM-DD-slug-linkedin.md`):
   - Same YAML header as the draft, plus `linkedin-cover: <hero-image path>` if a cover image was specified.
   - Same H2 heading structure — LinkedIn Pulse renders headings.
   - Use Unicode punctuation (em-dashes `—`, curly quotes `""`), no HTML entities.
   - Note body images as `[IMAGE: filename — Caption]` placeholder lines to be added manually in the LinkedIn editor.
   - Remove or replace all relative links — there is no personal website. If a DeeperPoint reference is appropriate, use the full `https://deeperpoint.com/` URL. Otherwise, remove the link.
   - End with a 2–3 sentence CTA inviting engagement ("What's your experience with this?", "I'd be glad to hear your thoughts.").

3. **Generate a LinkedIn Feed Post** (`YYYY-MM-DD-slug-linkedin-post.txt`):
   - Plain text only — no markdown, no HTML.
   - 150–250 words.
   - Opening hook in the first 2 lines (shown before LinkedIn's "see more" cut).
   - 3–5 short paragraphs separated by blank lines.
   - Maximum 1–2 emoji, used purposefully.
   - End with a CTA and 3–5 hashtags. No external URL required — link to the LinkedIn Article if one is being published, otherwise close with hashtags and an engagement question.

4. **Confirm** both files are written and display a preview of the feed post `.txt` for quick review.

---

### Notes

- If `-linkedin.md` or `-linkedin-post.txt` files already exist for this slug, ask the user whether to overwrite or skip.
- The LinkedIn Article is intended for copy-paste into LinkedIn's native article editor (Pulse). It does not auto-publish.
- The feed post `.txt` is intended for copy-paste into a regular LinkedIn status update. It does not auto-publish.
- Personal voice: first-person, conversational. This is Vic's personal account, not DeeperPoint marketing.
