import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'
persist_dir = os.path.join(root_dir, 'persist')
use_cfg_dir = os.path.join(persist_dir, 'use')

weapon_slots = {
    1: "0.460000 0.205400 0.690000 0.349300",
    2: "0.710000 0.205400 0.940000 0.349300",
    3: "0.460000 0.349300 0.690000 0.493100",
    4: "0.710000 0.349300 0.940000 0.493100",
    5: "0.460000 0.493100 0.690000 0.636900",
    6: "0.710000 0.493100 0.940000 0.636900"
}

cat_map = {
    'weapons': {'prefix': 'w', 'reset': '_reset_weap_indicators', 'ind_base': '_weap_p', 'exec': '_safe_exec_equip', 'img_key': 'weapons', 'max_pages': 14},
    'secondary': {'prefix': 's', 'reset': '_reset_secondary_indicators', 'ind_base': '_sec_p', 'exec': '_safe_exec_equip_sec', 'img_key': 'secondary', 'max_pages': 4},
    'melee': {'prefix': 'm', 'reset': '_reset_melee_indicators', 'ind_base': '_melee_p', 'exec': '_safe_exec_equip', 'img_key': 'melee', 'max_pages': 4},
    'explosive': {'prefix': 'e', 'reset': '_reset_explosive_indicators', 'ind_base': '_explosive_p', 'exec': '_safe_exec_equip', 'img_key': 'explosive', 'max_pages': 2},
    'special': {'prefix': 'p', 'reset': '_reset_special_indicators', 'ind_base': '_special_p', 'exec': '_safe_exec_equip', 'img_key': 'special', 'max_pages': 2}
}

def fix_extensions_v5():
    print("Fixing extensions in all page configs (v5)...")
    for cat in cat_map.keys():
        folder_path = os.path.join(root_dir, cat)
        if not os.path.exists(folder_path): continue
        for file in os.listdir(folder_path):
            if file.endswith('.cfg'):
                filepath = os.path.join(folder_path, file)
                with open(filepath, 'r') as f: content = f.read()
                def sub_ext(match):
                    full_match = match.group(0)
                    path = match.group(1)
                    if path.endswith('.tga') or path.endswith('.png') or path.endswith('.jpg'): return full_match
                    return f'"{path}.tga"'
                new_content = re.sub(r'"(addons/neda/image/[^"]+)"', sub_ext, content)
                if new_content != content:
                    with open(filepath, 'w') as f: f.write(new_content)
    print("  Extensions fixed.")

def generate_use_files_v5():
    print("Generating unique persistence files (v5)...")
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

def rebuild_databases_v5():
    print("Building Image-to-Slot-Page Mapping...")
    master_mapping = {} # {category: {image_name: (page, slot)}}
    for cat, info in cat_map.items():
        img_cat = info['img_key']
        cat_dir = os.path.join(root_dir, cat)
        cat_mapping = {}
        if not os.path.exists(cat_dir): continue
        for i in range(1, 15):
            page_file = os.path.join(cat_dir, f'page{i}.cfg')
            if not os.path.exists(page_file): continue
            with open(page_file, 'r') as pf:
                p_content = pf.read()
                # Find image line: _lobby_typeN "addons/neda/image/cat/name.tga"
                pattern = f'_lobby_.*?(\\d)"\\s+"addons/neda/image/{img_cat}/(.*?)\\.tga"'
                matches = re.findall(pattern, p_content)
                for slot, img_name in matches:
                    img_name = img_name.strip().replace(' ', '_').lower()
                    cat_mapping[img_name] = (i, slot)
        master_mapping[cat] = cat_mapping
    
    print("Rebuilding Databases (v5)...")
    for cat, info in cat_map.items():
        db_name = cat[:-1] if cat == 'weapons' else cat
        db_path = os.path.join(persist_dir, f'{db_name}_db.cfg')
        if not os.path.exists(db_path): continue
        
        prefix = info['prefix']
        reset_alias = info['reset']
        ind_base = info['ind_base']
        exec_alias = info['exec']
        mapping = master_mapping.get(cat, {})
        max_pages = info['max_pages']
        
        with open(db_path, 'r') as f: lines = f.readlines()
        
        # Reset alias update: clear ALL page indicators
        page_ind_clears = "; ".join([f"alias {ind_base}{p}_indicator _null" for p in range(1, max_pages + 1)])
        
        new_lines = []
        for line in lines:
            if f'alias {reset_alias}' in line:
                line = f'alias {reset_alias} "touch_removebutton _{prefix}_badge_s*; touch_removebutton _weap_equip_status_badge; {page_ind_clears}"\n'
            
            match = re.search(r'alias _db_(.*)_full "(.*?)"', line)
            if match:
                original_id = match.group(1)
                item_id = original_id.lower()
                mapping_data = mapping.get(item_id)
                if not mapping_data:
                    for k, v in mapping.items():
                        if k in item_id or item_id in k:
                            mapping_data = v; break
                
                if mapping_data:
                    page, slot = mapping_data
                    # Set the specific page indicator
                    line = f'alias _db_{original_id}_full "{reset_alias}; alias {ind_base}{page}_indicator \\"exec addons/neda/persist/use/{prefix}{slot}.cfg\\"; {ind_base}{page}_indicator; alias _show_equip_{original_id} {exec_alias}; _show_equip_{original_id}"\n'
            new_lines.append(line)
        
        with open(db_path, 'w') as f: f.write("".join(new_lines))
        print(f"  Rebuilt: {db_name}_db.cfg")

def update_mapmode_control_v5():
    print("Updating mapmode_control.cfg (v5)...")
    filepath = os.path.join(root_dir, 'mapmode_control.cfg')
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f: content = f.read()
    
    # Update _add_indicators to include ALL cat indicators
    # We'll just build a large string for all categories and their pages
    all_inds = ["_map_p1_indicator", "_map_p2_indicator", "_map_p3_indicator", "_mode_p1_indicator", "_char_p1_badge", "_char_p2_badge"]
    for cat, info in cat_map.items():
        ind_base = info['ind_base']
        for p in range(1, info['max_pages'] + 1):
            all_inds.append(f"{ind_base}{p}_indicator")
    
    inds_string = "; ".join(all_inds)
    content = re.sub(r'alias _add_indicators ".*?"', f'alias _add_indicators "{inds_string}"', content)
    
    # Same for character inventory specialized loader
    char_inds_string = "; ".join(all_inds[4:]) # Skip maps and modes
    content = re.sub(r'alias _add_indicators_char_inv ".*?"', f'alias _add_indicators_char_inv "{char_inds_string}"', content)

    with open(filepath, 'w') as f: f.write(content)
    print("  Fixed mapmode_control.cfg (v5)")

fix_extensions_v5()
generate_use_files_v5()
rebuild_databases_v5()
update_mapmode_control_v5()
print("v5 Comprehensive Fix Finish.")
