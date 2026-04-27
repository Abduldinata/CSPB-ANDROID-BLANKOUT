import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'
inventory_cfg = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\inventory.cfg'

replacements = [
    (r'addons/neda/persist/weapon/', 'addons/neda/persist/main/'),
    (r'persist/weapon/', 'persist/main/'),
    (r'_load_weapon_db', '_load_main_db'),
]

def process_file(fp):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    except:
        pass
    return False

count = 0
# Process all files in neda/
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.lower().endswith('.cfg'):
            if process_file(os.path.join(root, f)):
                count += 1

# Process inventory.cfg
if process_file(inventory_cfg):
    count += 1

print(f'Done! Successfully updated {count} files with the new "main" category nomenclature.')
