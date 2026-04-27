import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
teams = ["blueteam", "redteam"]

patterns_to_fix = [
    # Fix the double-suffix-2 bug: _weapon_inventory_char_name2_char_name -> _weapon_inventory2_char_name
    (r'_weapon_inventory_(\w+)2_\1', r'_weapon_inventory2_\1'),
    (r'_rmv_weapon_inventory_(\w+)2_\1', r'_rmv_weapon_inventory2_\1'),
    (r'_second_inventory_(\w+)2_\1', r'_second_inventory2_\1'),
    (r'_rmv_second_inventory_(\w+)2_\1', r'_rmv_second_inventory2_\1'),
    (r'_melee_inventory_(\w+)2_\1', r'_melee_inventory2_\1'),
    (r'_rmv_melee_inventory_(\w+)2_\1', r'_rmv_melee_inventory2_\1'),
    (r'_explosive_inventory_(\w+)2_\1', r'_explosive_inventory2_\1'),
    (r'_rmv_explosive_inventory_(\w+)2_\1', r'_rmv_explosive_inventory2_\1'),
    (r'_special_inventory_(\w+)2_\1', r'_special_inventory2_\1'),
    (r'_rmv_special_inventory_(\w+)2_\1', r'_rmv_special_inventory2_\1'),
    (r'_char_inventory_(\w+)2_\1', r'_char_inventory2_\1'),
    (r'_rmv_char_inventory_(\w+)2_\1', r'_rmv_char_inventory2_\1'),
]

for team in teams:
    team_p = os.path.join(base_path, team)
    if not os.path.exists(team_p): continue
    for char_n in os.listdir(team_p):
        char_p = os.path.join(team_p, char_n)
        if not os.path.isdir(char_p): continue
        
        # Traverse all directories in character folder
        for root, dirs, files in os.walk(char_p):
            for file in files:
                if file.endswith(".cfg"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r") as f:
                        content = f.read()
                    
                    new_content = content
                    for pattern, replacement in patterns_to_fix:
                        new_content = re.sub(pattern, replacement, new_content)
                    
                    if new_content != content:
                        with open(fpath, "w") as f:
                            f.write(new_content)
                        print(f"Fixed double-suffix in {fpath}")

# Also check root neda files
for file in os.listdir(base_path):
    if file.endswith(".cfg"):
        fpath = os.path.join(base_path, file)
        with open(fpath, "r") as f:
            content = f.read()
        new_content = content
        for pattern, replacement in patterns_to_fix:
            new_content = re.sub(pattern, replacement, new_content)
        if new_content != content:
            with open(fpath, "w") as f:
                f.write(new_content)
            print(f"Fixed double-suffix in root file {fpath}")

print("Cleanup of double-suffixes complete.")
