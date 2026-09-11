#!/usr/bin/env python3
import os
import math
from PIL import Image, ImageDraw, ImageFont

ICONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icons")
os.makedirs(ICONS_DIR, exist_ok=True)

SIZE = 128
BORDER_COLOR = "#0e0e0d"
BORDER_WIDTH = 4
RADIUS = 28

def create_base_icon(bg_color):
    """Creates a transparent 128x128 image with a brutalist rounded squircle."""
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        [4, 4, SIZE - 5, SIZE - 5],
        radius=RADIUS,
        fill=bg_color,
        outline=BORDER_COLOR,
        width=BORDER_WIDTH
    )
    return img, draw

# 1. Excuses: Certified document with red seal & clock
def gen_excuses():
    img, draw = create_base_icon("#ea34df")
    # Document paper
    draw.rounded_rectangle([32, 24, 96, 104], radius=6, fill="#ffffff", outline=BORDER_COLOR, width=3)
    # Text lines
    draw.line([42, 38, 76, 38], fill=BORDER_COLOR, width=3)
    draw.line([42, 50, 86, 50], fill=BORDER_COLOR, width=3)
    draw.line([42, 62, 70, 62], fill=BORDER_COLOR, width=3)
    draw.line([42, 74, 82, 74], fill=BORDER_COLOR, width=3)
    # Red wax stamp / seal
    draw.ellipse([64, 76, 92, 104], fill="#e82803", outline=BORDER_COLOR, width=2)
    draw.ellipse([70, 82, 86, 98], fill="#ffb800", outline=BORDER_COLOR, width=1)
    img.save(os.path.join(ICONS_DIR, "excuses.png"))

# 2. Overthinking: Swirling chaotic brain / thought vortex
def gen_overthinking():
    img, draw = create_base_icon("#e82803")
    # Central white skull/brain silhouette
    draw.rounded_rectangle([34, 38, 94, 96], radius=16, fill="#ffffff", outline=BORDER_COLOR, width=3)
    # Brain folds / spiral labyrinth
    draw.arc([42, 44, 86, 88], 0, 270, fill="#e82803", width=4)
    draw.arc([48, 50, 80, 82], 90, 360, fill="#ea34df", width=4)
    draw.ellipse([60, 62, 68, 70], fill=BORDER_COLOR)
    # Lightning spark
    draw.polygon([(78, 22), (68, 36), (76, 36), (64, 52), (84, 34), (76, 34)], fill="#ffb800", outline=BORDER_COLOR)
    img.save(os.path.join(ICONS_DIR, "overthinking.png"))

# 3. Hmm AI: Retro pixel robot with question marks
def gen_hmm_ai():
    img, draw = create_base_icon("#244638")
    # Antenna
    draw.line([64, 18, 64, 32], fill="#ffffff", width=3)
    draw.ellipse([60, 14, 68, 22], fill="#00c2cb", outline=BORDER_COLOR, width=2)
    # Robot Head
    draw.rounded_rectangle([28, 32, 100, 96], radius=12, fill="#ffffff", outline=BORDER_COLOR, width=3)
    # Cyan Visor / Eyes
    draw.rounded_rectangle([38, 44, 90, 66], radius=6, fill="#0e0e0d", outline=BORDER_COLOR, width=2)
    draw.ellipse([46, 50, 56, 60], fill="#00c2cb")
    draw.ellipse([72, 50, 82, 60], fill="#00c2cb")
    # Non-committal mouth "---"
    draw.line([48, 80, 80, 80], fill="#e82803", width=4)
    # Ears
    draw.rounded_rectangle([20, 52, 28, 76], radius=3, fill="#ffb800", outline=BORDER_COLOR, width=2)
    draw.rounded_rectangle([100, 52, 108, 76], radius=3, fill="#ffb800", outline=BORDER_COLOR, width=2)
    img.save(os.path.join(ICONS_DIR, "hmm_ai.png"))

# 4. Analytics: Plunging bar chart into the abyss
def gen_analytics():
    img, draw = create_base_icon("#ea34df")
    # Chart background box
    draw.rounded_rectangle([26, 26, 102, 102], radius=8, fill="#ffffff", outline=BORDER_COLOR, width=3)
    # Bars going strictly downward
    draw.rectangle([34, 46, 48, 92], fill="#244638", outline=BORDER_COLOR, width=2)
    draw.rectangle([54, 62, 68, 92], fill="#ffb800", outline=BORDER_COLOR, width=2)
    draw.rectangle([74, 78, 88, 92], fill="#e82803", outline=BORDER_COLOR, width=2)
    # Plunging arrow
    draw.line([(34, 38), (56, 52), (76, 70), (92, 94)], fill="#e82803", width=4)
    draw.polygon([(92, 94), (80, 92), (90, 82)], fill="#e82803")
    img.save(os.path.join(ICONS_DIR, "analytics.png"))

# 5. ScreenTime: Smartphone glowing hypnotically
def gen_screentime():
    img, draw = create_base_icon("#00c2cb")
    # Phone Body
    draw.rounded_rectangle([38, 18, 90, 110], radius=10, fill="#0e0e0d", outline="#ffffff", width=2)
    # Screen
    draw.rounded_rectangle([44, 26, 84, 96], radius=4, fill="#ffffff", outline=BORDER_COLOR, width=2)
    # Hypnotic spiral / rectangle trap
    draw.rounded_rectangle([50, 34, 78, 88], radius=3, fill="#ea34df")
    draw.rounded_rectangle([56, 42, 72, 80], radius=2, fill="#ffb800")
    draw.rounded_rectangle([60, 48, 68, 74], radius=1, fill="#0e0e0d")
    # Home button / notch
    draw.ellipse([61, 100, 67, 106], fill="#ffffff")
    img.save(os.path.join(ICONS_DIR, "screentime.png"))

# 6. Existential: Black hole / void swirl with '?'
def gen_existential():
    img, draw = create_base_icon("#ffb800")
    # Black hole
    draw.ellipse([26, 26, 102, 102], fill="#0e0e0d", outline="#ffffff", width=3)
    # Orbiting accretion rings
    draw.arc([16, 44, 112, 84], 0, 360, fill="#ea34df", width=4)
    draw.arc([22, 36, 106, 92], 45, 225, fill="#00c2cb", width=3)
    # Giant white question mark in center
    draw.arc([54, 42, 74, 62], 180, 360, fill="#ffffff", width=4)
    draw.line([(74, 52), (64, 66), (64, 74)], fill="#ffffff", width=4)
    draw.ellipse([61, 82, 67, 88], fill="#ffffff")
    img.save(os.path.join(ICONS_DIR, "existential.png"))

# 7. Emotional Bin: Playful trash can with heart
def gen_emotional_bin():
    img, draw = create_base_icon("#ff6b00")
    # Can body
    draw.polygon([(40, 48), (88, 48), (82, 106), (46, 106)], fill="#ffffff", outline=BORDER_COLOR)
    # Lid
    draw.rounded_rectangle([32, 38, 96, 48], radius=3, fill="#ffffff", outline=BORDER_COLOR, width=2)
    draw.rounded_rectangle([56, 32, 72, 38], radius=2, fill="#0e0e0d")
    # Ridges on can
    draw.line([54, 54, 52, 100], fill="#0e0e0d", width=2)
    draw.line([64, 54, 64, 100], fill="#0e0e0d", width=2)
    draw.line([74, 54, 76, 100], fill="#0e0e0d", width=2)
    # Little heart badge in center
    draw.ellipse([58, 66, 70, 78], fill="#ea34df")
    img.save(os.path.join(ICONS_DIR, "emotional_bin.png"))

# 8. Alarm: Ringing alarm clock with Zzz
def gen_alarm():
    img, draw = create_base_icon("#e82803")
    # Bells
    draw.ellipse([26, 26, 48, 48], fill="#ffb800", outline=BORDER_COLOR, width=2)
    draw.ellipse([80, 26, 102, 48], fill="#ffb800", outline=BORDER_COLOR, width=2)
    draw.polygon([(46, 40), (54, 30), (74, 30), (82, 40)], fill=BORDER_COLOR)
    # Feet
    draw.line([40, 96, 30, 108], fill=BORDER_COLOR, width=4)
    draw.line([88, 96, 98, 108], fill=BORDER_COLOR, width=4)
    # Clock Face
    draw.ellipse([30, 32, 98, 100], fill="#ffffff", outline=BORDER_COLOR, width=3)
    # Hands showing wrong time
    draw.line([64, 66, 64, 46], fill="#0e0e0d", width=3)
    draw.line([64, 66, 84, 66], fill="#0e0e0d", width=3)
    draw.ellipse([61, 63, 67, 69], fill="#e82803")
    # Zzz
    draw.line([76, 20, 84, 20], fill="#ffffff", width=2)
    draw.line([84, 20, 76, 28], fill="#ffffff", width=2)
    draw.line([76, 28, 84, 28], fill="#ffffff", width=2)
    img.save(os.path.join(ICONS_DIR, "alarm.png"))

# 9. Settings: Brutalist gears and sliders
def gen_settings():
    img, draw = create_base_icon("#c0326b")
    # Gear outer rim
    draw.ellipse([32, 32, 96, 96], fill="#ffffff", outline=BORDER_COLOR, width=3)
    # Gear teeth
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        tx = 64 + int(36 * math.cos(rad))
        ty = 64 + int(36 * math.sin(rad))
        draw.rectangle([tx - 6, ty - 6, tx + 6, ty + 6], fill="#ffffff", outline=BORDER_COLOR, width=2)
    # Gear center hole
    draw.ellipse([50, 50, 78, 78], fill="#c0326b", outline=BORDER_COLOR, width=3)
    # Slider switch on top
    draw.rounded_rectangle([30, 88, 98, 102], radius=4, fill="#ffb800", outline=BORDER_COLOR, width=2)
    draw.ellipse([70, 84, 86, 106], fill="#ffffff", outline=BORDER_COLOR, width=2)
    img.save(os.path.join(ICONS_DIR, "settings.png"))

# 10. Terminal: Brutalist CLI with prompt >_
def gen_terminal():
    img, draw = create_base_icon("#0e0e0d")
    # Inner monitor screen
    draw.rounded_rectangle([18, 18, 110, 110], radius=8, fill="#1a1a19", outline="#333330", width=2)
    # Window title buttons
    draw.ellipse([26, 26, 32, 32], fill="#e82803")
    draw.ellipse([36, 26, 42, 32], fill="#ffb800")
    draw.ellipse([46, 26, 52, 32], fill="#244638")
    # Terminal Prompt ">_"
    # ">"
    draw.line([(32, 54), (48, 68), (32, 82)], fill="#ea34df", width=4)
    # "_" cursor
    draw.line([(56, 82), (78, 82)], fill="#00c2cb", width=5)
    img.save(os.path.join(ICONS_DIR, "terminal.png"))

def gen_mascot():
    img, draw = create_base_icon("#ea34df")
    # Body
    draw.rounded_rectangle([28, 38, 100, 98], radius=16, fill="#ffffff", outline=BORDER_COLOR, width=3)
    # Ear
    draw.rounded_rectangle([18, 44, 38, 86], radius=10, fill="#ffb800", outline=BORDER_COLOR, width=3)
    # Eye
    draw.rectangle([48, 52, 56, 62], fill=BORDER_COLOR)
    # Trunk
    draw.line([(82, 68), (96, 68), (96, 88), (86, 88)], fill=BORDER_COLOR, width=6)
    # Crown
    draw.polygon([(46, 38), (40, 22), (54, 30), (64, 18), (74, 30), (88, 22), (82, 38)], fill="#e82803", outline=BORDER_COLOR)
    img.save(os.path.join(ICONS_DIR, "mascot.png"))

if __name__ == "__main__":
    gen_excuses()
    gen_overthinking()
    gen_hmm_ai()
    gen_analytics()
    gen_screentime()
    gen_existential()
    gen_emotional_bin()
    gen_alarm()
    gen_settings()
    gen_terminal()
    gen_mascot()
    print(f"Successfully generated all app icons + mascot in {ICONS_DIR}")
