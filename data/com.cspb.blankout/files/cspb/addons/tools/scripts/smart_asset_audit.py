import os
import re
import glob

root = r"e:\Games\PROJECT LOBBY CSPB\addons"
game_root = os.path.dirname(root)

# 1. Map all existing assets
print("Mapping existing assets...")
existing_assets = {} # lowercase_basename -> full_game_relative_path
all_existing_paths = set()

for dirpath, _, filenames in os.walk(root):
    if "image" in dirpath.lower():
        for f in filenames:
            if f.lower().endswith(".tga"):
                full_p = os.path.join(dirpath, f)
                rel_p = os.path.relpath(full_p, game_root).replace(os.sep, "/").lower()
                all_existing_paths.add(rel_p)
                
                basename = f.lower()
                if basename not in existing_assets:
                    existing_assets[basename] = []
                existing_assets[basename].append(rel_p)
                
                # Also store "collapsed" name (no underscores/spaces)
                collapsed = basename.replace("_", "").replace(" ", "")
                if collapsed not in existing_assets:
                    existing_assets[collapsed] = []
                existing_assets[collapsed].append(rel_p)

# 2. Check all CFG/DB files
print("Scanning configuration files...")
tga_pattern = re.compile(r'"([\w\./\\ ]+?\.tga)"')
mismatches = []

all_files = glob.glob(os.path.join(root, "**/*.cfg"), recursive=True) + \
            glob.glob(os.path.join(root, "**/*.db"), recursive=True)

for filepath in all_files:
    if "asset_audit" in filepath or "missing_tga" in filepath: continue
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for m in tga_pattern.finditer(content):
                original = m.group(1)
                target = original.replace('\\', '/').lower().strip()
                if not target.startswith('addons'): continue
                
                if target not in all_existing_paths:
                    # Try to find a match
                    basename = os.path.basename(target)
                    collapsed = basename.replace("_", "").replace(" ", "")
                    
                    suggestions = sorted(list(set(existing_assets.get(basename, []) + existing_assets.get(collapsed, []))))
                    
                    mismatches.append({
                        "file": os.path.relpath(filepath, root),
                        "line": content[:m.start()].count('\n') + 1,
                        "original": original,
                        "suggestions": suggestions
                    })
    except Exception:
        pass

# 3. Report
print("\n--- DETAILED ASSET MISMATCH REPORT ---")
if not mismatches:
    print("All TGA references are valid!")
else:
    # Sort by original reference to group identical issues
    mismatches.sort(key=lambda x: x["original"])
    current_target = None
    for m in mismatches:
        if m["original"] != current_target:
            current_target = m["original"]
            print(f"\n[BROKEN PATH] '{current_target}'")
            if m["suggestions"]:
                print("  SUGGESTIONS:")
                for s in m["suggestions"]:
                    print(f"    -> {s}")
            else:
                print("  NO SIMILAR ASSETS FOUND.")
        print(f"  Used in: {m['file']} (L{m['line']})")

print(f"\nTotal broken references found: {len(mismatches)}")
