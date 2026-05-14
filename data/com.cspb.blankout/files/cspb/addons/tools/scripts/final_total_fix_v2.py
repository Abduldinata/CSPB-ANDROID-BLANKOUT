import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
lobby_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. CATEGORY MAPPING FOR INVENTORY LOADERS
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

# 2. GLOBAL ROUTE UPDATE & LOADER FIX
def process_cfg_v2(fpath, fname):
    with open(fpath, "r") as f:
        content = f.read()
    
    original_content = content
    
    # Ensure image paths in addons/neda/image/ have .tga extensions if they don't have it
    lines = content.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        if 'touch_addbutton' in line and 'addons/neda/image/' in line:
            parts = line.split('"')
            if len(parts) >= 5:
                img_path = parts[3]
                # If it's a valid path without extension
                if img_path.startswith('addons/neda/image/') and not img_path.lower().endswith('.tga') and not '.' in os.path.basename(img_path):
                    parts[3] = img_path + ".tga"
                    lines[i] = '"'.join(parts)
    
    content = '\n'.join(lines)
    
    # ADD LOADER IF IT'S AN INVENTORY FILE
    if fname in category_loaders:
        loader = category_loaders[fname]
        # Check if the loader is being executed on a standalone line (to avoid alias definitions)
        # We look for the loader NOT preceded by 'alias' or followed by '\'
        loader_regex = rf'(?m)^[ \t]*{re.escape(loader)}[ \t]*$'
        if not re.search(loader_regex, content):
            if not content.strip().endswith(loader):
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
            if process_cfg_v2(fpath, name):
                print(f"Fixed V2 in {fpath}")

print("Total fix v2 complete (TGA extensions & Page Loaders).")
