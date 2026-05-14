import os

def create_databases():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist"
    
    # --- SECONDARY ---
    secondary_items = [
        # Page 1
        "bow", "coltpython", "desert_eagle", "desert_eagle_dual", "dualhandgun", "glock",
        # Page 2
        "k5", "raging_bull"
    ]
    
    with open(os.path.join(base_path, "secondary_db.cfg"), "w") as f:
        f.write("// Secondary Weapon Persistence Database\n\n")
        f.write('alias _reset_secondary_indicators "touch_removebutton _persist_use_badge1; touch_removebutton _persist_use_badge2; touch_removebutton _persist_use_badge3; touch_removebutton _persist_use_badge4; touch_removebutton _persist_use_badge5; touch_removebutton _persist_use_badge6; touch_removebutton _persist_equip_badge"\n\n')
        
        # Equip Loaders
        f.write("// Equip Badge Loaders\n")
        for item in secondary_items:
            f.write(f'alias _show_equip_{item} "exec addons/neda/persist/secondary/equip.cfg"\n')
        
        # Full Aliases
        f.write("\n// Full Persistence Aliases\n")
        for i, item in enumerate(secondary_items, 1):
            badge_idx = ((i-1)%6) + 1
            f.write(f'alias _db_{item}_full "_reset_secondary_indicators; alias _secondary_use_indicator \\"exec addons/neda/persist/use/use{badge_idx}.cfg\\"; _secondary_use_indicator"\n')

        f.write('\nalias _secondary_use_indicator "_blank"\n')

    print("Created secondary_db.cfg")

    # --- MELEE ---
    melee_items = [
        # Page 1
        "amok", "arabian_sword", "bone_knife", "butterfly", "candy_cane", "combat",
        # Page 2
        "dual_knife", "fangblade", "icefork", "karambit", "keris", "m7",
        # Page 3
        "brass_knuckle", "miniaxe", "saber"
    ]
    
    with open(os.path.join(base_path, "melee_db.cfg"), "w") as f:
        f.write("// Melee Weapon Persistence Database\n\n")
        f.write('alias _reset_melee_indicators "touch_removebutton _persist_use_badge1; touch_removebutton _persist_use_badge2; touch_removebutton _persist_use_badge3; touch_removebutton _persist_use_badge4; touch_removebutton _persist_use_badge5; touch_removebutton _persist_use_badge6; touch_removebutton _persist_equip_badge"\n\n')
        
        # Equip Loaders
        f.write("// Equip Badge Loaders\n")
        for item in melee_items:
            f.write(f'alias _show_equip_{item} "exec addons/neda/persist/melee/equip.cfg"\n')
            
        # Full Aliases
        f.write("\n// Full Persistence Aliases\n")
        for i, item in enumerate(melee_items, 1):
            badge_idx = ((i-1)%6) + 1
            f.write(f'alias _db_{item}_full "_reset_melee_indicators; alias _melee_use_indicator \\"exec addons/neda/persist/use/use{badge_idx}.cfg\\"; _melee_use_indicator"\n')

        f.write('\nalias _melee_use_indicator "_blank"\n')

    print("Created melee_db.cfg")

    # --- EXPLOSIVE ---
    explosive_items = [
        # Page 1
        "gasbomb", "k400"
    ]
    
    with open(os.path.join(base_path, "explosive_db.cfg"), "w") as f:
        f.write("// Explosive Persistence Database\n\n")
        f.write('alias _reset_explosive_indicators "touch_removebutton _persist_use_badge1; touch_removebutton _persist_use_badge2; touch_removebutton _persist_use_badge3; touch_removebutton _persist_use_badge4; touch_removebutton _persist_use_badge5; touch_removebutton _persist_use_badge6; touch_removebutton _persist_equip_badge"\n\n')
        
        # Equip Loaders
        f.write("// Equip Badge Loaders\n")
        for item in explosive_items:
            f.write(f'alias _show_equip_{item} "exec addons/neda/persist/explosive/equip.cfg"\n')
            
        # Full Aliases
        f.write("\n// Full Persistence Aliases\n")
        for i, item in enumerate(explosive_items, 1):
            badge_idx = ((i-1)%6) + 1
            f.write(f'alias _db_{item}_full "_reset_explosive_indicators; alias _explosive_use_indicator \\"exec addons/neda/persist/use/use{badge_idx}.cfg\\"; _explosive_use_indicator"\n')

        f.write('\nalias _explosive_use_indicator "_blank"\n')

    print("Created explosive_db.cfg")

    # --- SPECIAL ---
    special_items = [
        # Page 1
        "smoke"
    ]
    
    with open(os.path.join(base_path, "special_db.cfg"), "w") as f:
        f.write("// Special Persistence Database\n\n")
        f.write('alias _reset_special_indicators "touch_removebutton _persist_use_badge1; touch_removebutton _persist_use_badge2; touch_removebutton _persist_use_badge3; touch_removebutton _persist_use_badge4; touch_removebutton _persist_use_badge5; touch_removebutton _persist_use_badge6; touch_removebutton _persist_equip_badge"\n\n')
        
        # Equip Loaders
        f.write("// Equip Badge Loaders\n")
        for item in special_items:
            f.write(f'alias _show_equip_{item} "exec addons/neda/persist/special/equip.cfg"\n')
            
        # Full Aliases
        f.write("\n// Full Persistence Aliases\n")
        for i, item in enumerate(special_items, 1):
            badge_idx = ((i-1)%6) + 1
            f.write(f'alias _db_{item}_full "_reset_special_indicators; alias _special_use_indicator \\"exec addons/neda/persist/use/use{badge_idx}.cfg\\"; _special_use_indicator"\n')

        f.write('\nalias _special_use_indicator "_blank"\n')

    print("Created special_db.cfg")

if __name__ == "__main__":
    create_databases()
