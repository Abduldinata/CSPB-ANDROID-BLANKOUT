import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'
teams = ['redteam', 'blueteam']

for team in teams:
    team_dir = os.path.join(root_dir, team)
    if not os.path.exists(team_dir): continue
    for char in os.listdir(team_dir):
        char_dir = os.path.join(team_dir, char)
        if not os.path.isdir(char_dir): continue
        inv_file = os.path.join(char_dir, 'inventory_character.cfg')
        if os.path.exists(inv_file):
            with open(inv_file, 'r') as f:
                lines = f.readlines()
            
            new_lines = []
            for line in lines:
                # Add _rmv_chr_detail to Exit and Back buttons
                if ('_lobby_out3' in line or '_lobby_back2' in line) and 'touch_addbutton' in line:
                    # Insert _rmv_chr_detail; before the last part of commands
                    # Usually commands start with " and end with "
                    match = re.search(r'("(.*?)")', line)
                    if match:
                        original_cmds = match.group(2)
                        if '_rmv_chr_detail' not in original_cmds:
                            # Add at the beginning of command string for quick cleanup
                            new_cmds = '_rmv_chr_detail; ' + original_cmds
                            line = line.replace(f'"{original_cmds}"', f'"{new_cmds}"')
                
                new_lines.append(line)
            
            # Ensure _active_char_detail is at the end
            content = "".join(new_lines).strip()
            if '_active_char_detail' not in content:
                content += '\n\n// Show Equipped Character Detail\n_active_char_detail\n'
            
            with open(inv_file, 'w') as f:
                f.write(content + '\n')
            print(f"  Updated: {team}/{char}/inventory_character.cfg")

print("Theme configs updated.")
