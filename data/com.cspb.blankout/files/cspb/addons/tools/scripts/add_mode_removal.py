import os
import re

team_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"

def add_mode_removal_to_exit_buttons():
    """Add _rmv_mode_all to exit and back buttons in all team configs"""
    processed = 0
    
    for filename in os.listdir(team_dir):
        if filename.startswith("team_") and filename.endswith(".cfg"):
            path = os.path.join(team_dir, filename)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Pattern 1: Exit button (usually _lobby_out)
            # Add _rmv_mode_all after rmv_all_stat
            content = re.sub(
                r'(touch_addbutton "_lobby_out\d+" "" "_tap_cnd_back; rmv_all_stat;)',
                r'\1 _rmv_mode_all;',
                content
            )
            
            # Pattern 2: Back button (usually _lobby_back)
            # Add _rmv_mode_all after rmv_all_stat
            content = re.sub(
                r'(touch_addbutton "_lobby_back\d+" "" "_tap_cnd_back; rmv_all_stat;)',
                r'\1 _rmv_mode_all;',
                content
            )
            
            if content != original:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                processed += 1
                print(f"Updated {filename}")
    
    return processed

count = add_mode_removal_to_exit_buttons()
print(f"\nAdded mode removal to {count} team config files.")
