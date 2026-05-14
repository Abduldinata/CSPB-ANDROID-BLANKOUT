import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Fix reset_indicators.cfg (Keep only alias resets, touch_remove is redundant and causes flickering)
reset_files = [
    os.path.join(root_dir, "select_main", "weapon", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_map", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "secondary", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "melee", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "explosive", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "special", "reset_indicators.cfg")
]

for rfile in reset_files:
    if os.path.exists(rfile):
        with open(rfile, 'r') as f:
            lines = f.readlines()
        new_lines = [line for line in lines if "touch_removebutton" not in line]
        with open(rfile, 'w') as f:
            f.writelines(new_lines)

# 2. Fix order in Weapon/Map selection configs
# Move _reset_* to the front of the button string
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".cfg"):
            filepath = os.path.join(root, file)
            # Focus on weapon/map pages and weapon/map selection files
            if any(x in filepath for x in ["select_main", "select_map", "weapons"]):
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Regex to find button strings and move _reset_ to the front
                def reorder_cmds(match):
                    btn_logic = match.group(1)
                    if "_reset_" in btn_logic:
                        # Extract the reset command
                        resets = re.findall(r'_reset_[^; ]+', btn_logic)
                        other_logic = btn_logic
                        for r in resets:
                            other_logic = other_logic.replace(r + ";", "").replace(";" + r, "").replace(r, "")
                        
                        # Clean up semicolons
                        other_logic = other_logic.strip("; ")
                        new_logic = "; ".join(resets) + "; " + other_logic
                        return '"' + new_logic.strip("; ") + '"'
                    return match.group(0)

                new_content = re.sub(r'"(_tap_cnd[^"]+)"', reorder_cmds, content)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)

print("Logic standardization and resetting flickering prevention complete.")
