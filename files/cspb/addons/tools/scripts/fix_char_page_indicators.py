import os

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"

chars = {
    "redteam": ["viper", "redbull", "tarantula", "dfox", "ricalopez"],
    "blueteam": ["acidpool", "keeneyes", "leopard", "hide", "judychou"]
}

# For character selection pages, the indicator needed is _char_p1_badge or _char_p2_badge
# plus all the full indicator chain via _add_indicators_char_inv
# character/page1.cfg -> page1 of char select
# character/page2.cfg -> page2 of char select
char_page_indicators = {
    "character":  [("page1.cfg", "_char_p1_badge"), ("page2.cfg", "_char_p2_badge")],
    "character2": [("page1.cfg", "_char_p1_badge"), ("page2.cfg", "_char_p2_badge")],
}

fixed = 0

for team, char_list in chars.items():
    for char in char_list:
        for folder, pages in char_page_indicators.items():
            folder_path = os.path.join(base_path, team, char, folder)
            if not os.path.isdir(folder_path):
                continue
            
            for page_file, badge_alias in pages:
                page_path = os.path.join(folder_path, page_file)
                if not os.path.isfile(page_path):
                    continue
                
                with open(page_path, "r") as f:
                    content = f.read()
                
                changed = False
                
                # Add badge alias if missing
                if badge_alias not in content:
                    content = content.rstrip() + f"\n\n{badge_alias}\n"
                    changed = True
                
                # Add _add_indicators_char_inv if missing
                if "_add_indicators_char_inv" not in content:
                    content = content.rstrip() + f"\n_add_indicators_char_inv\n"
                    changed = True
                
                if changed:
                    with open(page_path, "w") as f:
                        f.write(content)
                    print(f"Fixed: {team}/{char}/{folder}/{page_file}")
                    fixed += 1

print(f"\nTotal fixed: {fixed}")
