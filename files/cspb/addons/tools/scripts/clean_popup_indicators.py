import os
import glob
import re

# Root directory
base_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# Target directories/files that are considered "POPUP" or "SECONDARY"
# These should NOT have persistent map/mode indicators visible on top of them
target_patterns = [
    os.path.join(base_dir, "team", "team_*.cfg"),
    os.path.join(base_dir, "redteam", "*", "team_*.cfg"),
    os.path.join(base_dir, "blueteam", "*", "team_*.cfg"),
    os.path.join(base_dir, "team_red_fade_in.cfg"),
    os.path.join(base_dir, "team_blue_fade_in.cfg"),
    os.path.join(base_dir, "change_team_fade_in.cfg"),
]

indicators_to_remove = [
    "_map_p1_indicator",
    "_map_p2_indicator",
    "_map_p3_indicator",
    "_mode_indicator",
    "_add_indicators"
]

def clean_popup_files():
    count = 0
    files_to_process = []
    for pattern in target_patterns:
        files_to_process.extend(glob.glob(pattern))
    
    # Remove duplicates
    files_to_process = list(set(files_to_process))
    
    for file_path in files_to_process:
        with open(file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        changed = False
        for line in lines:
            stripped = line.strip()
            # Remove the line if it's just one of the indicators
            if stripped in indicators_to_remove:
                changed = True
                continue
            # Remove them even if they are at the end of a line or part of a sequence?
            # Actually, most of them are on their own line at the end of the file.
            # But just in case:
            new_line = line
            for ind in indicators_to_remove:
                # Only remove if it's a standalone word or at the end
                # (to avoid hitting touch_addbutton params)
                pattern = r'(?<!\w)' + re.escape(ind) + r'(?!\w)'
                if re.search(pattern, new_line):
                    # Special check: don't remove if it's inside a touch_addbutton command string
                    # unless it's a specific popup file where we definitely don't want it.
                    # For now, let's just remove the standalone calls at the end of files.
                    if "touch_addbutton" not in new_line:
                        new_line = re.sub(pattern, "", new_line).strip() + "\n"
                        changed = True
            
            if new_line.strip() or not line.strip(): # keep empty lines or non-empty results
                new_lines.append(new_line)

        if changed:
            with open(file_path, "w", encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Cleaned indicators from: {os.path.basename(file_path)}")
            count += 1
            
    print(f"Total files cleaned: {count}")

if __name__ == "__main__":
    clean_popup_files()
