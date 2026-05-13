import os

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# Target directories for persistence proxies
folders = [
    "persist",
    "select_main", # Some legacy ones might be here
    "select_map"
]

count = 0
for folder in folders:
    target_dir = os.path.join(root_dir, folder)
    if not os.path.exists(target_dir): continue
    
    for root, dirs, files in os.walk(target_dir):
        for f in os.listdir(root):
            if f.endswith(".cfg"):
                filepath = os.path.join(root, f)
                with open(filepath, 'r') as file_obj:
                    content = file_obj.read()
                
                changed = False
                # 1. Convert Type 7 to Type 4 at the end of touch_addbutton lines
                # Pattern: 255 255 255 255 7
                if "255 255 255 255 7" in content:
                    content = content.replace("255 255 255 255 7", "255 255 255 255 4")
                    changed = True
                
                # 2. Ensure flag "c" and coordinates are consistent
                # Some might have legacy formats
                if '"" -0.020000' in content:
                    content = content.replace('"" -0.020000', '"c" -0.020000')
                    changed = True
                
                if changed:
                    with open(filepath, 'w') as file_obj:
                        file_obj.write(content)
                    count += 1

print(f"Standardized {count} files to Type 4 rendering.")
