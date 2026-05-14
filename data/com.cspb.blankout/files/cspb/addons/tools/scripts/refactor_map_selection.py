import os
import re

select_map_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_map"

def simplify_removal_cfg(filename):
    path = os.path.join(select_map_dir, filename)
    if not os.path.exists(path):
        return
    with open(path, "r", encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith("touch_removebutton"):
            # Extract only the ID (the first quoted argument)
            match = re.search(r'touch_removebutton\s+"([^"]+)"', line)
            if match:
                btn_id = match.group(1)
                new_lines.append(f'touch_removebutton "{btn_id}"')
            else:
                new_lines.append(line)
        elif line:
            new_lines.append(line)
            
    with open(path, "w", encoding='utf-8') as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Simplified {filename}")

def update_select_open_cfg(filename):
    path = os.path.join(select_map_dir, filename)
    if not os.path.exists(path):
        return
    with open(path, "r", encoding='utf-8') as f:
        content = f.read()
    
    # Add _map_p1_indicator to the end of map selection button commands
    # The map aliases usually look like _sl_burning_hall, _sl_crackdown_v1, etc.
    # We want to find commands containing _sl_ and append _map_p1_indicator
    
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if 'touch_addbutton' in line and '_sl_' in line and 'changelevel' in line:
            # Find the command string (usually the 3rd or 4th argument)
            # Pattern: touch_addbutton "ID" "IMAGE" "CMD" ...
            # We look for the last semicolon or the end of the command string before the coordinates
            
            # Simplified approach: Replace 'changelevel' with '_map_p1_indicator; changelevel'
            if '_map_p1_indicator' not in line:
                line = line.replace('changelevel', '_map_p1_indicator; changelevel')
                
        new_lines.append(line)
        
    with open(path, "w", encoding='utf-8') as f:
        f.write("\n".join(new_lines) + "\n")
    print(f"Updated {filename}")

# List of files to simplify
removal_files = [
    "remove_all_map_cmd.cfg", "remove_all_map_cmd2.cfg", "remove_all_map_cmd3.cfg",
    "remove_select_open_cmd.cfg", "remove_select_open_cmd2.cfg", "remove_select_open_cmd3.cfg",
    "remove_select_close_cmd.cfg", "remove_select_close_cmd2.cfg", "remove_select_close_cmd3.cfg",
    "remove_selectmap.cfg"
]

for f in removal_files:
    simplify_removal_cfg(f)

# List of files to update with indicator logic
select_files = ["select_open1.cfg", "select_open2.cfg", "select_open3.cfg"]
for f in select_files:
    update_select_open_cfg(f)

print("Refactor complete.")
