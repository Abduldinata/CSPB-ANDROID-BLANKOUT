import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

def remove_duplicate_indicators():
    processed = 0
    
    # Patterns for all indicator types
    patterns = [
        r'_weap_p\d+_indicator',
        r'_sec_p\d+_indicator',
        r'_melee_p\d+_indicator',
        r'_exp_p\d+_indicator',
        r'_spc_p\d+_indicator',
        r'_chr_p\d+_indicator',
        r'_map_p\d+_indicator',
        r'_mode_indicator'
    ]
    
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg"):
                path = os.path.join(root, f)
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()
                
                original = lines.copy()
                seen_indicators = set()
                new_lines = []
                
                for line in lines:
                    # Check if line is an indicator call
                    is_duplicate = False
                    for pattern in patterns:
                        if re.match(f'^{pattern}\\s*$', line.strip()):
                            if line.strip() in seen_indicators:
                                is_duplicate = True
                                break
                            else:
                                seen_indicators.add(line.strip())
                    
                    if not is_duplicate:
                        new_lines.append(line)
                
                if new_lines != original:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.writelines(new_lines)
                    processed += 1
    
    return processed

count = remove_duplicate_indicators()
print(f"Removed duplicate indicators from {count} files.")
