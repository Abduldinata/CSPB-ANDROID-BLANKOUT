import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"

chars = {
    "redteam": ["viper", "redbull", "tarantula", "dfox", "ricalopez"],
    "blueteam": ["acidpool", "keeneyes", "leopard", "hide", "judychou"]
}

# -----------------------------------------------------------------
# FIX 1: Remove _add_indicators_char_inv from weapon/secondary/melee/
#         explosive/special page files — this alias calls ALL indicators
#         causing badges to bleed across pages and tabs.
# -----------------------------------------------------------------
inv_categories = ["weapons", "weapons2", "secondary", "secondary2",
                  "melee", "melee2", "explosive", "explosive2",
                  "special", "special2"]

removed_add_inv = 0
for team, char_list in chars.items():
    for char in char_list:
        for cat in inv_categories:
            folder = os.path.join(base_path, team, char, cat)
            if not os.path.isdir(folder):
                continue
            for fname in os.listdir(folder):
                if not fname.endswith(".cfg"):
                    continue
                fpath = os.path.join(folder, fname)
                with open(fpath, "r") as f:
                    content = f.read()
                # Remove the line _add_indicators_char_inv
                new_content = re.sub(r"^\s*_add_indicators_char_inv\s*\n", "", content, flags=re.MULTILINE)
                if new_content != content:
                    with open(fpath, "w") as f:
                        f.write(new_content)
                    print(f"[Fix1] Removed _add_indicators_char_inv: {team}/{char}/{cat}/{fname}")
                    removed_add_inv += 1

print(f"\nFix1 done: {removed_add_inv} files cleaned\n")

# -----------------------------------------------------------------
# FIX 2: Add _active_char_inventory call to all equip_char_btn buttons
#         in select_character/character/page*/  and page2/ files.
#         The button command "_tap_cnd_use; _db_char_X" needs to become
#         "_tap_cnd_use; _db_char_X; _active_char_inventory"
# -----------------------------------------------------------------
select_char_path = os.path.join(base_path, "select_character", "character")
fixed_equip_btn = 0

for page_folder in ["page1", "page2"]:
    folder = os.path.join(select_char_path, page_folder)
    if not os.path.isdir(folder):
        continue
    for fname in os.listdir(folder):
        if not fname.endswith(".cfg"):
            continue
        fpath = os.path.join(folder, fname)
        with open(fpath, "r") as f:
            content = f.read()

        # Match equip_char_btn command ending in _db_char_X" (without _active_char_inventory)
        # Pattern: "_tap_cnd_use; _db_char_SOMETHING" followed by close quote
        # We want to add "; _active_char_inventory" before the closing quote
        def add_inv_call(m):
            cmd = m.group(1)
            if "_active_char_inventory" not in cmd:
                return f'"{cmd}; _active_char_inventory"'
            return m.group(0)

        pattern = r'"(_tap_cnd_use;\s*_db_char_\w+)"'
        new_content = re.sub(pattern, add_inv_call, content)

        if new_content != content:
            with open(fpath, "w") as f:
                f.write(new_content)
            print(f"[Fix2] Added _active_char_inventory to equip btn: {page_folder}/{fname}")
            fixed_equip_btn += 1

print(f"\nFix2 done: {fixed_equip_btn} equip buttons updated\n")
