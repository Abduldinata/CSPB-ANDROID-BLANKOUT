import os
import re
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
game_root = os.path.dirname(root)

all_files = glob.glob(os.path.join(root, "**/*.cfg"), recursive=True) + \
            glob.glob(os.path.join(root, "**/*.db"), recursive=True)

exec_pattern = re.compile(r'exec\s+([\w\./\\-]+)')
tga_pattern = re.compile(r'"([\w\./\\ ]+?\.tga)"')


def normalize_exec_target(raw: str) -> str:
    target = raw.strip().replace('/', os.sep).replace('\\', os.sep)
    # In cfg alias strings, escaped quote often leaves a trailing backslash in regex capture.
    while target.endswith(os.sep):
        target = target[:-1]
    target = target.rstrip(';')
    return target

issues = []

print(f"Checking paths in {len(all_files)} files...")

for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Execs
            for m in exec_pattern.finditer(content):
                target = normalize_exec_target(m.group(1))
                if not target.startswith('addons'): continue
                
                full_p = os.path.join(game_root, target)
                if not os.path.exists(full_p):
                    issues.append(f"BROKEN EXEC: '{target}' in {os.path.relpath(filepath, root)}")
            
            # TGAs
            for m in tga_pattern.finditer(content):
                target = m.group(1).replace('/', os.sep).replace('\\', os.sep)
                if not target.startswith('addons'): continue
                
                full_p = os.path.join(game_root, target)
                if not os.path.exists(full_p):
                    issues.append(f"BROKEN TGA: '{target}' in {os.path.relpath(filepath, root)}")

    except Exception as e:
        pass

unique_issues = sorted(list(set(issues)))
if not unique_issues:
    print("\nOK: All paths are valid.")
else:
    print(f"\nFound {len(unique_issues)} broken paths:")
    for issue in unique_issues:
        print(issue)
