import os
import re

persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist'

replacements = [
    (r'exec addons/neda/persist/weapon/equip\.cfg', '_safe_exec_equip'),
    (r'exec addons/neda/persist/use/w1\.cfg', '_safe_exec_use1'),
    (r'exec addons/neda/persist/use/w2\.cfg', '_safe_exec_use2'),
    (r'exec addons/neda/persist/use/w3\.cfg', '_safe_exec_use3'),
    (r'exec addons/neda/persist/use/w4\.cfg', '_safe_exec_use4'),
    (r'exec addons/neda/persist/use/w5\.cfg', '_safe_exec_use5'),
    (r'exec addons/neda/persist/use/w6\.cfg', '_safe_exec_use6'),
    (r'exec addons/neda/persist/use/use_m\.cfg', '_safe_exec_use_m'),
]

count = 0
for db_file in ['weapon_db.cfg', 'secondary_db.cfg', 'melee_db.cfg', 'explosive_db.cfg', 'special_db.cfg']:
    fp = os.path.join(persist_dir, db_file)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = content
        for pattern, replacement in replacements:
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)
            
        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f'Optimized DB entries in: {db_file}')

print(f'Done! Optimized {count} database files by shrinking alias strings.')
