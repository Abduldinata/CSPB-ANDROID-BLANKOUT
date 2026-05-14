import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\team"
files = [
    "team_blue_class1.cfg", "team_blue_class2.cfg", "team_blue_class3.cfg",
    "team_blue_class4.cfg", "team_blue_class5.cfg", "team_red_class1.cfg",
    "team_red_class2.cfg", "team_red_class3.cfg", "team_red_class4.cfg",
    "team_red_class5.cfg"
]

def update_lobby_exit_triggers(fpath):
    with open(fpath, "r") as f:
        content = f.read()

    modified = False
    
    # 1. Update _lobby_out5 (Exit)
    # Match: touch_addbutton "_lobby_out5" "" "COMMMANDS"
    out_pattern = r'(touch_addbutton\s+"_lobby_out5"\s+""\s+")([^"]+)"'
    def replace_out(m):
        prefix = m.group(1)
        cmds = m.group(2)
        if "_rmv_persist_all" not in cmds:
            # Add _rmv_persist_all after rmv_all_stat if present, else at the beginning
            if "rmv_all_stat;" in cmds:
                new_cmds = cmds.replace("rmv_all_stat;", "rmv_all_stat; _rmv_persist_all;")
            else:
                new_cmds = "_rmv_persist_all; " + cmds
            return f'{prefix}{new_cmds}"'
        return m.group(0)

    new_content = re.sub(out_pattern, replace_out, content)
    if new_content != content:
        modified = True
        content = new_content

    # 2. Update _lobby_back3 (Back)
    back_pattern = r'(touch_addbutton\s+"_lobby_back3"\s+""\s+")([^"]+)"'
    def replace_back(m):
        prefix = m.group(1)
        cmds = m.group(2)
        if "_rmv_persist_all" not in cmds:
            if "rmv_all_stat;" in cmds:
                new_cmds = cmds.replace("rmv_all_stat;", "rmv_all_stat; _rmv_persist_all;")
            else:
                new_cmds = "_rmv_persist_all; " + cmds
            return f'{prefix}{new_cmds}"'
        return m.group(0)

    new_content = re.sub(back_pattern, replace_back, content)
    if new_content != content:
        modified = True
        content = new_content

    if modified:
        with open(fpath, "w") as f:
            f.write(content)
        return True
    return False

for fname in files:
    fpath = os.path.join(base_path, fname)
    if os.path.isfile(fpath):
        if update_lobby_exit_triggers(fpath):
            print(f"Updated exit triggers in {fname}")
        else:
            print(f"No changes needed for {fname}")
    else:
        print(f"File not found: {fname}")
