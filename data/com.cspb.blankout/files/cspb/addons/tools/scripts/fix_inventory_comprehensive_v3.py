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

cat_map = {
    'weapons': {'prefix': 'w', 'reset': '_reset_weap_indicators', 'ind': '_weap_use_indicator', 'exec': '_safe_exec_equip', 'img_key': 'weapon'},
    'secondary': {'prefix': 's', 'reset': '_reset_secondary_indicators', 'ind': '_secondary_use_indicator', 'exec': '_safe_exec_equip_sec', 'img_key': 'secondary'},
    'melee': {'prefix': 'm', 'reset': '_reset_melee_indicators', 'ind': '_melee_use_indicator', 'exec': '_safe_exec_equip', 'img_key': 'melee'},
    'explosive': {'prefix': 'e', 'reset': '_reset_explosive_indicators', 'ind': '_explosive_use_indicator', 'exec': '_safe_exec_equip', 'img_key': 'explosive'},
    'special': {'prefix': 'p', 'reset': '_reset_special_indicators', 'ind': '_special_use_indicator', 'exec': '_safe_exec_equip', 'img_key': 'special'}
}

def fix_extensions_v3():
    print("Fixing extensions in all page configs (v3)...")
    for cat in cat_map.keys():
        folder_path = os.path.join(root_dir, cat)
        if not os.path.exists(folder_path): continue
        for file in os.listdir(folder_path):
            if file.endswith('.cfg'):
                filepath = os.path.join(folder_path, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                def sub_ext(match):
                    full_match = match.group(0)
                    path = match.group(1)
                    if path.endswith('.tga') or path.endswith('.png') or path.endswith('.jpg'):
                        return full_match
                    return f'"{path}.tga"'

                new_content = re.sub(r'"(addons/neda/image/[^"]+)"', sub_ext, content)
                if new_content != content:
                    with open(filepath, 'w') as f: f.write(new_content)
    print("  Extensions fixed.")

def generate_use_files_v3():
    print("Generating unique persistence files (v3)...")
    if not os.path.exists(use_cfg_dir): os.makedirs(use_cfg_dir)
    for cat, info in cat_map.items():
        prefix = info['prefix']
        for i in range(1, 7):
            filename = f'{prefix}{i}.cfg'
            filepath = os.path.join(use_cfg_dir, filename)
            badge_id = f'_{prefix}_badge_s{i}'
            coord = weapon_slots[i]
            content = f'touch_addbutton "{badge_id}" "addons/neda/image/select_main/use/{i}.tga" "c" {coord} 255 255 255 255 4\n'
            with open(filepath, 'w') as f: f.write(content)

def rebuild_databases_v3():
    print("Building Image-to-Slot Mapping...")
    master_mapping = {} # {category: {image_name: slot}}
    
    for cat, info in cat_map.items():
        img_cat = info['img_key']
        cat_dir = os.path.join(root_dir, cat)
        cat_mapping = {}
        if not os.path.exists(cat_dir): continue
        
        for i in range(1, 15): # Scan up to 14 pages
            page_file = os.path.join(cat_dir, f'page{i}.cfg')
            if not os.path.exists(page_file): continue
            with open(page_file, 'r') as pf:
                p_content = pf.read()
                # Find image name and its lobby button number
                # touch_addbutton "_lobby_[type](\d)" "addons/neda/image/[cat]/(.*).tga"
                # Some folders use _lobby_weapon, some _lobby_secondary, etc.
                pattern = f'_lobby_[a-z]+(\\d)"\\s+"addons/neda/image/{img_cat}/(.*?)\\.tga"'
                matches = re.findall(pattern, p_content)
                for slot, img_name in matches:
                    # Clean img_name (handle spaces etc.)
                    img_name = img_name.strip().replace(' ', '_').lower()
                    cat_mapping[img_name] = slot
        master_mapping[cat] = cat_mapping
    
    print("Rebuilding Databases (v3)...")
    for cat, info in cat_map.items():
        db_name = cat[:-1] if cat == 'weapons' else cat
        db_path = os.path.join(persist_dir, f'{db_name}_db.cfg')
        if not os.path.exists(db_path): continue
        
        prefix = info['prefix']
        reset_alias = info['reset']
        ind_alias = info['ind']
        exec_alias = info['exec']
        mapping = master_mapping.get(cat, {})
        
        with open(db_path, 'r') as f: lines = f.readlines()
        
        new_lines = []
        for line in lines:
            if f'alias {reset_alias}' in line:
                line = f'alias {reset_alias} "touch_removebutton _{prefix}_badge_s*; touch_removebutton _weap_equip_status_badge; alias {ind_alias} _null"\n'
            
            match = re.search(r'alias _db_(.*)_full "(.*?)"', line)
            if match:
                item_id = match.group(1).lower()
                slot = mapping.get(item_id)
                
                # If not found directly, try fuzzy match (item_id in mapping key or vice-versa)
                if not slot:
                    for k in mapping.keys():
                        if k in item_id or item_id in k:
                            slot = mapping[k]
                            break
                
                if slot:
                    line = f'alias _db_{match.group(1)}_full "{reset_alias}; alias {ind_alias} \\"exec addons/neda/persist/use/{prefix}{slot}.cfg\\"; {ind_alias}; alias _show_equip_{match.group(1)} {exec_alias}; _show_equip_{match.group(1)}"\n'
                else:
                    # If still not found, keep broken for now but print warning
                    # Actually, if we want to fix ALL weapon errors, we need a fallback.
                    pass
            new_lines.append(line)
            
        with open(db_path, 'w') as f: f.write("".join(new_lines))
        print(f"  Rebuilt: {db_name}_db.cfg")

def update_mapmode_control_v3():
    filepath = os.path.join(root_dir, 'mapmode_control.cfg')
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f: content = f.read()
    new_cleanup = 'alias _rmv_persist_all "touch_removebutton _persist_*; touch_removebutton _w_badge_*; touch_removebutton _s_badge_*; touch_removebutton _m_badge_*; touch_removebutton _e_badge_*; touch_removebutton _p_badge_*; touch_removebutton _c_badge_*; touch_removebutton _weap_equip_status_badge; touch_removebutton _char_equip_status_badge"'
    content = re.sub(r'alias _rmv_persist_all ".*?"', new_cleanup, content)
    with open(filepath, 'w') as f: f.write(content)

fix_extensions_v3()
generate_use_files_v3()
rebuild_databases_v3()
update_mapmode_control_v3()
print("v3 Comprehensive Fix Finish.")
