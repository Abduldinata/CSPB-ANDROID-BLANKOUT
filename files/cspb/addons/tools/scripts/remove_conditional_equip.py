import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def remove_conditional_equip_logic():
    """Remove the _check_equip_XXX and _equipped_item tracker logic"""
    processed = 0
    
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                basename = os.path.splitext(f)[0]
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Remove the conditional check lines
                lines_to_remove = [
                    f'// Show Equip badge if this item is equipped',
                    f'alias _check_equip_{basename} "_equipped_item"',
                    f'_check_equip_{basename}'
                ]
                
                for line_pattern in lines_to_remove:
                    content = content.replace(line_pattern + '\r\n', '')
                    content = content.replace(line_pattern + '\n', '')
                
                # Remove alias _equipped_item _db_XXX_full from equip buttons
                content = re.sub(r'alias _equipped_item _db_\w+_full; ', '', content)
                
                # Clean up extra blank lines
                content = re.sub(r'\n\n\n+', '\n\n', content)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = remove_conditional_equip_logic()
print(f"Removed conditional Equip logic from {count} item configs.")
