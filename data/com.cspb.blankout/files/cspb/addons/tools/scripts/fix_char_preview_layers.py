import os
import re

roots = [
    r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page1',
    r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page2'
]

for root_dir in roots:
    if not os.path.exists(root_dir): continue
    for file in os.listdir(root_dir):
        if file.endswith('.cfg'):
            filepath = os.path.join(root_dir, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Find touch_addbutton "selected_..." and change layer 4 to 5
            # Example: touch_addbutton "selected_red1" "..." "" 0.46 0.62 0.62 0.78 255 255 255 255 4
            updated = re.sub(r'(touch_addbutton "selected_[^"]+" "[^"]+" "" [0-9.]+ [0-9.]+ [0-9.]+ [0-9.]+ 255 255 255 255 )4', r'\1 5', content)
            
            with open(filepath, 'w') as f:
                f.write(updated)

print("Character preview images moved to Layer 5.")
