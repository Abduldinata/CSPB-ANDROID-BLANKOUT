import os

def update_char_db():
    output_file = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\char_db.cfg"
    
    # Define mapping of Character Name -> Lobby Alias Part
    # e.g. redbull -> _redbull
    characters = [
        ("acidpool", "acidpool", "blue", "use2.cfg"),
        ("redbull", "redbull", "red", "use1.cfg"),
        ("tarantula", "tarantula", "red", "use3.cfg"),
        ("keeneyes", "keeneyes", "blue", "use4.cfg"),
        ("dfox", "dfox", "red", "use5.cfg"),
        ("leopard", "leopard", "blue", "use6.cfg"),
        ("viper", "viper", "red", "use7.cfg"),
        ("hide", "hide", "blue", "use8.cfg"),
        ("ricalopez", "ricalopez", "red", "use9.cfg"),
        ("judychou", "judychou", "blue", "use1.cfg"), # Page 2 blue
        ("natasha", "natasha", "red", "use3.cfg"), # Page 2 red
        ("queen", "queen", "blue", "use2.cfg"), # Page 2 blue
    ]

    header = """// --- CHARACTER THEME & PERSISTENCE DATABASE ---

// --- BADGE RESET ---
alias _reset_char_indicators "touch_removebutton _lobby_equip_image1; touch_removebutton _lobby_equip_image2; touch_removebutton _lobby_equip_image3; touch_removebutton _lobby_equip_image4; touch_removebutton _lobby_equip_image5; touch_removebutton _lobby_equip_image6; touch_removebutton _lobby_equip_image7; touch_removebutton _lobby_equip_image8; touch_removebutton _lobby_equip_image9; touch_removebutton _persist_char_badge; alias _char_p1_badge _blank; alias _char_p2_badge _blank"

// --- THEME SWITCHER (NON-RECURSIVE) ---
// Updates ALL inventory aliases to point to the new character's paths.
// Parameter: %NAME% = Character Name
"""

    with open(output_file, "w", encoding='utf-8') as f:
        f.write(header)
        
        for name, folder, team, badge_cfg in characters:
            # Determine lobby alias (usually _lobby_3b_NAME for Red, _lobby_1b_NAME for Blue)
            # Based on previous file content observation:
            # Redbull (red) -> _lobby_3b_redbull
            # Acidpool (blue) -> _lobby_1b_acidpool
            if team == "red":
                lobby_alias = f"_lobby_3b_{folder}"
            else:
                lobby_alias = f"_lobby_1b_{folder}"
            
            # Badge alias (_char_p1_badge or _char_p2_badge depending on page)
            # Assuming most are page 1. Judychou/Natasha/Queen seem to reflect page 2 but let's stick to standard logic.
            # actually looking at previous file, judychou uses _char_p2_badge.
            # Simplified logic based on previous file:
            badge_alias = "_char_p1_badge"
            if name in ["judychou", "natasha", "queen"]:
                badge_alias = "_char_p2_badge"
                
            cmd = f'alias _db_char_{name} "_reset_char_indicators; alias {badge_alias} \\"exec addons/neda/persist/character/{badge_cfg}\\"; alias _active_char_theme _db_char_{name}; alias _back_to_lobby {lobby_alias}; '
            
            # Add Inventory Aliases
            cmd += f'alias _main_inventory \\"_main_inventory_{folder}\\"; '
            cmd += f'alias _main_inventory2 \\"_main_inventory2_{folder}\\"; '
            cmd += f'alias _rmv_main_inventory \\"_rmv_main_inventory_{folder}\\"; '
            cmd += f'alias _rmv_main_inventory2 \\"_rmv_main_inventory2_{folder}\\"; '
            
            # NEW: Add Secondary, Melee, etc.
            cmd += f'alias _second_inventory \\"_second_inventory_{folder}\\"; '
            cmd += f'alias _rmv_second_inventory \\"_rmv_second_inventory_{folder}\\"; '
            
            cmd += f'alias _melee_inventory \\"_melee_inventory_{folder}\\"; '
            cmd += f'alias _rmv_melee_inventory \\"_rmv_melee_inventory_{folder}\\"; '
            
            cmd += f'alias _explosive_inventory \\"_explosive_inventory_{folder}\\"; '
            cmd += f'alias _rmv_explosive_inventory \\"_rmv_explosive_inventory_{folder}\\"; '
            
            cmd += f'alias _special_inventory \\"_special_inventory_{folder}\\"; '
            cmd += f'alias _rmv_special_inventory \\"_rmv_special_inventory_{folder}\\"; '
            
            cmd += f'alias _char_inventory \\"_char_inventory_{folder}\\"; '
            cmd += f'alias _rmv_char_inventory \\"_rmv_char_inventory_{folder}\\"; '
            
            # End with reloading the character inventory to reflect changes immediately
            cmd += '_char_inventory"'
            
            f.write(f"\n// {name.upper()}\n{cmd}\n")

        f.write("\n// Default\nalias _active_char_theme _db_char_acidpool\nalias _back_to_lobby _lobby_1b_acidpool\n")
        
    print(f"Updated {output_file}")

if __name__ == "__main__":
    update_char_db()
