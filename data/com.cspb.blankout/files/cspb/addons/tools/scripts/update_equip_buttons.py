import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def update_item_configs():
    processed = 0
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                basename = os.path.splitext(f)[0]
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Step 1: Update equip button to use _full version and set equipped tracker
                # Pattern: alias _CATEGORY_pX_indicator _db_XXX; _CATEGORY_pX_indicator
                # Replace with: alias _equipped_item "_db_XXX_full"; alias _CATEGORY_pX_indicator _db_XXX; _CATEGORY_pX_indicator
                
                pattern = r'(alias (_(weap|sec|melee|exp|spc)_p\d+_indicator) (_db_\w+); \2)'
                replacement = f'alias _equipped_item "\\4_full"; \\1'
                
                content = re.sub(pattern, replacement, content)
                
                # Step 2: Add conditional Equip display at the end of file
                # Check if this item is the equipped one, if yes show Equip badge
                if not content.strip().endswith(f'_check_equip_{basename}'):
                    # Remove any trailing whitespace/newlines
                    content = content.rstrip() + '\n\n'
                    # Add conditional check
                    content += f'// Show Equip badge if this item is equipped\n'
                    content += f'alias _check_equip_{basename} ""\n'
                    content += f'_check_equip_{basename}\n'
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = update_item_configs()
print(f"Updated {count} item configuration files with conditional Equip display.")
