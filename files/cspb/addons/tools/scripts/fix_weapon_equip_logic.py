import re

def fix_weapon_db_equip_logic():
    filepath = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\weapon_db.cfg"
    
    with open(filepath, "r", encoding='utf-8') as f:
        content = f.read()
    
    # Find all _db_*_full aliases and remove "; _show_equip_*" from the end
    # OLD: alias _db_ak47_full "_reset_weap_indicators; alias _weap_use_indicator \"exec addons/neda/persist/use/use1.cfg\"; _weap_use_indicator; _show_equip_ak47"
    # NEW: alias _db_ak47_full "_reset_weap_indicators; alias _weap_use_indicator \"exec addons/neda/persist/use/use1.cfg\"; _weap_use_indicator"
    
    content = re.sub(
        r'(_weap_use_indicator); _show_equip_\w+"',
        r'\1"',
        content
    )
    
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(content)
    
    print("Fixed weapon_db.cfg - Removed _show_equip_* from all _db_*_full aliases")
    print("Now Equip badge will ONLY show when clicking already-equipped weapon")

if __name__ == "__main__":
    fix_weapon_db_equip_logic()
