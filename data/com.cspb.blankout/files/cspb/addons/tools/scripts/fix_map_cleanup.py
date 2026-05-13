import os

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_map"

# 1. Update remove_all_map.cfg (and version 2 & 3)
remove_files = [
    "remove_all_map.cfg",
    "remove_all_map2.cfg",
    "remove_all_map3.cfg"
]

cleanup_command = 'touch_removebutton "_persist_map_badge" "" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4'

for fname in remove_files:
    path = os.path.join(root_dir, fname)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add persistence cleanup if missing
        if "_persist_map_badge" not in content:
            with open(path, 'a', encoding='utf-8') as f:
                if not content.endswith('\n'):
                    f.write('\n')
                f.write(f'{cleanup_command}\n')
            print(f"Updated {fname} with persistence cleanup")

# 2. Update remove_selectmap.cfg
select_files = ["remove_selectmap.cfg"]

for fname in select_files:
    path = os.path.join(root_dir, fname)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ensure it removes the specific open/close buttons potentially stuck
        # (This file generally looks fine based on view_file, but let's ensure it covers everything)
        pass 

print("Map cleanup scripts updated.")
