import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"

count = 0
for f in os.listdir(root_dir):
    if f.startswith("team_") and "class" in f and f.endswith(".cfg"):
        filepath = os.path.join(root_dir, f)
        with open(filepath, 'r') as file_obj:
            content = file_obj.read()
        
        changed = False
        
        # Fix TDM button (if it doesn't have persistence logic)
        old_tdm = '_tap_cnd_switch ; rmv_all_stat; _rmv_mode_all ; _rmv_cmode_all; _sl_mode_tdm; _mode_tdm'
        new_tdm = '_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _reset_mode_indicator; alias _mode_indicator _db_mode_tdm; _mode_indicator; _sl_mode_tdm; _mode_tdm'
        
        if old_tdm in content:
            content = content.replace(old_tdm, new_tdm)
            changed = True
        
        # Fix Bomb button (if it doesn't have persistence logic)
        old_bm = '_tap_cnd_switch ; rmv_all_stat; _rmv_mode_all ; _rmv_cmode_all; _sl_mode_bomb ; _mode_bomb'
        new_bm = '_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _reset_mode_indicator; alias _mode_indicator _db_mode_bm; _mode_indicator; _sl_mode_bomb; _mode_bomb'
        
        if old_bm in content:
            content = content.replace(old_bm, new_bm)
            changed = True
        
        if changed:
            with open(filepath, 'w') as file_obj:
                file_obj.write(content)
            count += 1

print(f"Mode persistence logic added to {count} team selection files.")
