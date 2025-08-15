#!/usr/bin/env python3
"""Use real CC-licensed images from reliable sources"""
import json
import re
from pathlib import Path

# Real CC-licensed images from stable sources
# These are direct links to actual images, not the upload.wikimedia.org URLs that get transformed
CC_IMAGES = {
    # NASA images (Public Domain) - extremely stable
    "cosmos_cmb": "https://map.gsfc.nasa.gov/media/121238/ilc_9yr_moll4096.png",
    "cosmos_hubble": "https://hubblesite.org/files/live/sites/hubble/files/home/hubble-30th-anniversary/images/_images/hubble_30th_images/hubble-30th-lagoon-nebula.jpg",
    "cosmos_galaxy": "https://www.nasa.gov/sites/default/files/thumbnails/image/hubble_friday_12102021.jpg",
    
    # Wikimedia Commons - using the actual media files, not the commons pages
    "physics_atom": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Hydrogen_Density_Plots.png/800px-Hydrogen_Density_Plots.png",
    "physics_wave": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Standing_wave_2.gif/800px-Standing_wave_2.gif",
    "physics_field": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Solenoid-1.png/800px-Solenoid-1.png",
    
    # More stable Wikimedia images
    "quantum_orbital": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/D_orbital_xz.png/800px-D_orbital_xz.png",
    "quantum_interference": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Single_slit_and_double_slit2.jpg/800px-Single_slit_and_double_slit2.jpg",
    "quantum_entanglement": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/SPDC_figure.png/800px-SPDC_figure.png",
    
    # Mathematics visualizations
    "math_golden": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Golden_ratio_line.png/800px-Golden_ratio_line.png",
    "math_fractal": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Mandel_zoom_00_mandelbrot_set.jpg/800px-Mandel_zoom_00_mandelbrot_set.jpg",
    "math_topology": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Torus_cycles.svg/800px-Torus_cycles.svg.png",
    
    # Spacetime and relativity
    "spacetime_curvature": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/GPB_circling_earth.jpg/800px-GPB_circling_earth.jpg",
    "spacetime_diagram": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/World_line.svg/800px-World_line.svg.png",
    "spacetime_gravity": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Gravitational_lens-full.jpg/800px-Gravitational_lens-full.jpg"
}

# Attribution data for the images
CC_ATTRIBUTIONS = {
    "cosmos_cmb": {"credit": "NASA / WMAP Science Team", "license": "Public Domain"},
    "cosmos_hubble": {"credit": "NASA, ESA, STScI", "license": "Public Domain"},
    "cosmos_galaxy": {"credit": "NASA", "license": "Public Domain"},
    "physics_atom": {"credit": "Wikimedia Commons", "license": "CC BY-SA 3.0"},
    "physics_wave": {"credit": "Wikimedia Commons", "license": "CC BY-SA 3.0"},
    "physics_field": {"credit": "Wikimedia Commons", "license": "CC BY-SA 4.0"},
    "quantum_orbital": {"credit": "Wikimedia Commons", "license": "CC BY-SA 3.0"},
    "quantum_interference": {"credit": "Wikimedia Commons", "license": "CC BY-SA 4.0"},
    "quantum_entanglement": {"credit": "Wikimedia Commons", "license": "CC BY-SA 3.0"},
    "math_golden": {"credit": "Wikimedia Commons", "license": "Public Domain"},
    "math_fractal": {"credit": "Wolfgang Beyer", "license": "CC BY-SA 3.0"},
    "math_topology": {"credit": "Wikimedia Commons", "license": "CC BY-SA 3.0"},
    "spacetime_curvature": {"credit": "NASA", "license": "Public Domain"},
    "spacetime_diagram": {"credit": "Wikimedia Commons", "license": "CC BY-SA 3.0"},
    "spacetime_gravity": {"credit": "NASA/ESA", "license": "Public Domain"}
}

def get_images_for_topic(title, category):
    """Select appropriate CC images based on topic"""
    title_lower = title.lower()
    category_lower = category.lower() if category else ""
    
    # Match images to topics
    if any(term in title_lower for term in ["big bang", "cosmic", "universe", "hubble"]):
        return ["cosmos_cmb", "cosmos_hubble", "cosmos_galaxy"]
    elif any(term in title_lower for term in ["quantum", "particle", "electron", "photon"]):
        return ["quantum_orbital", "quantum_interference", "quantum_entanglement"]
    elif any(term in title_lower for term in ["spacetime", "gravity", "relativity", "curvature"]):
        return ["spacetime_curvature", "spacetime_diagram", "spacetime_gravity"]
    elif any(term in title_lower for term in ["golden", "ratio", "fractal", "topology"]):
        return ["math_golden", "math_fractal", "math_topology"]
    elif "cosmology" in category_lower:
        return ["cosmos_galaxy", "cosmos_cmb", "cosmos_hubble"]
    elif "quantum" in category_lower:
        return ["quantum_orbital", "quantum_interference", "physics_atom"]
    else:
        # Default physics images
        return ["physics_atom", "physics_wave", "physics_field"]

def update_html_with_cc_images(html_file):
    """Update a single HTML file with real CC images"""
    content = html_file.read_text(encoding="utf-8", errors="ignore")
    
    # Extract title from the HTML
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else html_file.stem
    
    # Extract category
    category_match = re.search(r'<span class="category-badge">(.*?)</span>', content)
    category = category_match.group(1) if category_match else ""
    
    # Get appropriate images
    image_keys = get_images_for_topic(title, category)
    
    # Find all figure elements with images
    figure_pattern = r'<figure[^>]*>.*?<img[^>]*src="([^"]*)"[^>]*>.*?<figcaption>(.*?)</figcaption>.*?</figure>'
    figures = list(re.finditer(figure_pattern, content, re.DOTALL))
    
    new_content = content
    for i, match in enumerate(figures):
        if i < len(image_keys):
            old_figure = match.group(0)
            old_src = match.group(1)
            old_caption = match.group(2)
            
            # Get new image and attribution
            image_key = image_keys[i]
            new_src = CC_IMAGES[image_key]
            attribution = CC_ATTRIBUTIONS[image_key]
            
            # Extract just the caption text (before the bullet)
            caption_parts = old_caption.split('•')
            caption_text = caption_parts[0].strip() if caption_parts else old_caption
            
            # Create new figure with proper attribution
            new_figure = old_figure.replace(old_src, new_src)
            new_caption = f'{caption_text} • <span class="figure-credit">{attribution["credit"]}</span> • <span class="figure-license">{attribution["license"]}</span>'
            new_figure = re.sub(r'<figcaption>.*?</figcaption>', f'<figcaption>{new_caption}</figcaption>', new_figure, flags=re.DOTALL)
            
            new_content = new_content.replace(old_figure, new_figure)
    
    return new_content

def main():
    # Update all encyclopedia HTML files
    enc_dir = Path("encyclopedia")
    updated_count = 0
    
    for html_file in enc_dir.glob("*.html"):
        if html_file.name == "index.html":
            continue
        
        try:
            new_content = update_html_with_cc_images(html_file)
            html_file.write_text(new_content, encoding="utf-8")
            updated_count += 1
            print(f"Updated: {html_file.name}")
        except Exception as e:
            print(f"Error processing {html_file.name}: {e}")
    
    print(f"\nUpdated {updated_count} files with real CC-licensed images")
    
    # Also update the manifest for future generations
    manifest_file = Path("assets/data/encyclopedia-images.json")
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Update manifest with a selection of CC images
    default_images = [
        {"src": CC_IMAGES["physics_atom"], "credit": CC_ATTRIBUTIONS["physics_atom"]["credit"], 
         "license": CC_ATTRIBUTIONS["physics_atom"]["license"]},
        {"src": CC_IMAGES["math_golden"], "credit": CC_ATTRIBUTIONS["math_golden"]["credit"], 
         "license": CC_ATTRIBUTIONS["math_golden"]["license"]},
        {"src": CC_IMAGES["quantum_orbital"], "credit": CC_ATTRIBUTIONS["quantum_orbital"]["credit"], 
         "license": CC_ATTRIBUTIONS["quantum_orbital"]["license"]}
    ]
    
    for page_id, page_data in manifest.items():
        if "images" in page_data:
            for i, img in enumerate(page_data["images"]):
                if i < len(default_images):
                    img.update(default_images[i])
    
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print("Updated manifest with real CC images")

if __name__ == "__main__":
    main()
