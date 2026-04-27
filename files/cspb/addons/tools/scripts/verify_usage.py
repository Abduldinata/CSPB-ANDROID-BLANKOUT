import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ADDONS_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
root_dir = os.path.join(ADDONS_ROOT, "neda")

# 1. Collect all defined _db_ aliases
defined_aliases = set()
db_files = [
    os.path.join(root_dir, "select_main", "weapon", "persist_db.cfg"),
    os.path.join(root_dir, "select_map", "map_db.cfg"),
    os.path.join(root_dir, "mode", "mode_db.cfg")
]

for db_file in db_files:
    if os.path.exists(db_file):
        with open(db_file, 'r') as f:
            for line in f:
                match = re.match(r'alias\s+(_db_\S+)\s+', line.strip())
                if match:
                    defined_aliases.add(match.group(1))

print(f"Total defined DB aliases found: {len(defined_aliases)}")

# 2. Scan selection configs for usage
usage_patterns = [
    r'alias\s+(_weap_p\d+_indicator)\s+(_db_\S+)',
    r'alias\s+(_sec_p\d+_indicator)\s+(_db_\S+)',
    r'alias\s+(_melee_p\d+_indicator)\s+(_db_\S+)',
    r'alias\s+(_exp_p\d+_indicator)\s+(_db_\S+)',
    r'alias\s+(_special_p\d+_indicator)\s+(_db_\S+)',
    r'alias\s+(_map_p\d+_indicator)\s+(_db_\S+)',
    r'alias\s+(_mode_indicator)\s+(_db_\S+)'
]

search_dirs = [
    os.path.join(root_dir, "select_main"),
    os.path.join(root_dir, "select_map"),
    os.path.join(root_dir, "mode")
]

errors = []

for s_dir in search_dirs:
    for root, dirs, files in os.walk(s_dir):
        for f in files:
            if f.endswith(".cfg"):
                path = os.path.join(root, f)
                with open(path, 'r', errors='ignore') as file_obj:
                    content = file_obj.read()
                    for pattern in usage_patterns:
                        matches = re.finditer(pattern, content)
                        for m in matches:
                            indicator = m.group(1)
                            db_alias = m.group(2)
                            # Clean up trailing semicolons if they got caught
                            db_alias = db_alias.split(';')[0].strip()
                            
                            if db_alias not in defined_aliases:
                                errors.append(f"MISSING ALIAS in {os.path.relpath(path, root_dir)}: {db_alias} (assigned to {indicator})")

if errors:
    print("\nFOUND ERRORS IN ALIAS USAGE:")
    for e in errors:
        print(e)
else:
    print("\nOK: All used DB aliases are correctly defined in the databases.")
