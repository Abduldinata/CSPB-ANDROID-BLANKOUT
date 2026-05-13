import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Fix Persist Proxies (add "c" flag, ensure .tga)
persist_dirs = [
    os.path.join(root_dir, "persist", "weapon"),
    os.path.join(root_dir, "persist", "use"),
    os.path.join(root_dir, "persist", "map"),
    os.path.join(root_dir, "persist", "secondary"),
    os.path.join(root_dir, "persist", "melee"),
    os.path.join(root_dir, "persist", "explosive"),
    os.path.join(root_dir, "persist", "special")
]

for pdir in persist_dirs:
    if not os.path.exists(pdir): continue
    for filename in os.listdir(pdir):
        if filename.endswith(".cfg"):
            filepath = os.path.join(pdir, filename)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Add "c" flag if missing before coordinates
            content = content.replace('"" -0.020000', '"c" -0.020000')
            
            # Ensure .tga in paths
            content = re.sub(r'(\.tga)?(?=" "c"| ""| " -0\.02)', '.tga', content)
            
            with open(filepath, 'w') as f:
                f.write(content)

# 2. Fix Standard Use Configs (select_main/use*.cfg)
select_use_dir = os.path.join(root_dir, "select_main")
for filename in os.listdir(select_use_dir):
    if filename.startswith("use") and filename.endswith(".cfg"):
        filepath = os.path.join(select_use_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Add "c" flag and ensure .tga
        content = content.replace('"" -0.020000', '"c" -0.020000')
        content = re.sub(r'(\.tga)?(?=" "c"| ""| " -0\.02)', '.tga', content)
        if '"c"' not in content and '""' in content:
             content = content.replace('"" -0.020000', '"c" -0.020000')
        
        with open(filepath, 'w') as f:
            f.write(content)

# 3. Clean up navigation buttons (Remove _rmv_use_all and _rmv_persist_all)
bad_cmds = ["_rmv_use_all", "_rmv_persist_all"]

for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".cfg"):
            filepath = os.path.join(root, file)
            # Skip persistence folders to be safe
            if "persist" in filepath: continue
            
            changed = False
            with open(filepath, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            for line in lines:
                if 'touch_addbutton' in line:
                    original_line = line
                    for bad in bad_cmds:
                        # Clean up with semicolons
                        line = line.replace('; ' + bad, '').replace(';' + bad, '').replace(bad + ';', '').replace(bad, '')
                    if line != original_line:
                        changed = True
                new_lines.append(line)
            
            if changed:
                with open(filepath, 'w') as f:
                    f.writelines(new_lines)

print("Global cleanup and proxy fix complete.")
