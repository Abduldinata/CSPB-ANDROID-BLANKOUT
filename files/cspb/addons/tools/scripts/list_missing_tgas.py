import os
import re
import glob

root = r"e:\Games\PROJECT LOBBY CSPB\addons"
game_root = os.path.dirname(root)

all_files = glob.glob(os.path.join(root, "**/*.cfg"), recursive=True) + \
            glob.glob(os.path.join(root, "**/*.db"), recursive=True)

tga_pattern = re.compile(r'"([\w\./\\ ]+?\.tga)"')

missing_tgas = {}

print(f"Scanning {len(all_files)} files for TGA references...")

for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            for m in tga_pattern.finditer(content):
                target = m.group(1).replace('/', os.sep).replace('\\', os.sep)
                if not target.startswith('addons'): continue
                
                full_p = os.path.join(game_root, target)
                if not os.path.exists(full_p):
                    if target not in missing_tgas:
                        missing_tgas[target] = []
                    missing_tgas[target].append(os.path.relpath(filepath, root))

    except Exception as e:
        pass

if not missing_tgas:
    print("\nOK: No missing TGAs found.")
else:
    print("\n--- MISSING TGA LIST ---")
    # Group by directory for better readability
    paths = sorted(missing_tgas.keys())
    for p in paths:
        print(f"PATH: {p}")
        # print(f"  Used in: {', '.join(set(missing_tgas[p]))}")
