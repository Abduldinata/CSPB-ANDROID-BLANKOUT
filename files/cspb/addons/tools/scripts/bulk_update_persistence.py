import re
import os

def update_db(filepath, reset_alias, equip_status_alias, equip_show_prefix, indicator_alias):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    with open(filepath, 'r') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Update Reset Alias
        if f'alias {reset_alias}' in line:
            if f'alias {equip_status_alias} _null' not in line:
                line = line.rstrip('\n').rstrip('"') + f'; alias {equip_status_alias} _null"\n'
        
        # Update Full Database Aliases
        # Example: alias _db_aug_full "_reset_weap_indicators; alias _weap_use_indicator \"exec addons/neda/persist/use/use5.cfg\"; _weap_use_indicator"
        # We want to add: alias _weap_equip_status _show_equip_aug; _weap_equip_status
        if '_full' in line and 'alias _db_' in line:
            # Find the weapon/char name
            match = re.search(r'alias _db_(.*)_full', line)
            if match:
                name = match.group(1)
                if f'alias {equip_status_alias} {equip_show_prefix}{name}' not in line:
                    # Insert before the last quote
                    line = line.rstrip('\n').rstrip('"') + f'; alias {equip_status_alias} {equip_show_prefix}{name}; {equip_status_alias}"\n'
        
        # Specifically for char_db.cfg which doesn't use _full suffix normally
        if 'char_db.cfg' in filepath and 'alias _db_char_' in line:
             match = re.search(r'alias _db_char_(.*) "_reset_char_indicators', line)
             if match:
                name = match.group(1)
                if f'alias {equip_status_alias} {equip_show_prefix}{name}' not in line:
                    line = line.rstrip('\n').rstrip('"') + f'; alias {equip_status_alias} {equip_show_prefix}{name}; {equip_status_alias}"\n'

        new_lines.append(line)
    
    # Ensure default pointers are there
    content = "".join(new_lines)
    if f'alias {equip_status_alias} "_null"' not in content and f'alias {equip_status_alias} _null' not in content:
        new_lines.append(f'alias {equip_status_alias} "_null"\n')

    with open(filepath, 'w') as f:
        f.write("".join(new_lines))
    print(f"Updated {filepath}")

# Update Primary
update_db(r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\weapon_db.cfg', 
          '_reset_weap_indicators', '_weap_equip_status', '_show_equip_', '_weap_use_indicator')

# Update Secondary
update_db(r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\secondary_db.cfg', 
          '_reset_secondary_indicators', '_sec_equip_status', '_show_equip_', '_secondary_use_indicator')

# Update Characters
update_db(r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg', 
          '_reset_char_indicators', '_char_equip_status', '_show_equip_char_', '_char_p1_badge')
