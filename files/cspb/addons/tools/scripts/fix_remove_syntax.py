import os
import re

base_dir = r"e:\Games\PROJECT LOBBY CSPB\addons"

def fix_remove_syntax(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".cfg"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding='utf-8') as f:
                        lines = f.readlines()
                except UnicodeDecodeError:
                    continue
                
                new_lines = []
                changed = False
                for line in lines:
                    # Match touch_removebutton with more than one quoted argument or extra text
                    # Target: touch_removebutton "ID" "EXTRA" ...
                    # Replaced with: touch_removebutton "ID"
                    if 'touch_removebutton' in line:
                        match = re.search(r'(touch_removebutton\s+"[^"]+")\s+.*', line)
                        if match:
                            new_line = match.group(1) + "\n"
                            if new_line != line:
                                new_lines.append(new_line)
                                changed = True
                            else:
                                new_lines.append(line)
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                
                if changed:
                    with open(path, "w", encoding='utf-8') as f:
                        f.writelines(new_lines)
                    count += 1
    print(f"Fixed {count} files with invalid touch_removebutton syntax.")

fix_remove_syntax(base_dir)
