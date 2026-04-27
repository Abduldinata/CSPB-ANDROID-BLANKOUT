import os
import re

# Base paths
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

# Categories
# Prefix: w=weapon, s=secondary, m=melee, e=explosive, p=special
categories = {
    'weapon': 'w',
    'secondary': 's',
    'melee': 'm',
    'explosive': 'e',
    'special': 'p'
}

def fix_extensions_in_pages():
    print("Fixing extensions in page configs...")
    for cat in categories.keys():
        cat_dir = os.path.join(root_dir, cat)
        if not os.path.exists(cat_dir): continue
        for file in os.listdir(cat_dir):
            if file.startswith('page') and file.endswith('.cfg'):
                filepath = os.path.join(cat_dir, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                
                # Add .tga where missing, and handle spaces
                # Example: addons/neda/image/weapons/aug -> addons/neda/image/weapons/aug.tga
                # Only if not already ending in .tga
                def sub_ext(match):
                    path = match.group(1)
                    if path.endswith('.tga'): return match.group(0)
                    return f'"{path}.tga"'
                
                # Match: "addons/neda/image/[cat]/..."
                pattern = f'"(addons/neda/image/{cat}/[^"]+)"'
                new_content = re.sub(pattern, sub_ext, content)
                
                if new_content != content:
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"  Fixed extensions in {cat}/{file}")

def generate_unique_use_files():
    print("Generating unique persistence files...")
    if not os.path.exists(use_cfg_dir): os.makedirs(use_cfg_dir)
    for cat, prefix in categories.items():
        for i in range(1, 7):
            filename = f'{prefix}{i}.cfg'
            filepath = os.path.join(use_cfg_dir, filename)
            badge_id = f'_{prefix}_badge_s{i}'
            coord = weapon_slots[i]
            # Layer 4 because 5 is not supported
            content = f'touch_addbutton "{badge_id}" "addons/neda/image/select_main/use/{i}.tga" "c" {coord} 255 255 255 255 4\n'
            with open(filepath, 'w') as f:
                f.write(content)
    print("  Unique persistence files generated.")

def fix_databases():
    print("Fixing database files...")
    for cat, prefix in categories.items():
        db_file = f'{cat}_db.cfg'
        db_path = os.path.join(persist_dir, db_file)
        if not os.path.exists(db_path): continue
        
        with open(db_path, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        reset_alias = f'_reset_{cat}_indicators' if cat != 'weapon' else '_reset_weap_indicators'
        if cat == 'special': reset_alias = '_reset_special_indicators'
        
        badge_prefix = f'_{prefix}_badge_s'
        ind_alias = f'_{cat}_use_indicator' if cat != 'weapon' else '_weap_use_indicator'
        if cat == 'special': ind_alias = '_special_use_indicator'
        
        equip_safe_exec = '_safe_exec_equip'
        if cat == 'secondary': equip_safe_exec = '_safe_exec_equip_sec'
        # For others we might need to define them if they don't exist
        
        for line in lines:
            # 1. Update Reset Alias
            if f'alias {reset_alias}' in line:
                # alias _reset_weap_indicators "touch_removebutton _w_badge_s*; touch_removebutton _weap_equip_status_badge; alias _weap_use_indicator _null"
                new_reset = f'alias {reset_alias} "touch_removebutton {badge_prefix}*; touch_removebutton _weap_equip_status_badge; alias {ind_alias} _null"\n'
                new_lines.append(new_reset)
            
            # 2. Fix _db_*_full aliases
            elif '_full' in line and 'alias _db_' in line:
                # Match name and extract slot number if possible, but easier to use the category logic
                # We need to find which use file to exec.
                # Usually it was use[1-6].cfg.
                # Let's search for "use(\d).cfg"
                use_match = re.search(r'use(\d)\.cfg', line)
                if use_match:
                    slot_num = use_match.group(1)
                    name_match = re.search(r'alias _db_(.*)_full', line)
                    if name_match:
                        name = name_match.group(1)
                        # Rebuild: alias _db_name_full "_reset_cat_indicators; alias _cat_use_indicator \"exec addons/neda/persist/use/prefixN.cfg\"; _cat_use_indicator; alias _show_equip_name _safe_exec_equip; _show_equip_name"
                        new_full = f'alias _db_{name}_full "{reset_alias}; alias {ind_alias} \\"exec addons/neda/persist/use/{prefix}{slot_num}.cfg\\"; {ind_alias}; alias _show_equip_{name} {equip_safe_exec}; _show_equip_{name}"\n'
                        new_lines.append(new_full)
                    else: new_lines.append(line)
                else:
                    # Broken line like: alias _db_bow_full "_reset_secondary_indicators; alias _secondary_use_indicator \; ..."
                    # We might need a lookup table if slot is missing. 
                    # But for now let's hope it matches.
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        with open(db_path, 'w') as f:
            f.write("".join(new_lines))
        print(f"  Fixed {db_file}")

def fix_mapmode_control():
    print("Fixing mapmode_control.cfg...")
    filepath = os.path.join(root_dir, 'mapmode_control.cfg')
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Update _rmv_persist_all to handle all unique prefixes
    new_cleanup = 'alias _rmv_persist_all "touch_removebutton _persist_*; touch_removebutton _w_badge_*; touch_removebutton _s_badge_*; touch_removebutton _m_badge_*; touch_removebutton _e_badge_*; touch_removebutton _p_badge_*; touch_removebutton _c_badge_*; touch_removebutton _weap_equip_status_badge; touch_removebutton _char_equip_status_badge"'
    
    content = re.sub(r'alias _rmv_persist_all ".*?"', new_cleanup, content)
    
    with open(filepath, 'w') as f:
        f.write(content)
    print("  Fixed mapmode_control.cfg")

fix_extensions_in_pages()
generate_unique_use_files()
fix_databases()
fix_mapmode_control()
