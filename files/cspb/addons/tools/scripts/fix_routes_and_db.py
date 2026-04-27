import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
teams = ["blueteam", "redteam"]

# 1. FIX char_db.cfg Corruption
char_db_path = os.path.join(base_path, "persist", "char_db.cfg")
lines = [
    "// --- CHARACTER THEME & PERSISTENCE DATABASE (REFINED) ---",
    "",
    "// --- BADGE RESET ---",
    'alias _reset_char_badges "touch_removebutton _c_badge_p1_s1; touch_removebutton _c_badge_p1_s2; touch_removebutton _c_badge_p1_s3; touch_removebutton _c_badge_p1_s4; touch_removebutton _c_badge_p1_s5; touch_removebutton _c_badge_p1_s6; touch_removebutton _c_badge_p1_s7; touch_removebutton _c_badge_p1_s8; touch_removebutton _c_badge_p1_s9; touch_removebutton _c_badge_p2_s1; touch_removebutton _c_badge_p2_s2; touch_removebutton _c_badge_p2_s3; touch_removebutton _c_badge_p2_s4; touch_removebutton _c_badge_p2_s5; touch_removebutton _c_badge_p2_s6; touch_removebutton _c_badge_p2_s7; touch_removebutton _c_badge_p2_s8; touch_removebutton _c_badge_p2_s9"',
    'alias _reset_char_indicators "_reset_char_badges; touch_removebutton _char_equip_status_badge; touch_removebutton _persist_char_equip_badge; _rmv_chr_detail; alias _char_p1_badge _null; alias _char_p2_badge _null; alias _char_equip_badge _null; alias _active_char_detail _null; alias _active_char_inventory _null; alias _active_char_selection _null; _reset_char_equip_status_pointers"',
    "",
    'alias _reset_char_equip_status_pointers "alias _show_equip_char_acidpool _null; alias _show_equip_char_redbull _null; alias _show_equip_char_tarantula _null; alias _show_equip_char_keeneyes _null; alias _show_equip_char_dfox _null; alias _show_equip_char_leopard _null; alias _show_equip_char_viperred _null; alias _show_equip_char_hide _null; alias _show_equip_char_ricalopez _null; alias _show_equip_char_judychou _null; alias _show_equip_char_natasha _null; alias _show_equip_char_queen _null"',
    "",
    "// --- CHARACTER ENTRIES ---",
    "// NOTE: Each entry now executes a separate config file to avoid 'alias too long' limit.",
    "",
]

char_names = ["redbull", "acidpool", "tarantula", "keeneyes", "dfox", "leopard", "viper", "hide", "ricalopez", "judychou", "queen", "natasha"]
for char in char_names:
    lines.append(f'alias _db_char_{char} "exec addons/neda/persist/character/db_{char}.cfg"')

with open(char_db_path, "w") as f:
    f.write("\n".join(lines))

# 2. FIX inventory_weapon*.cfg Routes
for team in teams:
    team_p = os.path.join(base_path, team)
    if not os.path.exists(team_p): continue
    for char_n in os.listdir(team_p):
        char_p = os.path.join(team_p, char_n)
        if not os.path.isdir(char_p): continue
        
        for root, dirs, files in os.walk(char_p):
            for file in files:
                if file.startswith("inventory_weapon") and file.endswith(".cfg"):
                    fpath = os.path.join(root, file)
                    with open(fpath, "r") as f:
                        content = f.read()
                    
                    new_content = content
                    # Change /weapons/ to /main/
                    new_content = re.sub(r'/weapons/', r'/main/', new_content)
                    new_content = re.sub(r'/weapons2/', r'/main2/', new_content)
                    
                    if new_content != content:
                        with open(fpath, "w") as f:
                            f.write(new_content)
                        print(f"Fixed routes in {fpath}")

print("Fix complete.")
