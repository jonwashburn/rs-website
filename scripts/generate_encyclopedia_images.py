#!/usr/bin/env python3
"""Generate image manifest entries for all encyclopedia pages with CC/Public Domain images"""
import json
import os
from pathlib import Path

# Image sources by category - all CC or Public Domain
IMAGE_SOURCES = {
    "Recognition Physics Fundamentals": [
        {
            "placement": "hero",
            "src": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Lorenz_attractor_trajectory.png",
            "alt": "Lorenz attractor showing complex dynamics",
            "caption": "Complex patterns emerge from simple recognition rules",
            "credit": "Wikimedia Commons",
            "license": "Public Domain"
        },
        {
            "placement": "after_heading",
            "heading": "How It Works",
            "src": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Feynman_Diagram_Gluon_Radiation.svg",
            "alt": "Feynman diagram showing particle interactions",
            "caption": "Recognition events create observable particle interactions",
            "credit": "JabberWok",
            "license": "CC BY-SA 3.0"
        },
        {
            "placement": "after_heading",
            "heading": "Mathematical Framework",
            "src": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Penrose_triangle.svg",
            "alt": "Penrose triangle impossible object",
            "caption": "Self-referential structures reveal fundamental constraints",
            "credit": "Tobias R.",
            "license": "Public Domain"
        }
    ],
    "Fundamental Constants": [
        {
            "placement": "hero",
            "src": "https://upload.wikimedia.org/wikipedia/commons/9/9b/Golden_ratio_line.svg",
            "alt": "Golden ratio geometric construction",
            "caption": "The golden ratio φ emerges from self-similar cost minimization",
            "credit": "Dicklyon",
            "license": "Public Domain"
        },
        {
            "placement": "after_heading",
            "heading": "Physical Meaning",
            "src": "https://upload.wikimedia.org/wikipedia/commons/4/4d/Feynman_Diagram_of_Electron-Positron_Annihilation.svg",
            "alt": "Feynman diagram of electron-positron annihilation",
            "caption": "Fundamental constants govern all particle interactions",
            "credit": "JabberWok",
            "license": "CC BY-SA 3.0"
        },
        {
            "placement": "after_heading",
            "heading": "Experimental Verification",
            "src": "https://upload.wikimedia.org/wikipedia/commons/c/c3/NGC_4414_%28NASA-med%29.jpg",
            "alt": "Spiral galaxy NGC 4414",
            "caption": "Cosmic structures reveal universal constants at work",
            "credit": "NASA/ESA",
            "license": "Public Domain"
        }
    ],
    "Quantum & Particle Physics": [
        {
            "placement": "hero",
            "src": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Hydrogen_Density_Plots.png",
            "alt": "Hydrogen orbital probability densities",
            "caption": "Quantum states emerge from recognition path interference",
            "credit": "PoorLeno",
            "license": "Public Domain"
        },
        {
            "placement": "after_heading",
            "heading": "Quantum Behavior",
            "src": "https://upload.wikimedia.org/wikipedia/commons/2/21/Quantum_tunnel_effect_and_its_application_to_the_tunnel_diode.svg",
            "alt": "Quantum tunneling diagram",
            "caption": "Tunneling arises from recognition path summation",
            "credit": "Max Schmid",
            "license": "CC BY-SA 4.0"
        },
        {
            "placement": "after_heading",
            "heading": "Particle Interactions",
            "src": "https://upload.wikimedia.org/wikipedia/commons/1/1f/Higgs_Boson_Decay_Channels.png",
            "alt": "Higgs boson decay channels",
            "caption": "Particle masses emerge from coherence energy cascades",
            "credit": "CERN",
            "license": "CC BY-SA 4.0"
        }
    ],
    "Spacetime & Gravity": [
        {
            "placement": "hero",
            "src": "https://upload.wikimedia.org/wikipedia/commons/2/22/Black_hole_-_Messier_87_crop_max_res.jpg",
            "alt": "First image of a black hole in M87",
            "caption": "Extreme spacetime curvature from dense recognition events",
            "credit": "Event Horizon Telescope",
            "license": "CC BY 4.0"
        },
        {
            "placement": "after_heading",
            "heading": "Gravitational Effects",
            "src": "https://upload.wikimedia.org/wikipedia/commons/d/d1/GPB_circling_earth.jpg",
            "alt": "Gravity Probe B orbiting Earth",
            "caption": "Frame-dragging confirms spacetime as dynamic ledger geometry",
            "credit": "NASA",
            "license": "Public Domain"
        },
        {
            "placement": "after_heading",
            "heading": "Spacetime Structure",
            "src": "https://upload.wikimedia.org/wikipedia/commons/2/2a/Spacetime_curvature.png",
            "alt": "Spacetime curvature visualization",
            "caption": "Mass-energy curves the recognition ledger manifold",
            "credit": "Johnstone",
            "license": "CC BY-SA 3.0"
        }
    ],
    "Cosmology & Astrophysics": [
        {
            "placement": "hero",
            "src": "https://upload.wikimedia.org/wikipedia/commons/2/2f/Hubble_ultra_deep_field.jpg",
            "alt": "Hubble Ultra Deep Field",
            "caption": "Deep field reveals cosmic evolution through 13 billion years",
            "credit": "NASA/ESA",
            "license": "Public Domain"
        },
        {
            "placement": "after_heading",
            "heading": "Cosmic Evolution",
            "src": "https://upload.wikimedia.org/wikipedia/commons/b/b5/WMAP_2008.png",
            "alt": "WMAP cosmic microwave background",
            "caption": "CMB anisotropies encode primordial recognition patterns",
            "credit": "NASA/WMAP Science Team",
            "license": "Public Domain"
        },
        {
            "placement": "after_heading",
            "heading": "Observable Universe",
            "src": "https://upload.wikimedia.org/wikipedia/commons/3/32/Andromeda_Galaxy_%28with_h-alpha%29.jpg",
            "alt": "Andromeda Galaxy",
            "caption": "Galaxy structures trace dark matter recognition interference",
            "credit": "Adam Evans",
            "license": "CC BY 2.0"
        }
    ]
}

# Default images for categories without specific ones
DEFAULT_IMAGES = [
    {
        "placement": "hero",
        "src": "https://upload.wikimedia.org/wikipedia/commons/a/a2/Atomic_orbital_clouds_n%3D6_l%3D0-5.png",
        "alt": "Atomic orbital visualization",
        "caption": "Complex patterns from simple quantum rules",
        "credit": "Geek3",
        "license": "CC BY-SA 3.0"
    },
    {
        "placement": "after_heading",
        "heading": "Mathematical Structure",
        "src": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Mandelbrot_set_-_Periodicites.png",
        "alt": "Mandelbrot set showing self-similarity",
        "caption": "Self-similar patterns reflect Recognition's fractal nature",
        "credit": "Prokofiev",
        "license": "CC BY-SA 3.0"
    },
    {
        "placement": "after_heading",
        "heading": "Physical Implications",
        "src": "https://upload.wikimedia.org/wikipedia/commons/3/35/Helium_atom_QM.svg",
        "alt": "Helium atom quantum mechanical model",
        "caption": "Quantum mechanics emerges from recognition statistics",
        "credit": "Yzmo",
        "license": "CC BY-SA 3.0"
    }
]

def get_images_for_category(category):
    """Get appropriate images for a category"""
    # Check if we have specific images for this category
    for cat_key in IMAGE_SOURCES:
        if cat_key in category:
            return IMAGE_SOURCES[cat_key]
    
    # Otherwise use defaults
    return DEFAULT_IMAGES

def main():
    # Get list of existing encyclopedia pages
    encyclopedia_dir = Path("encyclopedia")
    existing_pages = []
    
    for html_file in encyclopedia_dir.glob("*.html"):
        if html_file.name != "index.html":
            existing_pages.append(html_file.stem)
    
    print(f"Found {len(existing_pages)} encyclopedia pages")
    
    # Load task data to get categories
    tasks_file = Path("agents/encyclopedia/tasks.complete-2000.json")
    with open(tasks_file, "r", encoding="utf-8") as f:
        all_tasks = json.load(f)
    
    # Create task lookup by slug
    task_by_slug = {}
    for task in all_tasks:
        slug = task["title"].lower().replace(" ", "-").replace("(", "").replace(")", "").replace(",", "")
        slug = "-".join(slug.split())
        task_by_slug[slug] = task
    
    # Load existing manifest
    manifest_file = Path("assets/data/encyclopedia-images.json")
    if manifest_file.exists():
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    else:
        manifest = {}
    
    # Generate entries for all existing pages
    updated = 0
    for page_slug in existing_pages:
        if page_slug not in manifest:
            # Find the task for this page
            task = task_by_slug.get(page_slug)
            if task:
                category = task.get("category", "General")
                images = get_images_for_category(category)
                
                # Customize images with page-specific data
                customized_images = []
                for img in images:
                    custom_img = img.copy()
                    # Update alt text to be more specific
                    if "hero" in img.get("placement", ""):
                        custom_img["alt"] = f"{task['title']} conceptual visualization"
                    customized_images.append(custom_img)
                
                manifest[page_slug] = {"images": customized_images}
                updated += 1
                print(f"Added images for: {page_slug}")
    
    # Write updated manifest
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nUpdated manifest with {updated} new entries")
    print(f"Total pages with images: {len(manifest)}")
    
    # Run the image addition script
    print("\nApplying images to HTML pages...")
    os.system("python scripts/add_encyclopedia_images.py")

if __name__ == "__main__":
    main()
