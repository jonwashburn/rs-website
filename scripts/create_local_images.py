#!/usr/bin/env python3
"""Create local SVG images for encyclopedia entries"""
import json
from pathlib import Path

def create_svg_placeholder(title, subtitle, color_scheme):
    """Create a simple SVG placeholder image"""
    bg_color, text_color, accent_color = color_scheme
    
    svg = f'''<svg width="800" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{bg_color};stop-opacity:1" />
      <stop offset="100%" style="stop-color:{accent_color};stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="800" height="400" fill="url(#grad)"/>
  <text x="400" y="180" font-family="Arial, sans-serif" font-size="48" font-weight="bold" text-anchor="middle" fill="{text_color}">{title}</text>
  <text x="400" y="230" font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="{text_color}" opacity="0.8">{subtitle}</text>
  <circle cx="400" cy="300" r="30" fill="none" stroke="{text_color}" stroke-width="2" opacity="0.3"/>
  <circle cx="400" cy="300" r="20" fill="none" stroke="{text_color}" stroke-width="2" opacity="0.4"/>
  <circle cx="400" cy="300" r="10" fill="none" stroke="{text_color}" stroke-width="2" opacity="0.5"/>
</svg>'''
    return svg

def main():
    # Color schemes for different categories
    color_schemes = {
        "physics": ("#1a2f4b", "#ffffff", "#2a4f7b"),
        "quantum": ("#2b1f4d", "#ffffff", "#4b3f7d"),
        "cosmos": ("#0f1f3f", "#ffffff", "#1f3f6f"),
        "math": ("#1f3f1f", "#ffffff", "#3f5f3f"),
        "default": ("#2f2f2f", "#ffffff", "#4f4f4f")
    }
    
    # Create basic placeholder images
    images_dir = Path("assets/images/encyclopedia")
    
    # Create hero images
    placeholders = [
        ("hero-physics", "Recognition Science", "Fundamental Framework", color_schemes["physics"]),
        ("hero-quantum", "Quantum Recognition", "Measurement & Reality", color_schemes["quantum"]),
        ("hero-cosmos", "Cosmic Structure", "Universe as Recognition", color_schemes["cosmos"]),
        ("hero-math", "Mathematical Framework", "The Ledger Calculus", color_schemes["math"]),
        ("hero-default", "Recognition Physics", "Encyclopedia Entry", color_schemes["default"]),
        
        # Section images
        ("section-how", "How It Works", "Mechanism & Process", color_schemes["physics"]),
        ("section-math", "Mathematical Foundation", "Formal Structure", color_schemes["math"]),
        ("section-physical", "Physical Meaning", "Real-World Implications", color_schemes["quantum"]),
        ("section-testable", "Testable Predictions", "Experimental Verification", color_schemes["cosmos"]),
        ("section-implications", "Key Implications", "Broader Consequences", color_schemes["default"])
    ]
    
    for filename, title, subtitle, colors in placeholders:
        svg_content = create_svg_placeholder(title, subtitle, colors)
        svg_path = images_dir / f"{filename}.svg"
        svg_path.write_text(svg_content)
        print(f"Created: {svg_path}")
    
    # Update all HTML files to use local images
    enc_dir = Path("encyclopedia")
    fixed_count = 0
    
    for html_file in enc_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue
        
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            
            # Replace placeholder.com URLs with local SVGs
            replacements = [
                ("https://via.placeholder.com/800x400/1a2f4b/ffffff?text=Recognition+Science", 
                 "/assets/images/encyclopedia/hero-physics.svg"),
                ("https://via.placeholder.com/800x400/2b4162/ffffff?text=Mathematical+Framework",
                 "/assets/images/encyclopedia/section-math.svg"),
                ("https://via.placeholder.com/800x400/3c5273/ffffff?text=Physical+Implications",
                 "/assets/images/encyclopedia/section-physical.svg"),
                # Also catch any other placeholder URLs
                ("https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=400&fit=crop",
                 "/assets/images/encyclopedia/hero-physics.svg"),
                ("https://images.unsplash.com/photo-1635070041409-e63e783ce3c1?w=800&h=400&fit=crop",
                 "/assets/images/encyclopedia/hero-quantum.svg"),
                ("https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&h=400&fit=crop",
                 "/assets/images/encyclopedia/hero-cosmos.svg")
            ]
            
            new_content = content
            for old_url, new_url in replacements:
                new_content = new_content.replace(old_url, new_url)
            
            if new_content != content:
                html_file.write_text(new_content, encoding="utf-8")
                fixed_count += 1
                print(f"Fixed: {html_file.name}")
                
        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")
    
    print(f"\nFixed {fixed_count} HTML files to use local images")
    
    # Update manifest for future generations
    manifest_file = Path("assets/data/encyclopedia-images.json")
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Update to use local images
    for page_id, page_data in manifest.items():
        if "images" in page_data:
            for i, img in enumerate(page_data["images"]):
                if i == 0:  # Hero image
                    img["src"] = "/assets/images/encyclopedia/hero-default.svg"
                elif "How It Works" in img.get("heading", ""):
                    img["src"] = "/assets/images/encyclopedia/section-how.svg"
                elif "Mathematical" in img.get("heading", ""):
                    img["src"] = "/assets/images/encyclopedia/section-math.svg"
                else:
                    img["src"] = "/assets/images/encyclopedia/section-physical.svg"
                
                img["credit"] = "Recognition Physics Institute"
                img["license"] = "CC BY 4.0"
    
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print("Updated manifest to use local images")

if __name__ == "__main__":
    main()
