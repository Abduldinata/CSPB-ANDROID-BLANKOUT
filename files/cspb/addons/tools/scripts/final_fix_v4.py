import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. GLOBAL COMMENT SANITIZATION (/* ... */ -> //) & "c" FLAG FIX
def sanitize_cfg(fpath):
    with open(fpath, "r", encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace /* ... */ with // ... //
    new_content = re.sub(r'/\*(.*?)\*/', r'// \1 //', content, flags=re.DOTALL)
    
    # Fix misparsed "c" flags and "restart" in Start Game buttons
    lines = new_content.split('\n')
    new_lines = []
    changed = False
    
    for line in lines:
        original_line = line
        # Fix corrupted flags (result of previous script)
        line = line.replace('"" "c"', '"" ""')
        
        # Remove `; restart` from all start game buttons (Host_Error fix)
        if '_lobby_start_' in line:
            line = line.replace('; restart"', '"')
            line = line.replace(';restart"', '"')
        
        # Fix specific button in class selection files
        if 'touch_addbutton "_lobby_teamblue_class' in line:
             line = line.replace('"" "c"', '"" ""')
             line = line.replace('" "c"', '" ""')
        
        if line != original_line:
            changed = True
        new_lines.append(line)
    
    if changed or (new_content != content):
        with open(fpath, "w", encoding='utf-8') as f:
            f.write('\n'.join(new_lines) if changed else new_content)
        return True
    return False

# 2. SEPARATE DB REFACTORING FOR Melee, Explosive, Special
def refactor_db(category):
    db_file = os.path.join(base_path, "neda", "persist", f"{category}_db.cfg")
    if not os.path.exists(db_file):
        return
    
    target_dir = os.path.join(base_path, "neda", "persist", category)
    os.makedirs(target_dir, exist_ok=True)
    
    with open(db_file, "r") as f:
        content = f.read()
    
    lines = content.split('\n')
    new_db_lines = []
    
    for line in lines:
        if 'alias _db_' in line and '_full "' in line:
            # alias _db_amok_full "..."
            match = re.search(r'alias (_db_([a-zA-Z0-9_ -]+)_full) "(.*)"', line)
            if match:
                alias_name = match.group(1)
                short_name = match.group(2).replace(' ', '_').lower()
                full_cmd = match.group(3)
                
                sub_cfg_path = os.path.join(target_dir, f"db_{short_name}.cfg")
                with open(sub_cfg_path, "w") as sub_f:
                    sub_f.write(f"// Modular DB for {short_name}\n")
                    sub_f.write(full_cmd.replace('\\"', '"') + "\n")
                
                new_db_lines.append(f'alias {alias_name} "exec addons/neda/persist/{category}/db_{short_name}.cfg"')
                continue
        new_db_lines.append(line)
    
    with open(db_file, "w") as f:
        f.write('\n'.join(new_db_lines))
    print(f"Refactored {category}_db.cfg")

# 3. FIX LOBBY 3 BACK (Restore specific back commands)
def fix_lobby_nav(fpath, char_name):
    with open(fpath, "r") as f:
        content = f.read()
    
    changed = False
    # Standard back for lobby_menu3.cfg
    if 'lobby_menu3.cfg' in fpath:
        if '_rmv_persist_all' in content and 'touch_addbutton "_lobby_back2"' in content:
            back_cmd = f"_tap_cnd_back; _hapus; _remove_3_{char_name}; _back_2_{char_name}"
            content = re.sub(r'touch_addbutton "_lobby_back2" "" ".*?"', 
                            f'touch_addbutton "_lobby_back2" "" "touch_removebutton _lobby_back2; {back_cmd}"', 
                            content)
            changed = True
            
    # Fix Character Inventory Badges Overlap
    if 'inventory_character.cfg' in fpath:
        if '_add_indicators' in content and '_add_indicators_char_inv' not in content:
            content = content.replace('_add_indicators', '_add_indicators_char_inv')
            changed = True
            
    if changed:
        with open(fpath, "w") as f:
            f.write(content)
        return True
    return False

# EXECUTION
for root, dirs, files in os.walk(base_path):
    for name in files:
        fpath = os.path.join(root, name)
        if name.endswith(".cfg"):
            sanitize_cfg(fpath)

refactor_db("melee")
refactor_db("explosive")
refactor_db("special")

# Fix Lobby Nav per character
for root, dirs, files in os.walk(os.path.join(base_path, "neda")):
    for name in files:
        if name == "lobby_menu3.cfg" or name == "inventory_character.cfg" or name == "inventory_character2.cfg":
            fpath = os.path.join(root, name)
            # Find char name from parent folder
            char_name = os.path.basename(root)
            if fix_lobby_nav(fpath, char_name):
                print(f"Fixed Navigation/Badges for {char_name}: {name}")

print("Final Comprehensive Fix complete.")
