import os

file_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() in ['alias _char_p1_badge _null', 'alias _char_p2_badge _null', 'alias _char_equip_badge _null']:
        new_lines.append('// ' + line)
    else:
        new_lines.append(line)

with open(file_path, 'w') as f:
    f.write("".join(new_lines))

print("Disabled aggressive char resets in char_db.cfg.")
