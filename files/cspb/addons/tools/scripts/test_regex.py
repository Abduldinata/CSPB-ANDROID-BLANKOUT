import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
layout_dir = os.path.join(base_path, "blueteam", "acidpool", "weapons")

item_map = {}
for fname in os.listdir(layout_dir):
    if fname.startswith("page") and fname.endswith(".cfg"):
        page_num = int(re.search(r"page(\d+)", fname).group(1))
        with open(os.path.join(layout_dir, fname), "r") as f:
            lines = f.readlines()
            
        print(f"Scanning {fname} (Page {page_num})")
        for line in lines:
            # We want to match: "_lobby_select1" ... "_sl_aug"
            # It could also be _sl_something_with_underscores
            match = re.search(r'"_lobby_select(\d+)".*?_sl_([a-zA-Z0-9_]+)', line)
            if match:
                slot_num = int(match.group(1))
                item_name = match.group(2)
                item_map[item_name] = (page_num, slot_num)
                print(f"  Match: slot {slot_num}, item {item_name}")
                
print(f"Total items found: {len(item_map)}")
