import os
import glob
import re

def add_equip_logic_to_characters():
    # Step 1: Update char_db.cfg to add _show_equip_char_* aliases
    char_db_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\char_db.cfg"
    
    with open(char_db_path, "r", encoding='utf-8') as f:
        content = f.read()
    
    # Extract all character names from _db_char_* aliases
    char_names = re.findall(r'alias _db_char_(\w+) ', content)
    
    # Add _show_equip_char_* definitions after badge reset
    equip_defs = "\n// --- EQUIP BADGE SHOW (for temporary display) ---\n"
    for i, char_name in enumerate(char_names, 1):
        equip_defs += f'alias _show_equip_char_{char_name} "exec addons/neda/select_character/equip{i}.cfg"\n'
    equip_defs += "\n"
    
    # Insert after _reset_char_indicators
    content = content.replace(
        'alias _reset_char_indicators "touch_removebutton _lobby_equip_image1; touch_removebutton _lobby_equip_image2; touch_removebutton _lobby_equip_image3; touch_removebutton _lobby_equip_image4; touch_removebutton _lobby_equip_image5; touch_removebutton _lobby_equip_image6; touch_removebutton _lobby_equip_image7; touch_removebutton _lobby_equip_image8; touch_removebutton _lobby_equip_image9; touch_removebutton _persist_char_badge; alias _char_p1_badge _blank; alias _char_p2_badge _blank"',
        'alias _reset_char_indicators "touch_removebutton _lobby_equip_image1; touch_removebutton _lobby_equip_image2; touch_removebutton _lobby_equip_image3; touch_removebutton _lobby_equip_image4; touch_removebutton _lobby_equip_image5; touch_removebutton _lobby_equip_image6; touch_removebutton _lobby_equip_image7; touch_removebutton _lobby_equip_image8; touch_removebutton _lobby_equip_image9; touch_removebutton _persist_char_badge; alias _char_p1_badge _blank; alias _char_p2_badge _blank"\n' + equip_defs
    )
    
    with open(char_db_path, "w", encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated char_db.cfg with {len(char_names)} character equip aliases")
    
    # Step 2: Update all character selection files to add _show_equip_char_* call
    char_files = glob.glob(r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_character\character\page*\*.cfg")
    
    updated_count = 0
    for filepath in char_files:
        filename = os.path.basename(filepath).replace('.cfg', '')
        
        # Find matching character name
        matching_char = None
        for char_name in char_names:
            if char_name.lower() in filename.lower():
                matching_char = char_name
                break
        
        if not matching_char:
            print(f"No matching character for {filename}")
            continue
        
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Check if _show_equip already exists
        if f"_show_equip_char_{matching_char}" in content:
            print(f"Already has equip logic: {filename}")
            continue
        
        # Add _show_equip_char_* call at the end
        content = content.rstrip() + f"\n\n_show_equip_char_{matching_char}\n"
        
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(content)
        
        updated_count += 1
        print(f"Added equip logic to: {filename}")
    
    print(f"\nTotal character files updated: {updated_count}")

if __name__ == "__main__":
    add_equip_logic_to_characters()
