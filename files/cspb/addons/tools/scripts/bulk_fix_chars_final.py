import os
import re

# Character Slot Map per Page
# Page 1: 1-9
# Page 2: 1-9 -> use1_p2.cfg etc.
# We'll map them based on their names in char_db.cfg

char_db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'
detail_roots = [
    r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page1',
    r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page2'
]

def update_char_db():
    if not os.path.exists(char_db_path): return
    with open(char_db_path, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        if 'alias _db_char_' in line:
            # Match the character name and current persistence file
            # Example: alias _db_char_redbull "... use1.cfg" ...
            match = re.search(r'alias _db_char_([a-z0-9_]+) "(.*?)"', line)
            if match:
                name = match.group(1)
                content = match.group(2)
                
                # Extract use file
                use_match = re.search(r'exec addons/neda/persist/character/(use[0-9_p2]*.cfg)', content)
                use_file = use_match.group(1) if use_match else ""
                
                # Extract team and slot pointers (back_to_lobby often contains team info)
                team_prefix = "3b" if "lobby_3b" in content else "1b"
                badge_type = "_char_p1_badge" if team_prefix == "3b" else "_char_p2_badge"
                
                # Rebuild the logic
                # Includes _reset_char_indicators, alias badge_type use_file, alias _show_equip _show_char_change_btn, ...
                new_cmd = f'_reset_char_indicators; alias {badge_type} \\"exec addons/neda/persist/character/{use_file}\\"; alias _show_equip_char_{name} _show_char_change_btn; alias _active_char_theme _db_char_{name}; alias _back_to_lobby _lobby_{team_prefix}_{name}; alias _char_inventory \\"_char_inventory_{name}\\"; alias _rmv_char_inventory \\"_rmv_char_inventory_{name}\\"; _char_inventory; {badge_type}; _show_equip_char_{name}'
                new_line = f'alias _db_char_{name} "{new_cmd}"\n'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(char_db_path, 'w') as f:
        f.write("".join(new_lines))
    print("char_db.cfg updated.")

def update_detail_configs():
    for root in detail_roots:
        if not os.path.exists(root): continue
        for file in os.listdir(root):
            if file.endswith('.cfg'):
                filepath = os.path.join(root, file)
                name = file.replace('.cfg', '')
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Fix Preview Image (touch_addbutton "selected_..." to Layer 5)
                # Ensure no redundant spaces before Layer number
                content = re.sub(r'(touch_addbutton "selected_[^"]+" "[^"]+" "" [0-9.]+ [0-9.]+ [0-9.]+ [0-9.]+ 255 255 255 255 )([0-9])', r'\1 5', content)
                
                # Fix Equip Button Hitbox (ensure unique ID and Layer 4)
                # touch_addbutton "equip_acidpool" "" "_tap_cnd_use; _db_char_acidpool" ...
                # Actually, the user wants it to be simple.
                # Just Ensure Layer 4 for Hitbox and Layer 5 for Dark Button Overlay
                
                # Final Call
                if f'_show_equip_char_{name}' not in content:
                    content += f'\n_show_equip_char_{name}\n'
                
                with open(filepath, 'w') as f:
                    f.write(content)
    print("Detail configs updated.")

update_char_db()
update_detail_configs()
