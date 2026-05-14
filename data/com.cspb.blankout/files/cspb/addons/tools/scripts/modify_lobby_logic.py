import re

def modify_lobby_cfg():
    filepath = r"e:\Games\PROJECT LOBBY CSPB\addons\lobby.cfg"
    
    with open(filepath, "r", encoding='utf-8') as f:
        content = f.read()
    
    # 1. Modify _lobby_3b to SKIP loading screen and go straight to lobby 3
    # OLD: alias _lobby_3b "exec addons/neda/default/lobby_menu3_load.cfg"
    # NEW: alias _lobby_3b "exec addons/neda/default/lobby_menu3.cfg"
    content = content.replace(
        'alias _lobby_3b "exec addons/neda/default/lobby_menu3_load.cfg"',
        'alias _lobby_3b "exec addons/neda/default/lobby_menu3.cfg"'
    )
    
    # 2. Check for other loading screens (lobby3_open.cfg)
    # The user said "lobby1, lobby2, lobby3, lobby3 load hilangkan load... hanya perlu di lobby4"
    # So we should establish direct links where possible.
    
    # _open_lobby3 "exec addons/neda/lobby3_open.cfg" -> "exec addons/neda/lobby_menu3.cfg"
    content = content.replace(
        'alias _open_lobby3 "exec addons/neda/lobby3_open.cfg"',
        'alias _open_lobby3 "exec addons/neda/default/lobby_menu3.cfg"'
    )
    
    with open(filepath, "w", encoding='utf-8') as f:
        f.write(content)
        
    print("Modified lobby.cfg to bypass default/lobby_menu3_load.cfg and lobby3_open.cfg")

if __name__ == "__main__":
    modify_lobby_cfg()
