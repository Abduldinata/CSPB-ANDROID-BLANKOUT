import os
import re

# Paths
stat_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\stat"
remove_stat_path = os.path.join(stat_dir, "remove_all_stat.cfg")

def restore_stat_paths():
    if not os.path.exists(remove_stat_path):
        return
    
    with open(remove_stat_path, "r", encoding='utf-8') as f:
        remove_lines = f.readlines()
    
    new_remove_lines = []
    restored_count = 0
    
    for line in remove_lines:
        match = re.search(r'touch_removebutton\s+"(stat_[^"]+)"', line)
        if match:
            stat_id = match.group(1)
            # Find the image path from the individual stat file
            # Most stat files are named stat_id minus "stat_" or similar.
            # Filename is usually stat_id.cfg (e.g. stat_aug.cfg)
            # Wait, let's just find the file in the directory.
            stat_file = os.path.join(stat_dir, f"{stat_id.replace('stat_', '')}.cfg")
            
            image_path = ""
            if os.path.exists(stat_file):
                with open(stat_file, "r", encoding='utf-8') as sf:
                    content = sf.read()
                    # Pattern: touch_addbutton "ID" "IMAGE" ...
                    img_match = re.search(r'touch_addbutton\s+"[^"]+"\s+"([^"]+)"', content)
                    if img_match:
                        image_path = img_match.group(1)
            
            if image_path:
                # Restore to the format the user had before (estimated)
                # touch_removebutton "ID" "IMAGE" "c" -0.02 0.00 1 1 255 255 255 255 4
                restored_line = f'touch_removebutton "{stat_id}" "{image_path}" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4\n'
                new_remove_lines.append(restored_line)
                restored_count += 1
            else:
                new_remove_lines.append(line)
        else:
            new_remove_lines.append(line)
            
    with open(remove_stat_path, "w", encoding='utf-8') as f:
        f.writelines(new_remove_lines)
    print(f"Restored {restored_count} image paths in remove_all_stat.cfg")

restore_stat_paths()
