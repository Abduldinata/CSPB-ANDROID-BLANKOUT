import os
import re

roots = [
    r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page1',
    r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page2'
]

def sweep_configs():
    for root in roots:
        if not os.path.exists(root): continue
        for file in os.listdir(root):
            if file.endswith('.cfg'):
                filepath = os.path.join(root, file)
                name = file.replace('.cfg', '')
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # 1. Fix Image Extension (.tga) for selected_...
                # touch_addbutton "selected_..." "..."
                content = re.sub(r'("addons/neda/image/character/[^.]+)"', r'\1.tga"', content)
                
                # 2. Fix Layer (Set to 5 for previews and dark buttons)
                # Matches the end part: 255 255 255 255 [Layer]
                # We want 5 for the image, 4 for the hitbox, but the status call is a command.
                
                # Fix Preview Image line to Layer 5
                content = re.sub(r'(touch_addbutton "(selected_[^"]+)" "[^"]+" "" [0-9.]+ [0-9.]+ [0-9.]+ [0-9.]+ 255 255 255 255\s+)[0-9]', r'\1 5', content)
                
                # Fix Equiped status call
                # Ensure it points to the correct alias from char_db.cfg
                # Correct alias format: _show_equip_char_[name]
                status_call = f'_show_equip_char_{name}'
                # Some files might use _show_equip_char_viper but file is viperred.cfg
                # Let's trust the name of the file or the existing name in the content.
                
                # If there's an existing status call, replace it.
                if '_show_equip_char_' in content:
                     content = re.sub(r'_show_equip_char_[a-z0-9_]+', status_call, content)
                else:
                     content += f'\n{status_call}\n'
                
                # 3. Clean up whitespace
                content = content.replace('  5', ' 5')
                
                with open(filepath, 'w') as f:
                    f.write(content)
    print("Final character sweep completed.")

sweep_configs()
