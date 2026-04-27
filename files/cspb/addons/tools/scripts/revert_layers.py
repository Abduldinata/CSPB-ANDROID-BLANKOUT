import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'

def revert_layers():
    count = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.cfg') or file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Replace Layer 5 with Layer 4
                # Target: 255 255 255 255  4  -> 255 255 255 255 4
                # Also handle potentially different spaces (like 255  5)
                # re.sub(r'(255\s+)5(\s*)$', r'\1 4\2', content, flags=re.MULTILINE)
                
                # Match "255 5" at end of line or before whitespace/newline
                # The grep showed many instances of "255 255 255 255 5"
                new_content = re.sub(r'(\s+255\s+)5(\s*)$', r'\1 4\2', content, flags=re.MULTILINE)
                new_content = re.sub(r'(\s+255\s+)5(\s+)', r'\1 4\2', new_content)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Reverted Layer 5 in: {file}")
                    count += 1
    print(f"Total files reverted: {count}")

revert_layers()
