import os
import re

# Paths
char_db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'
weapon_db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\weapon_db.cfg'

# 1. Weapon Logic Cleanup (No persistence for button status)
with open(weapon_db_path, 'r') as f:
    weapon_db = f.readlines()

new_weapon_db = []
for line in weapon_db:
    if 'alias _db_' in line and '_full "' in line:
        # Reconstruct to only save badge
        # Original: alias _db_ak47_full "_reset_weap_indicators; alias _weap_p1_indicator \"exec addons/neda/persist/use/w6.cfg\"; _weap_p1_indicator; alias _show_equip_ak47 _safe_exec_equip; _show_equip_ak47"
        # New: alias _db_ak47_full "_reset_weap_indicators; alias _weap_p1_indicator \"exec addons/neda/persist/use/w6.cfg\"; _weap_p1_indicator"
        match = re.search(r'(alias _db_.*?_full "_reset_weap_indicators; alias _weap_p[0-9]+_indicator \\"exec addons/neda/persist/use/w[0-9]+.cfg\\"; _weap_p[0-9]+_indicator)', line)
        if match:
            line = match.group(1) + '"\n'
    new_weapon_db.append(line)

with open(weapon_db_path, 'w') as f:
    f.write("".join(new_weapon_db))


# 2. Character Logic Cleanup (Only use + equip badges)
char_entries = [
    ('redbull', '1', 'redteam/redbull', '_lobby_3b_redbull', 'p1'),
    ('acidpool', '2', 'blueteam/acidpool', '_lobby_1b_acidpool', 'p2'),
    ('tarantula', '3', 'redteam/tarantula', '_lobby_3b_tarantula', 'p1'),
    ('keeneyes', '4', 'blueteam/keeneyes', '_lobby_1b_keeneyes', 'p2'),
    ('dfox', '5', 'redteam/dfox', '_lobby_3b_dfox', 'p1'),
    ('leopard', '6', 'blueteam/leopard', '_lobby_1b_leopard', 'p2'),
    ('viper', '7', 'redteam/viper', '_lobby_3b_viper', 'p1'),
    ('hide', '8', 'blueteam/hide', '_lobby_1b_hide', 'p2'),
    ('ricalopez', '9', 'redteam/ricalopez', '_lobby_3b_ricalopez', 'p1'),
    ('judychou', '1_p2', 'blueteam/judychou', '_lobby_1b_judychou', 'p2'),
    ('queen', '2_p2', 'blueteam/acidpool', '_lobby_1b_acidpool', 'p2'),
    ('natasha', '3', 'redteam/redbull', '_lobby_3b_redbull', 'p1')
]

content = [
    '// --- CHARACTER THEME & PERSISTENCE DATABASE (SIMPLIFIED) ---',
    '',
    '// --- BADGE RESET ---',
    'alias _reset_char_indicators "touch_removebutton _c_badge_*; touch_removebutton _char_equip_status_badge; touch_removebutton _persist_char_equip_badge; alias _char_p1_badge _null; alias _char_p2_badge _null; alias _char_equip_badge _null; _reset_char_equip_status_pointers"',
    '',
    'alias _reset_char_equip_status_pointers "alias _show_equip_char_acidpool _null; alias _show_equip_char_redbull _null; alias _show_equip_char_tarantula _null; alias _show_equip_char_keeneyes _null; alias _show_equip_char_dfox _null; alias _show_equip_char_leopard _null; alias _show_equip_char_viperred _null; alias _show_equip_char_hide _null; alias _show_equip_char_ricalopez _null; alias _show_equip_char_judychou _null; alias _show_equip_char_natasha _null; alias _show_equip_char_queen _null"',
    '',
    '// --- EQUIP BUTTON REFRESH ---',
    'alias _show_char_change_btn "exec addons/neda/select_character/show_change.cfg"',
    '',
    '// --- CHARACTER ENTRIES ---',
    ''
]

for name, slot, theme, lobby, team in char_entries:
    badge_ptr = f'_char_{team}_badge'
    # Use slot number for equip badge
    equip_num = slot.split('_')[0]
    entry = (f'alias _db_char_{name} "_reset_char_indicators; '
             f'alias {badge_ptr} \\"exec addons/neda/persist/character/use{slot}.cfg\\"; '
             f'alias _char_equip_badge \\"exec addons/neda/persist/character/equip{equip_num}.cfg\\"; '
             f'alias _active_char_theme _db_char_{name}; '
             f'alias _back_to_lobby {lobby}; '
             f'exec addons/neda/{theme}/inventory_character.cfg; '
             f'{badge_ptr}; _char_equip_badge"')
    content.append(f'// {name.upper()}')
    content.append(entry)
    content.append('')

content.append('// Default')
content.append('alias _char_p1_badge _null')
content.append('alias _char_p2_badge _null')
content.append('alias _char_equip_badge _null')

with open(char_db_path, 'w') as f:
    f.write('\n'.join(content))

print("Logic simplified: Weapons only save badge, Chars save use + equip.")
