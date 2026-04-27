import os
import re

char_db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'

# Mapping from name to detail alias
detail_map = {
    'redbull': '_sl_redc1',
    'acidpool': '_sl_bluec1',
    'tarantula': '_sl_redc2',
    'keeneyes': '_sl_bluec2',
    'dfox': '_sl_redc3',
    'leopard': '_sl_bluec3',
    'viper': '_sl_redc4',
    'hide': '_sl_bluec4',
    'ricalopez': '_sl_redc5',
    'judychou': '_sl_bluec5',
    'queen': '_sl_bluec6',
    'natasha': '_sl_redc6'
}

with open(char_db_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    # Update Reset
    if 'alias _reset_char_indicators' in line:
        line = 'alias _reset_char_indicators "touch_removebutton _c_badge_*; touch_removebutton _char_equip_status_badge; touch_removebutton _persist_char_equip_badge; _rmv_chr_detail; alias _char_p1_badge _null; alias _char_p2_badge _null; alias _char_equip_badge _null; alias _active_char_detail _null; _reset_char_equip_status_pointers"\n'
    
    # Update Character Entry with Detail Pointer
    # alias _db_char_...
    match = re.search(r'alias _db_char_(\w+)', line)
    if match:
        name = match.group(1).lower()
        detail_alias = detail_map.get(name, '_null')
        # Inject detail alias setting
        line = line.replace('; alias _active_char_theme', f'; alias _active_char_detail {detail_alias}; alias _active_char_theme')
    
    new_lines.append(line)

with open(char_db_path, 'w') as f:
    f.write("".join(new_lines))

print("Updated char_db.cfg with detail pointers and enhanced reset.")
