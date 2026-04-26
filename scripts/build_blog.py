# Copyright (c) 2026 Mustafa Uzumeri. All rights reserved.

"""
Blog Build Script for uzumeri.com

Reads Markdown posts from blog/posts/, converts them to HTML using the site's
design system, and generates a blog index page and RSS feed.

Simplified from the DeeperPoint blog builder — no streams, no series.

Usage:
    python scripts/build_blog.py

Posts must have YAML frontmatter with: title, date, tags, summary, slug.
"""

import re
from datetime import datetime
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, tostring

import markdown
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = SITE_ROOT / "blog" / "posts"
BLOG_OUT = SITE_ROOT / "blog"
SITE_URL = "https://uzumeri.com"
FEED_TITLE = "Vic Uzumeri — Writing"
FEED_DESC = "Independent professional writing on strategy, technology, trade, and the world."

MD_EXTENSIONS = ["fenced_code", "tables", "toc", "smarty", "attr_list", "footnotes", "md_in_html"]

# ---------------------------------------------------------------------------
# Tag colors — consistent with the existing blog.html card styling
# ---------------------------------------------------------------------------

TAG_COLORS = {
    "strategy":   ("#fbbf24", "rgba(245,158,11,.15)"),
    "opinion":    ("#f87171", "rgba(248,113,113,.15)"),
    "trade":      ("#60a5fa", "rgba(59,130,246,.15)"),
    "ai":         ("#a78bfa", "rgba(139,92,246,.15)"),
    "canada":     ("#34d399", "rgba(16,185,129,.15)"),
    "technology": ("#38bdf8", "rgba(56,189,248,.15)"),
    "education":  ("#fb923c", "rgba(251,146,60,.15)"),
    "reflection": ("#c084fc", "rgba(192,132,252,.15)"),
}

DEFAULT_TAG_COLOR = ("#94a3b8", "rgba(148,163,184,.12)")

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

PAGE_HEAD = """<!-- Copyright (c) 2026 Mustafa Uzumeri. All rights reserved. -->
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Vic Uzumeri</title>
  <meta name="description" content="{description}">

  <!-- Open Graph -->
  <meta property="og:type" content="{og_type}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="Vic Uzumeri">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap"
    rel="stylesheet">
  <link rel="stylesheet" href="{css_path}">
  <link rel="alternate" type="application/rss+xml" title="{feed_title}" href="{feed_url}">
</head>

<body>

  <!-- Animated Background -->
  <div class="bg-mesh" aria-hidden="true">
    <div class="bg-mesh__orb bg-mesh__orb--1"></div>
    <div class="bg-mesh__orb bg-mesh__orb--2"></div>
    <div class="bg-mesh__orb bg-mesh__orb--3"></div>
  </div>

  <!-- Navigation -->
  <nav class="nav" id="nav">
    <div class="nav__inner">
      <a href="{root}index.html" class="nav__logo">Vic<span>Uzumeri</span></a>
      <button class="nav__toggle" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
        <span class="nav__toggle-bar"></span>
      </button>
      <ul class="nav__links">
        <li><a href="{root}index.html" class="nav__link">Home</a></li>
        <li><a href="{root}history.html" class="nav__link">History</a></li>
        <li><a href="{root}blog/index.html" class="nav__link{blog_active}">Blog</a></li>
      </ul>
    </div>
  </nav>
"""

PAGE_FOOTER = """
  <!-- Footer -->
  <footer class="footer">
    <div class="container">
      <div class="footer__inner">
        <div class="footer__copyright">
          &copy; 2026 Mustafa Uzumeri. All rights reserved.
        </div>
        <ul class="footer__links">
          <li><a href="https://deeperpoint.com" class="footer__link" target="_blank" rel="noopener">DeeperPoint</a></li>
          <li><a href="https://uzumeri.substack.com" class="footer__link" target="_blank" rel="noopener">Substack</a></li>
          <li><a href="https://github.com/uzumeri" class="footer__link" target="_blank" rel="noopener">GitHub</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script src="{root}reveal.js"></script>
  <script src="{root}nav-mobile.js"></script>
</body>

</html>
"""

# ---------------------------------------------------------------------------
# Blog Index Styles
# ---------------------------------------------------------------------------

BLOG_INDEX_STYLES = """  <style>
    .blog-tag-strip {
      display: flex; flex-wrap: wrap; gap: .35rem;
      justify-content: center; margin-bottom: 1.75rem;
    }
    .blog-tag-pill {
      padding: 3px 11px; border-radius: 14px;
      border: 1px solid rgba(99,102,241,.22);
      background: transparent; color: #64748b;
      font-size: .72rem; font-weight: 600; cursor: pointer;
      font-family: inherit; letter-spacing: .04em;
      transition: background .12s, color .12s, border-color .12s;
      white-space: nowrap;
    }
    .blog-tag-pill:hover {
      background: rgba(99,102,241,.1); color: #a5b4fc;
      border-color: rgba(99,102,241,.45);
    }
    .blog-tag-pill.active {
      background: rgba(99,102,241,.2); color: #c7d2fe;
      border-color: #6366f1;
    }
    .blog-index-count {
      text-align: center; font-size: .82rem;
      color: #64748b; margin-bottom: 1.75rem;
    }
    #blog-post-count { font-weight: 700; color: #a5b4fc; }
    .blog-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 1.25rem;
      align-items: start;
    }
    @media (max-width: 740px) {
      .blog-grid { grid-template-columns: 1fr; }
    }
    .blog-year-heading {
      grid-column: 1 / -1;
      font-size: .68rem; font-weight: 700; letter-spacing: .15em;
      text-transform: uppercase; color: #475569;
      border-bottom: 1px solid rgba(99,102,241,.12);
      padding-bottom: .45rem; margin-top: 1rem;
    }
    .blog-year-heading:first-child { margin-top: 0; }
    .blog-card--featured { grid-column: 1 / -1; }
    .blog-card--featured .blog-card__title { font-size: 1.3rem; }
    .blog-index-item--hidden { display: none !important; }
  </style>"""

# ---------------------------------------------------------------------------
# Post Parsing
# ---------------------------------------------------------------------------


def parsePost(filepath):
    """Parse a Markdown file with YAML frontmatter. Returns (metadata, html_body)."""
    text = filepath.read_text(encoding="utf-8")

    # Strip HTML comment copyright line if present
    text = re.sub(r"^<!--.*?-->\s*\n?", "", text, count=1)

    # Split frontmatter from body
    match = re.search(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, flags=re.DOTALL | re.MULTILINE)
    if not match:
        print(f"  SKIP {filepath.name} — no YAML frontmatter")
        return None, None

    meta = yaml.safe_load(match.group(1))
    body_md = match.group(2)

    # Validate required fields
    required = ["title", "date", "tags", "summary", "slug"]
    missing = [f for f in required if f not in meta]
    if missing:
        print(f"  SKIP {filepath.name} — missing fields: {', '.join(missing)}")
        return None, None

    # Ensure date is a datetime.date
    if isinstance(meta["date"], str):
        meta["date"] = datetime.strptime(meta["date"], "%Y-%m-%d").date()

    # Convert Markdown to HTML
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    body_html = md.convert(body_md)

    # Estimate reading time
    word_count = len(body_md.split())
    meta["reading_time"] = max(1, round(word_count / 250))

    return meta, body_html


# ---------------------------------------------------------------------------
# Page Generation
# ---------------------------------------------------------------------------


def buildTagHtml(tag):
    """Build a styled tag span."""
    color, bg = TAG_COLORS.get(tag, DEFAULT_TAG_COLOR)
    return (
        f'<span style="background:{bg};color:{color};padding:2px 8px;'
        f'border-radius:100px;font-size:0.6875rem;font-weight:600;'
        f'margin-right:0.5rem;">{tag}</span>'
    )


def buildPostPage(meta, body_html):
    """Generate a full HTML page for a single blog post."""
    date_str = meta["date"].strftime("%B %d, %Y")
    tags_html = "".join(
        f'<span class="blog-tag">{tag}</span>' for tag in meta["tags"]
    )

    head = PAGE_HEAD.format(
        title=meta["title"],
        description=meta["summary"],
        og_type="article",
        url=f"{SITE_URL}/blog/{meta['slug']}.html",
        css_path="../styles.css",
        feed_title=FEED_TITLE,
        feed_url=f"{SITE_URL}/blog/feed.xml",
        root="../",
        blog_active=" nav__link--active",
    )

    content = f"""
  <section class="section" id="blog-post" style="padding-top: calc(var(--space-4xl) + 60px);">
    <div class="container container--narrow">
      <div class="reveal">
        <a href="index.html" class="blog-back">&larr; All Posts</a>
        <div class="blog-meta">
          <time datetime="{meta['date'].isoformat()}">{date_str}</time>
          <span class="blog-meta__sep">&middot;</span>
          <span>{meta['reading_time']} min read</span>
        </div>
        <h1 class="blog-post__title">{meta['title']}</h1>
        <div class="blog-meta" style="margin-bottom: var(--space-2xl);">
          {tags_html}
        </div>
      </div>
      <article class="blog-post">
        {body_html}
      </article>
    </div>
  </section>
"""

    footer = PAGE_FOOTER.format(root="../")

    return head + content + footer


def buildPostCardHtml(meta, is_featured=False):
    """Build a post card for the blog index."""
    date_str = meta["date"].strftime("%B %d, %Y")
    year = str(meta["date"].year)
    tags_html = "".join(buildTagHtml(tag) for tag in meta["tags"])
    featured_class = " blog-card--featured" if is_featured else ""
    tags_attr = " ".join(meta.get("tags", []))
    return f"""
        <a href="{meta['slug']}.html"
           class="blog-card card reveal{featured_class}"
           data-year="{year}" data-tags="{tags_attr}">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:var(--space-md);flex-wrap:wrap;margin-bottom:var(--space-sm);">
            <span style="font-family:var(--font-mono);font-size:0.8125rem;color:var(--dp-blue-light);">{date_str}</span>
            <span style="font-size:0.75rem;color:var(--dp-muted);">{meta['reading_time']} min read</span>
          </div>
          <h3 style="font-size:1.25rem;margin-bottom:var(--space-sm);">{meta['title']}</h3>
          <p style="color:var(--dp-silver);font-size:0.9375rem;line-height:1.7;">{meta['summary']}</p>
          <div style="margin-top:var(--space-md);font-size:0.8125rem;color:var(--dp-muted);">{tags_html}</div>
        </a>"""


def buildIndexPage(posts):
    """Generate the blog listing page."""
    head = PAGE_HEAD.format(
        title="Writing",
        description="Independent professional writing by Vic Uzumeri on strategy, technology, trade, and the world.",
        og_type="website",
        url=f"{SITE_URL}/blog/",
        css_path="../styles.css",
        feed_title=FEED_TITLE,
        feed_url=f"{SITE_URL}/blog/feed.xml",
        root="../",
        blog_active=" nav__link--active",
    )

    total = len(posts)

    # Group by year
    year_groups = {}
    year_order = []
    for meta in posts:
        yr = str(meta["date"].year)
        if yr not in year_groups:
            year_groups[yr] = []
            year_order.append(yr)
        year_groups[yr].append(meta)

    # Render grid
    grid_html = ""
    is_first = True
    for yr in year_order:
        grid_html += f'\n        <div class="blog-year-heading" data-year="{yr}">{yr}</div>'
        for meta in year_groups[yr]:
            grid_html += buildPostCardHtml(meta, is_featured=is_first)
            is_first = False

    # Collect all tags
    all_tags = sorted({t for m in posts for t in m.get("tags", [])})
    tags_strip_html = "".join(
        f'<button class="blog-tag-pill" data-tag="{t}">{t}</button>\n        '
        for t in all_tags
    )

    filter_js = """
  <script>
  (function () {
    var items     = Array.from(document.querySelectorAll('[data-tags]'));
    var yearHeads = Array.from(document.querySelectorAll('.blog-year-heading'));
    var countEl   = document.getElementById('blog-post-count');
    var clearBtn  = document.getElementById('blog-clear-btn');
    var activeTag = '';

    function cardTags(el) {
      return el.dataset.tags ? el.dataset.tags.split(' ').filter(Boolean) : [];
    }

    function applyFilter() {
      var vis = 0;
      items.forEach(function (el) {
        var show = !activeTag || cardTags(el).indexOf(activeTag) !== -1;
        el.classList.toggle('blog-index-item--hidden', !show);
        if (show) vis++;
      });

      // Featured: first visible card gets full-width only in unfiltered view
      var first = items.find(function (el) {
        return !el.classList.contains('blog-index-item--hidden');
      });
      items.forEach(function (el) { el.classList.remove('blog-card--featured'); });
      if (!activeTag && first) first.classList.add('blog-card--featured');

      // Hide year headings with no visible items
      yearHeads.forEach(function (h) {
        var yr  = h.dataset.year;
        var has = items.some(function (el) {
          return el.dataset.year === yr && !el.classList.contains('blog-index-item--hidden');
        });
        h.classList.toggle('blog-index-item--hidden', !has);
      });

      if (countEl) countEl.textContent = vis;
      if (clearBtn) clearBtn.style.display = activeTag ? 'inline-flex' : 'none';

      document.querySelectorAll('.blog-tag-pill').forEach(function (btn) {
        btn.classList.toggle('active', btn.dataset.tag === activeTag);
      });
    }

    document.querySelectorAll('.blog-tag-pill').forEach(function (btn) {
      btn.addEventListener('click', function () {
        activeTag = activeTag === this.dataset.tag ? '' : this.dataset.tag;
        applyFilter();
      });
    });

    if (clearBtn) {
      clearBtn.addEventListener('click', function () {
        activeTag = '';
        applyFilter();
      });
    }

    applyFilter();
  })();
  </script>"""

    content = f"""
  <section class="section" id="blog-index" style="padding-top: calc(var(--space-4xl) + 60px);">
    <div class="container container--narrow">
      <div class="reveal text-center" style="margin-bottom: var(--space-2xl);">
        <div class="hero__badge" style="margin-bottom: var(--space-md);">
            <span class="hero__badge__dot"></span>
            Personal Writing
        </div>
        <h1 class="section__title">Writing</h1>
        <p class="section__desc section__desc--centered">
          Independent professional writing published on
          <a href="https://uzumeri.substack.com/" target="_blank" rel="noopener">Substack</a>
          and here. Reflections on strategy, technology, trade, and the world.
        </p>
      </div>
      <div class="blog-tag-strip">
        {tags_strip_html}
      </div>
      <div class="blog-index-count">
        Showing <span id="blog-post-count">{total}</span> of {total} posts
        <button id="blog-clear-btn"
                style="display:none;margin-left:.75rem;padding:2px 10px;border-radius:14px;
                       border:1px solid rgba(239,68,68,.4);background:transparent;
                       color:#fca5a5;font-size:.74rem;font-weight:600;
                       cursor:pointer;font-family:inherit;
                       transition:background .15s;"
                onmouseover="this.style.background='rgba(239,68,68,.12)'"
                onmouseout="this.style.background='transparent'"">&#10005; Show all</button>
      </div>
      <div class="blog-grid">
        {grid_html}
      </div>

      <!-- Substack CTA -->
      <div class="reveal" style="margin-top: var(--space-3xl); text-align: center;">
        <div style="background: rgba(255, 255, 255, 0.03); padding: var(--space-xl); border-radius: var(--radius-lg); border: 1px solid rgba(255, 255, 255, 0.1);">
          <p style="color: var(--dp-silver); margin-bottom: var(--space-lg);">
            Subscribe on Substack to receive new articles by email.
          </p>
          <a href="https://uzumeri.substack.com/" target="_blank" rel="noopener" class="btn btn--primary">
            Subscribe on Substack &rarr;
          </a>
        </div>
      </div>
    </div>
  </section>
{filter_js}
"""

    # Inject index-specific styles into the head
    index_head = head.replace("</head>", BLOG_INDEX_STYLES + "\n</head>")
    footer = PAGE_FOOTER.format(root="../")

    return index_head + content + footer


# ---------------------------------------------------------------------------
# RSS Feed
# ---------------------------------------------------------------------------


def buildRssFeed(posts):
    """Generate an RSS 2.0 XML feed."""
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    SubElement(channel, "title").text = FEED_TITLE
    SubElement(channel, "link").text = f"{SITE_URL}/blog/"
    SubElement(channel, "description").text = FEED_DESC
    SubElement(channel, "language").text = "en"
    SubElement(channel, "lastBuildDate").text = datetime.now(
        tz=__import__("datetime").timezone.utc
    ).strftime(
        "%a, %d %b %Y %H:%M:%S +0000"
    )

    for meta in posts:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = meta["title"]
        SubElement(item, "link").text = f"{SITE_URL}/blog/{meta['slug']}.html"
        SubElement(item, "description").text = meta["summary"]
        SubElement(item, "pubDate").text = meta["date"].strftime(
            "%a, %d %b %Y 00:00:00 +0000"
        )
        SubElement(item, "guid").text = f"{SITE_URL}/blog/{meta['slug']}.html"
        for tag in meta["tags"]:
            SubElement(item, "category").text = tag

    xml_bytes = tostring(rss, encoding="unicode", xml_declaration=False)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_bytes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    """Build all blog pages from Markdown sources."""
    print("Blog build starting...")
    print(f"  Posts dir: {POSTS_DIR}")
    print(f"  Output dir: {BLOG_OUT}")

    if not POSTS_DIR.exists():
        print(f"  Creating posts directory: {POSTS_DIR}")
        POSTS_DIR.mkdir(parents=True, exist_ok=True)
        print("  No posts found. Done.")
        return

    # Collect and parse all posts
    md_files = sorted(POSTS_DIR.glob("*.md"))
    if not md_files:
        print("  No .md files found in posts directory.")
        return

    posts = []
    for filepath in md_files:
        meta, body_html = parsePost(filepath)
        if meta is None:
            continue
        meta["_body_html"] = body_html
        posts.append(meta)
        print(f"  Parsed: {filepath.name} -> {meta['slug']}.html")

    # Sort by date, newest first
    posts.sort(key=lambda p: p["date"], reverse=True)

    # Generate individual post pages
    BLOG_OUT.mkdir(parents=True, exist_ok=True)
    for meta in posts:
        body_html = meta.pop("_body_html")
        page = buildPostPage(meta, body_html)
        out_path = BLOG_OUT / f"{meta['slug']}.html"
        out_path.write_text(page, encoding="utf-8")
        print(f"  Wrote: {out_path.name}")

    # Generate index page
    index_html = buildIndexPage(posts)
    index_path = BLOG_OUT / "index.html"
    index_path.write_text(index_html, encoding="utf-8")
    print(f"  Wrote: index.html ({len(posts)} posts)")

    # Generate RSS feed
    feed_xml = buildRssFeed(posts)
    feed_path = BLOG_OUT / "feed.xml"
    feed_path.write_text(feed_xml, encoding="utf-8")
    print("  Wrote: feed.xml")

    print(f"Blog build complete. {len(posts)} posts published.")


if __name__ == "__main__":
    main()
