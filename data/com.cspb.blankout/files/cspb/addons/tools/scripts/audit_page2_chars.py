import os

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page2'

for file in os.listdir(root_dir):
    if file.endswith('.cfg'):
        filepath = os.path.join(root_dir, file)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        # Consistent with page1 logic
        with open(filepath, 'w') as f:
            f.write("".join(lines))

print("Character page2 files audited.")
