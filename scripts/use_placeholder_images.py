#!/usr/bin/env python3
"""Replace broken Wikipedia images with placeholder images until we find better sources"""
import json
from pathlib import Path

def main():
    # Create placeholder URLs based on category
    placeholders = {
        "Recognition Physics Fundamentals": [
            "https://via.placeholder.com/800x400/4a5568/ffffff?text=Recognition+Physics",
            "https://via.placeholder.com/800x400/5a6578/ffffff?text=How+It+Works",
            "https://via.placeholder.com/800x400/6a7588/ffffff?text=Mathematical+Framework"
        ],
        "Fundamental Constants": [
            "https://via.placeholder.com/800x400/2e5266/ffffff?text=Fundamental+Constants",
            "https://via.placeholder.com/800x400/3e6276/ffffff?text=Physical+Meaning",
            "https://via.placeholder.com/800x400/4e7286/ffffff?text=Experimental+Verification"
        ],
        "Quantum & Particle Physics": [
            "https://via.placeholder.com/800x400/4b0082/ffffff?text=Quantum+Physics",
            "https://via.placeholder.com/800x400/5b1092/ffffff?text=Quantum+Behavior",
            "https://via.placeholder.com/800x400/6b20a2/ffffff?text=Particle+Interactions"
        ],
        "Spacetime & Gravity": [
            "https://via.placeholder.com/800x400/1a1a2e/ffffff?text=Spacetime+%26+Gravity",
            "https://via.placeholder.com/800x400/2a2a3e/ffffff?text=Gravitational+Effects",
            "https://via.placeholder.com/800x400/3a3a4e/ffffff?text=Spacetime+Structure"
        ],
        "Cosmology & Astrophysics": [
            "https://via.placeholder.com/800x400/0f3460/ffffff?text=Cosmology",
            "https://via.placeholder.com/800x400/1f4470/ffffff?text=Cosmic+Evolution",
            "https://via.placeholder.com/800x400/2f5480/ffffff?text=Observable+Universe"
        ],
        "default": [
            "https://via.placeholder.com/800x400/333333/ffffff?text=Recognition+Science",
            "https://via.placeholder.com/800x400/444444/ffffff?text=Conceptual+Diagram",
            "https://via.placeholder.com/800x400/555555/ffffff?text=Mathematical+Structure"
        ]
    }
    
    # Load manifest
    manifest_file = Path("assets/data/encyclopedia-images.json")
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Update all images to use placeholders
    for page_id, page_data in manifest.items():
        if "images" in page_data:
            # Find the category for this page
            category = None
            # Try to determine category from existing images
            for img in page_data["images"]:
                if "Recognition Physics" in img.get("caption", ""):
                    category = "Recognition Physics Fundamentals"
                    break
                elif "constant" in img.get("caption", "").lower():
                    category = "Fundamental Constants"
                    break
                elif "quantum" in img.get("caption", "").lower():
                    category = "Quantum & Particle Physics"
                    break
                elif "spacetime" in img.get("caption", "").lower() or "gravity" in img.get("caption", "").lower():
                    category = "Spacetime & Gravity"
                    break
                elif "cosmic" in img.get("caption", "").lower() or "universe" in img.get("caption", "").lower():
                    category = "Cosmology & Astrophysics"
                    break
            
            # Get appropriate placeholders
            placeholder_urls = placeholders.get(category, placeholders["default"])
            
            # Update each image
            for i, img in enumerate(page_data["images"]):
                # Use appropriate placeholder based on position
                placeholder_index = min(i, len(placeholder_urls) - 1)
                img["src"] = placeholder_urls[placeholder_index]
                # Keep original caption but update credit
                img["credit"] = "Placeholder Image"
                img["license"] = "CC0"
    
    # Save updated manifest
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print("Updated all images to use placeholders")
    
    # Re-apply images to HTML files
    import os
    os.system("python scripts/add_encyclopedia_images.py")

if __name__ == "__main__":
    main()
