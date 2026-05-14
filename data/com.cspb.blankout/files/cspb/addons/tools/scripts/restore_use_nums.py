import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Load Persist DB to know which weapon uses which USE badge
db_path = os.path.join(root_dir, "select_main", "weapon", "persist_db.cfg")
db_map = {} # alias -> use_num
with open(db_path, 'r', encoding='utf-8') as f:
    for line in f:
        # alias _db_aug "...; exec addons/neda/persist/use/use1.cfg"
        match = re.search(r'alias (_db_\w+) ".*use(\d)\.cfg"', line)
        if match:
            alias, num = match.groups()
            db_map[alias] = num

def fix_placeholders(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    if "_rmv_useX" not in content:
        return False
    
    original = content
    
    # Identify which _db_ alias is used in this file
    match = re.search(r'(_db_\w+)', content)
    if match:
        alias = match.group(1)
        if alias in db_map:
            num = db_map[alias]
            content = content.replace("_rmv_useX", f"_rmv_use{num}")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

processed = 0
search_dir = os.path.join(root_dir, "select_main")
for root, _, files in os.walk(search_dir):
    for f in files:
        if f.endswith(".cfg"):
            if fix_placeholders(os.path.join(root, f)):
                processed += 1

print(f"Fixed {processed} files with correct USE numbers.")
