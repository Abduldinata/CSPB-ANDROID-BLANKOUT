import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Fix double .tga.tga
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".cfg"):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            if ".tga.tga" in content:
                content = content.replace(".tga.tga", ".tga")
                with open(filepath, 'w') as f:
                    f.write(content)

# 2. Move loaders to bottom in character inventory files and lobby files
def move_loaders_to_bottom(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    loader_lines = []
    other_lines = []
    
    in_loader_block = False
    for line in lines:
        if any(x in line for x in ["_map_p", "_weap_p", "_sec_p", "_melee_p", "_exp_p", "_special_p", "// Full Persistence Loaders"]):
            # Check if it's an alias definition or a call
            # Persistence loaders are usually single word calls in this context
            stripped = line.strip()
            if stripped and not stripped.startswith("alias") and not stripped.startswith("touch_addbutton") and not stripped.startswith("exec"):
                 loader_lines.append(line)
            elif "// Full Persistence Loaders" in line:
                 loader_lines.append(line)
            else:
                 other_lines.append(line)
        else:
            other_lines.append(line)
    
    if loader_lines:
        # Remove empty lines from the end of other_lines
        while other_lines and not other_lines[-1].strip():
            other_lines.pop()
        
        new_content = "".join(other_lines) + "\n\n" + "".join(loader_lines)
        with open(filepath, 'w') as f:
            f.write(new_content)

# Apply to character folders
for team in ["blueteam", "redteam"]:
    team_dir = os.path.join(root_dir, team)
    if not os.path.exists(team_dir): continue
    for char in os.listdir(team_dir):
        char_dir = os.path.join(team_dir, char)
        if os.path.isdir(char_dir):
            inv_file = os.path.join(char_dir, "inventory_main.cfg")
            if os.path.exists(inv_file):
                move_loaders_to_bottom(inv_file)
            
            lobby_file = os.path.join(char_dir, "lobby_menu3.cfg")
            if os.path.exists(lobby_file):
                move_loaders_to_bottom(lobby_file)

print("Correction and Loader repositioning complete.")
