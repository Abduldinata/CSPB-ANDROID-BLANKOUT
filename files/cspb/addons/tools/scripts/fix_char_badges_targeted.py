import os

# Updated coordinates for character slots (based on page1.cfg audit)
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

char_persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\character'

# Fix use1.cfg through use9.cfg (and _p2 versions)
for i in range(1, 10):
    for suffix in ['', '_p2']:
        filename = f'use{i}{suffix}.cfg'
        filepath = os.path.join(char_persist_dir, filename)
        
        if os.path.exists(filepath):
            badge_id = "_persist_char_badge1" if suffix == '' else "_persist_char_badge2"
            # We'll use a specific indicator image for the checkmark if we want to be consistent with weapons
            # But the user might want the special char equip images which are numbered 1-9.
            # "addons/neda/image/select_char/equip/1.tga"
            
            coord = slot_coords[i]
            # We use Layer 5 to ensure it's on top of the card (Layer 4)
            content = f'touch_addbutton "{badge_id}" "addons/neda/image/select_char/equip/{i}.tga" "c" {coord} 255 255 255 255 5\n'
            
            with open(filepath, 'w') as f:
                f.write(content)
            print(f"Fixed {filename}")

# Also fix the selection detail images in page1/ and page2/ to use Layer 5
# and the Change button
print("Character persistence badges fixed to targeted coordinates.")
