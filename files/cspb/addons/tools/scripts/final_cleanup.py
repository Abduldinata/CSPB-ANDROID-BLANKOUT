import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def final_cleanup():
    processed = 0
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Fix the specific pattern: remove the duplicate after _db_XXX;
                # Pattern: alias _ind_XXX "..."; _CATEGORY_pX_indicator _db_XXX; alias _ind_XXX "..."; _CATEGORY_pX_indicator
                # Should be: alias _ind_XXX "..."; _CATEGORY_pX_indicator _db_XXX; _CATEGORY_pX_indicator
                pattern = r'(alias _ind_\w+ "exec addons/neda/persist/weapon/equip\.cfg";) (_(weap|sec|melee|exp|spc)_p\d+_indicator) (_db_\w+); \1 \2'
                content = re.sub(pattern, r'\1 \2 \4; \2', content)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = final_cleanup()
print(f"Final cleanup completed on {count} files.")
