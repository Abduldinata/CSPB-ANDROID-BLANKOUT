import os

team_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\team'

files = [f for f in os.listdir(team_dir) if f.startswith('team_') and f.endswith('.cfg')]

for filename in files:
    filepath = os.path.join(team_dir, filename)
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    modified = False
    for line in lines:
        if 'touch_addbutton' in line and ('_lobby_out5' in line or '_lobby_back3' in line):
            # Split by quotes. Command string is usually index 5
            parts = line.split('"')
            if len(parts) >= 6:
                cmds = parts[5]
                # Remove _rmv_persist_all
                if '_rmv_persist_all' in cmds:
                    cmds = cmds.replace('_rmv_persist_all', '').replace('; ;', ';').strip('; ')
                    parts[5] = cmds
                    line = '"'.join(parts)
                    modified = True
        new_lines.append(line)
    
    if modified:
        with open(filepath, 'w') as f:
            f.write("".join(new_lines))
        print(f"  Refined: {filename}")

print("Team folder button cleanup complete.")
