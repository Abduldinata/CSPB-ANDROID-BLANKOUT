import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'

replacements = [
    # Character Borders: select_char/1.tga -> select_char/border/1.tga
    # Only if it's NOT already in border/ or equip/
    (r'(addons/neda/image/select_char/)([1-9]\.tga)', r'\1border/\2'),
    
    # Character Change: select_char/change.tga -> select_char/change/change.tga
    (r'addons/neda/image/select_char/change\.tga', r'addons/neda/image/select_char/change/change.tga'),
    
    # Main/Weapon Borders: select_main/1.tga -> select_main/border/1.tga
    # Only if NOT in use/ or equip/
    (r'(addons/neda/image/select_main/)([1-6]\.tga)', r'\1border/\2'),
    
    # Main/Weapon Equip: select_main/equip.tga -> select_main/equip/equip.tga
    (r'addons/neda/image/select_main/equip\.tga', r'addons/neda/image/select_main/equip/equip.tga')
]

# We need to be careful with character borders vs equip badges if they share the same number.
# Border: addons/neda/image/select_char/[1-9].tga
# Badge: addons/neda/image/select_char/equip/[1-9].tga
# If the path already has 'equip/' or 'border/' or 'change/' or 'use/', we skip.

def update_paths():
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.cfg') or file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                new_content = content
                for pattern, subst in replacements:
                    # Lookaround to avoid matching if already in a subfolder
                    # But the regex above is simple, so let's refine it.
                    if pattern == r'(addons/neda/image/select_char/)([1-9]\.tga)':
                        # Only replace if NOT preceded by border/ or equip/ or change/
                        # Actually, just check if the string "addons/neda/image/select_char/border/1.tga" exists exactly.
                        pass # Regex handles it if we match the full path without subfolder
                    
                    # Refinement: Match "addons/neda/image/select_char/border/1.tga" but NOT "addons/neda/image/select_char/border/1.tga"
                    new_content = re.sub(pattern, subst, new_content)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Updated: {file}")
                    count += 1
    print(f"Total files updated: {count}")

update_paths()
