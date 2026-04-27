import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"

# Standards
coords_out3 = "0.940000 0.906067 0.980000 0.992360 255 255 255 255 6"
coords_back2 = "0.900000 0.819775 0.980000 0.906067 255 255 255 255 6"

def sanitize_and_fix(fpath):
    with open(fpath, "r") as f:
        lines = f.readlines()
    
    new_lines = []
    changed = False
    
    for line in lines:
        if 'touch_addbutton "_lobby_out3"' in line or 'touch_addbutton "_lobby_back2"' in line:
            # We want to extract the command and rebuild the line correctly.
            # Pattern: touch_addbutton "ID" "IMG" "CMD" COORDS
            is_out3 = "_lobby_out3" in line
            id_name = "_lobby_out3" if is_out3 else "_lobby_back2"
            coords = coords_out3 if is_out3 else coords_back2
            
            # Try to find the actual command string. 
            # Because of corruption, there might be extra quotes.
            # Usually the command string contains something like '_tap_cnd_back' or '_rmv_wp_page1'
            
            cmd_match = re.search(r'(_tap_cnd_back;.*?[0-9a-zA-Z_ ])', line)
            if not cmd_match:
                # Fallback if corrupted beyond simple search
                if is_out3:
                    cmd_str = "_tap_cnd_back; _hapus; _rmv_persist_all"
                else:
                    cmd_str = "_tap_cnd_back; _hapus; _rmv_persist_all"
            else:
                # Extract starting from the first underscore-prefixed command
                cmd_str = line[line.find('_'):line.rfind('"')]
                # Clean up if it grabbed too much
                cmd_str = cmd_str.split('"')[0].strip()
            
            # Ensure touch_removebutton is at the start
            if f"touch_removebutton {id_name};" not in cmd_str:
                cmd_str = f"touch_removebutton {id_name}; " + cmd_str
            
            # Rebuild clean line
            new_line = f'touch_addbutton "{id_name}" "" "{cmd_str}" {coords}\n'
            new_lines.append(new_line)
            changed = True
        else:
            new_lines.append(line)
            
    if changed:
        with open(fpath, "w") as f:
            f.writelines(new_lines)
        return True
    return False

for root, dirs, files in os.walk(base_path):
    for name in files:
        if name.endswith(".cfg") and ("inventory_" in name or "lobby_menu3" in name):
            fpath = os.path.join(root, name)
            if sanitize_and_fix(fpath):
                print(f"Sanitized and fixed: {fpath}")

print("UI Sanitization complete.")
