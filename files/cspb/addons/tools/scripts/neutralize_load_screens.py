import glob
import os

def neutralize_loading_screens():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"
    
    # Pattern to find all lobby_menu3_load.cfg files recursively
    # This includes the main one in neda/ and ones in team subdirectories
    pattern = os.path.join(base_path, "**", "lobby_menu3_load.cfg")
    files = glob.glob(pattern, recursive=True)
    
    content_to_write = "// Loading screen disabled by user request\n_add_indicators\n"
    
    count = 0
    for filepath in files:
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(content_to_write)
        print(f"Neutralized: {filepath}")
        count += 1
        
    print(f"Total files neutralized: {count}")

if __name__ == "__main__":
    neutralize_loading_screens()
