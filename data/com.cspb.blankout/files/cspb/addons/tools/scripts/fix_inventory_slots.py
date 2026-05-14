import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
teams = ["blueteam", "redteam"]

# 1. CATEGORY MAPPING
# Mapping from inventory file to the alias/command it should execute at the end to show page 1
category_loaders = {
    "inventory_weapon.cfg": "_load_wp_p1",
    "inventory_weapon2.cfg": "_load_wp_p1", # weapon2 usually also uses _load_wp_p1 which is context-mapped
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

# 2. IMAGE PATH FIXES
# Ensure background images have .tga extension
def fix_image_path(line):
    # Match touch_addbutton "pattern" "path" ... where path is under addons/neda/image
    # And check if it's an inventory_ background
    if 'touch_addbutton' in line and 'addons/neda/image/' in line:
        parts = line.split('"')
        if len(parts) >= 5:
            img_path = parts[3]
            # If it's an inventory background without .tga extension
            if 'inventory_' in img_path and not img_path.endswith('.tga'):
                parts[3] = img_path + '.tga'
                return '"'.join(parts)
    return line

for team in teams:
    team_p = os.path.join(base_path, team)
    if not os.path.exists(team_p): continue
    for char_n in os.listdir(team_p):
        char_p = os.path.join(team_p, char_n)
        if not os.path.isdir(char_p): continue
        
        for file_name in os.listdir(char_p):
            if file_name.startswith("inventory_") and file_name.endswith(".cfg"):
                fpath = os.path.join(char_p, file_name)
                with open(fpath, "r") as f:
                    lines = f.readlines()
                
                # Fix image paths
                new_lines = [fix_image_path(line) for line in lines]
                
                # Check if loader is already present
                loader = category_loaders.get(file_name)
                if loader:
                    loader_found = any(loader in line and 'alias' not in line for line in lines)
                    if not loader_found:
                        # Append a newline if last line doesn't have one
                        if new_lines and not new_lines[-1].endswith('\n'):
                            new_lines[-1] += '\n'
                        new_lines.append(f"\n{loader}\n")
                        print(f"Added loader {loader} to {fpath}")
                
                # Write back if changed
                new_content = "".join(new_lines)
                with open(fpath, "w") as f:
                    f.write(new_content)

print("Inventory missing slots fix complete.")
