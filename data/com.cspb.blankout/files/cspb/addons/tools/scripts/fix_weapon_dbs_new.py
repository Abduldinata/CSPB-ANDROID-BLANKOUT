import os

def fix_weapon_db(filepath, reset_name, badge_prefix, equip_badge_id, ind_alias):
    if not os.path.exists(filepath): return
    
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    # 1. Update Reset Alias
    # touch_removebutton _weap_badge_s*; touch_removebutton _weap_equip_status_badge; alias _weap_use_indicator _null
    reset_line = f'alias {reset_name} "touch_removebutton {badge_prefix}*; touch_removebutton {equip_badge_id}; alias {ind_alias} _null"\n'
    
    found_reset = False
    for line in lines:
        if f'alias {reset_name}' in line:
            new_lines.append(reset_line)
            found_reset = True
        elif 'alias _show_equip_' in line:
            # We standardize these to just use the safe_exec alias if they exist
            # alias _show_equip_ak47 "exec addons/neda/persist/weapon/equip.cfg"
            # It's better to keep them as is BUT we can make them dynamic if we want.
            # For now, let's keep them and focus on the FULL alias.
            new_lines.append(line)
        elif '_full' in line and 'alias _db_' in line:
            # alias _db_ak47_full "_reset_weap_indicators; alias _weap_use_indicator \"exec addons/neda/persist/use/use1.cfg\"; _weap_use_indicator; alias _weap_equip_status _show_equip_ak47; _weap_equip_status"
            # We want to change it to use the new IDs
            import re
            match = re.search(r'alias _db_(.*)_full "(.*?)"', line)
            if match:
                name = match.group(1)
                cmd = match.group(2)
                # Clean up existing status pointers from previous bulk update
                cmd = re.sub(r'; alias _weap_equip_status .*?; _weap_equip_status', '', cmd)
                cmd = re.sub(r'; alias _sec_equip_status .*?; _sec_equip_status', '', cmd)
                
                # Re-add with NEW pointers
                new_full = f'alias _db_{name}_full "{cmd}; alias _show_equip_{name} _safe_exec_equip; _show_equip_{name}"\n'
                if 'secondary_db' in filepath:
                    new_full = f'alias _db_{name}_full "{cmd}; alias _show_equip_{name} _safe_exec_equip_sec; _show_equip_{name}"\n'
                new_lines.append(new_full)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
            
    with open(filepath, 'w') as f:
        f.write("".join(new_lines))
    print(f"Fixed {filepath}")

# IDs
fix_weapon_db(r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\weapon_db.cfg',
              '_reset_weap_indicators', '_weap_badge_s', '_weap_equip_status_badge', '_weap_use_indicator')

fix_weapon_db(r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\secondary_db.cfg',
              '_reset_secondary_indicators', '_weap_badge_s', '_weap_equip_status_badge', '_secondary_use_indicator')
