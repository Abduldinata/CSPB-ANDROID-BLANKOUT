import glob
import os

def fix_weapon_quotes():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_main"
    
    # helper mappings
    replacements = {
        '"exec addons/neda/persist/weapon/equip.cfg"': '_safe_exec_equip',
        '"exec addons/neda/persist/use/use1.cfg"': '_safe_exec_use1',
        '"exec addons/neda/persist/use/use2.cfg"': '_safe_exec_use2',
        '"exec addons/neda/persist/use/use3.cfg"': '_safe_exec_use3',
        '"exec addons/neda/persist/use/use4.cfg"': '_safe_exec_use4',
        '"exec addons/neda/persist/use/use5.cfg"': '_safe_exec_use5',
        '"exec addons/neda/persist/use/use6.cfg"': '_safe_exec_use6',
    }
    
    # We need to scan recursively in select_main
    # patterns: select_main/weapon/page*/*.cfg, select_main/secondary/page*/*.cfg, etc.
    
    categories = ["weapon", "secondary", "melee", "explosive", "special"]
    
    total_fixed = 0
    
    for cat in categories:
        cat_path = os.path.join(base_path, cat)
        if not os.path.exists(cat_path):
            continue
            
        # Recursive glob or just walk?
        # glob '**/*.cfg' is easiest if supported by python version, else walk
        for root, dirs, files in os.walk(cat_path):
            for filename in files:
                if not filename.endswith(".cfg"):
                    continue
                    
                filepath = os.path.join(root, filename)
                
                with open(filepath, "r", encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                modified = False
                
                for target, replacement in replacements.items():
                    if target in new_content:
                        # Replace nested quote pattern
                        new_content = new_content.replace(target, replacement)
                        modified = True
                
                if modified:
                    with open(filepath, "w", encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed quotes in: {filename}")
                    total_fixed += 1

    print(f"Total files fixed: {total_fixed}")

if __name__ == "__main__":
    fix_weapon_quotes()
