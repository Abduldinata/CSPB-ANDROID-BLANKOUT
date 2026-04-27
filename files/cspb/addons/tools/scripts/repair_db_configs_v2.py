import os
import re

persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist'
select_main_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_main'

db_files = ['weapon_db.cfg', 'explosive_db.cfg', 'sec_db.cfg', 'melee_db.cfg']

# Build a mapping from alias name (e.g. _db_ak47_full) to the indicator script it should use
alias_to_indicator = {}

for root, _, files in os.walk(select_main_dir):
    for filename in files:
        if filename.endswith('.cfg'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r') as f:
                content = f.read()
                
            match = re.search(r'alias\s+(_[a-z0-9_]+_indicator)\s+(_db_[a-z0-9_]+)', content)
            if match:
                indicator_name = match.group(1) # e.g. _weap_p1_indicator
                db_alias = match.group(2) # e.g. _db_ak47
                
                # We need to map _db_ak47_full to the use file based on the indicator name.
                # e.g. _weap_p1_indicator -> w1.cfg
                # _sec_p2_indicator -> s2.cfg
                
                # Determine prefix
                if 'weap' in indicator_name: prefix = 'w'
                elif 'sec' in indicator_name: prefix = 's'
                elif 'melee' in indicator_name: prefix = 'm'
                elif 'exp' in indicator_name: prefix = 'e'
                elif 'spc' in indicator_name or 'special' in indicator_name: prefix = 'p'
                else: prefix = 'w'
                
                # Determine number
                num_match = re.search(r'p(\d+)', indicator_name)
                num = num_match.group(1) if num_match else '1'
                
                use_file = f"{prefix}{num}.cfg"
                
                alias_to_indicator[db_alias + '_full'] = (indicator_name, use_file)


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
            # It's truncated.
            alias_match = re.match(r'alias\s+(_db_[a-z0-9_]+_full)', line)
            if alias_match:
                db_full_alias = alias_match.group(1)
                
                if db_full_alias in alias_to_indicator:
                    indicator_name, use_file = alias_to_indicator[db_full_alias]
                    
                    # Ensure we don't duplicate alias decls if it's already in the truncated line
                    base_line = line.strip()
                    if base_line.endswith(f'alias {indicator_name} \\"'):
                        tail = f'exec addons/neda/persist/use/{use_file}\\"; {indicator_name}"'
                    else:
                        base_line = base_line[:-2] # Remove the trailing \"
                        tail = f'; alias {indicator_name} \\"exec addons/neda/persist/use/{use_file}\\"; {indicator_name}"'
                        
                    repaired_line = base_line + tail + '\n'
                    new_lines.append(repaired_line)
                    modified = True
                else:
                    print(f"Warning: No mapping found for {db_full_alias}")
                    new_lines.append(line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    if modified:
        with open(filepath, 'w') as f:
            f.write("".join(new_lines))
        print(f"Repaired {cfg_name}")

print("Done repairing DB configs.")
