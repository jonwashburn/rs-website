#!/usr/bin/env python3
"""
Normalize all HTML pages to use the shared header/footer includes and JS loader.

Actions per file:
  - Remove any inline <header class="site-header"> ... </header> blocks
  - Ensure <div id="header-placeholder"></div> and <div id="sitewide-banner-placeholder"></div> right after <body>
  - Ensure <div id="footer-placeholder"></div> before </body>
  - Ensure <script src="/assets/js/main.js"></script> is included before </body>

Run from repo root: python3 scripts/normalize_header.py
"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def normalize_html(path: Path) -> bool:
    text = path.read_text(encoding='utf-8', errors='ignore')
    original = text

    # Remove any existing inline site header block to avoid duplicates
    text = re.sub(
        r"<header[^>]*class=\"site-header\"[\s\S]*?</header>",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # Ensure header + banner placeholders after <body>
    if 'id="header-placeholder"' not in text:
        m = re.search(r"<body[^>]*>", text, flags=re.IGNORECASE)
        if m:
            insert_pos = m.end()
            inject = "\n  <div id=\"header-placeholder\"></div>\n  <div id=\"sitewide-banner-placeholder\"></div>\n"
            text = text[:insert_pos] + inject + text[insert_pos:]

    # Ensure footer placeholder before </body>
    if 'id="footer-placeholder"' not in text:
        text = re.sub(
            r"</body>",
            "  \n  <div id=\"footer-placeholder\"></div>\n</body>",
            text,
            flags=re.IGNORECASE,
        )

    # Ensure main.js loader present
    if '/assets/js/main.js' not in text:
        text = re.sub(
            r"</body>",
            "  \n  <script src=\"/assets/js/main.js\"></script>\n</body>",
            text,
            flags=re.IGNORECASE,
        )

    if text != original:
        path.write_text(text, encoding='utf-8')
        return True
    return False

def should_skip(path: Path) -> bool:
    p = str(path)
    skip_parts = [
        '/_includes/',
        '/node_modules/',
        '/tools/',
        '/scripts/',
        '/assets/',
        'test-styling.html',
    ]
    return any(s in p for s in skip_parts)

def main():
    html_files = sorted(ROOT.glob('**/*.html'))
    changed = 0
    for f in html_files:
        if should_skip(f):
            continue
        try:
            if normalize_html(f):
                changed += 1
                print(f"normalized: {f.relative_to(ROOT)}")
        except Exception as e:
            print(f"error: {f} -> {e}")
    print(f"Done. Changed {changed} files.")

if __name__ == '__main__':
    main()


