import os
import math
from PIL import Image, ImageDraw

os.makedirs('SPRITES/PLATAFORMA/3 Objects/Hazards', exist_ok=True)
os.makedirs('SPRITES/PLATAFORMA/4 Animated objects', exist_ok=True)

# 1. SPIKES (32x32)
def create_spikes():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Base beam
    base_color = (61, 37, 59, 255)
    base_dark = (37, 19, 26, 255)
    draw.rectangle([0, 28, 31, 31], fill=base_dark)
    draw.rectangle([0, 26, 31, 28], fill=base_color)
    draw.line([0, 26, 31, 26], fill=(92, 107, 83, 255)) # Moss trim
    
    # 3 Sharp Steel Spikes
    spike_xs = [5, 16, 26]
    for sx in spike_xs:
        # Shadow / dark side
        draw.polygon([(sx, 6), (sx - 4, 26), (sx, 26)], fill=(70, 75, 90, 255))
        # Light side
        draw.polygon([(sx, 6), (sx, 26), (sx + 4, 26)], fill=(155, 170, 190, 255))
        # Highlight edge
        draw.line([(sx, 6), (sx, 26)], fill=(225, 235, 245, 255))
        # Tip glint
        img.putpixel((sx, 6), (255, 255, 255, 255))
        img.putpixel((sx, 7), (240, 250, 255, 255))
        # Base shadow
        draw.rectangle([sx - 4, 25, sx + 4, 26], fill=(30, 20, 30, 200))
    
    img.save('SPRITES/PLATAFORMA/3 Objects/Hazards/spikes.png')
    print("Created spikes.png")

# 2. ROTATING SAW BLADE (4 frames of 32x32 -> 128x32)
def create_saw_blade():
    w, h = 32, 32
    frames = 4
    sheet = Image.new('RGBA', (w * frames, h), (0, 0, 0, 0))
    for f in range(frames):
        angle_offset = (f / frames) * (math.pi / 4)
        frame_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        cx, cy = 16, 16
        r_outer = 13
        r_inner = 9
        teeth = 8
        
        poly = []
        for i in range(teeth):
            a1 = angle_offset + (i / teeth) * 2 * math.pi
            a2 = a1 + (1 / (teeth * 2)) * 2 * math.pi
            # Tip of tooth
            x1 = cx + r_outer * math.cos(a1)
            y1 = cy + r_outer * math.sin(a1)
            # Valley between teeth
            x2 = cx + r_inner * math.cos(a2)
            y2 = cy + r_inner * math.sin(a2)
            poly.append((x1, y1))
            poly.append((x2, y2))
            
        draw.polygon(poly, fill=(130, 140, 155, 255))
        
        # Inner hub disc
        draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(85, 95, 110, 255), outline=(190, 205, 220, 255))
        # Center bolt
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(210, 160, 40, 255), outline=(50, 40, 30, 255))
        # Glint
        draw.point((cx - 1, cy - 1), fill=(255, 255, 255, 255))
        
        sheet.paste(frame_img, (f * w, 0))
        
    sheet.save('SPRITES/PLATAFORMA/4 Animated objects/saw_blade.png')
    print("Created saw_blade.png")

# 3. MOVING PLATFORM (64x16)
def create_moving_platform():
    w, h = 64, 16
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Wood body
    draw.rectangle([0, 2, w - 1, h - 1], fill=(82, 59, 64, 255), outline=(37, 19, 26, 255))
    draw.rectangle([1, 3, w - 2, 7], fill=(115, 85, 90, 255))
    # Mossy grass top
    draw.rectangle([0, 0, w - 1, 2], fill=(138, 150, 31, 255))
    draw.rectangle([0, 2, w - 1, 3], fill=(92, 107, 83, 255))
    # Corner iron brackets and rivets
    for bx in [2, w - 8]:
        draw.rectangle([bx, 2, bx + 6, h - 2], fill=(60, 70, 85, 255), outline=(30, 35, 45, 255))
        draw.point((bx + 2, 4), fill=(180, 195, 210, 255))
        draw.point((bx + 4, 4), fill=(180, 195, 210, 255))
        draw.point((bx + 2, h - 5), fill=(180, 195, 210, 255))
        draw.point((bx + 4, h - 5), fill=(180, 195, 210, 255))
    # Wood plank vertical seams
    for px in [18, 32, 46]:
        draw.line([px, 3, px, h - 2], fill=(45, 30, 35, 255))
        
    img.save('SPRITES/PLATAFORMA/3 Objects/Hazards/moving_plat.png')
    print("Created moving_plat.png")

# 4. CRACKED SECRET WALL (32x32)
def create_cracked_wall():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Base stone texture matching Tile_12
    draw.rectangle([0, 0, 31, 31], fill=(61, 37, 59, 255), outline=(37, 19, 26, 255))
    draw.rectangle([2, 2, 29, 29], fill=(82, 59, 64, 255))
    # Stone highlights
    draw.line([2, 2, 29, 2], fill=(115, 85, 90, 255))
    draw.line([2, 2, 2, 29], fill=(115, 85, 90, 255))
    
    # Deep prominent cracks
    crack_lines = [
        [(5, 7), (12, 13), (18, 11), (25, 17), (29, 15)],
        [(12, 13), (10, 22), (16, 26), (15, 30)],
        [(18, 11), (22, 24), (28, 27)],
        [(7, 19), (10, 22)]
    ]
    for seg in crack_lines:
        for i in range(len(seg) - 1):
            draw.line([seg[i], seg[i + 1]], fill=(15, 10, 15, 255), width=2)
            # Glowing subtle rune behind crack
            draw.line([seg[i], seg[i + 1]], fill=(255, 180, 50, 120))
            
    img.save('SPRITES/PLATAFORMA/3 Objects/Hazards/cracked_wall.png')
    print("Created cracked_wall.png")

# 5. CHECKPOINT TORCH (32x48, 5 frames -> 160x48)
def create_checkpoint_torch():
    w, h = 32, 48
    frames = 5
    sheet = Image.new('RGBA', (w * frames, h), (0, 0, 0, 0))
    for f in range(frames):
        frame_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        # Stone Pillar Base
        draw.rectangle([10, 26, 21, 47], fill=(61, 37, 59, 255), outline=(37, 19, 26, 255))
        draw.rectangle([7, 42, 24, 47], fill=(37, 19, 26, 255))
        draw.rectangle([8, 23, 23, 26], fill=(82, 59, 64, 255), outline=(37, 19, 26, 255))
        # Iron Brazier Bowl
        draw.polygon([(6, 17), (25, 17), (21, 23), (10, 23)], fill=(50, 55, 65, 255), outline=(25, 30, 40, 255))
        
        if f > 0: # Lit flames!
            # Flame heights flicker per frame
            flame_h = [0, 14, 16, 15, 17][f]
            fx = 16
            fy = 17
            # Outer orange glow
            draw.polygon([(fx, fy - flame_h), (fx - 7, fy), (fx + 7, fy)], fill=(255, 100, 20, 220))
            # Mid gold flame
            draw.polygon([(fx, fy - flame_h + 3), (fx - 4, fy), (fx + 4, fy)], fill=(255, 200, 30, 240))
            # Core bright white/cyan spark
            draw.polygon([(fx, fy - flame_h + 6), (fx - 2, fy), (fx + 2, fy)], fill=(255, 255, 220, 255))
            # Floating fire embers
            draw.point((fx - 3 + (f % 3), fy - flame_h - 2), fill=(255, 220, 50, 255))
            draw.point((fx + 2 - (f % 2), fy - flame_h - 4), fill=(255, 120, 20, 255))
        else:
            # Unlit coal
            draw.ellipse([9, 15, 22, 19], fill=(20, 15, 20, 255))
            
        sheet.paste(frame_img, (f * w, 0))
        
    sheet.save('SPRITES/PLATAFORMA/4 Animated objects/checkpoint_torch.png')
    print("Created checkpoint_torch.png")

# 6. HEALTH POTION ELIXIR (24x24, 4 frames -> 96x24)
def create_potion():
    w, h = 24, 24
    frames = 4
    sheet = Image.new('RGBA', (w * frames, h), (0, 0, 0, 0))
    for f in range(frames):
        frame_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        # Cork
        draw.rectangle([10, 3, 13, 5], fill=(160, 100, 50, 255), outline=(70, 40, 20, 255))
        # Glass neck
        draw.rectangle([9, 6, 14, 9], fill=(200, 230, 255, 140), outline=(100, 150, 200, 200))
        # Flask body (round bulb)
        draw.ellipse([5, 8, 18, 21], fill=(220, 30, 60, 240), outline=(140, 190, 240, 255))
        # Liquid highlight
        draw.ellipse([6, 9, 17, 14], fill=(255, 90, 120, 220))
        # Animated bubble inside
        bx = 8 + (f % 3) * 3
        by = 17 - f * 2
        draw.point((bx, by), fill=(255, 230, 230, 255))
        # Glass reflection shine
        draw.arc([6, 9, 17, 20], start=130, end=210, fill=(255, 255, 255, 255), width=2)
        
        sheet.paste(frame_img, (f * w, 0))
        
    sheet.save('SPRITES/PLATAFORMA/4 Animated objects/potion.png')
    print("Created potion.png")

# 7. RELIC GEMS (24x24, 4 frames -> 96x24)
def create_gem():
    w, h = 24, 24
    frames = 4
    sheet = Image.new('RGBA', (w * frames, h), (0, 0, 0, 0))
    for f in range(frames):
        frame_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        # Gem facets (Octagon / Emerald cut)
        poly_outer = [(8, 4), (15, 4), (20, 9), (20, 15), (15, 20), (8, 20), (3, 15), (3, 9)]
        draw.polygon(poly_outer, fill=(30, 180, 120, 255), outline=(10, 90, 60, 255))
        # Inner facets
        draw.polygon([(9, 7), (14, 7), (17, 10), (17, 14), (14, 17), (9, 17), (6, 14), (6, 10)], fill=(70, 230, 160, 255))
        # Center core
        draw.rectangle([9, 10, 14, 14], fill=(140, 255, 200, 255))
        
        # Rotating glint star
        gx = [7, 14, 15, 8][f]
        gy = [8, 8, 15, 14][f]
        draw.line([(gx - 2, gy), (gx + 2, gy)], fill=(255, 255, 255, 255))
        draw.line([(gx, gy - 2), (gx, gy + 2)], fill=(255, 255, 255, 255))
        draw.point((gx, gy), fill=(255, 255, 255, 255))
        
        sheet.paste(frame_img, (f * w, 0))
        
    sheet.save('SPRITES/PLATAFORMA/4 Animated objects/gem.png')
    print("Created gem.png")

# 8. SLASH VFX (4 frames of 64x64 -> 256x64)
def create_slash_vfx():
    w, h = 64, 64
    frames = 4
    sheet = Image.new('RGBA', (w * frames, h), (0, 0, 0, 0))
    for f in range(frames):
        frame_img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(frame_img)
        # Crescent wave expanding
        arc_r = 16 + f * 9
        cx, cy = 20, 32
        alpha_core = max(50, 255 - f * 55)
        # Outer cyan glow
        draw.arc([cx - arc_r, cy - arc_r, cx + arc_r, cy + arc_r], start=-60 + f * 10, end=60 - f * 5, fill=(60, 220, 255, alpha_core), width=5)
        # Inner white bright edge
        draw.arc([cx - arc_r + 1, cy - arc_r + 1, cx + arc_r - 1, cy + arc_r - 1], start=-55 + f * 10, end=55 - f * 5, fill=(255, 255, 255, alpha_core), width=2)
        
        sheet.paste(frame_img, (f * w, 0))
        
    sheet.save('SPRITES/PLATAFORMA/4 Animated objects/slash_vfx.png')
    print("Created slash_vfx.png")

if __name__ == '__main__':
    create_spikes()
    create_saw_blade()
    create_moving_platform()
    create_cracked_wall()
    create_checkpoint_torch()
    create_potion()
    create_gem()
    create_slash_vfx()
    print("All custom pixel-art sprites generated successfully!")
