import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def fix_nested_quotes():
    processed = 0
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Fix: alias _equipped_item "_db_XXX_full" -> alias _equipped_item _db_XXX_full
                # Inside the touch_addbutton command
                
                pattern = r'alias _equipped_item "(_db_\w+_full)"'
                replacement = r'alias _equipped_item \1'
                
                content = re.sub(pattern, replacement, content)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = fix_nested_quotes()
print(f"Fixed nested quotes in {count} item configuration files.")
