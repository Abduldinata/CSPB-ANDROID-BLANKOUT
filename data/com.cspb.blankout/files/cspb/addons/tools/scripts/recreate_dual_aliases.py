import os
import re

db_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\persist_db.cfg"

def create_dual_aliases():
    with open(db_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Match pattern: alias _db_XXX "exec .../equip.cfg; exec .../useY.cfg"
        match = re.match(r'alias (_db_\w+) "exec addons/neda/persist/weapon/equip\.cfg; exec (addons/neda/persist/use/use\d+\.cfg)"', line)
        
        if match:
            alias_name = match.group(1)
            use_path = match.group(2)
            
            # Create two aliases:
            # 1. Use-only version (for page load)
            new_lines.append(f'alias {alias_name} "exec {use_path}"\n')
            # 2. Full version with Equip (for when equipping)
            new_lines.append(f'alias {alias_name}_full "exec addons/neda/persist/weapon/equip.cfg; exec {use_path}"\n')
        else:
            # Keep comments and blank lines
            new_lines.append(line)
    
    with open(db_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("Created dual alias system in persist_db.cfg")

create_dual_aliases()
