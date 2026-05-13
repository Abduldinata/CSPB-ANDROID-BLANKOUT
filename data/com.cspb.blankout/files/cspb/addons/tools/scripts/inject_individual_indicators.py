import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"
db_path = os.path.join(root_dir, "select_main", "weapon", "persist_db.cfg")
reset_file = os.path.join(root_dir, "select_main", "reset_individual_indicators.cfg")

# 1. Parse DB to get all weapon/item keys
keys = []
with open(db_path, 'r', encoding='utf-8') as f:
    for line in f:
        match = re.search(r'alias (_db_(\w+))', line)
        if match:
            keys.append(match.group(2)) # e.g. "aug"

# 2. Create the individual reset script
with open(reset_file, 'w', encoding='utf-8') as f:
    f.write("// Reset all individual item indicators\n")
    for key in keys:
        f.write(f'alias _ind_{key} ""\n')

# 3. Update reset_indicators.cfg for each category to include the new script
# (Actually, let's just make one global individual reset and call it in all category resets)
cat_resets = [
    os.path.join(root_dir, "select_main", "weapon", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "secondary", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "melee", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "explosive", "reset_indicators.cfg"),
    os.path.join(root_dir, "select_main", "special", "reset_indicators.cfg")
]

for cr in cat_resets:
    if os.path.exists(cr):
        with open(cr, 'a', encoding='utf-8') as f:
            f.write(f'\nexec addons/neda/select_main/reset_individual_indicators.cfg\n')

# 4. Inject logic into item files
# Maps key to possible file matches
def update_item_files():
    search_dir = os.path.join(root_dir, "select_main")
    for root, _, files in os.walk(search_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                # Check which key this file belongs to (basename usually matches)
                basename = os.path.splitext(f)[0]
                if basename in keys:
                    key = basename
                    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                        content = file.read()
                    
                    original = content
                    
                    # A. Add individual loader at the end
                    if f"_ind_{key}" not in content:
                        content += f"\n_ind_{key}\n"
                    
                    # B. Update Equip button to set the indicator
                    # Find: touch_addbutton "equip_[key]" "" "... _weap_pX_indicator" ...
                    # Insert: alias _ind_[key] \"exec addons/neda/persist/weapon/equip.cfg\"; 
                    # before: _weap_pX_indicator (or equivalent slot indicator)
                    
                    # Pattern matches the equip button command part
                    # We want to insert the alias set before any category indicator call (_weap_, _sec_, _melee_, etc)
                    pattern = r'(_(weap|sec|melee|exp|spc)_p\d+_indicator)'
                    replacement = f'alias _ind_{key} \"exec addons/neda/persist/weapon/equip.cfg\"; \\1'
                    content = re.sub(pattern, replacement, content)
                    
                    if content != original:
                        with open(path, 'w', encoding='utf-8') as file:
                            file.write(content)

update_item_files()
print("Individual indicator injection completed.")
