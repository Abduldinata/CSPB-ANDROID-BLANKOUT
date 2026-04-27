import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
lobby_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. RENAME IMAGE FOLDERS
image_root = os.path.join(base_path, "image")

# Rename image/weapons -> image/main
old_img_weapons = os.path.join(image_root, "weapons")
new_img_main = os.path.join(image_root, "main")
if os.path.exists(old_img_weapons) and not os.path.exists(new_img_main):
    os.rename(old_img_weapons, new_img_main)
    print(f"Renamed image folder {old_img_weapons} -> {new_img_main}")

# Rename image/select_main -> image/select_weapon
old_img_select_main = os.path.join(image_root, "select_main")
new_img_select_weapon = os.path.join(image_root, "select_weapon")
if os.path.exists(old_img_select_main) and not os.path.exists(new_img_select_weapon):
    os.rename(old_img_select_main, new_img_select_weapon)
    print(f"Renamed image folder {old_img_select_main} -> {new_img_select_weapon}")

# 2. FILE TYPE MAPPING FOR INVENTORY LOADERS
category_loaders = {
    "inventory_weapon.cfg": "_load_wp_p1",
    "inventory_weapon2.cfg": "_load_wp_p1",
    "inventory_secondary.cfg": "_scd_prevpage1",
    "inventory_secondary2.cfg": "_scd_prevpage1",
    "inventory_melee.cfg": "_ml_prevpage1",
    "inventory_melee2.cfg": "_ml_prevpage1",
    "inventory_explosive.cfg": "_exp_prevpage1",
    "inventory_explosive2.cfg": "_exp_prevpage1",
    "inventory_special.cfg": "_spc_prevpage1",
    "inventory_special2.cfg": "_spc_prevpage1",
    "inventory_character.cfg": "_chr_prevpage1",
    "inventory_character2.cfg": "_chr_prevpage1",
}

# 3. GLOBAL ROUTE UPDATE & LOADER FIX
def process_cfg(fpath, fname):
    with open(fpath, "r") as f:
        content = f.read()
    
    original_content = content
    
    # Replace routes
    content = content.replace("/image/weapons/", "/image/main/")
    content = content.replace("/image/select_main/", "/image/select_weapon/")
    content = content.replace("/select_main/", "/select_weapon/")
    # Handle weapons/ folder name in root list too
    content = content.replace("/neda/weapons/", "/neda/main/")
    
    # Fix .tga extension in background images if missing
    if "inventory_" in content and "touch_addbutton" in content:
        lines = content.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            if 'touch_addbutton' in line and 'addons/neda/image/' in line:
                if 'inventory_' in line and not '.tga' in line.split('"')[3]:
                    parts = line.split('"')
                    if len(parts) >= 5:
                        parts[3] = parts[3] + ".tga"
                        lines[i] = '"'.join(parts)
        content = '\n'.join(lines)

    # ADD LOADER IF IT'S AN INVENTORY FILE
    if fname in category_loaders:
        loader = category_loaders[fname]
        if loader not in content:
            if not content.endswith('\n'):
                content += '\n'
            content += f"\n{loader}\n"
    
    if content != original_content:
        with open(fpath, "w") as f:
            f.write(content)
        return True
    return False

# Iterate over all .cfg files in addons/
for root, dirs, files in os.walk(lobby_path):
    for name in files:
        if name.endswith(".cfg"):
            fpath = os.path.join(root, name)
            if process_cfg(fpath, name):
                print(f"Processed results in {fpath}")

print("Total fix of Missing TGA and Missing Slots complete.")
