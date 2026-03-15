---
description: Generate Substack article and LinkedIn feed teaser from an approved draft
---

## /substack-post — Draft → Substack + LinkedIn

Use this workflow when you have a reviewed and approved draft and want to generate the Substack-ready article and LinkedIn teaser.

### How to invoke

In chat, say one of these:

> `/substack-post my-post-slug`
> `/substack-post 2026-03-07-my-post-slug`

You may pass either the bare slug or the full filename. The date prefix is optional.

---

### What the agent will do

1. **Locate the source draft** — search `drafts/` and `published/` for a file matching the slug.

2. **Move to `published/`** — if the draft is still in `drafts/`, copy it to `published/YYYY-MM-DD-slug.md` using the date from the YAML frontmatter. Ask the user whether to also remove the original from `drafts/`.

3. **Generate a Substack-ready version** (`YYYY-MM-DD-slug-substack.md` in `published/`):
   - Same content as the source draft with these modifications:
   - **Remove YAML frontmatter** — Substack doesn't use it. Instead, the title becomes an H1 at the top, and the summary becomes a subtitle line (italic, immediately below the title).
   - **Convert tables to bullet lists** — Substack does not render markdown tables. Restructure them as descriptive bullet points or labeled paragraphs.
   - **Use Unicode punctuation** — em-dashes `—`, curly quotes `""''`, ellipses `…`. No HTML entities.
   - **Remove relative links** — replace with absolute URLs where appropriate, or remove if no suitable target exists.
   - **Remove code blocks with language identifiers** — Substack renders plain code blocks poorly. Convert to indented plain text if the content is essential, or describe in prose.
   - **Keep:** headings (H2/H3), bold, italic, block quotes, ordered/unordered lists, horizontal rules, absolute links.
   - **End with a discussion CTA** — 1–2 sentences inviting comments or sharing ("What's your experience with this? I'd love to hear your take.").
   - **Add footer:** A brief "About the author" line: *Vic Uzumeri writes about market design, technology, and the craft of engineering useful systems. Subscribe at substack.com/@vicuzumeri.*

4. **Generate a LinkedIn Feed Post** (`YYYY-MM-DD-slug-linkedin-post.txt` in `published/`):
   - Plain text only — no markdown, no HTML.
   - 150–250 words.
   - Opening hook in the first 2 lines (shown before LinkedIn's "see more" cut).
   - 3–5 short paragraphs separated by blank lines.
   - Maximum 1–2 emoji, used purposefully.
   - **Do NOT put the Substack URL in the post body** — LinkedIn's algorithm suppresses posts with external links.
   - End with: "Full article on my Substack → link in the first comment" or similar phrasing.
   - 3–5 hashtags at the end.

5. **Confirm** all files are written. Display:
   - The opening paragraph of the Substack version
   - The full LinkedIn feed post for quick review

---

### Notes

- If `-substack.md` or `-linkedin-post.txt` files already exist for this slug, ask the user whether to overwrite or skip.
- The Substack version is intended for copy-paste: run `python scripts/preview.py published/YYYY-MM-DD-slug-substack.md`, then select-all → copy → paste into Substack's editor.
- Personal voice: first-person, conversational, reflective. This is Vic's independent writing, not DeeperPoint marketing.
- Images cannot be embedded via paste — note `[IMAGE: description]` placeholders and add manually in Substack's editor.
