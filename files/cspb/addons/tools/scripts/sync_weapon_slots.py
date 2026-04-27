import os
import re

def sync_weapon_db():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\weapons"
    db_file = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\weapon_db.cfg"
    
    weapon_to_slot = {}
    
    # Scan all 16 pages
    for i in range(1, 17):
        page_file = os.path.join(base_path, f"page{i}.cfg")
        if not os.path.exists(page_file):
            continue
            
        with open(page_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Match pattern: _sl_weaponname in the button command
        # And determine slot from _lobby_selectX
        for slot in range(1, 7):
            match = re.search(f'_lobby_select{slot}".*?_sl_([a-zA-Z0-9_]+)', content)
            if match:
                weap_name = match.group(1)
                weapon_to_slot[weap_name] = slot
                print(f"Found {weap_name} at Slot {slot} on Page {i}")

    # Read current DB
    with open(db_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith("alias _db_") and "_full" in line:
            # Match alias _db_weaponname_full
            m = re.match(r'alias _db_([a-zA-Z0-9_]+)_full', line)
            if m:
                weap_name = m.group(1)
                if weap_name in weapon_to_slot:
                    slot = weapon_to_slot[weap_name]
                    # Update useX.cfg
                    new_line = re.sub(r'use\d\.cfg', f'use{slot}.cfg', line)
                    new_lines.append(new_line)
                    continue
        new_lines.append(line)

    with open(db_file, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("weapon_db.cfg synchronized successfully.")

if __name__ == "__main__":
    sync_weapon_db()
