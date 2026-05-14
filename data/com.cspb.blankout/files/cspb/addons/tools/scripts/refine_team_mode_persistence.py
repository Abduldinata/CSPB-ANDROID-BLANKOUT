import os

team_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\team'

for root, _, files in os.walk(team_dir):
    for filename in files:
        if filename.startswith('team_') and filename.endswith('.cfg'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                lines = f.readlines()
                
            modified = False
            for i in range(len(lines)):
                if '_lobby_out' in lines[i] or '_lobby_back' in lines[i]:
                    if '_rmv_mode_all' in lines[i]:
                        lines[i] = lines[i].replace('_rmv_mode_all; ', '')
                        lines[i] = lines[i].replace(' _rmv_mode_all;', '')
                        lines[i] = lines[i].replace('_rmv_mode_all', '')
                        modified = True
                        
            if modified:
                with open(filepath, 'w') as f:
                    f.write("".join(lines))
                print(f"Refined {filename}")

print("Done refining mode logic from team exit and back buttons.")
