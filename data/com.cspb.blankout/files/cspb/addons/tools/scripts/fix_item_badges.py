import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"

categories = {
    "weapons": {
        "db": "weapon_db.cfg",
        "reset": "_reset_weap_indicators",
        "ind": "_weap_p",
        "use": "w",
        "equip": "weapon/equip.cfg"
    },
    "secondary": {
        "db": "secondary_db.cfg",
        "reset": "_reset_secondary_indicators",
        "ind": "_sec_p",
        "use": "s",
        "equip": "secondary/equip.cfg"
    },
    "melee": {
        "db": "melee_db.cfg",
        "reset": "_reset_melee_indicators",
        "ind": "_melee_p",
        "use": "m",
        "equip": "melee/equip.cfg"
    },
    "explosive": {
        "db": "explosive_db.cfg",
        "reset": "_reset_explosive_indicators",
        "ind": "_exp_p",
        "use": "e",
        "equip": "explosive/equip.cfg"
    },
    "special": {
        "db": "special_db.cfg",
        "reset": "_reset_special_indicators",
        "ind": "_special_p",
        "use": "p",
        "equip": "special/equip.cfg"
    }
}

# Commands to ignore when looking for item aliases
blocklist = ["weap", "weap_cmd", "melee", "melee_cmd", "secondary", "secondary_cmd", "explosive", "explosive_cmd", "special", "special_cmd", "all_sl_weap", "all_sl_weap_cmd", "all_sl_melee", "all_sl_melee_cmd", "all_sl_explosive", "all_sl_explosive_cmd", "all_sl_secondary", "all_sl_secondary_cmd", "all_sl_special", "all_sl_special_cmd"]

for cat_folder, cat_data in categories.items():
    print(f"Processing category: {cat_folder}")
    layout_dir = os.path.join(base_path, "blueteam", "acidpool", cat_folder)
    item_map = {} # item_name -> (page, slot)
    
    if os.path.isdir(layout_dir):
        for fname in os.listdir(layout_dir):
            if fname.startswith("page") and fname.endswith(".cfg"):
                try:
                    page_num = int(re.search(r"page(\d+)", fname).group(1))
                except:
                    continue
                    
                with open(os.path.join(layout_dir, fname), "r") as f:
                    content = f.read()
                
                # Match touch_addbutton "_lobby_selectX" ... "commands" ...
                # Using a more robust match for the button command string
                btn_matches = re.finditer(r'touch_addbutton\s+"_lobby_select(\d+)"\s+""\s+"([^"]+)"', content)
                for btn in btn_matches:
                    slot_num = int(btn.group(1))
                    cmd_string = btn.group(2)
                    
                    # Split commands by semicolon
                    cmds = [c.strip() for c in cmd_string.split(";")]
                    item_name = None
                    for c in cmds:
                        # Look for _sl_ITEM
                        if c.startswith("_sl_"):
                            name = c[4:] # strip _sl_
                            if name and name not in blocklist and not name.startswith("all_"):
                                item_name = name
                                break
                    
                    if item_name:
                        item_map[item_name] = (page_num, slot_num)
                        print(f"  Mapped {item_name} -> Page {page_num}, Slot {slot_num}")
                            
    print(f"Total {cat_folder} items mapped: {len(item_map)}")
    
    # 2. Rewrite the db file
    db_file_path = os.path.join(base_path, "persist", cat_data["db"])
    if os.path.isfile(db_file_path):
        with open(db_file_path, "r") as f:
            lines = f.readlines()
            
        modified = False
        for i, line in enumerate(lines):
            # Focus on Full Persistence Aliases
            if line.startswith("alias _db_") and "_full" in line:
                m = re.match(r'^alias\s+_db_([a-zA-Z0-9_]+)_full\s+"', line)
                if m:
                    item_alias = m.group(1)
                    if item_alias in item_map:
                        p, s = item_map[item_alias]
                        # Construct standardized alias
                        # Order: Reset -> Equip Badge Alias -> Call Equip Badge -> Set Use Badge Alias -> Call Use Badge
                        new_line = f'alias _db_{item_alias}_full "{cat_data["reset"]}; alias _show_equip_{item_alias} \\"exec addons/neda/persist/{cat_data["equip"]}\\"; _show_equip_{item_alias}; alias {cat_data["ind"]}{p}_indicator \\"exec addons/neda/persist/use/{cat_data["use"]}{s}.cfg\\"; {cat_data["ind"]}{p}_indicator"\n'
                        
                        if line != new_line:
                            lines[i] = new_line
                            modified = True
                            # print(f"    Updated DB for {item_alias}")

        if modified:
            with open(db_file_path, "w") as f:
                f.writelines(lines)
            print(f"  ==> Saved updates to {cat_data['db']}\n")
    else:
        print(f"  Notice: DB file {cat_data['db']} not found.\n")

print("Done adjusting all item persistence mappings.")
