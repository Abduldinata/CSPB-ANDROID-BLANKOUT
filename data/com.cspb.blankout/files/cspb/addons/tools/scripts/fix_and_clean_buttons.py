import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def fix_and_clean(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # 1. Fix the typo introduced by the previous bad regex
    # _rmvalias -> _rmv_useX; alias (approximate fix)
    # Actually, it's easier to just look for the pattern and restore it.
    # Pattern was likely _rmv_useX; _useX; alias ...
    # And it became _rmvalias ...
    # We want it to be _rmv_useX; alias ...
    # But wait, we wanted to REMOVE _useX;, correctly.
    
    # First, fix the typoed string if it exists
    content = content.replace("_rmvalias", "_rmv_useX; alias") # Placeholder to split them
    
    # Better yet, let's use a smarter regex for the cleanup
    # We want to remove ONLY the standalone "_useX;" and NOT parts of "_rmv_useX;"
    
    # 2. Correct cleanup for _equip and _useX
    # Pattern: match "; _equip;" or " _equip;" but not "some_equip"
    # Matches that are preceded by space or semicolon and followed by space or semicolon
    content = re.sub(r'(?<=[ ;])_equip;?\s*', '', content)
    
    # For _useX;, we must avoid matching _rmv_useX;
    # We use negative lookbehind for "_rmv"
    content = re.sub(r'(?<!_rmv)(?<!_rmv_)(?<!\w)_use\d+;?\s*', '', content)
    
    # 3. Final cleanup of any double semicolons or weird spacing
    content = content.replace(";;", ";")
    content = content.replace("  ", " ")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

processed = 0
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.endswith(".cfg"):
            if fix_and_clean(os.path.join(root, f)):
                processed += 1

print(f"Fixed and cleaned {processed} files.")
