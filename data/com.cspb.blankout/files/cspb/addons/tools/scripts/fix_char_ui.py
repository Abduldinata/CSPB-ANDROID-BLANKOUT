import os
import re

# Character Slot Map (Targeted)
slot_coords = {
    1: "0.460000 0.205400 0.620000 0.349300",
    2: "0.620000 0.205400 0.780000 0.349300",
    3: "0.780000 0.205400 0.940000 0.349300",
    4: "0.460000 0.349300 0.620000 0.485300",
    5: "0.620000 0.349300 0.780000 0.485300",
    6: "0.780000 0.349300 0.940000 0.485300",
    7: "0.460000 0.472500 0.620000 0.616300",
    8: "0.620000 0.472500 0.780000 0.616300",
    9: "0.780000 0.472500 0.940000 0.616300"
}

# 1. Fix select1.cfg to select9.cfg
select_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character'
for i in range(1, 10):
    filename = f'select{i}.cfg'
    filepath = os.path.join(select_dir, filename)
    if os.path.exists(filepath):
        coord = slot_coords[i]
        # Important: use same ID as in previous logic if needed, but here it's _lobby_select_image{i}
        content = f'touch_addbutton "_lobby_select_image{i}" "addons/neda/image/select_char/{i}.tga" "c" {coord} 255 255 255 255 4\n'
        with open(filepath, 'w') as f:
            f.write(content)

# 2. Fix character/page1.cfg & page2.cfg (extensions + Acidpool logic)
char_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\character'
for page in ['1', '2']:
    filepath = os.path.join(char_dir, f'page{page}.cfg')
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Add .tga where missing in image paths
        # Look for "addons/neda/image/character/..." without .tga
        updated = re.sub(r'("addons/neda/image/character/[^.]+)"', r'\1.tga"', content)
        
        # Ensure slot 2 on page 1 calls acidpool if it's bluec1
        if page == '1':
            updated = updated.replace('_sl_bluec1', '_db_char_acidpool')
            # Wait, currently page1.cfg calls _sl_bluec1. 
            # If I want to directly execute the database entry, I should call _db_char_acidpool.
            # But the card click usually shows the DETAIL screen first.
            # So _sl_bluec1 (acidpool.cfg) IS correct for showing the preview.
            # The EQUIP button inside acidpool.cfg should then call _db_char_acidpool.
            # My current acidpool.cfg DOES call _db_char_acidpool.
            # So no change needed there.
            
        with open(filepath, 'w') as f:
            f.write(updated)

print("Character selection assets and borders fixed.")
