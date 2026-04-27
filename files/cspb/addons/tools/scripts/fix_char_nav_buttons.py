import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"

chars = {
    "redteam": ["viper", "redbull", "tarantula", "dfox", "ricalopez"],
    "blueteam": ["acidpool", "keeneyes", "leopard", "hide", "judychou"]
}

# Buttons that should NOT be in character selection pages
buttons_to_remove_patterns = [
    r'touch_addbutton\s+"_lobby_inventory_second\d*"[^\n]*\n',
    r'touch_addbutton\s+"_lobby_inventory_melee\d*"[^\n]*\n',
    r'touch_addbutton\s+"_lobby_inventory_special\d*"[^\n]*\n',
    r'touch_addbutton\s+"_lobby_inventory_explosive\d*"[^\n]*\n',
]

# Comments associated with those buttons (also remove)
comment_patterns = [
    r'//secondary inventory page\r?\n',
    r'//melee inventory page\r?\n',
    r'//special page\r?\n',
    r'//explosive page\r?\n',
]

fixed_files = 0

for team, char_list in chars.items():
    for char in char_list:
        # Process character/ and character2/ folders
        for char_folder in ["character", "character2"]:
            char_path = os.path.join(base_path, team, char, char_folder)
            if not os.path.isdir(char_path):
                continue
            
            for page_file in os.listdir(char_path):
                if not page_file.endswith(".cfg"):
                    continue
                
                page_path = os.path.join(char_path, page_file)
                with open(page_path, "r") as f:
                    content = f.read()
                
                new_content = content
                
                # Remove button lines
                for pat in buttons_to_remove_patterns:
                    new_content = re.sub(pat, "", new_content)
                
                # Remove comment lines
                for pat in comment_patterns:
                    new_content = re.sub(pat, "", new_content)
                
                if new_content != content:
                    with open(page_path, "w") as f:
                        f.write(new_content)
                    print(f"Fixed: {team}/{char}/{char_folder}/{page_file}")
                    fixed_files += 1

print(f"\nTotal character page files fixed: {fixed_files}")
