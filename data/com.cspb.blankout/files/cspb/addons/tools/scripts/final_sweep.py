import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Broad Sweep for Rendering Flags and Extensions
# Target: touch_addbutton lines in any .cfg file
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith(".cfg"):
            filepath = os.path.join(root, file)
            # Skip indicators themselves to avoid recursiveness if any
            if "indicators.cfg" in filepath: continue
            
            with open(filepath, 'r') as f:
                content = f.read()
            
            changed = False
            # Fix "" -> "c" before coordinates
            if '"" -0.020000' in content:
                content = content.replace('"" -0.020000', '"c" -0.020000')
                changed = True
            
            # Ensure .tga in paths that don't have it
            # Matches: "path/to/image" "" -0.02 OR "path/to/image" "c" -0.02
            new_content = re.sub(r'("addons/neda/image/[^"]+?)(?=" (?:""|"c") -0\.02)', r'\1.tga', content)
            if new_content != content:
                content = new_content
                changed = True
            
            # Fix double .tga.tga just in case
            if ".tga.tga" in content:
                content = content.replace(".tga.tga", ".tga")
                changed = True
                
            if changed:
                with open(filepath, 'w') as f:
                    f.write(content)

# 2. Page Loader Consistency
def ensure_loader(filepath, loader_call):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if loader_call not in content:
        # Add to bottom
        with open(filepath, 'a') as f:
            f.write(f"\n\n// Execute Persistent Indicator\n{loader_call}\n")

# Map files
for i in range(1, 4):
    f = os.path.join(root_dir, "select_map", f"select_open{i}.cfg")
    if os.path.exists(f): ensure_loader(f, "_map_p1_indicator")

# Weapon files
weap_dir = os.path.join(root_dir, "weapons")
if os.path.exists(weap_dir):
    for f in os.listdir(weap_dir):
        if f.startswith("page") and f.endswith(".cfg"):
            ensure_loader(os.path.join(weap_dir, f), "_weap_p1_indicator")

# Secondary
sec_dir = os.path.join(root_dir, "secondary")
if os.path.exists(sec_dir):
    for f in os.listdir(sec_dir):
        if f.startswith("page") and f.endswith(".cfg"):
            ensure_loader(os.path.join(sec_dir, f), "_sec_p1_indicator")

# Melee
mel_dir = os.path.join(root_dir, "melee")
if os.path.exists(mel_dir):
    for f in os.listdir(mel_dir):
        if f.startswith("page") and f.endswith(".cfg"):
            ensure_loader(os.path.join(mel_dir, f), "_melee_p1_indicator")

# Explosive
exp_dir = os.path.join(root_dir, "explosive")
if os.path.exists(exp_dir):
    for f in os.listdir(exp_dir):
        if f.startswith("page") and f.endswith(".cfg"):
            ensure_loader(os.path.join(exp_dir, f), "_exp_p1_indicator")

# Special
spc_dir = os.path.join(root_dir, "special")
if os.path.exists(spc_dir):
    for f in os.listdir(spc_dir):
        if f.startswith("page") and f.endswith(".cfg"):
            ensure_loader(os.path.join(spc_dir, f), "_special_p1_indicator")

print("Final sweep and consistency check complete.")
