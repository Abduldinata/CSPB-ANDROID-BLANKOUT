import os
import re

persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist'
db_files = {
    'weapon_db.cfg': '_reset_weap_indicators',
    'explosive_db.cfg': '_reset_explosive_indicators',
    'secondary_db.cfg': '_reset_secondary_indicators',
    'melee_db.cfg': '_reset_melee_indicators'
}

for cfg_file, reset_alias in db_files.items():
    filepath = os.path.join(persist_dir, cfg_file)
    if not os.path.exists(filepath):
        print(f"File not found: {cfg_file}")
        continue
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    pointers = []
    
    for line in lines:
        if line.startswith('alias _show_equip_'):
            # It's a pointer definition like `alias _show_equip_ak47 "exec..."`
            # We want to change it to `alias _show_equip_ak47 _null`
            parts = line.split()
            alias_name = parts[1]
            pointers.append(f"alias {alias_name} _null")
            new_lines.append(f"alias {alias_name} _null\n")
        elif line.startswith(f"alias {reset_alias}"):
            # Add pointer reset
            reset_pointers_alias = f"{reset_alias}_pointers"
            new_lines.append(f"alias {reset_alias} \"{reset_pointers_alias}; {line[len(f'alias {reset_alias} &quot;'):]}")
            # wait, if it's already modified, check if it contains the pointer reset
            if reset_pointers_alias not in line:
                # Assuming the line is `alias _reset... "touch...`
                new_lines.pop()
                cmd_part = line.split('"', 1)[1]
                new_lines.append(f'alias {reset_alias} "{reset_pointers_alias}; {cmd_part}')
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    # Add the reset pointer definition at the top or after reset_alias
    if pointers:
        reset_pointers_alias = f"{reset_alias}_pointers"
        reset_cmd = f"alias {reset_pointers_alias} \"{'; '.join(pointers)}\"\n"
        
        # Insert it after the reset alias
        for i, line in enumerate(new_lines):
            if line.startswith(f"alias {reset_alias}"):
                new_lines.insert(i + 1, reset_cmd)
                break
                
    with open(filepath, 'w') as f:
        f.write("".join(new_lines))
    print(f"Fixed pointers in {cfg_file}")
