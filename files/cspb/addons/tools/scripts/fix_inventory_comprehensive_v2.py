import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'
persist_dir = os.path.join(root_dir, 'persist')
use_cfg_dir = os.path.join(persist_dir, 'use')

# Coordinate Map for Slots 1-6
weapon_slots = {
    1: "0.460000 0.205400 0.690000 0.349300",
    2: "0.710000 0.205400 0.940000 0.349300",
    3: "0.460000 0.349300 0.690000 0.493100",
    4: "0.710000 0.349300 0.940000 0.493100",
    5: "0.460000 0.493100 0.690000 0.636900",
    6: "0.710000 0.493100 0.940000 0.636900"
}

# Categories and their directory names
# Prefix: w=weapon, s=secondary, m=melee, e=explosive, p=special
cat_map = {
    'weapons': {'prefix': 'w', 'reset': '_reset_weap_indicators', 'ind': '_weap_use_indicator', 'exec': '_safe_exec_equip'},
    'secondary': {'prefix': 's', 'reset': '_reset_secondary_indicators', 'ind': '_secondary_use_indicator', 'exec': '_safe_exec_equip_sec'},
    'melee': {'prefix': 'm', 'reset': '_reset_melee_indicators', 'ind': '_melee_use_indicator', 'exec': '_safe_exec_equip'},
    'explosive': {'prefix': 'e', 'reset': '_reset_explosive_indicators', 'ind': '_explosive_use_indicator', 'exec': '_safe_exec_equip'},
    'special': {'prefix': 'p', 'reset': '_reset_special_indicators', 'ind': '_special_use_indicator', 'exec': '_safe_exec_equip'}
}

def fix_extensions_v2():
    print("Fixing extensions in all page configs...")
    for cat in cat_map.keys():
        folder_path = os.path.join(root_dir, cat)
        if not os.path.exists(folder_path): continue
        for file in os.listdir(folder_path):
            if file.endswith('.cfg'):
                filepath = os.path.join(folder_path, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Broad extension fix for any image path in addons/neda/image/
                def sub_ext(match):
                    full_match = match.group(0)
                    path = match.group(1)
                    if path.endswith('.tga') or path.endswith('.png') or path.endswith('.jpg'):
                        return full_match
                    # If it's a directory path, skip (unlikely in touch_addbutton)
                    return f'"{path}.tga"'

                new_content = re.sub(r'"(addons/neda/image/[^"]+)"', sub_ext, content)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"  Fixed: {cat}/{file}")

def generate_use_files_v2():
    print("Generating unique persistence files (v2)...")
    if not os.path.exists(use_cfg_dir): os.makedirs(use_cfg_dir)
    for cat, info in cat_map.items():
        prefix = info['prefix']
        for i in range(1, 7):
            filename = f'{prefix}{i}.cfg'
            filepath = os.path.join(use_cfg_dir, filename)
            badge_id = f'_{prefix}_badge_s{i}'
            coord = weapon_slots[i]
            content = f'touch_addbutton "{badge_id}" "addons/neda/image/select_main/use/{i}.tga" "c" {coord} 255 255 255 255 4\n'
            with open(filepath, 'w') as f:
                f.write(content)

def rebuild_databases_v2():
    print("Rebuilding databases to fix broken aliases and standardize IDs...")
    for cat, info in cat_map.items():
        # Map database filename (some plural, some singular)
        # weapons -> weapon_db.cfg
        db_name = cat[:-1] if cat == 'weapons' else cat
        db_path = os.path.join(persist_dir, f'{db_name}_db.cfg')
        if not os.path.exists(db_path): continue
        
        prefix = info['prefix']
        reset_alias = info['reset']
        ind_alias = info['ind']
        exec_alias = info['exec']
        
        with open(db_path, 'r') as f:
            lines = f.readlines()
        
        # We need to find the slot for each weapon in the database
        # We'll use the current content of the page configs to build a mapping
        slot_mapping = {}
        cat_dir = os.path.join(root_dir, cat)
        for i in range(1, 4): # Check pages 1-3
            page_file = os.path.join(cat_dir, f'page{i}.cfg')
            if not os.path.exists(page_file): continue
            with open(page_file, 'r') as pf:
                p_content = pf.read()
                # Find "_sl_itemname" and "selectX"
                # touch_addbutton "_lobby_selectX" ... _sl_itemname"
                matches = re.findall(r'_lobby_select(\d)".*_sl_([a-z0-9_ ]+)', p_content)
                for slot, item in matches:
                    item = item.strip().replace(' ', '_')
                    slot_mapping[item] = slot
        
        new_lines = []
        for line in lines:
            # Refresh Reset alias
            if f'alias {reset_alias}' in line:
                line = f'alias {reset_alias} "touch_removebutton _{prefix}_badge_s*; touch_removebutton _weap_equip_status_badge; alias {ind_alias} _null"\n'
            
            # Rebuild _db_*_full
            # alias _db_item_full "..."
            match = re.search(r'alias _db_([a-z0-9_]+)_full "(.*?)"', line)
            if match:
                item_name = match.group(1)
                # Try to get slot from mapping, otherwise fallback to existing useX.cfg if present
                slot = slot_mapping.get(item_name)
                if not slot:
                    # Fallback lookup in existing line
                    use_m = re.search(r'use(\d)\.cfg', line)
                    if use_m: slot = use_m.group(1)
                
                if slot:
                    line = f'alias _db_{item_name}_full "{reset_alias}; alias {ind_alias} \\"exec addons/neda/persist/use/{prefix}{slot}.cfg\\"; {ind_alias}; alias _show_equip_{item_name} {exec_alias}; _show_equip_{item_name}"\n'
            
            new_lines.append(line)
            
        with open(db_path, 'w') as f:
            f.write("".join(new_lines))
        print(f"  Rebuilt: {db_name}_db.cfg")

def update_mapmode_control_v2():
    filepath = os.path.join(root_dir, 'mapmode_control.cfg')
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Update _rmv_persist_all: w, s, m, e, p, c...
    new_cleanup = 'alias _rmv_persist_all "touch_removebutton _persist_*; touch_removebutton _w_badge_*; touch_removebutton _s_badge_*; touch_removebutton _m_badge_*; touch_removebutton _e_badge_*; touch_removebutton _p_badge_*; touch_removebutton _c_badge_*; touch_removebutton _weap_equip_status_badge; touch_removebutton _char_equip_status_badge"'
    content = re.sub(r'alias _rmv_persist_all ".*?"', new_cleanup, content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print("Fixed mapmode_control.cfg (v2)")

fix_extensions_v2()
generate_use_files_v2()
rebuild_databases_v2()
update_mapmode_control_v2()
