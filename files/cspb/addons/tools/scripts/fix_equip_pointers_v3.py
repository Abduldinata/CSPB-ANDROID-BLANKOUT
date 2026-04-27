import os

persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist'
db_files = {
    'weapon_db.cfg': ('_reset_weap_indicators_pointers', 'exec addons/neda/persist/weapon/equip.cfg'),
    'explosive_db.cfg': ('_reset_explosive_indicators_pointers', 'exec addons/neda/persist/explosive/equip.cfg'),
    'secondary_db.cfg': ('_reset_sec_indicators_pointers', 'exec addons/neda/persist/secondary/equip.cfg'),
    'melee_db.cfg': ('_reset_melee_indicators_pointers', 'exec addons/neda/persist/melee/equip.cfg')
}

for cfg_name, (reset_prefix, equip_cmd) in db_files.items():
    if cfg_name == 'secondary_db.cfg':
        filepath = os.path.join(persist_dir, 'sec_db.cfg')
        if not os.path.exists(filepath):
            filepath = os.path.join(persist_dir, cfg_name)
    else:
        filepath = os.path.join(persist_dir, cfg_name)
        
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        continue
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    
    for line in lines:
        if line.startswith('alias _db_') and '_full' in line:
            # Rebuild the full line logic
            parts = line.split('"')
            if len(parts) >= 2:
                cmd_part = parts[1].strip()
                alias_name = parts[0].split()[1] # _db_ak47_full
                item_name = alias_name.replace('_db_', '').replace('_full', '')
                show_equip_alias = f"_show_equip_{item_name}"
                
                # Check where to inject
                inject_str = f'alias {show_equip_alias} \\"{equip_cmd}\\"; {show_equip_alias}; '
                
                # if already injected by v2 or manually, remove it first
                if show_equip_alias in cmd_part:
                    cmd_part = cmd_part.replace(inject_str, '')
                    
                # Clean up multiple semi-colons
                cmd_part = cmd_part.replace(';;', ';').replace('; ;', ';').strip('; ')
                
                # We inject after the first semi-colon which is usually the _reset alias
                if ';' in cmd_part:
                    sub_parts = cmd_part.split(';', 1)
                    new_cmd = f"{sub_parts[0]}; {inject_str}{sub_parts[1].strip()}"
                else:
                    new_cmd = f"{inject_str}{cmd_part}"
                    
                new_line = f'alias {alias_name} "{new_cmd}"\n'
                new_lines.append(new_line)
            else:
                 new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(filepath, 'w') as f:
        f.write("".join(new_lines))
    print(f"Fixed full db lines in {cfg_name}")
