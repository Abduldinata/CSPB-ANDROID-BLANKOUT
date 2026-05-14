import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def add_conditional_equip_display():
    processed = 0
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                basename = os.path.splitext(f)[0]
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                
                original = content
                
                # Update the _check_equip_XXX alias to conditionally show Equip badge
                # If _equipped_item is set to _db_XXX_full, execute it to show Equip badge
                pattern = f'alias _check_equip_{basename} ""'
                replacement = f'alias _check_equip_{basename} "_equipped_item"'
                
                content = content.replace(pattern, replacement)
                
                if content != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(content)
                    processed += 1
    
    return processed

count = add_conditional_equip_display()
print(f"Added conditional Equip display to {count} item configs.")

# Also need to initialize _equipped_item to empty in reset scripts
reset_files = [
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\secondary\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\melee\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\explosive\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\special\reset_indicators.cfg"
]

for reset_file in reset_files:
    if os.path.exists(reset_file):
        with open(reset_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add _equipped_item reset if not already there
        if 'alias _equipped_item ""' not in content:
            content = content.rstrip() + '\n\nalias _equipped_item ""\n'
            
            with open(reset_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Added _equipped_item reset to {os.path.basename(reset_file)}")

print("Conditional Equip display system complete!")
