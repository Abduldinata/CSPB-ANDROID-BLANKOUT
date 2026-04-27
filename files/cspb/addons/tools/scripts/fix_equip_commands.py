import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

def fix_equip_commands():
    processed = 0
    for root, _, files in os.walk(root_dir):
        for f in files:
            if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                path = os.path.join(root, f)
                basename = os.path.splitext(f)[0]
                
                with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                    lines = file.readlines()
                
                new_lines = []
                modified = False
                
                for line in lines:
                    if 'touch_addbutton "equip_' in line:
                        # Extract the command part (between the quotes)
                        match = re.search(r'touch_addbutton "equip_\w+" "" "(.*?)"', line)
                        if match:
                            cmd = match.group(1)
                            
                            # Remove all existing alias _ind_XXX assignments
                            cmd = re.sub(r'alias _ind_\w+ "exec addons/neda/persist/weapon/equip\.cfg";\s*', '', cmd)
                            
                            # Find the category indicator pattern and inject the alias before it
                            # Pattern: _weap_p1_indicator, _sec_p1_indicator, etc.
                            pattern = r'(_(weap|sec|melee|exp|spc)_p\d+_indicator)'
                            if re.search(pattern, cmd):
                                # Inject the alias assignment once, right before the indicator
                                cmd = re.sub(pattern, f'alias _ind_{basename} "exec addons/neda/persist/weapon/equip.cfg"; \\1', cmd)
                            
                            # Rebuild the line
                            line = re.sub(r'touch_addbutton "equip_\w+" "" ".*?"', f'touch_addbutton "equip_{basename}" "" "{cmd}"', line)
                            modified = True
                    
                    new_lines.append(line)
                
                if modified:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.writelines(new_lines)
                    processed += 1
    
    return processed

count = fix_equip_commands()
print(f"Fixed {count} item configuration files.")
