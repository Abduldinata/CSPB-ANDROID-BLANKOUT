import os
import re

db_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\persist_db.cfg"

def decouple_db():
    with open(db_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove "exec addons/neda/persist/weapon/equip.cfg; " from all aliases
    # Using regex to handle potential spacing variations
    new_content = re.sub(r'exec addons/neda/persist/weapon/equip.cfg;\s*', '', content)
    
    with open(db_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

decouple_db()
print("Decoupled indicators in persist_db.cfg.")
