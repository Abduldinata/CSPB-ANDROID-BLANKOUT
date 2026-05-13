import os

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\character'

# 1. Update existing use1.cfg to use9.cfg to _persist_char_badge1
for i in range(1, 10):
    filename = f'use{i}.cfg'
    filepath = os.path.join(root_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        new_content = content.replace('_persist_char_badge', '_persist_char_badge1')
        with open(filepath, 'w') as f:
            f.write(new_content)

# 2. Create use1_p2.cfg to use9_p2.cfg with _persist_char_badge2
for i in range(1, 10):
    filename_src = f'use{i}.cfg'
    filename_dst = f'use{i}_p2.cfg'
    filepath_src = os.path.join(root_dir, filename_src)
    filepath_dst = os.path.join(root_dir, filename_dst)
    
    if os.path.exists(filepath_src):
        with open(filepath_src, 'r') as f:
            content = f.read()
        new_content = content.replace('_persist_char_badge1', '_persist_char_badge2')
        with open(filepath_dst, 'w') as f:
            f.write(new_content)

print("Standardized P1 badges and created P2 badges.")
