import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"
db_path = os.path.join(root_dir, "select_main", "weapon", "persist_db.cfg")
reset_file = os.path.join(root_dir, "select_main", "reset_individual_indicators.cfg")

# 1. Parse DB to get all weapon/item keys
keys = []
with open(db_path, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.search(r'alias (_db_(\w+))', line)
        if match:
            keys.append(match.group(2)) # e.g. "aug"

# 2. Create the individual reset script
with open(reset_file, 'w', encoding='utf-8') as f:
    f.write("// Reset all individual item indicators\n")
    for key in keys:
        f.write(f'alias _ind_{key} ""\n')

print(f"Created reset file with {len(keys)} individual indicators.")

# 3. Update item files with proper logic
def update_item_files():
    search_dir = os.path.join(root_dir, "select_main")
    processed = 0
    
    for root, _, files in os.walk(search_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                basename = os.path.splitext(f)[0]
                
                # Check if this file corresponds to a known key
                if basename in keys:
                    key = basename
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                    
                    original = content
                    
                    # Remove any existing _ind_ calls at the end
                    content = re.sub(r'\n_ind_\w+\n*$', '', content)
                    
                    # Fix the equip button command
                    # Find the equip button line
                    lines = content.split('\n')
                    new_lines = []
                    
                    for line in lines:
                        if f'touch_addbutton "equip_{key}"' in line:
                            # Clean up any existing malformed alias injections
                            line = re.sub(r'alias alias _ind_\w+ "[^"]*";\s*', '', line)
                            line = re.sub(r'alias _ind_\w+ "exec addons/neda/persist/weapon/equip\.cfg";\s*', '', line)
                            
                            # Now inject the correct logic before the category indicator
                            # Pattern: find _weap_pX_indicator, _sec_pX_indicator, etc.
                            pattern = r'(_(weap|sec|melee|exp|spc)_p\d+_indicator)'
                            if re.search(pattern, line):
                                line = re.sub(pattern, f'alias _ind_{key} "exec addons/neda/persist/weapon/equip.cfg"; \\1', line)
                        
                        new_lines.append(line)
                    
                    content = '\n'.join(new_lines)
                    
                    # Add the individual loader at the end
                    if not content.endswith('\n'):
                        content += '\n'
                    content += f'\n_ind_{key}\n'
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as file:
                            file.write(content)
                        processed += 1
    
    return processed

count = update_item_files()
print(f"Updated {count} item configuration files.")
