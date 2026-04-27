import os
import re

# Paths
map_persist_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\map"
mode_persist_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\mode"
char_persist_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\character"

def update_layer(dir_path, target_layer="5"):
    if not os.path.exists(dir_path):
        return
    count = 0
    for fname in os.listdir(dir_path):
        if fname.endswith(".cfg"):
            path = os.path.join(dir_path, fname)
            with open(path, "r", encoding='utf-8') as f:
                content = f.read()
            
            # Update layer to 5
            fixed_content = re.sub(r'(touch_addbutton\s+"[^"]+"\s+"[^"]*"\s+"[^"]*"\s+[\d\.-]+\s+[\d\.-]+\s+[\d\.-]+\s+[\d\.-]+\s+\d+\s+\d+\s+\d+\s+\d+\s+)\d+', r'\g<1>' + target_layer, content)
            
            if fixed_content != content:
                with open(path, "w", encoding='utf-8') as f:
                    f.write(fixed_content)
                count += 1
    print(f"Updated {count} files in {os.path.basename(dir_path)} to layer {target_layer}")

update_layer(map_persist_dir, "5")
update_layer(mode_persist_dir, "5")
update_layer(char_persist_dir, "5")
