import glob
import os

def restore_loading_screens():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"
    pattern = os.path.join(base_path, "**", "lobby_menu3_load.cfg")
    files = glob.glob(pattern, recursive=True)
    
    for filepath in files:
        # Determine image path based on file location
        # Default for generic neda/lobby_menu3_load.cfg
        image_path = "addons/neda/image/lobby3_load.tga"
        
        # Check if it's in a team folder
        parts = filepath.replace("\\", "/").split("/")
        # e.g., .../addons/neda/redteam/viper/lobby_menu3_load.cfg
        if "redteam" in parts or "blueteam" in parts:
            # The character name is usually the parent folder
            character_name = parts[-2]
            image_path = f"addons/neda/image/{character_name}/lobby3_load.tga"
        
        content = f"""touch_addbutton "_lobby_bg3_load" "{image_path}" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4 ;wait;wait;wait;wait;wait;wait
touch_addbutton "_lobby_bg3_load" "{image_path}" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4 ;wait;wait;wait;wait;wait
touch_addbutton "_lobby_bg3_load" "{image_path}" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4 ;wait;wait;wait;wait;
touch_addbutton "_lobby_bg3_load" "{image_path}" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4 ;wait;wait;wait;wait;
touch_addbutton "_lobby_bg3_load" "{image_path}" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4 ;wait;wait;wait;wait
touch_removebutton "_lobby_bg3_load"

// Restore Persistence Badges
_add_indicators
"""
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"Restored: {filepath} with image {image_path}")

if __name__ == "__main__":
    restore_loading_screens()
