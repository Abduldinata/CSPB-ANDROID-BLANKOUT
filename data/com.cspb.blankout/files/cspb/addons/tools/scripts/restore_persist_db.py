import os
import re

db_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\persist_db.cfg"

def restore_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add back the equip.cfg execution to all aliases
    # Pattern: alias _db_XXX "exec addons/neda/persist/use/useY.cfg"
    # Replace with: alias _db_XXX "exec addons/neda/persist/weapon/equip.cfg; exec addons/neda/persist/use/useY.cfg"
    
    pattern = r'alias (_db_\w+) "exec addons/neda/persist/use/(use\d+\.cfg)"'
    replacement = r'alias \1 "exec addons/neda/persist/weapon/equip.cfg; exec addons/neda/persist/use/\2"'
    
    new_content = re.sub(pattern, replacement, content)
    
    with open(db_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Restored persist_db.cfg with Equip badge execution.")

restore_db()
