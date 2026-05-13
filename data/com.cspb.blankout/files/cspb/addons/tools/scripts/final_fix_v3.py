import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. GLOBAL COMMENT SANITIZATION (/* ... */ -> //) & "c" FLAG FIX
# Also fix the `/*database` issue from the logs.
def sanitize_cfg(fpath):
    with open(fpath, "r", encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace /* ... */ with // ... //
    # Simple regex for multiline /* */
    new_content = re.sub(r'/\*(.*?)\*/', r'// \1 //', content, flags=re.DOTALL)
    
    # Fix the `touch_addbutton ... "img" "c" ...` which triggers `Unknown command: c`
    # Ensure parameter "c" is not after a standalone quote that could be parsed as a command.
    # In GoldSrc, if CMD is "c", it runs "c".
    # Often it should be "" "c" (Empty command, button flag c)
    
    # If a line has '"c"' at it's place (CMD is empty, flag is c)
    # The engine expects: touch_addbutton "ID" "IMG" "CMD" X1 Y1 X2 Y2 FLAGS
    # Many people use "c" as a flag after coordinates.
    # Wait, the user said `Unknown command: c`. This means "c" IS in the CMD position.
    
    # Correct: touch_addbutton "ID" "IMG" "" X1 Y1 X2 Y2 ... 4 (center flag)
    # Incorrect: touch_addbutton "ID" "IMG" "c" ...
    new_content = new_content.replace('"" "c"', '"" ""')
    new_content = new_content.replace('" "c"', '" ""')
    
    if new_content != content:
        with open(fpath, "w", encoding='utf-8') as f:
            f.write(new_content)
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
        lines = f.readlines()
    
    new_db_lines = []
    
    for line in lines:
        if 'alias _db_' in line and '_full "' in line:
            # Extract alias name and content
            # alias _db_amok_full "..."
            match = re.search(r'alias (_db_([a-zA-Z0-9_]+)_full) "(.*)"', line)
            if match:
                alias_name = match.group(1)
                short_name = match.group(2)
                full_cmd = match.group(3)
                
                # Create sub-config
                sub_cfg_path = os.path.join(target_dir, f"db_{short_name}.cfg")
                with open(sub_cfg_path, "w") as sub_f:
                    sub_f.write(f"// Modular DB for {short_name}\n")
                    # Unescape quotes if any
                    clean_cmd = full_cmd.replace('\\"', '"')
                    sub_f.write(clean_cmd + "\n")
                
                # Update main DB to use exec
                new_db_lines.append(f'alias {alias_name} "exec addons/neda/persist/{category}/db_{short_name}.cfg"\n')
                continue
        new_db_lines.append(line)
    
    with open(db_file, "w") as f:
        f.writelines(new_db_lines)
    print(f"Refactored {category}_db.cfg")

# 3. FIX LOBBY 3 BACK (Restore specific back commands)
def fix_lobby3_back(fpath, char_name):
    with open(fpath, "r") as f:
        content = f.read()
    
    # Pattern to find the Back button and its command string
    # We want to replace the cleanup-only command with one that navigates back.
    # Standard back for lobby_menu3.cfg is usually _back_2_charname
    
    # We only fix it if it has our standardized Broken command
    if '_rmv_persist_all' in content and 'touch_addbutton "_lobby_back2"' in content:
        # Restore the back navigation
        # We'll use a standardized back command for each character.
        back_cmd = f"_tap_cnd_back; _hapus; _remove_3_{char_name}; _back_2_{char_name}"
        
        # Replace the CMD part.
        # We look for: touch_addbutton "_lobby_back2" "" "..."
        regex = r'touch_addbutton "_lobby_back2" "" ".*?"'
        new_content = re.sub(regex, f'touch_addbutton "_lobby_back2" "" "touch_removebutton _lobby_back2; {back_cmd}"', content)
        
        if new_content != content:
            with open(fpath, "w") as f:
                f.write(new_content)
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

# Fix Lobby 3 Back per character
for root, dirs, files in os.walk(os.path.join(base_path, "neda")):
    if "lobby_menu3.cfg" in files:
        # Folder is like blueteam/acidpool
        fpath = os.path.join(root, "lobby_menu3.cfg")
        char_name = os.path.basename(root)
        if fix_lobby3_back(fpath, char_name):
            print(f"Fixed Lobby 3 Back for {char_name}")

print("Final Fix 1.0 complete (DB, Sanitization, Navigation).")
