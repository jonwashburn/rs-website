import hashlib
import random
import argparse
from PIL import Image, ImageDraw, ImageFilter

# --- Soul Data Generation (mirrors Solidity logic) ---

class Soul:
    def __init__(self, token_id):
        self.token_id = token_id
        
        # Generate a deterministic seed from the token ID
        seed_material = str(token_id).encode('utf-8')
        self.soul_hash = hashlib.sha256(seed_material).digest()
        
        # Use the hash to generate properties
        self.fundamental_rhythm = 8
        self.cost_state_signature = self._get_cost_state()
        self.core_opcode = int.from_bytes(self.soul_hash[:2], 'big') % 16
        self.recognition_seed = int.from_bytes(self.soul_hash[2:6], 'big')

    def _get_cost_state(self):
        signature = []
        for i in range(9):
            # Create a new hash for each state to ensure independence
            state_hash = hashlib.sha256(self.soul_hash + str(i).encode('utf-8')).digest()
            val = int.from_bytes(state_hash[:2], 'big') % 9 - 4
            signature.append(val)
        return signature

# --- Visualization Engine ---

def get_color_from_cost(cost, alpha=200):
    """ Maps a cost state to a color. """
    if cost > 0: # Positive, creative, outward energy
        return (186, 255, 201, alpha)  # Pastel Green
    if cost < 0: # Negative, destructive, inward energy
        return (255, 179, 186, alpha)  # Pastel Red
    return (255, 255, 255, alpha)      # White/Neutral

def generate_soul_image(soul, size=(1200, 1200)):
    """ Creates a high-fidelity image of a soul """
    image = Image.new('RGBA', size, (0, 0, 0, 255))
    draw = ImageDraw.Draw(image)
    
    center_x, center_y = size[0] / 2, size[1] / 2
    max_radius = min(size) / 2.5
    
    # Use the recognition seed for all random operations to ensure determinism
    random.seed(soul.recognition_seed)

    # 1. Background Nebula/Aura
    for _ in range(50):
        # Choose a random point and radius for a blurred circle
        x = center_x + random.uniform(-max_radius, max_radius)
        y = center_y + random.uniform(-max_radius, max_radius)
        r = random.uniform(max_radius / 4, max_radius)
        
        # Color is based on a random cost state from the signature
        color = get_color_from_cost(random.choice(soul.cost_state_signature), alpha=random.randint(5, 15))
        
        # Create a temporary image for the blurred circle
        nebula_layer = Image.new('RGBA', size, (0,0,0,0))
        nebula_draw = ImageDraw.Draw(nebula_layer)
        nebula_draw.ellipse((x-r, y-r, x+r, y+r), fill=color)
        
        # Apply a strong blur
        nebula_layer = nebula_layer.filter(ImageFilter.GaussianBlur(radius=r/2))
        
        # Composite it onto the main image
        image = Image.alpha_composite(image, nebula_layer)

    # 2. Core Opcode Representation (The Central Star)
    core_radius = max_radius / 4 + (soul.core_opcode * 5)
    core_color = get_color_from_cost(sum(soul.cost_state_signature) % 9 - 4, alpha=255)
    
    # Draw the core as a series of glowing, layered circles
    for i in range(10, 0, -1):
        radius = core_radius * (i / 10.0)
        alpha = 50 - (i * 4)
        draw.ellipse(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            fill=(core_color[0], core_color[1], core_color[2], alpha)
        )

    # 3. Cost State Signature (Orbital Paths/Glyphs)
    for i, cost in enumerate(soul.cost_state_signature):
        angle = (360 / 9) * i
        distance = max_radius * 0.7 + (cost * 15)
        
        # Calculate position on the circle
        rad_angle = (angle * 3.14159) / 180
        x = center_x + distance * random.uniform(0.95, 1.05) * (1 if i % 2 == 0 else -1)
        y = center_y + distance * random.uniform(0.95, 1.05) * (1 if i % 2 != 0 else -1)

        # Draw a small glyph representing the cost
        glyph_radius = 10 + abs(cost) * 2
        glyph_color = get_color_from_cost(cost, alpha=220)
        draw.ellipse(
            (x - glyph_radius, y - glyph_radius, x + glyph_radius, y + glyph_radius),
            fill=glyph_color,
            outline=(255,255,255,100),
            width=2
        )
        
        # Draw a faint connecting line to the core
        draw.line([(center_x, center_y), (x, y)], fill=(glyph_color[0], glyph_color[1], glyph_color[2], 30), width=2)
        
    # Final touches - add a subtle bloom/glow effect
    image = image.filter(ImageFilter.BoxBlur(1))
    
    return image


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate an image of a Ledger Soul.')
    parser.add_argument('token_id', type=int, help='The token ID of the soul to generate.')
    parser.add_argument('output_path', type=str, help='The path to save the generated image.')
    args = parser.parse_args()

    soul_to_generate = Soul(args.token_id)
    
    print(f"--- Generating Soul #{args.token_id} ---")
    print(f"  - Hash (first 8 bytes): {soul_to_generate.soul_hash[:8].hex()}")
    print(f"  - Cost State Signature: {soul_to_generate.cost_state_signature}")
    print(f"  - Core Opcode: {soul_to_generate.core_opcode}")
    
    soul_image = generate_soul_image(soul_to_generate)
    
    soul_image.save(args.output_path, "PNG")
    
    print(f"\n✓ Successfully generated soul image.")
    print(f"✓ Saved to: {args.output_path}")
