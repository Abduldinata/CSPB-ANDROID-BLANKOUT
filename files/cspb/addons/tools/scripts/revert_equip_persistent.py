import os
import re

persist_db_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\persist_db.cfg"

def revert_to_persistent_equip():
    """Revert the dual alias system back to original persistent Equip+Use"""
    
    with open(persist_db_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    skip_next = False
    
    for line in lines:
        # Skip _full aliases
        if '_full' in line and 'alias _db_' in line:
            skip_next = False
            continue
        
        # Update Use-only aliases back to Equip+Use
        match = re.match(r'alias (_db_\w+) "exec (addons/neda/persist/use/use\d+\.cfg)"', line)
        if match:
            alias_name = match.group(1)
            use_path = match.group(2)
            # Restore original format with Equip
            new_lines.append(f'alias {alias_name} "exec addons/neda/persist/weapon/equip.cfg; exec {use_path}"\n')
        else:
            new_lines.append(line)
    
    with open(persist_db_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("Reverted persist_db.cfg to persistent Equip+Use behavior")

revert_to_persistent_equip()
