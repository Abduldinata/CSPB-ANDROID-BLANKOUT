import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
lobby_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"
teams = ["blueteam", "redteam"]

# 1. RENAME Files: inventory_main.cfg -> inventory_weapon.cfg (and the remove_ variations)
for team in teams:
    team_path = os.path.join(base_path, team)
    if not os.path.isdir(team_path): continue
    for char_name in os.listdir(team_path):
        char_path = os.path.join(team_path, char_name)
        if not os.path.isdir(char_path): continue
        
        rename_map = {
            "inventory_main.cfg": "inventory_weapon.cfg",
            "inventory_main2.cfg": "inventory_weapon2.cfg",
            "remove_inventory_main.cfg": "remove_inventory_weapon.cfg",
            "remove_inventory_main2.cfg": "remove_inventory_weapon2.cfg"
        }
        
        for old_name, new_name in rename_map.items():
            old_path = os.path.join(char_path, old_name)
            new_path = os.path.join(char_path, new_name)
            if os.path.exists(old_path):
                os.rename(old_path, new_path)

# 2. FIX ALIASES AND EXC in lobby_*.cfg
for fname in os.listdir(lobby_path):
    if fname.startswith("lobby_") and fname.endswith(".cfg"):
        fpath = os.path.join(lobby_path, fname)
        with open(fpath, "r") as f:
            content = f.read()
        
        # Replace occurrences of inventory_main.cfg with inventory_weapon.cfg
        content = content.replace("inventory_main.cfg", "inventory_weapon.cfg")
        content = content.replace("inventory_main2.cfg", "inventory_weapon2.cfg")
        content = content.replace("remove_inventory_main.cfg", "remove_inventory_weapon.cfg")
        content = content.replace("remove_inventory_main2.cfg", "remove_inventory_weapon2.cfg")
        
        # Replace alias names if needed.
        # e.g., alias _main_inventory_acidpool -> alias _weapon_inventory_acidpool
        content = content.replace("_main_inventory_", "_weapon_inventory_")
        content = content.replace("_main_inventory2_", "_weapon_inventory2_")
        
        with open(fpath, "w") as f:
            f.write(content)

# 3. FIX global aliases in lobby.cfg and inventory.cfg
# Wait, inventory.cfg has alias _main_inventory "_main_inventory_acidpool" ? 
# Let's check inventory.cfg
inv_cfg_path = os.path.join(lobby_path, "inventory.cfg")
if os.path.exists(inv_cfg_path):
    with open(inv_cfg_path, "r") as f:
        content = f.read()
    content = content.replace("_main_inventory", "_weapon_inventory")
    # Wait! If it replaces _main_inventory, it also replaces _rmv_main_inventory -> _rmv_weapon_inventory
    # We should be careful. 
    with open(inv_cfg_path, "w") as f:
        f.write(content)

# We must also do it for all character pages where _main_inventory is called!
for team in teams:
    team_path = os.path.join(base_path, team)
    if not os.path.isdir(team_path): continue
    for char_name in os.listdir(team_path):
        for cat in ["main", "main2", "secondary", "secondary2", "melee", "melee2", "explosive", "explosive2", "special", "special2", "character", "character2", "weapons", "weapons2"]:
            cat_path = os.path.join(team_path, char_name, cat)
            if os.path.isdir(cat_path):
                for fname in os.listdir(cat_path):
                    if fname.startswith("page") and fname.endswith(".cfg"):
                        fpath = os.path.join(cat_path, fname)
                        with open(fpath, "r") as f:
                            content = f.read()
                        
                        # Replace _main_inventory -> _weapon_inventory inside the buttons
                        content = content.replace("_main_inventory", "_weapon_inventory")
                        
                        with open(fpath, "w") as f:
                            f.write(content)

# Same for team selection files like team_blue_class1.cfg which might call _main_inventory2_acidpool
team_conf_dir = os.path.join(base_path, "team")
if os.path.exists(team_conf_dir):
    for fname in os.listdir(team_conf_dir):
        if fname.endswith(".cfg"):
            fpath = os.path.join(team_conf_dir, fname)
            with open(fpath, "r") as f:
                content = f.read()
            content = content.replace("_main_inventory", "_weapon_inventory")
            with open(fpath, "w") as f:
                f.write(content)

# And inside lobby_menu directories where buttons lead to inventory
# Just globally replace in all .cfg files inside redteam/char_name and blueteam/char_name at root level
for team in teams:
    team_path = os.path.join(base_path, team)
    if not os.path.isdir(team_path): continue
    for char_name in os.listdir(team_path):
        char_path = os.path.join(team_path, char_name)
        if not os.path.isdir(char_path): continue
        for fname in os.listdir(char_path):
            if fname.endswith(".cfg"):
                fpath = os.path.join(char_path, fname)
                with open(fpath, "r") as f:
                    content = f.read()
                content = content.replace("_main_inventory", "_weapon_inventory")
                with open(fpath, "w") as f:
                    f.write(content)

print("Renamed inventory files and updated aliases.")
