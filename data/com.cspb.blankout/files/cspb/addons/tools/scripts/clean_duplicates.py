import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def clean_duplicates():
    processed = 0
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Remove duplicate alias _ind_XXX assignments in the same line
                # Pattern: alias _ind_XXX "..."; ... alias _ind_XXX "...";
                content = re.sub(r'(alias _ind_\w+ "exec addons/neda/persist/weapon/equip\.cfg";)\s*\1', r'\1', content)
                
                # Also clean up any remaining "alias alias" typos
                content = content.replace("alias alias", "alias")
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = clean_duplicates()
print(f"Cleaned {count} files with duplicate assignments.")
