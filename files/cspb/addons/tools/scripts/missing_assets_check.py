import os
import re
import glob

root = r"e:\Games\PROJECT LOBBY CSPB\addons"
game_root = os.path.dirname(root)

all_files = glob.glob(os.path.join(root, "**/*.cfg"), recursive=True) + \
            glob.glob(os.path.join(root, "**/*.db"), recursive=True)

tga_pattern = re.compile(r'"([\w\./\\ ]+?\.tga)"')

missing_tgas = set()

for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for m in tga_pattern.finditer(content):
                target = m.group(1).replace('/', os.sep).replace('\\', os.sep)
                if not target.startswith('addons'): continue
                full_p = os.path.join(game_root, target)
                if not os.path.exists(full_p):
                    missing_tgas.add(target)
    except Exception:
        pass

# Organize by directory
dirs = {}
for tga in sorted(list(missing_tgas)):
    d = os.path.dirname(tga)
    if d not in dirs:
        dirs[d] = []
    dirs[d].append(os.path.basename(tga))

print("Found missing TGAs in these directories:")
for d in dirs:
    print(f"\n--- FOLDER: {d} ---")
    for f in dirs[d]:
        print(f"  [MISSING] {f}")
