import glob
import os

def inject_equip_logic():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"
    
    # Map categories to their folders
    categories = {
        "secondary": ["secondary"],
        "melee": ["melee"],
        "explosive": ["explosive"],
        "special": ["special"]
    }
    
    count = 0
    
    for category, folders in categories.items():
        for folder in folders:
            # Recursively find all .cfg files in page subdirectories
            files = glob.glob(os.path.join(base_path, folder, "page*", "*.cfg"))
            
            for filepath in files:
                filename = os.path.basename(filepath).replace('.cfg', '')
                
                # Construct the _show_equip alias name
                alias_name = f"_show_equip_{filename}"
                
                with open(filepath, "r", encoding='utf-8') as f:
                    content = f.read()
                
                # Check if alias call already exists
                if alias_name in content:
                    print(f"Skipping {filename}: already has equip logic")
                    continue
                
                # Add the alias call to the end of the file
                # Ensure there's a newline before it
                new_content = content.rstrip() + f"\n\n{alias_name}\n"
                
                with open(filepath, "w", encoding='utf-8') as f:
                    f.write(new_content)
                
                count += 1
                print(f"Injected {alias_name} into {filename}")

    print(f"Total files updated: {count}")

if __name__ == "__main__":
    inject_equip_logic()
