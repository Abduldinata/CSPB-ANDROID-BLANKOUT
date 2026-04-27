import os
import re
import shutil

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
lobby_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. RENAME FOLDERS
old_select_main = os.path.join(base_path, "select_main")
new_select_weapon = os.path.join(base_path, "select_weapon")

if os.path.exists(old_select_main):
    os.rename(old_select_main, new_select_weapon)
    print(f"Renamed {old_select_main} -> {new_select_weapon}")

old_weapon_sub = os.path.join(new_select_weapon, "weapon")
new_main_sub = os.path.join(new_select_weapon, "main")

if os.path.exists(old_weapon_sub):
    os.rename(old_weapon_sub, new_main_sub)
    print(f"Renamed {old_weapon_sub} -> {new_main_sub}")

# 2. GLOBAL STRING REPLACEMENT
def replace_in_file(fpath):
    with open(fpath, "r") as f:
        content = f.read()
    
    # Priority 1: select_main/weapon/ -> select_weapon/main/
    new_content = content.replace("select_main/weapon/", "select_weapon/main/")
    # Priority 2: select_main/ -> select_weapon/
    new_content = new_content.replace("select_main/", "select_weapon/")
    
    if new_content != content:
        with open(fpath, "w") as f:
            f.write(new_content)
        return True
    return False

# Iterate over all .cfg files in addons/
for root, dirs, files in os.walk(lobby_path):
    for name in files:
        if name.endswith(".cfg"):
            fpath = os.path.join(root, name)
            if replace_in_file(fpath):
                print(f"Updated routes in {fpath}")

print("Restructuring and routing update complete.")
