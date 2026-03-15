# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Preview Script for VicPersonalBlog

Renders a Markdown file to styled HTML and opens it in the default browser.
Designed for Substack copy-paste workflow: open the preview, select-all,
copy, then paste into Substack's rich-text editor.

Usage:
    python scripts/preview.py <path-to-markdown-file>

Examples:
    python scripts/preview.py published/2026-03-15-my-post-substack.md
    python scripts/preview.py drafts/rough-idea.md
"""

import sys
import tempfile
import webbrowser
from pathlib import Path

import markdown


PREVIEW_CSS = """
body {
    max-width: 680px;
    margin: 40px auto;
    padding: 0 20px;
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 18px;
    line-height: 1.7;
    color: #1a1a1a;
    background: #fff;
}
h1 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 2em;
    line-height: 1.2;
    margin-bottom: 0.2em;
    color: #111;
}
h2 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 1.4em;
    margin-top: 2em;
    margin-bottom: 0.5em;
    color: #222;
}
h3 {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 1.15em;
    margin-top: 1.5em;
    color: #333;
}
p {
    margin-bottom: 1.2em;
}
blockquote {
    border-left: 3px solid #ccc;
    margin: 1.5em 0;
    padding: 0.5em 1.2em;
    color: #555;
    font-style: italic;
}
ul, ol {
    margin-bottom: 1.2em;
    padding-left: 1.5em;
}
li {
    margin-bottom: 0.4em;
}
a {
    color: #0066cc;
    text-decoration: underline;
}
hr {
    border: none;
    border-top: 1px solid #ddd;
    margin: 2em 0;
}
strong {
    font-weight: 700;
}
em {
    font-style: italic;
}
code {
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.9em;
    background: #f5f5f5;
    padding: 2px 5px;
    border-radius: 3px;
}
.subtitle {
    font-size: 1.15em;
    color: #666;
    font-style: italic;
    margin-top: -0.5em;
    margin-bottom: 2em;
}
.preview-banner {
    background: #fff3cd;
    border: 1px solid #ffc107;
    padding: 10px 16px;
    border-radius: 6px;
    font-family: -apple-system, sans-serif;
    font-size: 13px;
    color: #856404;
    margin-bottom: 2em;
    text-align: center;
}
"""

MD_EXTENSIONS = ["fenced_code", "tables", "smarty", "attr_list"]


def stripFrontmatter(text):
    """Remove YAML frontmatter from markdown text, return (frontmatter_lines, body)."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i, line in enumerate(lines[1:], start=1):
            if line.strip() == "---":
                return lines[1:i], "\n".join(lines[i + 1:])
    return [], text


def renderMarkdown(filepath):
    """Render a markdown file to a complete HTML page for browser preview."""
    text = Path(filepath).read_text(encoding="utf-8")

    # Strip copyright comment if present
    if text.startswith("<!--"):
        end = text.find("-->")
        if end != -1:
            text = text[end + 3:].lstrip("\n")

    frontmatter_lines, body = stripFrontmatter(text)

    # Extract title from frontmatter if present
    title = "Preview"
    for line in frontmatter_lines:
        if line.startswith("title:"):
            title = line.split(":", 1)[1].strip().strip("'\"")
            break

    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    bodyHtml = md.convert(body)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Preview</title>
    <style>{PREVIEW_CSS}</style>
</head>
<body>
    <div class="preview-banner">
        📋 Preview mode — Select All (⌘A), Copy (⌘C), then paste into Substack's editor.
    </div>
    {bodyHtml}
</body>
</html>"""

    return html


def main():
    """Render markdown to HTML and open in browser."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/preview.py <path-to-markdown-file>")
        print("Example: python scripts/preview.py published/2026-03-15-slug-substack.md")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    html = renderMarkdown(filepath)

    # Write to temp file and open
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        prefix="substack-preview-",
        delete=False,
        encoding="utf-8",
    ) as f:
        f.write(html)
        tmpPath = f.name

    print(f"Preview written to: {tmpPath}")
    print("Opening in browser...")
    webbrowser.open(f"file://{tmpPath}")


if __name__ == "__main__":
    main()
