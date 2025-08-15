#!/usr/bin/env python3
"""Fix Wikipedia Commons image URLs to use direct links"""
import json
import re
from pathlib import Path

# Mapping of problematic URLs to working alternatives
URL_FIXES = {
    # SVG files - use PNG versions instead
    "https://upload.wikimedia.org/wikipedia/commons/9/9b/Golden_ratio_line.svg": 
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Golden_ratio_line.svg/1200px-Golden_ratio_line.svg.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/e/e8/Feynman_Diagram_Gluon_Radiation.svg":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Feynman_Diagram_Gluon_Radiation.svg/1200px-Feynman_Diagram_Gluon_Radiation.svg.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/2/2f/Penrose_triangle.svg":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Penrose_triangle.svg/1200px-Penrose_triangle.svg.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/4/4d/Feynman_Diagram_of_Electron-Positron_Annihilation.svg":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Feynman_Diagram_of_Electron-Positron_Annihilation.svg/1200px-Feynman_Diagram_of_Electron-Positron_Annihilation.svg.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/2/21/Quantum_tunnel_effect_and_its_application_to_the_tunnel_diode.svg":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Quantum_tunnel_effect_and_its_application_to_the_tunnel_diode.svg/1200px-Quantum_tunnel_effect_and_its_application_to_the_tunnel_diode.svg.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/3/35/Helium_atom_QM.svg":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Helium_atom_QM.svg/1200px-Helium_atom_QM.svg.png",
    
    # PNG files that should work but might need the direct link
    "https://upload.wikimedia.org/wikipedia/commons/d/d3/Lorenz_attractor_trajectory.png":
        "https://upload.wikimedia.org/wikipedia/commons/d/d3/Lorenz_attractor_trajectory.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/e/e7/Hydrogen_Density_Plots.png":
        "https://upload.wikimedia.org/wikipedia/commons/e/e7/Hydrogen_Density_Plots.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/1/1f/Higgs_Boson_Decay_Channels.png":
        "https://upload.wikimedia.org/wikipedia/commons/1/1f/Higgs_Boson_Decay_Channels.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/2/2a/Spacetime_curvature.png":
        "https://upload.wikimedia.org/wikipedia/commons/2/2a/Spacetime_curvature.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/a/a2/Atomic_orbital_clouds_n%3D6_l%3D0-5.png":
        "https://upload.wikimedia.org/wikipedia/commons/a/a2/Atomic_orbital_clouds_n%3D6_l%3D0-5.png",
    
    "https://upload.wikimedia.org/wikipedia/commons/d/d7/Mandelbrot_set_-_Periodicites.png":
        "https://upload.wikimedia.org/wikipedia/commons/d/d7/Mandelbrot_set_-_Periodicites.png",
    
    # JPG files
    "https://upload.wikimedia.org/wikipedia/commons/2/22/Black_hole_-_Messier_87_crop_max_res.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/2/22/Black_hole_-_Messier_87_crop_max_res.jpg",
    
    "https://upload.wikimedia.org/wikipedia/commons/d/d1/GPB_circling_earth.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/d/d1/GPB_circling_earth.jpg",
    
    "https://upload.wikimedia.org/wikipedia/commons/2/2f/Hubble_ultra_deep_field.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/2/2f/Hubble_ultra_deep_field.jpg",
    
    "https://upload.wikimedia.org/wikipedia/commons/3/32/Andromeda_Galaxy_%28with_h-alpha%29.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/3/32/Andromeda_Galaxy_%28with_h-alpha%29.jpg",
    
    "https://upload.wikimedia.org/wikipedia/commons/c/c3/NGC_4414_%28NASA-med%29.jpg":
        "https://upload.wikimedia.org/wikipedia/commons/c/c3/NGC_4414_%28NASA-med%29.jpg",
    
    # WMAP/NASA images
    "https://upload.wikimedia.org/wikipedia/commons/b/b5/WMAP_2008.png":
        "https://map.gsfc.nasa.gov/media/080997/080997_PowerSpectrum_WMAP_PRL102_041301_2009.png"
}

def fix_url(url):
    """Fix a URL if it's in our mapping, otherwise return as-is"""
    return URL_FIXES.get(url, url)

def main():
    # Fix the manifest
    manifest_file = Path("assets/data/encyclopedia-images.json")
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    updated_manifest = False
    for page_id, page_data in manifest.items():
        if "images" in page_data:
            for img in page_data["images"]:
                old_src = img.get("src", "")
                new_src = fix_url(old_src)
                if new_src != old_src:
                    img["src"] = new_src
                    updated_manifest = True
                    print(f"Updated {page_id}: {old_src} -> {new_src}")
    
    if updated_manifest:
        with open(manifest_file, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        print(f"\nUpdated manifest file")
    
    # Fix already-generated HTML files
    enc_dir = Path("encyclopedia")
    updated_files = 0
    
    for html_file in enc_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue
            
        content = html_file.read_text(encoding="utf-8")
        original_content = content
        
        # Replace URLs in the content
        for old_url, new_url in URL_FIXES.items():
            content = content.replace(old_url, new_url)
        
        if content != original_content:
            html_file.write_text(content, encoding="utf-8")
            updated_files += 1
            print(f"Updated HTML: {html_file.name}")
    
    print(f"\nUpdated {updated_files} HTML files")
    
    # Add fallback images to the manifest for resilience
    print("\nAdding fallback URLs...")
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Add a generic fallback for all images
    fallback_url = "https://via.placeholder.com/800x400/f0f0f0/666666?text=Image+Loading..."
    
    for page_id, page_data in manifest.items():
        if "images" in page_data:
            for img in page_data["images"]:
                if "fallback_src" not in img:
                    img["fallback_src"] = fallback_url
    
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print("Added fallback URLs to all images")

if __name__ == "__main__":
    main()
