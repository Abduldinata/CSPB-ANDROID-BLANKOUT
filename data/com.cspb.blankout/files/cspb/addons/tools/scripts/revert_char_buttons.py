import os
import re

# Base directory for character selection files
select_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_character\character"

# Mapping: slot -> original_cmd (approximately)
# We can extract the slot number from the equip_ID
# e.g. equip_bluec1 uses _rmv_equiped2; _equiped2 (based on previous view_file)
# Wait, I should check the files first or use a safer regex.

def revert_char_buttons(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cfg"):
                path = os.path.join(root, file)
                with open(path, "r", encoding='utf-8') as f:
                    lines = f.readlines()
                
                new_lines = []
                changed = False
                for line in lines:
                    match = re.search(r'touch_addbutton "(equip_([a-z]+)c(\d+))"', line)
                    if match:
                        id_full = match.group(1)
                        team = match.group(2)
                        slot = match.group(3)
                        
                        # Inventory slot mapping logic from previous research:
                        # redc1 -> _equiped1
                        # bluec1 -> _equiped2
                        # redc2 -> _equiped3
                        # bluec2 -> _equiped4
                        # redc3 -> _equiped5
                        # bluec3 -> _equiped6
                        # redc4 -> _equiped7
                        # bluec4 -> _equiped8
                        # redc5 -> _equiped9
                        
                        # Let's see if we can derive the equiped number
                        if team == "red":
                            eq_num = (int(slot) * 2) - 1
                        else:
                            eq_num = int(slot) * 2
                            
                        # Exception for page 2 if needed... but let's stick to the visible ones first.
                        # Actually, looking at redbull.cfg (slot 1): _rmv_equiped1; _equiped1
                        # Looking at acidpool.cfg (slot 1): _rmv_equiped2; _equiped2
                        
                        cmd = f"_rmv_equiped{eq_num};_equiped{eq_num}"
                        
                        # Reconstruct the line
                        new_line = re.sub(r'("[^"]*"\s+"[^"]*"\s+)"[^"]*"', r'\1"' + cmd + r'"', line)
                        if new_line != line:
                            new_lines.append(new_line)
                            changed = True
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                
                if changed:
                    with open(path, "w", encoding='utf-8') as f:
                        f.writelines(new_lines)
                    count += 1
    print(f"Reverted {count} character button files.")

revert_char_buttons(select_dir)
