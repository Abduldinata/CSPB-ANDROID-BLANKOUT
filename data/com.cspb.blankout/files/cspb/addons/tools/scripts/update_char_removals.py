import os

# 1. Update character/remove_page*.cfg
dir_pages = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\character'
for i in range(1, 3):
    filename = f'remove_page{i}.cfg'
    filepath = os.path.join(dir_pages, filename)
    if os.path.exists(filepath):
        with open(filepath, 'a') as f:
            f.write("touch_removebutton \"_persist_char_badge1\"\ntouch_removebutton \"_persist_char_badge2\"\n")

# 2. Update all remove_inventory_character.cfg
root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file == 'remove_inventory_character.cfg':
            filepath = os.path.join(root, file)
            with open(filepath, 'a') as f:
                f.write("_rmv_persist_all\n")

print("Updated character removal scripts.")
