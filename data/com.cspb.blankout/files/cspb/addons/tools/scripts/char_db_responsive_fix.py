import os
import re

db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'

mappings = {
    'redbull': {'folder': 'redteam/redbull', 'lobby': '_lobby_3b_redbull'},
    'tarantula': {'folder': 'redteam/tarantula', 'lobby': '_lobby_3b_tarantula'},
    'dfox': {'folder': 'redteam/dfox', 'lobby': '_lobby_3b_dfox'},
    'viper': {'folder': 'redteam/viper', 'lobby': '_lobby_3b_viper'},
    'ricalopez': {'folder': 'redteam/ricalopez', 'lobby': '_lobby_3b_ricalopez'},
    'natasha': {'folder': 'redteam/redbull', 'lobby': '_lobby_3b_natasha'},
    'acidpool': {'folder': 'blueteam/acidpool', 'lobby': '_lobby_1b_acidpool'},
    'keeneyes': {'folder': 'blueteam/keeneyes', 'lobby': '_lobby_1b_keeneyes'},
    'leopard': {'folder': 'blueteam/leopard', 'lobby': '_lobby_1b_leopard'},
    'hide': {'folder': 'blueteam/hide', 'lobby': '_lobby_1b_hide'},
    'judychou': {'folder': 'blueteam/judychou', 'lobby': '_lobby_1b_judychou'},
    'queen': {'folder': 'blueteam/acidpool', 'lobby': '_lobby_1b_queen'}
}

with open(db_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    match = re.search(r'alias _db_char_(.*?) "(.*?)"', line)
    if match:
        name = match.group(1).lower()
        if name in mappings:
            meta = mappings[name]
            is_red = 'redteam' in meta['folder']
            reset = '_reset_char_indicators_p1' if is_red else '_reset_char_indicators_p2'
            badge_type = '_char_p1_badge' if is_red else '_char_p2_badge'
            
            # Find current slot config
            badge_cfg_match = re.search(r'alias ' + badge_type + r' \\"(.*?)\\"', line)
            badge_cfg = badge_cfg_match.group(1) if badge_cfg_match else "ERROR"
            
            pointer = f'_show_equip_char_{name}'
            if name == 'viper': pointer = '_show_equip_char_viperred'
            
            # Use Fallback lobby if specific one is missing (Natasha/Queen)
            final_lobby = meta['lobby']
            if name == 'natasha': final_lobby = '_lobby_3b_redbull'
            if name == 'queen': final_lobby = '_lobby_1b_acidpool'
            
            cmd = (f'{reset}; _reset_char_equip_status_pointers; '
                   f'alias {badge_type} \\"{badge_cfg}\\"; '
                   f'alias {pointer} _show_char_change_btn; '
                   f'alias _active_char_theme _db_char_{name}; '
                   f'alias _back_to_lobby {final_lobby}; '
                   f'exec addons/neda/{meta["folder"]}/inventory_character.cfg; '
                   f'{badge_type}; {pointer}')
            
            line = f'alias _db_char_{name} "{cmd}"\n'
    new_lines.append(line)

with open(db_path, 'w') as f:
    f.write("".join(new_lines))

print("char_db.cfg updated for responsive team switching.")
