import os
import re

persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist'
db_files = {
    'weapon_db.cfg': '_reset_weap_indicators',
    'explosive_db.cfg': '_reset_explosive_indicators',
    'secondary_db.cfg': '_reset_sec_indicators',
    'melee_db.cfg': '_reset_melee_indicators'
}

for cfg_file, reset_alias in db_files.items():
    filepath = os.path.join(persist_dir, cfg_file)
    if not os.path.exists(filepath):
        # We might need to check if filename was correct
        if cfg_file == 'secondary_db.cfg':
            if not os.path.exists(filepath):
                cfg_file = 'sec_db.cfg'
                filepath = os.path.join(persist_dir, cfg_file)
        if not os.path.exists(filepath):
            print(f"File not found: {cfg_file}")
            continue
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # First pass: gather original pointers
    original_pointers = {}
    for line in lines:
        if line.startswith('alias _show_equip_'):
            parts = line.split('"')
            if len(parts) >= 2:
                alias_def = line.split()[1] # e.g. _show_equip_ak47
                val = parts[1]
                if val != "_null": # Only capture actual executing strings
                    original_pointers[alias_def] = val

    # Second pass: rebuild file
    new_lines = []
    pointers_reset_cmds = []
    
    for line in lines:
        if line.startswith('alias _show_equip_'):
            # Convert to null definition
            alias_name = line.split()[1]
            if alias_name in original_pointers: # Only add to reset list if we know about it
                pointers_reset_cmds.append(f"alias {alias_name} _null")
                new_lines.append(f"alias {alias_name} _null\n")
            else:
                 new_lines.append(line)
        elif line.startswith(f"alias {reset_alias}"):
            # Inject pointer reset call
            reset_pointers_alias = f"{reset_alias}_pointers"
            
            if reset_pointers_alias not in line:
                cmd_part = line.split('"', 1)[1]
                if '{reset_pointers_alias}' in line:
                     new_lines.append(line)
                else:
                     new_lines.append(f'alias {reset_alias} "{reset_pointers_alias}; {cmd_part}')
            else:
                new_lines.append(line)
        elif line.startswith('alias _db_'):
            # It's a full persistence alias, e.g. alias _db_ak47_full "_reset_...; _weap_p1..."
            # We want to inject `alias _show_equip_ak47 "exec ..."; _show_equip_ak47`
            
            # Extract item name from _db_ITEM_full
            parts = line.split()
            alias_name = parts[1]
            if '_full' in alias_name:
                item_name = alias_name.replace('alias ', '').replace('_db_', '').replace('_full', '')
                show_equip = f"_show_equip_{item_name}"
                
                if show_equip in original_pointers:
                    # Inject it
                    if show_equip not in line:
                        cmd_part = line.split('"', 1)[1]
                        inject_str = f'alias {show_equip} \\"{original_pointers[show_equip]}\\"; {show_equip}; '
                        # Add right after the reset alias
                        new_cmd = cmd_part.replace(f'{reset_alias}; ', f'{reset_alias}; {inject_str}')
                        if new_cmd == cmd_part: # If reset alias isn't exactly like that
                             new_cmd = inject_str + cmd_part
                        new_lines.append(f'alias {alias_name} "{new_cmd}')
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            else:
                 new_lines.append(line)
        else:
            new_lines.append(line)
            
    # Add the reset pointer definition at the top or after reset_alias
    if pointers_reset_cmds:
        reset_pointers_alias = f"{reset_alias}_pointers"
        reset_cmd = f"alias {reset_pointers_alias} \"{'; '.join(pointers_reset_cmds)}\"\n"
        
        # Insert it after the reset alias
        inserted = False
        for i, line in enumerate(new_lines):
            if line.startswith(f"alias {reset_alias}"):
                # Check if it's already there
                if not any(reset_pointers_alias in l for l in new_lines[i-2:i+2] if l.startswith('alias ' + reset_pointers_alias)):
                    new_lines.insert(i + 1, reset_cmd)
                inserted = True
                break
        if not inserted:
             new_lines.append(reset_cmd)
                
    with open(filepath, 'w') as f:
        f.write("".join(new_lines))
    print(f"Fixed pointers in {cfg_file}")
