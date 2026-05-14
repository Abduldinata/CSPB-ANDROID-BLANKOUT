import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

teams = ["blueteam", "redteam"]

def audit_and_fix_inventory(filepath, char_name):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # 1. Correct the persistence cleanup alias typo
    content = content.replace("_rmv_rmv_persist_all", "_rmv_persist_all")
    
    # 2. Correct the secondary inventory removal alias typo
    # Pattern: _rmv_secondary_inventory_[char] -> _rmv_second_inventory_[char]
    content = content.replace(f"_rmv_secondary_inventory_{char_name}", f"_rmv_second_inventory_{char_name}")
    
    # 3. Ensure _rmv_persist_all is present in Back and Exit buttons
    # Check lines with _lobby_back or _lobby_out
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if 'touch_addbutton "_lobby_back' in line or 'touch_addbutton "_lobby_out' in line:
            if "_rmv_persist_all" not in line:
                # Insert it before the final redirection alias (usually starts with _back_ or _add_menu or _main_inventory)
                # Let's just insert it after _hapus;
                line = line.replace("_hapus;", "_hapus; _rmv_persist_all;")
        
        # 4. Standardize Back button redirection
        # inventory_* (from Lobby 3) -> _back_3_[char]
        # inventory_*2 (from Lobby 4) -> _back_4_[char] (If it exists, check lobby_[char].cfg)
        if 'touch_addbutton "_lobby_back' in line:
            if filepath.endswith("2.cfg"): # e.g. inventory_main2.cfg
                line = re.sub(r'_back_\d_[\w]+', f'_back_4_{char_name}', line)
            else:
                line = re.sub(r'_back_\d_[\w]+', f'_back_3_{char_name}', line)
        
        # 5. Cleanup double semicolons and extra spaces
        line = line.replace(";;", ";")
        line = re.sub(r';\s*;', ';', line)
        new_lines.append(line)
        
    content = "\n".join(new_lines)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

processed = 0
for team in teams:
    team_path = os.path.join(root_dir, team)
    if not os.path.exists(team_path): continue
    for char in os.listdir(team_path):
        char_path = os.path.join(team_path, char)
        if os.path.isdir(char_path):
            # Process inventory_*.cfg in the char root
            for f in os.listdir(char_path):
                if f.startswith("inventory_") and f.endswith(".cfg"):
                    if audit_and_fix_inventory(os.path.join(char_path, f), char):
                        processed += 1

print(f"Audited and fixed {processed} character inventory files.")
