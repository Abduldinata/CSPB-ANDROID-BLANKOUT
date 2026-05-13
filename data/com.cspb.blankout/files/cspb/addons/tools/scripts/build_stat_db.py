import os

stat_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\stat'
db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\stat_db.cfg'

with open(db_path, 'w', encoding='utf-8') as db:
    db.write('// Weapon Statistics Database\n')
    db.write('// This file consolidates 55 separate stat files into memory for performance.\n\n')
    
    for filename in os.listdir(stat_dir):
        if filename.endswith('.cfg') and filename != 'remove_all_stat.cfg':
            weapon_name = filename[:-4]
            fp = os.path.join(stat_dir, filename)
            try:
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                if content:
                    # Escape quotes for alias string
                    content = content.replace('"', '\\"')
                    db.write(f'alias stat_{weapon_name} "{content}"\n')
            except:
                pass

print(f'Successfully created stat_db.cfg with all weapon stats.')
