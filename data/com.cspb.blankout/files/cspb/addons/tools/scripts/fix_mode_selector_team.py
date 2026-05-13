import os
import re

def fix_team_class_files():
    team_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"
    files = [
        "team_blue_class1.cfg", "team_blue_class2.cfg", "team_blue_class3.cfg", 
        "team_blue_class4.cfg", "team_blue_class5.cfg",
        "team_red_class1.cfg", "team_red_class2.cfg", "team_red_class3.cfg", 
        "team_red_class4.cfg", "team_red_class5.cfg"
    ]
    
    for filename in files:
        filepath = os.path.join(team_dir, filename)
        if not os.path.exists(filepath):
            print(f"File not found: {filename}")
            continue
            
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
        
        # OLD: touch_addbutton "_mode_tdm" "" "_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _reset_add_indicators; alias _add_indicators _db_mode_tdm; _sl_mode_tdm; _mode_tdm" ...
        # NEW: touch_addbutton "_mode_tdm" "" "_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _db_mode_tdm; _sl_mode_tdm; _mode_tdm" ...
        
        # Replace TDM mode button
        content = re.sub(
            r'touch_addbutton "_mode_tdm" "" "_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _reset_add_indicators; alias _add_indicators _db_mode_tdm;',
            'touch_addbutton "_mode_tdm" "" "_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _db_mode_tdm;',
            content
        )
        
        # Replace BM mode button
        content = re.sub(
            r'touch_addbutton "_mode_bm" "" "_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _reset_add_indicators; alias _add_indicators _db_mode_bm;',
            'touch_addbutton "_mode_bm" "" "_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _db_mode_bm;',
            content
        )
        
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fixed: {filename}")

if __name__ == "__main__":
    fix_team_class_files()
