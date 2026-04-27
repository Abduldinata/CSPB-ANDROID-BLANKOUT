import os
import glob

def add_indicators_to_char_inventory():
    # Find all inventory_character.cfg files
    patterns = [
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\blueteam\*\inventory_character.cfg",
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\redteam\*\inventory_character.cfg"
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))
    
    for filepath in files:
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Check if _add_indicators already exists
        if "_add_indicators" in content:
            print(f"Already has _add_indicators: {os.path.basename(os.path.dirname(filepath))}/inventory_character.cfg")
            continue
        
        # Add _add_indicators at the end
        content = content.rstrip() + "\n\n// Restore Persistence Badges\n_add_indicators\n"
        
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(content)
        
        print(f"Added _add_indicators to: {os.path.basename(os.path.dirname(filepath))}/inventory_character.cfg")
    
    print(f"\nTotal processed: {len(files)} files")

if __name__ == "__main__":
    add_indicators_to_char_inventory()
