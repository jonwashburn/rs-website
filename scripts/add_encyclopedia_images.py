#!/usr/bin/env python3
import json
import sys
from pathlib import Path


FIGURE_TEMPLATE = (
    '<figure class="concept-visual">'
    '<img src="{src}" alt="{alt}" loading="lazy" decoding="async" />'
    '{cap_html}'
    '</figure>'
)


def build_caption(caption: str, credit: str) -> str:
    if not caption and not credit:
        return ""
    credit_html = f'<span class="figure-credit">{credit}</span>' if credit else ""
    if caption:
        if credit_html:
            return f"<figcaption>{caption} • {credit_html}</figcaption>"
        return f"<figcaption>{caption}</figcaption>"
    return f"<figcaption>{credit_html}</figcaption>"


def insert_hero_figure(html: str, figure_html: str) -> str:
    # Skip if a concept-visual figure already exists
    if 'figure class="concept-visual"' in html:
        return html
    sentinel = '<div class="template-reading">'
    idx = html.find(sentinel)
    if idx == -1:
        return html  # unexpected shape; don't modify
    return html[:idx] + figure_html + html[idx:]


def main():
    if len(sys.argv) > 1:
        manifest_path = Path(sys.argv[1])
    else:
        manifest_path = Path("assets/data/encyclopedia-images.json")
    root = Path(__file__).resolve().parents[1]
    enc_dir = root / "encyclopedia"

    if not manifest_path.exists():
        print(f"Manifest not found: {manifest_path}")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    updated = 0
    for slug, meta in manifest.items():
        page_path = enc_dir / f"{slug}.html"
        if not page_path.exists():
            print(f"Skip missing page: {slug}")
            continue
        try:
            src = meta.get("src") or f"/assets/images/encyclopedia/{slug}.svg"
            alt = meta.get("alt") or slug.replace("-", " ").title()
            caption = meta.get("caption", "")
            credit = meta.get("credit", "")
            cap_html = build_caption(caption, credit)
            figure_html = FIGURE_TEMPLATE.format(src=src, alt=alt, cap_html=cap_html)

            html = page_path.read_text(encoding="utf-8")
            new_html = insert_hero_figure(html, figure_html)
            if new_html != html:
                page_path.write_text(new_html, encoding="utf-8")
                updated += 1
                print(f"Updated: {slug}")
            else:
                print(f"No change (already has figure): {slug}")
        except Exception as e:
            print(f"Error updating {slug}: {e}")

    print(f"Done. Pages updated: {updated}")


if __name__ == "__main__":
    main()


