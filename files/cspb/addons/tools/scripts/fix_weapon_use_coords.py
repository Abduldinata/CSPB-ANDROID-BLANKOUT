import os
import re

persist_use_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\use'

# Regex pattern to match the incorrect coordinates
coord_pattern = re.compile(r'\s+0\.\d+\s+0\.\d+\s+0\.\d+\s+0\.\d+\s+255\s+255\s+255\s+255\s+4\s*')
full_screen_coords = ' -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4\n'

print("Fixing all items use coordinates...")
for root, _, files in os.walk(persist_use_dir):
    for filename in files:
        if filename.endswith('.cfg'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                content = f.read()

            if coord_pattern.search(content):
                new_content = coord_pattern.sub(full_screen_coords, content)
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Fixed coordinates in {filename}")

print("Done.")
