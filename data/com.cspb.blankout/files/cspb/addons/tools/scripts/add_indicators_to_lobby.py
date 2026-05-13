import os

def add_indicators_to_lobbies():
    # Files to update
    files = [
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\lobby_menu.cfg",
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\lobby_menu2.cfg",
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\lobby_menu3.cfg",
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\lobby_menu3_load.cfg",
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\lobby_menu4.cfg",
    ]
    
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue
            
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
        
        if "_add_indicators" in content:
            print(f"Already has _add_indicators: {os.path.basename(file_path)}")
            continue
        
        # Add _add_indicators at the end
        content = content.rstrip() + "\n\n// Restore Persistence Badges\n_add_indicators\n"
        
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        
        print(f"Added _add_indicators to: {os.path.basename(file_path)}")

if __name__ == "__main__":
    add_indicators_to_lobbies()
