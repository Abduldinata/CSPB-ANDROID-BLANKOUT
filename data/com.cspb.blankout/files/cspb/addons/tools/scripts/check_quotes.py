import os

root = r"e:\Games\PROJECT LOBBY CSPB\addons"
files = [os.path.join(root, "lobby.cfg"), os.path.join(root, "inventory.cfg"), os.path.join(root, "map.cfg"), os.path.join(root, "mode.cfg")]

for filepath in files:
    if not os.path.exists(filepath): continue
    print(f"Checking {os.path.basename(filepath)}...")
    with open(filepath, 'r') as f:
        for i, line in enumerate(f, 1):
            if line.strip().startswith('alias') and line.count('"') % 2 != 0:
                print(f"  L{i}: {line.strip()}")
