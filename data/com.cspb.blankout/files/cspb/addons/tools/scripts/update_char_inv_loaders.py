import os

def update_char_inv_loaders():
    # We need to find all inventory_character.cfg files
    # The grep previously showed they are in redteam/character_name/ folders
    base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
    
    count = 0
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == "inventory_character.cfg" or file == "inventory_character2.cfg":
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "_add_indicators" in content and "_add_indicators_char_inv" not in content:
                    new_content = content.replace("_add_indicators", "_add_indicators_char_inv")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {filepath}")
                    count += 1
    print(f"Total files updated: {count}")

if __name__ == "__main__":
    update_char_inv_loaders()
