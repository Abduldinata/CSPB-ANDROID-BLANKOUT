import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Update Persist DB to use correct Equip logic for all categories
def sync_persist_db():
    db_path = os.path.join(root_dir, "select_main", "weapon", "persist_db.cfg")
    with open(db_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace any specific category equip with the main weapon equip (which is correctly positioned)
    # The user wants "equip sesuaikan dengan main yg sekarang"
    content = content.replace("persist/secondary/equip.cfg", "persist/weapon/equip.cfg")
    content = content.replace("persist/melee/equip.cfg", "persist/weapon/equip.cfg")
    content = content.replace("persist/explosive/equip.cfg", "persist/weapon/equip.cfg")
    content = content.replace("persist/special/equip.cfg", "persist/weapon/equip.cfg")
    
    with open(db_path, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Cleanup redundant logic in sub-category item files (Sync with what we did for weapons)
def clean_sub_category_buttons():
    # Directories for secondary, melee, explosive, special
    dirs = [
        os.path.join(root_dir, "select_main", "secondary"),
        os.path.join(root_dir, "select_main", "melee"),
        os.path.join(root_dir, "select_main", "explosive"),
        os.path.join(root_dir, "select_main", "special")
    ]
    
    for d in dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for f in files:
                if f.endswith(".cfg"):
                    path = os.path.join(root, f)
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                    
                    original = content
                    # Remove _equip; and _useX; (same as weapon logic)
                    content = re.sub(r'_equip;\s*', '', content)
                    content = re.sub(r'_use\d+;\s*', '', content)
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as file:
                            file.write(content)

# 3. Fix "Back" buttons in inventory files to point to Lobby 3 correctly
def fix_back_buttons():
    # Only targeting the blueteam/leopard for now as per context, but can be expanded
    # We want back button to call _back_3_leopard (Lobby 3)
    target_dir = os.path.join(root_dir, "blueteam", "leopard")
    for f in os.listdir(target_dir):
        if f.startswith("inventory_") and f.endswith(".cfg"):
            path = os.path.join(target_dir, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
            
            new_lines = []
            changed = False
            for line in lines:
                if 'touch_addbutton "_lobby_back' in line:
                    # Replace whatever back alias is there with _back_3_leopard
                    # And ensure _rmv_rmv_persist_all is corrected to _rmv_persist_all
                    line = re.sub(r'_back_\d_leopard', '_back_3_leopard', line)
                    line = line.replace('_rmv_rmv_persist_all', '_rmv_persist_all')
                    line = line.replace('_rmv_secondary_inventory_leopard', '_rmv_second_inventory_leopard')
                    changed = True
                if 'touch_addbutton "_lobby_out' in line:
                    line = line.replace('_rmv_rmv_persist_all', '_rmv_persist_all')
                    line = line.replace('_rmv_secondary_inventory_leopard', '_rmv_second_inventory_leopard')
                    changed = True
                new_lines.append(line)
            
            if changed:
                with open(path, 'w', encoding='utf-8') as file:
                    file.write("".join(new_lines))

# 4. Correct _rmv_persist_all in lobby.cfg (ensure it's stable)
def stabilize_lobby_cfg():
    lobby_path = r"e:\Games\PROJECT LOBBY CSPB\addons\lobby.cfg"
    with open(lobby_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ensure _hapus uses _rmv_persist_all and not _persist_*
    content = content.replace('touch_removebutton _persist_*', '_rmv_persist_all')
    
    with open(lobby_path, 'w', encoding='utf-8') as f:
        f.write(content)

sync_persist_db()
clean_sub_category_buttons()
fix_back_buttons()
stabilize_lobby_cfg()
print("Sync completed.")
