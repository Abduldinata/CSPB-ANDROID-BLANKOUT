import os

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

def restore_indicators():
    # 1. Fix Map Selection Files
    map_files = [
        "select_map/select_open1.cfg",
        "select_map/select_open2.cfg",
        "select_map/select_open3.cfg"
    ]
    
    for relative_path in map_files:
        path = os.path.join(root_dir, relative_path)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if indicator is already called
            if "_map_p1_indicator" not in content[-50:]:  # Check near end
                with open(path, 'a', encoding='utf-8') as f:
                    if not content.endswith('\n'):
                        f.write('\n')
                    f.write('_map_p1_indicator\n')
                print(f"Restored map indicator in {relative_path}")

    # 2. Fix Mode Files
    mode_files = [
        "mode/tdm.cfg",
        "mode/bm.cfg",
        "mode/sg.cfg",
        "mode/sniper.cfg",
        "mode/knife.cfg"
    ]
    
    for relative_path in mode_files:
        path = os.path.join(root_dir, relative_path)
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if indicator is already called
            if "_mode_indicator" not in content[-50:]:  # Check near end
                with open(path, 'a', encoding='utf-8') as f:
                    if not content.endswith('\n'):
                        f.write('\n')
                    f.write('_mode_indicator\n')
                print(f"Restored mode indicator in {relative_path}")

restore_indicators()
