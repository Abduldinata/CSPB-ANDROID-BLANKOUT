import os
import re

# Character and team folders to process
root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'

old_exec = 'exec addons/ineeda.db'
new_exec = '_load_db'

count = 0
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.lower().endswith('.cfg'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Case-insensitive replacement of the exact string
                new_content = re.sub(re.escape(old_exec), new_exec, content, flags=re.IGNORECASE)
                
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1
                    # Optional: print(f'Optimized: {fp}')
            except:
                pass

print(f'Done! Optimized {count} files by implementing the _load_db guard.')
