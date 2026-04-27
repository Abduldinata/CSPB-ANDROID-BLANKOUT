import os
import re

def create_weapon_db():
    # Load stat.cfg to get all weapon names
    stat_file = r"e:\Games\PROJECT LOBBY CSPB\addons\stat.cfg"
    with open(stat_file, "r", encoding='latin-1') as f:
        content = f.read()
    
    # Extract all weapon names from "alias stat_WEAPONNAME"
    weapons = re.findall(r'alias stat_(\w+) ', content)
    
    output_file = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\weapon_db.cfg"
    
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("// Weapon Persistence Database\n")
        f.write("// This file defines all weapon persistence aliases\n\n")
        
        # Define reset alias
        f.write("// Badge Reset\n")
        f.write('alias _reset_weap_indicators "touch_removebutton _persist_use_badge1; touch_removebutton _persist_use_badge2; touch_removebutton _persist_use_badge3; touch_removebutton _persist_use_badge4; touch_removebutton _persist_use_badge5; touch_removebutton _persist_use_badge6; touch_removebutton _persist_equip_badge"\n\n')
        
        # Map weapon to use badge index (based on position in page)
        for i, weapon in enumerate(weapons, 1):
            # Determine which use badge to use (1-6 based on position in page)
            badge_index = ((i - 1) % 6) + 1
            
            # Full alias definition
            f.write(f'alias _db_{weapon}_full "_reset_weap_indicators; alias _weap_use_indicator \\\"exec addons/neda/persist/use/use{badge_index}.cfg\\\"; _weap_use_indicator; _show_equip_{weapon}"\n')
        
        f.write("\n// Default\n")
        f.write('alias _weap_use_indicator "_blank"\n')
    
    print(f"Created {output_file} with {len(weapons)} weapons")
    
    # Now update stat.cfg to load this file
    with open(stat_file, "r", encoding='latin-1') as f:
        lines = f.readlines()
    
    # Add exec line at the end
    if "exec addons/neda/select_main/weapon/weapon_db.cfg" not in "".join(lines):
        with open(stat_file, "a", encoding='latin-1') as f:
            f.write("\n// Load Weapon Persistence System\n")
            f.write("exec addons/neda/select_main/weapon/weapon_db.cfg\n")
        print("Added load weapon_db to stat.cfg")

if __name__ == "__main__":
    create_weapon_db()
