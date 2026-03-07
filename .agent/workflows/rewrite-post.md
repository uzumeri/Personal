---
description: Regenerate LinkedIn Article and feed post after editing a source draft
---

## /rewrite-post — Regenerate LinkedIn files after editing a draft

Use this workflow when you have edited a source `.md` draft after the LinkedIn files were already generated and you want to regenerate them.

### How to invoke

In chat, say one of these:

> `/rewrite-post my-post-slug`
> `/rewrite-post 2026-03-07-my-post-slug`

You may pass either the bare slug or the full filename. The date prefix is optional.

---

### What the agent will do

1. **Locate the source draft** in `VicPersonalBlog/` using the slug or filename provided.

2. **Check for existing LinkedIn files:**
   - `YYYY-MM-DD-slug-linkedin.md`
   - `YYYY-MM-DD-slug-linkedin-post.txt`

3. **Confirm with the user** before overwriting existing files.

4. **Regenerate both LinkedIn files** following the same rules as `/linkedin-post`:
   - Updated LinkedIn Article (`-linkedin.md`) reflecting the edited draft.
   - Updated LinkedIn Feed Post (`-linkedin-post.txt`) reflecting the edited draft.

5. **Confirm** both files are rewritten and display a preview of the feed post for quick review.

---

### Notes

- Always regenerate from the current state of the source `.md` — do not attempt to diff or patch the existing LinkedIn files.
- If no LinkedIn files exist yet, run `/linkedin-post` instead.
- Personal voice: first-person, conversational. This is Vic's personal account, not DeeperPoint marketing.
