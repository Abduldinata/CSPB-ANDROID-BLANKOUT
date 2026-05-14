import os

base_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# 1. Revert changes in persist/map/*.cfg (remove touch_removebutton)
persist_dir = os.path.join(base_dir, "persist", "map")
for fname in os.listdir(persist_dir):
    if fname.endswith(".cfg"):
        path = os.path.join(persist_dir, fname)
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
        
        # Remove lines containing the removal command we added earlier
        new_lines = [l for l in lines if 'touch_removebutton "_persist_map_badge"' not in l]
        
        if len(lines) != len(new_lines):
            with open(path, "w", encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Reverted {fname}")

# 2. Update select_map/map_db.cfg
db_path = os.path.join(base_dir, "select_map", "map_db.cfg")
with open(db_path, "r", encoding='utf-8') as f:
    content = f.read()

lines = content.splitlines()
new_lines = []
updated_count = 0

for line in lines:
    if line.strip().startswith("alias _db_map_"):
        # Check if already has removal command
        if "remove_all_map.cfg" not in line:
            parts = line.split('"')
            if len(parts) >= 3:
                # Inject removal execution
                cmd = parts[1]
                new_cmd = f"exec addons/neda/select_map/remove_all_map.cfg; {cmd}"
                line = f'{parts[0]}"{new_cmd}"{parts[2]}'
                updated_count += 1
    new_lines.append(line)

with open(db_path, "w", encoding='utf-8') as f:
    f.write("\n".join(new_lines))

print(f"Updated {updated_count} aliases in map_db.cfg")
