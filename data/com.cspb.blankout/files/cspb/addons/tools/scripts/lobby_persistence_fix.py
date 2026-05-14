import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Full Loader Block
loader_block = """

// Full Persistence Loaders
_map_p1_indicator
_map_p2_indicator
_map_p3_indicator
_weap_p1_indicator
_weap_p2_indicator
_weap_p3_indicator
_weap_p4_indicator
_weap_p5_indicator
_weap_p6_indicator
_weap_p7_indicator
_weap_p8_indicator
_weap_p9_indicator
_sec_p1_indicator
_melee_p1_indicator
_exp_p1_indicator
_special_p1_indicator
"""

# 2. Find target files
target_files = []

# Character Lobby Menus
for team in ["blueteam", "redteam"]:
    team_dir = os.path.join(root_dir, team)
    if not os.path.exists(team_dir): continue
    for char in os.listdir(team_dir):
        char_dir = os.path.join(team_dir, char)
        if os.path.isdir(char_dir):
            for f in os.listdir(char_dir):
                if f.startswith("lobby_menu") and f.endswith(".cfg"):
                    target_files.append(os.path.join(char_dir, f))

# Team Selection Files (Lobby 4)
team_dir = os.path.join(root_dir, "team")
if os.path.exists(team_dir):
    for f in os.listdir(team_dir):
        if f.startswith("team_") and "class" in f and f.endswith(".cfg"):
            target_files.append(os.path.join(team_dir, f))

# 3. Apply updates
for filepath in target_files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    changed = False
    
    # Add loaders if missing
    if "_map_p1_indicator" not in content:
        content = content.strip() + loader_block
        changed = True
    
    # Standardize rendering flags and extensions (consistency sweep)
    # Fix "" -> "c"
    if '"" -0.020000' in content:
        content = content.replace('"" -0.020000', '"c" -0.020000')
        changed = True
        
    # Ensure .tga
    new_content = re.sub(r'("addons/neda/image/[^"]+?)(?=" (?:""|"c") -0\.02)', r'\1.tga', content)
    if new_content != content:
        content = new_content
        changed = True

    # Fix double .tga.tga
    if ".tga.tga" in content:
        content = content.replace(".tga.tga", ".tga")
        changed = True
        
    # Clean up destructive commands just in case
    bad_cmds = ["_rmv_use_all", "_rmv_persist_all"]
    for bad in bad_cmds:
        if bad in content:
            content = content.replace('; ' + bad, '').replace(';' + bad, '').replace(bad + ';', '').replace(bad, '')
            changed = True

    if changed:
        with open(filepath, 'w') as f:
            f.write(content)

print(f"Lobby and Team Selection consistency fix complete for {len(target_files)} files.")
