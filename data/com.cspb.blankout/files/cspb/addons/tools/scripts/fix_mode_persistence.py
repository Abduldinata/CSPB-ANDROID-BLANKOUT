import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"

# 1. Fix mode/*.cfg
mode_folder = os.path.join(base_path, "mode")
fixed_modes = 0

if os.path.isdir(mode_folder):
    for fname in os.listdir(mode_folder):
        if not fname.endswith(".cfg"):
            continue
        fpath = os.path.join(mode_folder, fname)
        with open(fpath, "r") as f:
            content = f.read()

        # Fix the misspelled reset alias
        new_content = content.replace("_reset_mode_p1_indicator", "_reset_mode_indicator")
        if new_content != content:
            with open(fpath, "w") as f:
                f.write(new_content)
            print(f"[Mode] Fixed typo in {fname}")
            fixed_modes += 1

print(f"\nFixed {fixed_modes} mode config files.\n")

# 2. Fix team/team_*_class*.cfg
team_folder = os.path.join(base_path, "team")
fixed_teams = 0

if os.path.isdir(team_folder):
    for fname in os.listdir(team_folder):
        if not (fname.startswith("team_") and fname.endswith(".cfg") and "class" in fname):
            continue
        fpath = os.path.join(team_folder, fname)
        with open(fpath, "r") as f:
            content = f.read()

        # In team_*_class*.cfg, the mode buttons look like:
        # touch_addbutton "_mode_tdm" "" "_tap_cnd_switch; rmv_all_stat; _rmv_mode_all; _rmv_cmode_all; _db_mode_tdm; _sl_mode_tdm; _mode_tdm"
        # We need to replace: _db_mode_tdm;
        # with: _reset_mode_indicator; alias _mode_p1_indicator _db_mode_tdm; _mode_p1_indicator;

        def replace_mode_logic(m):
            mode_name = m.group(1) # e.g. tdm, bm, sniper
            return f"_rmv_cmode_all; _reset_mode_indicator; alias _mode_p1_indicator _db_mode_{mode_name}; _mode_p1_indicator;"

        # Regex matching _rmv_cmode_all; _db_mode_XYZ;
        pattern = r"_rmv_cmode_all;\s*_db_mode_(\w+);"
        new_content = re.sub(pattern, replace_mode_logic, content)

        if new_content != content:
            with open(fpath, "w") as f:
                f.write(new_content)
            print(f"[Team] Fixed mode persistence logic in {fname}")
            fixed_teams += 1

print(f"\nFixed {fixed_teams} team class lobby configs.\n")

