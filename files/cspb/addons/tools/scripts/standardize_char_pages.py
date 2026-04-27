import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
teams = ["blueteam", "redteam"]

# 1. Update character page configs to support persistent selection borders
for team in teams:
    team_path = os.path.join(base_path, team)
    if not os.path.isdir(team_path):
        continue
    for char_name in os.listdir(team_path):
        char_path = os.path.join(team_path, char_name, "character")
        if os.path.isdir(char_path):
            for fname in os.listdir(char_path):
                if fname.startswith("page") and fname.endswith(".cfg"):
                    fpath = os.path.join(char_path, fname)
                    with open(fpath, "r") as f:
                        lines = f.readlines()
                    
                    # Check if already added
                    if any("_active_char_selection" in line for line in lines):
                        print(f"Skipping {fpath}, already updated.")
                        continue
                    
                    # Add to the end
                    with open(fpath, "a") as f:
                        f.write("\n_active_char_selection\n")
                    print(f"Updated character selection persistence for {fpath}")

# 2. Standardize weapon pages (Remove hardcoded character paths)
# We look for _rmv_main_inventory_CHAR and replace with _rmv_main_inventory
# We look for _main_inventory_CHAR and replace with _main_inventory
for team in teams:
    team_path = os.path.join(base_path, team)
    if not os.path.isdir(team_path):
        continue
    for char_name in os.listdir(team_path):
        # Scan weapons and other inventory categories
        for cat in ["weapons", "secondary", "melee", "explosive", "special"]:
            cat_path = os.path.join(team_path, char_name, cat)
            if os.path.isdir(cat_path):
                for fname in os.listdir(cat_path):
                    if fname.startswith("page") and fname.endswith(".cfg"):
                        fpath = os.path.join(cat_path, fname)
                        with open(fpath, "r") as f:
                            content = f.read()
                        
                        # Generic replacements
                        patterns = [
                            (rf'_rmv_main_inventory_{char_name}', '_rmv_main_inventory'),
                            (rf'_main_inventory_{char_name}', '_main_inventory'),
                            (rf'_second_inventory_{char_name}', '_second_inventory'),
                            (rf'_rmv_second_inventory_{char_name}', '_rmv_second_inventory'),
                            (rf'_melee_inventory_{char_name}', '_melee_inventory'),
                            (rf'_rmv_melee_inventory_{char_name}', '_rmv_melee_inventory'),
                            (rf'_explosive_inventory_{char_name}', '_explosive_inventory'),
                            (rf'_rmv_explosive_inventory_{char_name}', '_rmv_explosive_inventory'),
                            (rf'_special_inventory_{char_name}', '_special_inventory'),
                            (rf'_rmv_special_inventory_{char_name}', '_rmv_special_inventory'),
                            (rf'_back_3_{char_name}', '_back_to_lobby'), # Back to Lobby 3
                            (rf'_lobby_3b_{char_name}', '_back_to_lobby'), # Entry to Lobby 3 Load
                        ]
                        
                        new_content = content
                        for old, new in patterns:
                            new_content = re.sub(old, new, new_content, flags=re.IGNORECASE)
                            
                        if new_content != content:
                            with open(fpath, "w") as f:
                                f.write(new_content)
                            print(f"Standardized paths in {fpath}")

print("Batch update complete.")
