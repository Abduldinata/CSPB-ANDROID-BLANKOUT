import os
import re
from collections import defaultdict

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons"

# Database files to check
db_files = [
    os.path.join(root_dir, "neda", "select_main", "weapon", "persist_db.cfg"),
    os.path.join(root_dir, "neda", "select_map", "map_db.cfg"),
    os.path.join(root_dir, "neda", "mode", "mode_db.cfg"),
    os.path.join(root_dir, "mode.cfg"),
    os.path.join(root_dir, "map.cfg"),
    os.path.join(root_dir, "inventory.cfg"),
]

print("=" * 80)
print("DATABASE ALIAS AUDIT")
print("=" * 80)

for db_file in db_files:
    if not os.path.exists(db_file):
        continue
    
    print(f"\nChecking: {os.path.basename(db_file)}")
    print("-" * 80)
    
    with open(db_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    # Track aliases
    aliases = {}  # alias_name -> command
    duplicates = defaultdict(list)  # command -> [alias_names]
    
    for i, line in enumerate(lines, 1):
        # Match alias definitions
        match = re.match(r'alias\s+(\S+)\s+"(.+)"', line.strip())
        if match:
            alias_name = match.group(1)
            command = match.group(2)
            
            # Check for duplicate alias names
            if alias_name in aliases:
                print(f"WARNING: DUPLICATE ALIAS NAME at line {i}: {alias_name}")
                print(f"    Old: {aliases[alias_name]}")
                print(f"    New: {command}")
            
            aliases[alias_name] = command
            duplicates[command].append(alias_name)
    
    # Check for same command with different alias names
    print(f"\nChecking for duplicate commands...")
    found_dup_cmd = False
    for command, alias_list in duplicates.items():
        if len(alias_list) > 1:
            print(f"WARNING: SAME COMMAND used by multiple aliases:")
            print(f"    Command: {command[:80]}...")
            print(f"    Aliases: {', '.join(alias_list)}")
            found_dup_cmd = True
    
    if not found_dup_cmd:
        print("OK: No duplicate commands found")
    
    # Check for common typos
    print(f"\nChecking for potential typos...")
    typo_patterns = [
        (r'exec.*\.tga\.tga', 'Double .tga.tga extension'),
        (r'addons//neda', 'Double slash //'),
        (r'exec\s+exec', 'Double exec'),
        (r'alias\s+alias', 'Double alias'),
        (r'\s{2,}', 'Multiple spaces'),
    ]
    
    found_typo = False
    for i, line in enumerate(lines, 1):
        for pattern, desc in typo_patterns:
            if re.search(pattern, line):
                print(f"WARNING: Potential typo at line {i}: {desc}")
                print(f"    {line.strip()[:100]}")
                found_typo = True
    
    if not found_typo:
        print("OK: No obvious typos found")

print("\n" + "=" * 80)
print("AUDIT COMPLETE")
print("=" * 80)
