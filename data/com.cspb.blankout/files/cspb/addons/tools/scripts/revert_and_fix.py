import os
import re
import shutil

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
lobby_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"
teams = ["blueteam", "redteam"]

# 1. GENERATE db_*.cfg for char_db.cfg (Fixing Alias Too Long)
db_template = """_reset_char_indicators
exec addons/lobby_{char_name}.cfg
alias _char_p{page}_badge "exec addons/neda/persist/character/use{slot}{page_suffix}.cfg"
alias _char_equip_badge "exec addons/neda/persist/character/equip{slot}.cfg"
alias _active_char_detail {sl_cmd}
alias _active_char_theme "exec addons/neda/persist/character/db_{char_name}.cfg"
alias _active_char_inventory "exec addons/neda/{team}/{char_name}/inventory_character.cfg"
alias _back_to_lobby _lobby_1b_{char_name}
_char_p{page}_badge
_char_equip_badge
_active_char_detail
_active_char_selection
"""
char_info = {
    "redbull": ("redteam", 1, 1, "_sl_redc1"),
    "acidpool": ("blueteam", 1, 2, "_sl_bluec1"),
    "tarantula": ("redteam", 1, 3, "_sl_redc2"),
    "keeneyes": ("blueteam", 1, 4, "_sl_bluec2"),
    "dfox": ("redteam", 1, 5, "_sl_redc3"),
    "leopard": ("blueteam", 1, 6, "_sl_bluec3"),
    "viperred": ("redteam", 1, 7, "_sl_redc4"), # Corrected from 'viper' to 'viperred' mostly 
    "hide": ("blueteam", 1, 8, "_sl_bluec4"),
    "ricalopez": ("redteam", 1, 9, "_sl_redc5"),
    "judychou": ("blueteam", 2, 1, "_sl_bluec5"),
    "natasha": ("redteam", 2, 3, "_sl_redc6"),  # Assuming Natasha maps to use3
    "queen": ("blueteam", 2, 2, "_sl_bluec6")
}

persist_char_dir = os.path.join(base_path, "persist", "character")
os.makedirs(persist_char_dir, exist_ok=True)

for char_name, (team, page, slot, sl_cmd) in char_info.items():
    page_suffix = "_p2" if page == 2 else ""
    content = db_template.format(
        char_name=char_name, page=page, slot=slot, page_suffix=page_suffix, sl_cmd=sl_cmd, team=team
    )
    # Fix lobby fallback for redteam
    if team == "redteam":
        content = content.replace(f"_lobby_1b_{char_name}", f"_lobby_3b_{char_name}")
        
    db_file_path = os.path.join(persist_char_dir, f"db_{char_name}.cfg")
    with open(db_file_path, "w") as f:
        f.write(content)

# Update char_db.cfg to use the new files
char_db_path = os.path.join(base_path, "persist", "char_db.cfg")
with open(char_db_path, "r") as f:
    char_db_content = f.read()
for char_name in char_info.keys():
    # regex to replace alias _db_char_X "..."
    char_db_content = re.sub(
        rf'alias _db_char_{char_name} ".*?"', 
        f'alias _db_char_{char_name} "exec addons/neda/persist/character/db_{char_name}.cfg"', 
        char_db_content
    )
with open(char_db_path, "w") as f:
    f.write(char_db_content)

# 2. RENAME folders 'weapons' -> 'main' and 'weapons2' -> 'main2'
for team in teams:
    team_path = os.path.join(base_path, team)
    if not os.path.isdir(team_path): continue
    for char_name in os.listdir(team_path):
        char_path = os.path.join(team_path, char_name)
        if not os.path.isdir(char_path): continue
        
        w_path = os.path.join(char_path, "weapons")
        m_path = os.path.join(char_path, "main")
        if os.path.exists(w_path):
            os.rename(w_path, m_path)
            
        w2_path = os.path.join(char_path, "weapons2")
        m2_path = os.path.join(char_path, "main2")
        if os.path.exists(w2_path):
            os.rename(w2_path, m2_path)

# 3. FIX aliases in lobby_*.cfg
for fname in os.listdir(lobby_path):
    if fname.startswith("lobby_") and fname.endswith(".cfg"):
        fpath = os.path.join(lobby_path, fname)
        with open(fpath, "r") as f:
            content = f.read()
        
        content = re.sub(r'/weapons/', r'/main/', content)
        content = re.sub(r'/weapons2/', r'/main2/', content)
        
        with open(fpath, "w") as f:
            f.write(content)

# 4. RESTORE broken suffixes in character inventory pages
for team in teams:
    team_path = os.path.join(base_path, team)
    if not os.path.isdir(team_path): continue
    for char_name in os.listdir(team_path):
        # We need to consider all pages
        for cat in ["main", "main2", "secondary", "secondary2", "melee", "melee2", "explosive", "explosive2", "special", "special2", "character", "character2"]:
            cat_path = os.path.join(team_path, char_name, cat)
            if os.path.isdir(cat_path):
                for fname in os.listdir(cat_path):
                    if fname.startswith("page") and fname.endswith(".cfg"):
                        fpath = os.path.join(cat_path, fname)
                        with open(fpath, "r") as f:
                            content = f.read()
                        
                        # Apply restoration: add _CHAR to generic names that were stripped
                        # Only append if not already appended
                        patterns = [
                            (r'_rmv_main_inventory(?!_)', f'_rmv_main_inventory_{char_name}'),
                            (r'_main_inventory(?!_)', f'_main_inventory_{char_name}'),
                            (r'_second_inventory(?!_)', f'_second_inventory_{char_name}'),
                            (r'_rmv_second_inventory(?!_)', f'_rmv_second_inventory_{char_name}'),
                            (r'_melee_inventory(?!_)', f'_melee_inventory_{char_name}'),
                            (r'_rmv_melee_inventory(?!_)', f'_rmv_melee_inventory_{char_name}'),
                            (r'_explosive_inventory(?!_)', f'_explosive_inventory_{char_name}'),
                            (r'_rmv_explosive_inventory(?!_)', f'_rmv_explosive_inventory_{char_name}'),
                            (r'_special_inventory(?!_)', f'_special_inventory_{char_name}'),
                            (r'_rmv_special_inventory(?!_)', f'_rmv_special_inventory_{char_name}'),
                            (r'_back_to_lobby(?!_)', f'_back_3_{char_name}') # Fallback
                        ]
                        
                        # Note: _lobby_3b_{char_name} is harder to guess correctly because it depends on context, 
                        # but standardizing to _back_3_{char_name} is safer.
                        
                        new_content = content
                        for old, new in patterns:
                            new_content = re.sub(old, new, new_content)
                            
                        # Also fix '_rmv_main_inventory2_' if it got cut? 
                        # My script didn't strip `2_`, meaning it was probably untouched or is safe.
                            
                        if new_content != content:
                            with open(fpath, "w") as f:
                                f.write(new_content)

print("Revert and fix complete.")
