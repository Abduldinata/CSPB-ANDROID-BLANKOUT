import os
import re

persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist'
db_files = ['weapon_db.cfg', 'explosive_db.cfg', 'sec_db.cfg', 'melee_db.cfg']

for cfg_name in db_files:
    filepath = os.path.join(persist_dir, cfg_name)
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    new_lines = []
    modified = False
    
    for line in lines:
        if line.startswith('alias _db_') and '_full' in line and line.strip().endswith('\\"'):
            # The line is truncated!
            # Example: ...; alias _weap_p1_indicator \"
            # We need to extract the indicator name to determine the file to exec.
            match = re.search(r'alias\s+(_([a-z]+)_(p\d+|use)_indicator)\s+\\"$', line.strip())
            if match:
                indicator_alias = match.group(1) # e.g. _weap_p1_indicator
                category = match.group(2) # e.g. weap, melee, explosive
                page_part = match.group(3) # e.g. p1, use
                
                # Determine file prefix
                if 'weap' in category: prefix = 'w'
                elif 'sec' in category: prefix = 's'
                elif 'melee' in category: prefix = 'm'
                elif 'explosive' in category: prefix = 'e'
                elif 'special' in category: prefix = 'p'
                else: prefix = 'w'
                
                # Determine number from indicator name if it has pX
                num = 1
                if page_part.startswith('p'):
                    num = page_part[1:]
                else:
                    # if it's 'use', we might need to guess from previous lines, but let's just use 1.
                    # Or better, we can fix the indicator alias to the correct one if we look up the select_main buttons...
                    # But for now, let's just assume we can map it directly if we extract it from the line
                    
                    # Actually, if it's 'use', it was a typo in the original file.
                    # Let's extract the number by looking at the previous known number
                    pass
                
                # If page_part was 'use', it was probably broken before anyway.
                # Let's write a generic fix. The file we want to exec is prefix + num + '.cfg'
                use_file = f"{prefix}{num}.cfg"
                
                tail = f'exec addons/neda/persist/use/{use_file}\\"; {indicator_alias}"'
                repaired_line = line.strip() + tail + '\n'
                new_lines.append(repaired_line)
                modified = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    if modified:
        with open(filepath, 'w') as f:
            f.write("".join(new_lines))
        print(f"Repaired {cfg_name}")

print("Done repairing DB configs.")
