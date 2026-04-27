import os

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
                if 'touch_addbutton' in line and ('_lobby_out3' in line or '_lobby_back2' in line):
                    # Split by quotes. Parts 1, 3, 5 are quoted strings.
                    parts = line.split('"')
                    if len(parts) >= 6:
                        # parts[5] is the command string
                        cmds = parts[5]
                        if '_rmv_chr_detail' not in cmds:
                            parts[5] = '_rmv_chr_detail; ' + cmds
                            line = '"'.join(parts)
                    
                    # Also fix the accidental ID change from previous run
                    line = line.replace('_rmv_chr_detail; _lobby_out3', '_lobby_out3')
                    line = line.replace('_rmv_chr_detail; _lobby_back2', '_lobby_back2')

                new_lines.append(line)
            
            content = "".join(new_lines).strip()
            # Ensure only one copy of _active_char_detail at end
            content = content.replace('// Show Equipped Character Detail\n_active_char_detail\n', '')
            content = content.replace('_active_char_detail', '')
            content = content.strip()
            content += '\n\n// Show Equipped Character Detail\n_active_char_detail\n'
            
            with open(inv_file, 'w') as f:
                f.write(content + '\n')
            print(f"  Fixed: {team}/{char}/inventory_character.cfg")

print("Theme configs fixed.")
