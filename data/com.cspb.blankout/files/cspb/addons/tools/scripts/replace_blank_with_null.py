import glob
import os

def replace_blank_with_null():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist"
    
    # Files to process
    files = [
        "weapon_db.cfg", "char_db.cfg", "map_db.cfg", "mode_db.cfg",
        "secondary_db.cfg", "melee_db.cfg", "explosive_db.cfg", "special_db.cfg"
    ]
    
    # Also check character_persistence.cfg in main directory
    extra_files = [r"e:\Games\PROJECT LOBBY CSPB\addons\neda\character_persistence.cfg"]

    for filename in files:
        filepath = os.path.join(base_path, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
            
        # Replace alias ... "_blank" with alias ... "_null"
        # Be careful not to replace "exec addons/neda/blank.cfg" if it exists in these files (unlikely in DBs)
        
        # Safe replacement: replace ' "_blank"' with ' "_null"'
        new_content = content.replace(' "_blank"', ' "_null"')
        # Also replace " _blank" at end of line? 
        # In char_db.cfg: alias _char_p2_badge _blank
        new_content = new_content.replace(' _blank"', ' "_null"') # fix for "alias ... _blank"
        new_content = new_content.replace(' _blank', ' _null')

        if content != new_content:
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filename}")

    for filepath in extra_files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
            
        new_content = content.replace(' "_blank"', ' "_null"')
        new_content = new_content.replace(' _blank', ' _null')
        
        if content != new_content:
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(filepath)}")

if __name__ == "__main__":
    replace_blank_with_null()
