import os

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
lobby_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. RENAME ROOT FOLDER
old_root_weapons = os.path.join(base_path, "weapons")
new_root_main = os.path.join(base_path, "main")

if os.path.exists(old_root_weapons):
    # Check if 'main' exists. If it does, we might need to merge or error.
    # Based on previous list_dir, 'main' does NOT exist at the root of neda/
    if not os.path.exists(new_root_main):
        os.rename(old_root_weapons, new_root_main)
        print(f"Renamed root folder {old_root_weapons} -> {new_root_main}")
    else:
        print(f"Warning: {new_root_main} already exists. Skipping rename.")

# 2. GLOBAL STRING REPLACEMENT
def replace_in_file(fpath):
    with open(fpath, "r") as f:
        content = f.read()
    
    # Replace root level reference /neda/weapons/ with /neda/main/
    new_content = content.replace("/neda/weapons/", "/neda/main/")
    
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
                print(f"Updated root routes in {fpath}")

print("Final root synchronization complete.")
