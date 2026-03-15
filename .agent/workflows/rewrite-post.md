---
description: Rewrite derivative files (Substack, LinkedIn, Facebook, Bluesky) after editing a source draft
---

## /rewrite-post — Regenerate Derivatives After Editing

Use this workflow when you have edited a source `.md` draft in `published/` and want to regenerate all derivative files to reflect the changes.

### How to invoke

In chat, say one of these:

> `/rewrite-post my-post-slug`
> `/rewrite-post 2026-03-07-my-post-slug`

You may pass either the bare slug or the full filename. The date prefix is optional.

---

### What the agent will do

1. **Locate the source draft** in `published/` using the slug or filename provided.

2. **Check for existing derivative files:**
   - `YYYY-MM-DD-slug-substack.md`
   - `YYYY-MM-DD-slug-linkedin-post.txt`
   - `YYYY-MM-DD-slug-facebook-post.txt`
   - `YYYY-MM-DD-slug-bluesky-post.txt`

3. **Confirm with the user** before overwriting existing files.

4. **Regenerate all files** following the same rules as `/substack-post`:
   - Updated Substack article (`-substack.md`) reflecting the edited draft.
   - Updated LinkedIn Feed Post (`-linkedin-post.txt`) reflecting the edited draft.
   - Updated Facebook Feed Post (`-facebook-post.txt`) reflecting the edited draft.
   - Updated Bluesky Post (`-bluesky-post.txt`) reflecting the edited draft.

5. **Confirm** all files are rewritten and display previews of all social posts for quick review.

---

### Notes

- Always regenerate from the current state of the source `.md` — do not attempt to diff or patch the existing derivative files.
- If no derivative files exist yet, this workflow creates them (same as `/substack-post`).
- Personal voice: first-person, conversational, reflective. This is Vic's independent writing, not DeeperPoint marketing.
