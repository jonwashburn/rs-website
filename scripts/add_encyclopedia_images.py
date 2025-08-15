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


def build_caption(caption: str, credit: str, license_str: str) -> str:
    if not caption and not credit and not license_str:
        return ""
    credit_html = f'<span class="figure-credit">{credit}</span>' if credit else ""
    license_html = f'<span class="figure-license">{license_str}</span>' if license_str else ""
    parts = [part for part in [caption, credit_html, license_html] if part]
    return f"<figcaption>{' • '.join(parts)}</figcaption>"


def insert_hero_figure(html: str, figure_html: str) -> str:
    # Skip if a concept-visual figure already exists
    if 'figure class="concept-visual"' in html:
        return html
    sentinel = '<div class="template-reading">'
    idx = html.find(sentinel)
    if idx == -1:
        return html  # unexpected shape; don't modify
    return html[:idx] + figure_html + html[idx:]


def insert_after_heading(html: str, heading_text: str, figure_html: str) -> str:
    import re
    # Insert figure immediately after the first matching <h2>Heading</h2>
    pattern = re.compile(rf"(<h2[^>]*>\s*{re.escape(heading_text)}\s*</h2>)", re.IGNORECASE)
    m = pattern.search(html)
    if not m:
        return html
    insert_at = m.end()
    return html[:insert_at] + figure_html + html[insert_at:]


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
            html = page_path.read_text(encoding="utf-8")

            # Support two formats: single image object, or {"images": [...]}
            images = []
            if isinstance(meta, dict) and "images" in meta and isinstance(meta["images"], list):
                images = meta["images"]
            else:
                images = [meta]

            changed = False
            for imeta in images:
                src = imeta.get("src") or f"/assets/images/encyclopedia/{slug}.svg"
                alt = imeta.get("alt") or slug.replace("-", " ").title()
                caption = imeta.get("caption", "")
                credit = imeta.get("credit", "")
                license_str = imeta.get("license", "")
                cap_html = build_caption(caption, credit, license_str)
                figure_html = FIGURE_TEMPLATE.format(src=src, alt=alt, cap_html=cap_html)
                placement = (imeta.get("placement") or "after_heading").lower()
                if placement == "hero":
                    new_html = insert_hero_figure(html, figure_html)
                elif placement == "after_heading":
                    heading = imeta.get("heading") or "How It Works"
                    new_html = insert_after_heading(html, heading, figure_html)
                else:
                    # default to after_heading How It Works
                    new_html = insert_after_heading(html, "How It Works", figure_html)
                if new_html != html:
                    html = new_html
                    changed = True

            if changed:
                page_path.write_text(html, encoding="utf-8")
                updated += 1
                print(f"Updated: {slug}")
            else:
                print(f"No changes for: {slug}")
        except Exception as e:
            print(f"Error updating {slug}: {e}")

    print(f"Done. Pages updated: {updated}")


if __name__ == "__main__":
    main()


