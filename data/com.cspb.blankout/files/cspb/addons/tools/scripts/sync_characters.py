import os

# Base directory
team_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"

# Mapping: filename -> correct character name
identity_map = {
    "team_red_class1.cfg": "redbull",
    "team_red_class2.cfg": "tarantula",
    "team_red_class3.cfg": "dfox",
    "team_red_class4.cfg": "viper",
    "team_red_class5.cfg": "ricalopez",
    "team_blue_class1.cfg": "acidpool",
    "team_blue_class2.cfg": "keeneyes",
    "team_blue_class3.cfg": "leopard",
    "team_blue_class4.cfg": "hide",
    "team_blue_class5.cfg": "judychou"
}

# Extensive list of prefixes that are followed by the character name
prefixes = [
    "_remove_1_", "_remove_2_", "_remove_3_", "_remove_4_",
    "_enter_1_", "_enter_2_", "_enter_3_", "_enter_4_",
    "_back_1_", "_back_2_", "_back_3_", "_back_4_", "_back_5_",
    "_change_team_", "sl_blue_team_", "sl_red_team_",
    "_clan_team_", "_clan_team2_", "_rmv_clan_team_", "_rmv_clan_team2_",
    "_mission_", "_rmv_mission_", "_mission2_", "_rmv_mission2_",
    "_title_", "_rmv_title_", "_title2_", "_rmv_title2_",
    "_rmv_lobby_m3_cmd_", "_rmv_lobby_m4_cmd_", "_rmv_lobby_start_cmd_",
    "_choose_1_", "_credit_1_",
    "_main_inventory_", "_rmv_main_inventory_", "_main_inventory2_", "_rmv_main_inventory2_",
    "_second_inventory_", "_second_inventory2_", "_melee_inventory_", "_melee_inventory2_",
    "_explosive_inventory_", "_explosive_inventory2_", "_special_inventory_", "_special_inventory2_",
    "_char_inventory_", "_char_inventory2_",
    "_add_menu_", "_lobby_3b_", "_lobby_4b_", "_lobby_1b_"
]

# Specifically for page navigation (sometimes they have numerical variants like prevpage1)
page_prefixes = [
    "_wp_prevpage", "_wp_nextpage", "_scd_prevpage", "_scd_nextpage",
    "_ml_prevpage", "_ml_nextpage", "_exp_prevpage", "_spc_prevpage", "_chr_prevpage", "_chr_nextpage"
]

import re

def sync_identities():
    count = 0
    for filename, char in identity_map.items():
        path = os.path.join(team_dir, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            new_line = line
            
            # 1. Fix lobby exec
            new_line = re.sub(r'exec addons/lobby_[a-z0-9_]+\.cfg', f'exec addons/lobby_{char}.cfg', new_line)
            
            # 2. Fix image path
            new_line = re.sub(r'(addons/neda/image/(?:red|blue)/)[a-z0-9_]+(\.tga)', r'\1' + char + r'\3', new_line)
            
            # 3. Fix prefixed commands
            for pref in prefixes:
                # Find occurrences of prefix followed by alphanumeric (but not starting with a space or semicolon)
                new_line = re.sub(re.escape(pref) + r'[a-z0-9_]+', pref + char, new_line)
            
            # 4. Fix page navigation (supports things like _wp_prevpage1_acidpool)
            for p_pref in page_prefixes:
                # Pattern: _wp_prevpage + [any number or string] + _ + [old_char]
                new_line = re.sub(re.escape(p_pref) + r'([0-9a-z]*_)[a-z0-9_]+', p_pref + r'\1' + char, new_line)
                
            new_lines.append(new_line)
            
        with open(path, "w", encoding='utf-8') as f:
            f.writelines(new_lines)
        count += 1
        print(f"Synchronized {filename} to {char}")

    print(f"Total files synchronized: {count}")

sync_identities()
