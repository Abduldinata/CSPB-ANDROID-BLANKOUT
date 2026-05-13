import os
import re

db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'

with open(db_path, 'r') as f:
    content = f.read()

# 1. Update Reset Logic
new_resets = """// --- BADGE RESET ---
alias _reset_char_indicators "touch_removebutton _c_badge_*; touch_removebutton _char_equip_status_badge; alias _char_p1_badge _null; alias _char_p2_badge _null; _reset_char_equip_status_pointers"

// Team Specific Resets (Parallel Sync)
alias _reset_char_indicators_p1 "touch_removebutton _c_badge_p1_*; touch_removebutton _char_equip_status_badge; alias _char_p1_badge _null"
alias _reset_char_indicators_p2 "touch_removebutton _c_badge_p2_*; touch_removebutton _char_equip_status_badge; alias _char_p2_badge _null"
"""

content = re.sub(r'// --- BADGE RESET ---\nalias _reset_char_indicators .*?\n', new_resets, content)

# 2. Update character aliases to use specific resets
# P1 (Red) characters
p1_chars = ['redbull', 'tarantula', 'dfox', 'viper', 'ricalopez', 'natasha']
# P2 (Blue) characters
p2_chars = ['acidpool', 'keeneyes', 'leopard', 'hide', 'judychou', 'queen']

for char in p1_chars:
    pattern = f'alias _db_char_{char} "_reset_char_indicators;'
    replace = f'alias _db_char_{char} "_reset_char_indicators_p1; _reset_char_equip_status_pointers;'
    content = content.replace(pattern, replace)

for char in p2_chars:
    pattern = f'alias _db_char_{char} "_reset_char_indicators;'
    replace = f'alias _db_char_{char} "_reset_char_indicators_p2; _reset_char_equip_status_pointers;'
    content = content.replace(pattern, replace)

with open(db_path, 'w') as f:
    f.write(content)

print("char_db.cfg synchronized for team-specific resets.")
