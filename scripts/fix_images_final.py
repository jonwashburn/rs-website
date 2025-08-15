#!/usr/bin/env python3
"""Final fix for encyclopedia images - use stable, working image sources"""
import json
import re
from pathlib import Path

# Stable image sources that work
STABLE_IMAGES = {
    # NASA/ESA images (Public Domain, very stable)
    "nasa_hubble": "https://www.nasa.gov/sites/default/files/thumbnails/image/hubble_friday_12102021.jpg",
    "nasa_nebula": "https://www.nasa.gov/sites/default/files/thumbnails/image/pia23122.jpg",
    "nasa_galaxy": "https://www.nasa.gov/sites/default/files/thumbnails/image/stsci-h-p2022a-f-1920x1080.jpg",
    
    # Placeholder images (always work)
    "physics_hero": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?w=800&h=400&fit=crop",
    "quantum_hero": "https://images.unsplash.com/photo-1635070041409-e63e783ce3c1?w=800&h=400&fit=crop", 
    "cosmos_hero": "https://images.unsplash.com/photo-1444703686981-a3abbc4d4fe3?w=800&h=400&fit=crop",
    
    # Simple colored placeholders as fallback
    "placeholder_1": "https://via.placeholder.com/800x400/1a2f4b/ffffff?text=Recognition+Science",
    "placeholder_2": "https://via.placeholder.com/800x400/2b4162/ffffff?text=Mathematical+Framework",
    "placeholder_3": "https://via.placeholder.com/800x400/3c5273/ffffff?text=Physical+Implications"
}

def get_stable_images_for_category(category):
    """Return stable images based on category"""
    if "cosmology" in category.lower() or "astrophysics" in category.lower():
        return [
            {"src": STABLE_IMAGES["cosmos_hero"], "credit": "Unsplash", "license": "Unsplash License"},
            {"src": STABLE_IMAGES["nasa_galaxy"], "credit": "NASA/ESA", "license": "Public Domain"},
            {"src": STABLE_IMAGES["nasa_nebula"], "credit": "NASA", "license": "Public Domain"}
        ]
    elif "quantum" in category.lower() or "particle" in category.lower():
        return [
            {"src": STABLE_IMAGES["quantum_hero"], "credit": "Unsplash", "license": "Unsplash License"},
            {"src": STABLE_IMAGES["placeholder_2"], "credit": "Placeholder", "license": "CC0"},
            {"src": STABLE_IMAGES["placeholder_3"], "credit": "Placeholder", "license": "CC0"}
        ]
    else:  # Default for physics/fundamentals
        return [
            {"src": STABLE_IMAGES["physics_hero"], "credit": "Unsplash", "license": "Unsplash License"},
            {"src": STABLE_IMAGES["placeholder_1"], "credit": "Placeholder", "license": "CC0"},
            {"src": STABLE_IMAGES["placeholder_2"], "credit": "Placeholder", "license": "CC0"}
        ]

def fix_html_images(html_content):
    """Replace broken Wikipedia URLs in HTML with stable ones"""
    # Pattern to find img tags
    img_pattern = r'<img\s+src="([^"]+)"([^>]+)>'
    
    def replace_img(match):
        src = match.group(1)
        attrs = match.group(2)
        
        # Check if it's a Wikipedia URL that might be broken
        if "wikipedia" in src or "/v1/AUTH_mw/" in src:
            # Replace with a stable placeholder
            new_src = STABLE_IMAGES["placeholder_1"]
            return f'<img src="{new_src}"{attrs}>'
        return match.group(0)
    
    return re.sub(img_pattern, replace_img, html_content)

def main():
    # Fix HTML files directly
    enc_dir = Path("encyclopedia")
    fixed_count = 0
    
    for html_file in enc_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue
        
        try:
            content = html_file.read_text(encoding="utf-8", errors="ignore")
            new_content = fix_html_images(content)
            
            if new_content != content:
                html_file.write_text(new_content, encoding="utf-8")
                fixed_count += 1
                print(f"Fixed: {html_file.name}")
        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")
    
    print(f"\nFixed {fixed_count} HTML files")
    
    # Also update the manifest for future generations
    manifest_file = Path("assets/data/encyclopedia-images.json")
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Simple approach: give each page stable images
    for page_id, page_data in manifest.items():
        if "images" in page_data:
            stable_imgs = get_stable_images_for_category("default")
            for i, img in enumerate(page_data["images"]):
                if i < len(stable_imgs):
                    img["src"] = stable_imgs[i]["src"]
                    img["credit"] = stable_imgs[i]["credit"]
                    img["license"] = stable_imgs[i]["license"]
    
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print("Updated manifest with stable images")

if __name__ == "__main__":
    main()
