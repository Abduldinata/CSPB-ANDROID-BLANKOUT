import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def fix_item_configs():
    processed = 0
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                basename = os.path.splitext(f)[0]
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Remove the _ind_XXX call at the end of files
                content = re.sub(r'\n_ind_\w+\s*\n*$', '\n', content)
                
                # Fix the equip button command
                # Remove: alias _ind_XXX "exec ..."; _CATEGORY_pX_indicator _db_XXX; _CATEGORY_pX_indicator
                # Replace with: alias _CATEGORY_pX_indicator _db_XXX; _CATEGORY_pX_indicator
                
                # Pattern to match the broken command
                pattern = r'alias _ind_\w+ "exec addons/neda/persist/weapon/equip\.cfg";\s*(_(weap|sec|melee|exp|spc)_p\d+_indicator)\s+(_db_\w+);\s*\1'
                replacement = r'alias \1 \3; \1'
                
                content = re.sub(pattern, replacement, content)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = fix_item_configs()
print(f"Fixed {count} item configuration files.")

# Also remove the broken reset file
reset_file = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\reset_individual_indicators.cfg"
if os.path.exists(reset_file):
    os.remove(reset_file)
    print("Removed broken reset_individual_indicators.cfg")
