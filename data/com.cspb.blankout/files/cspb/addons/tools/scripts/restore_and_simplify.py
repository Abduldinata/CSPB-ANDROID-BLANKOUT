import os
import re

# Paths
char_db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'
weapon_db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\weapon_db.cfg'
char_persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\character'
char_detail_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character'

# 1. Simplify char_db.cfg
with open(char_db_path, 'r') as f:
    char_db = f.readlines()

new_char_db = []
skip = False
for line in char_db:
    if '// Team Specific Resets' in line:
        skip = True
        continue
    if skip and 'alias _reset_char_indicators_' in line:
        continue
    if skip and line.strip() == '':
        skip = False
        continue
    
    # Revert alias _db_char_...
    match = re.search(r'alias _db_char_(.*?) "(.*?)"', line)
    if match:
        name = match.group(1)
        original_cmd = match.group(2)
        # simplify: use global reset, remove extra pointers if logic says so
        # user said: "yg tersimpan hanya use dan equip kalau di char inventory"
        # and "logika 2 sekaligus membuat pusing"
        
        # We need to extract the badge_type (p1/p2) and the badge_cfg
        is_p1 = '_char_p1_badge' in line
        badge_ptr = '_char_p1_badge' if is_p1 else '_char_p2_badge'
        
        # Extract badge cfg path
        cfg_match = re.search(badge_ptr + r' \\"(.*?)\\"', line)
        cfg_path = cfg_match.group(1) if cfg_match else "ERROR"
        
        # Extract lobby
        lobby_match = re.search(r'alias _back_to_lobby (.*?);', line)
        lobby = lobby_match.group(1) if lobby_match else "_lobby_3b_redbull" # fallback
        
        # Extract folder for theme
        theme_match = re.search(r'exec addons/neda/(.*?)/inventory_character\.cfg', line)
        theme_folder = theme_match.group(1) if theme_match else "redteam/redbull"
        
        # New simplified command
        cmd = (f'_reset_char_indicators; _reset_char_equip_status_pointers; '
               f'alias {badge_ptr} \\"{cfg_path}\\"; '
               f'alias _active_char_theme _db_char_{name}; '
               f'alias _back_to_lobby {lobby}; '
               f'exec addons/neda/{theme_folder}/inventory_character.cfg; '
               f'{badge_ptr}')
        
        line = f'alias _db_char_{name} "{cmd}"\n'
    
    new_char_db.append(line)

with open(char_db_path, 'w') as f:
    f.write("".join(new_char_db).replace('_reset_char_indicators_p1', '_reset_char_indicators').replace('_reset_char_indicators_p2', '_reset_char_indicators'))


# 2. Simplify weapon_db.cfg (Remove _show_equip_... persistence)
with open(weapon_db_path, 'r') as f:
    weapon_db = f.readlines()

new_weapon_db = []
for line in weapon_db:
    if 'alias _db_' in line and '_full "' in line:
        # Remove _show_equip_...; part
        line = re.sub(r'alias _show_equip_weap_.*?; ', '', line)
    new_weapon_db.append(line)

with open(weapon_db_path, 'w') as f:
    f.write("".join(new_weapon_db))


# 3. Restore use*.cfg coordinates
for i in range(1, 10):
    for suffix in ['', '_p2']:
        filepath = os.path.join(char_persist_dir, f'use{i}{suffix}.cfg')
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                content = f.read()
            # Replace coordinate with full-screen
            content = re.sub(r'[0-9.]+ [0-9.]+ [0-9.]+ [0-9.]+ 255 255 255 255 4', 
                            r'-0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4', content)
            with open(filepath, 'w') as f:
                f.write(content)

print("Simplified logic and restored badge coordinates.")
