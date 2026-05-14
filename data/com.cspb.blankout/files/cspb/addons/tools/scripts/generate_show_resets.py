import os
import re

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main"

# Collect all item names
item_names = set()

for root, _, files in os.walk(root_dir):
    for f in files:
        if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
            basename = os.path.splitext(f)[0]
            item_names.add(basename)

# Generate reset scripts for each category
categories = {
    "weapon": r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\reset_indicators.cfg",
    "secondary": r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\secondary\reset_indicators.cfg",
    "melee": r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\melee\reset_indicators.cfg",
    "explosive": r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\explosive\reset_indicators.cfg",
    "special": r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\special\reset_indicators.cfg"
}

for category, reset_path in categories.items():
    if os.path.exists(reset_path):
        with open(reset_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find items in this category's directory
        category_dir = os.path.dirname(reset_path)
        category_items = []
        
        for root, _, files in os.walk(category_dir):
            for f in files:
                if f.endswith(".cfg") and not f.startswith("reset_") and f != "persist_db.cfg":
                    basename = os.path.splitext(f)[0]
                    category_items.append(basename)
        
        # Add show alias resets
        for item in sorted(set(category_items)):
            reset_line = f'alias _show_equip_{item} ""\n'
            if f'_show_equip_{item}' not in content:
                content += reset_line
        
        with open(reset_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Updated {category} reset_indicators.cfg with {len(set(category_items))} show alias resets")

print("All reset scripts updated.")
