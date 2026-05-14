import os

team_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"
root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

files_to_clean = []

# Add class configs
for fname in os.listdir(team_dir):
    if fname.endswith(".cfg") and ("blue_class" in fname or "red_class" in fname):
        files_to_clean.append(os.path.join(team_dir, fname))

# Add main team configs
files_to_clean.append(os.path.join(root_dir, "team_blue.cfg"))
files_to_clean.append(os.path.join(root_dir, "team_red.cfg"))

cleaned_count = 0

for path in files_to_clean:
    if not os.path.exists(path):
        continue
        
    with open(path, "r", encoding='utf-8') as f:
        lines = f.readlines()
    
    # Remove lines triggering map indicators explicitly
    # We remove p1, p2, p3 just in case
    new_lines = []
    modified = False
    for line in lines:
        stripped = line.strip()
        if stripped in ["_map_p1_indicator", "_map_p2_indicator", "_map_p3_indicator"]:
            modified = True
            continue 
        new_lines.append(line)
    
    if modified:
        with open(path, "w", encoding='utf-8') as f:
            f.writelines(new_lines)
        cleaned_count += 1
        print(f"Cleaned {os.path.basename(path)}")

print(f"Total files cleaned: {cleaned_count}")
