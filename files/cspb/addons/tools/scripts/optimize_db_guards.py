import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'

replacements = [
    (r'exec\s+addons/neda/persist/weapon_db\.cfg', '_load_weapon_db'),
    (r'exec\s+addons/neda/persist/secondary_db\.cfg', '_load_secondary_db'),
    (r'exec\s+addons/neda/persist/melee_db\.cfg', '_load_melee_db'),
    (r'exec\s+addons/neda/persist/explosive_db\.cfg', '_load_explosive_db'),
    (r'exec\s+addons/neda/persist/special_db\.cfg', '_load_special_db'),
    (r'exec\s+addons/neda/persist/char_db\.cfg', '_load_char_db'),
    (r'exec\s+addons/neda/persist/map_db\.cfg', '_load_map_db'),
]

count = 0
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.lower().endswith('.cfg'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                for pattern, replacement in replacements:
                    new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
                
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1
            except:
                pass

print(f'Done! Optimized {count} additional files by implementing database load guards.')
