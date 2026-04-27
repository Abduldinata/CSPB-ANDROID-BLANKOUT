import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def update_equip_buttons():
    processed = 0
    
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                basename = os.path.splitext(f)[0]
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Update equip button to:
                # 1. Use _db_XXX_full during equip (shows both badges immediately)
                # 2. Set _show_equip_XXX for this item
                # 3. Update page indicator to use _db_XXX (Use only)
                
                # Pattern: alias _CATEGORY_pX_indicator _db_XXX; _CATEGORY_pX_indicator
                # Add: alias _show_equip_XXX "exec equip.cfg"
                pattern = r'(alias (_(weap|sec|melee|exp|spc)_p\d+_indicator) (_db_\w+); \2)'
                
                def replacement(match):
                    full_match = match.group(0)
                    indicator_alias = match.group(2)
                    db_alias = match.group(4)
                    
                    # Add show alias setter and use _full version for immediate display
                    return f'alias _show_equip_{basename} "exec addons/neda/persist/weapon/equip.cfg"; alias {indicator_alias} {db_alias}; {db_alias}_full'
                
                content = re.sub(pattern, replacement, content)
                
                # Add show alias call at end if not already there
                if f'_show_equip_{basename}' not in content or content.count(f'_show_equip_{basename}') == 1:
                    content = content.rstrip() + '\n\n'
                    content += f'_show_equip_{basename}\n'
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = update_equip_buttons()
print(f"Updated {count} item configs with per-item show aliases.")
