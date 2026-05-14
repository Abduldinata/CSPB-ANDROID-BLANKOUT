import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. FIX remove_inv_badges.cfg
# Add _rmv_inv_badges execution at the end of the file.
rib_path = os.path.join(base_path, "neda", "remove_inv_badges.cfg")
if os.path.exists(rib_path):
    with open(rib_path, "r") as f:
        content = f.read()
    if "_rmv_inv_badges" not in content.split('\n')[-2:]: # If not at the end
        if not content.endswith('\n'):
            content += '\n'
        content += "\n_rmv_inv_badges\n"
        with open(rib_path, "w") as f:
            f.write(content)
        print(f"Fixed {rib_path} (added execution call).")

# 2. UPDATE lobby.cfg (_hapus and coordinates)
lobby_path = os.path.join(base_path, "lobby.cfg")
if os.path.exists(lobby_path):
    with open(lobby_path, "r") as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        # Add _rmv_inv_badges to _hapus
        if 'alias _hapus "' in line and '_rmv_inv_badges' not in line:
            line = line.replace('_lobby_off;', '_lobby_off; _rmv_inv_badges;')
        new_lines.append(line)
    
    with open(lobby_path, "w") as f:
        f.writelines(new_lines)
    print(f"Updated {lobby_path} (added _rmv_inv_badges to _hapus).")

# 3. STANDARDIZE ALL inventory_*.cfg COORDINATES & ID REMOVAL
# Standard Coords:
# Exit (_lobby_out3): 0.940000 0.906067 0.980000 0.992360
# Back (_lobby_back2): 0.900000 0.819775 0.980000 0.906067

exit_coords = "0.940000 0.906067 0.980000 0.992360"
back_coords = "0.900000 0.819775 0.980000 0.906067"

def fix_nav_buttons(fpath):
    with open(fpath, "r") as f:
        content = f.read()
    
    original = content
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        if 'touch_addbutton "_lobby_out3"' in line:
            # Fix coordinates
            parts = line.split('"')
            if len(parts) >= 7:
                cmd = parts[4]
                # Prepend ID removal to ensure it replaces any previous button
                if 'touch_removebutton _lobby_out3' not in cmd:
                    parts[4] = "touch_removebutton _lobby_out3; " + cmd
                # Set Standard Coords
                # Format: "touch_addbutton" "ID" "img" "cmd" X1 Y1 X2 Y2 ...
                # Space separated values after the 4th quote
                rest = parts[5].strip().split(' ')
                if len(rest) >= 4:
                    rest[0] = "0.940000"
                    rest[1] = "0.906067"
                    rest[2] = "0.980000"
                    rest[3] = "0.992360"
                    parts[5] = " " + " ".join(rest) + " "
                line = '"'.join(parts)
        
        elif 'touch_addbutton "_lobby_back2"' in line:
            parts = line.split('"')
            if len(parts) >= 7:
                cmd = parts[4]
                if 'touch_removebutton _lobby_back2' not in cmd:
                    parts[4] = "touch_removebutton _lobby_back2; " + cmd
                rest = parts[5].strip().split(' ')
                if len(rest) >= 4:
                    rest[0] = "0.900000"
                    rest[1] = "0.819775"
                    rest[2] = "0.980000"
                    rest[3] = "0.906067"
                    parts[5] = " " + " ".join(rest) + " "
                line = '"'.join(parts)
        
        new_lines.append(line)
    
    final_content = '\n'.join(new_lines)
    if final_content != original:
        with open(fpath, "w") as f:
            f.write(final_content)
        return True
    return False

# Iterate over all character folders and root neda/ to fix buttons
for root, dirs, files in os.walk(os.path.join(base_path, "neda")):
    for name in files:
        if name.endswith(".cfg") and ("inventory_" in name or "lobby_menu3" in name):
            fpath = os.path.join(root, name)
            if fix_nav_buttons(fpath):
                print(f"Standardized buttons in {fpath}")

print("UI Stacking and Badge lingering fix complete.")
