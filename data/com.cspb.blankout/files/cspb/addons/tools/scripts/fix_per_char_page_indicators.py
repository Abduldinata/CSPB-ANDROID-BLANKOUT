import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"

# Characters and their team folders
chars = {
    "redteam": ["viper", "redbull", "tarantula", "dfox", "ricalopez"],
    "blueteam": ["acidpool", "keeneyes", "leopard", "hide", "judychou"]
}

# Categories and their indicator patterns
# (folder_name, indicator_prefix, indicator_per_page)
categories = [
    # (subfolder_name, indicator_alias_prefix, pages with that indicator number)
    ("weapons",   "_weap_p",  [("page1.cfg",  "1"), ("page2.cfg",  "2"), ("page3.cfg",  "3"),
                                ("page4.cfg",  "4"), ("page5.cfg",  "5"), ("page6.cfg",  "6"),
                                ("page7.cfg",  "7"), ("page8.cfg",  "8"), ("page9.cfg",  "9"),
                                ("page10.cfg", "10"), ("page11.cfg", "11")]),
    ("weapons2",  "_weap_p",  [("page1.cfg",  "1"), ("page2.cfg",  "2"), ("page3.cfg",  "3"),
                                ("page4.cfg",  "4"), ("page5.cfg",  "5"), ("page6.cfg",  "6"),
                                ("page7.cfg",  "7"), ("page8.cfg",  "8"), ("page9.cfg",  "9"),
                                ("page10.cfg", "10"), ("page11.cfg", "11")]),
    ("secondary",  "_sec_p",  [("page1.cfg", "1"), ("page2.cfg", "2"), ("page3.cfg", "3"), ("page4.cfg", "4")]),
    ("secondary2", "_sec_p",  [("page1.cfg", "1"), ("page2.cfg", "2"), ("page3.cfg", "3"), ("page4.cfg", "4")]),
    ("melee",      "_melee_p",[("page1.cfg", "1"), ("page2.cfg", "2"), ("page3.cfg", "3"), ("page4.cfg", "4")]),
    ("melee2",     "_melee_p",[("page1.cfg", "1"), ("page2.cfg", "2"), ("page3.cfg", "3"), ("page4.cfg", "4")]),
    ("explosive",  "_explosive_p", [("page1.cfg", "1"), ("page2.cfg", "2")]),
    ("explosive2", "_explosive_p", [("page1.cfg", "1"), ("page2.cfg", "2")]),
    ("special",    "_special_p",   [("page1.cfg", "1"), ("page2.cfg", "2")]),
    ("special2",   "_special_p",   [("page1.cfg", "1"), ("page2.cfg", "2")]),
]

fixed = 0
indicator_added = 0
add_inv_added = 0

for team, char_list in chars.items():
    for char in char_list:
        char_path = os.path.join(base_path, team, char)
        if not os.path.isdir(char_path):
            continue
        
        for (folder, ind_prefix, pages) in categories:
            folder_path = os.path.join(char_path, folder)
            if not os.path.isdir(folder_path):
                continue
            
            for (page_file, page_num) in pages:
                page_path = os.path.join(folder_path, page_file)
                if not os.path.isfile(page_path):
                    continue
                
                with open(page_path, 'r') as f:
                    content = f.read()
                
                changed = False
                indicator_alias = f"{ind_prefix}{page_num}_indicator"
                
                # Check if the indicator call exists
                if indicator_alias not in content:
                    # Append indicator call before end of file
                    content = content.rstrip()
                    content += f"\n\n{indicator_alias}\n"
                    changed = True
                    indicator_added += 1
                
                # Check if _add_indicators_char_inv is present at end
                if "_add_indicators_char_inv" not in content:
                    content = content.rstrip()
                    content += f"\n_add_indicators_char_inv\n"
                    changed = True
                    add_inv_added += 1
                
                if changed:
                    with open(page_path, 'w') as f:
                        f.write(content)
                    fixed += 1
                    print(f"Fixed: {team}/{char}/{folder}/{page_file}")

print(f"\nTotal files fixed: {fixed}")
print(f"  Indicator calls added: {indicator_added}")
print(f"  _add_indicators_char_inv calls added: {add_inv_added}")
