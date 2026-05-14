import os
import glob

def fix_char_inventory_loader():
    # Targets: addons/neda/*team/*/inventory_character.cfg
    base_dirs = [
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\redteam",
        r"e:\Games\PROJECT LOBBY CSPB\addons\neda\blueteam"
    ]
    
    for base_dir in base_dirs:
        # Search for all character folders
        char_folders = glob.glob(os.path.join(base_dir, "*"))
        for char_folder in char_folders:
            inv_file = os.path.join(char_folder, "inventory_character.cfg")
            if os.path.exists(inv_file):
                with open(inv_file, "r", encoding='utf-8') as f:
                    content = f.read()
                
                # Check if it calls _chr_prevpage1 (loader)
                if "_chr_prevpage1" not in content and "page1.cfg" not in content:
                    print(f"Fixing loader in {inv_file}")
                    with open(inv_file, "a", encoding='utf-8') as f:
                        f.write("\n// Load Generic Character List\n_chr_prevpage1\n")
                else:
                    print(f"Loader already present in {inv_file}")

if __name__ == "__main__":
    fix_char_inventory_loader()
