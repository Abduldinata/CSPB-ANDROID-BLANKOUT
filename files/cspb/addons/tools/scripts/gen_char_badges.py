import os

# Directory for character persistence badges
out_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\character"
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Slots based on UI coordinates provided in page1.cfg
# Format: SLOT_ID -> IMAGE_ID (matches slot position)
slots = range(1, 10)

def generate_badges():
    for s in slots:
        path = os.path.join(out_dir, f"use{s}.cfg")
        # Image 1.tga corresponds to Slot 1, 2.tga to Slot 2, etc.
        content = f'touch_addbutton "_persist_char_badge" "addons/neda/image/select_char/equip/{s}.tga" "" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4\n'
        with open(path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {path}")

generate_badges()
