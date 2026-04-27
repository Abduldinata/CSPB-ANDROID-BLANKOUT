import os

persist_map_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\map"

def add_removal_to_persist_maps():
    """Add touch_removebutton _persist_map_badge before addbutton to prevent stacking"""
    processed = 0
    
    for filename in os.listdir(persist_map_dir):
        if filename.endswith(".cfg"):
            path = os.path.join(persist_map_dir, filename)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if removal already exists
            if 'touch_removebutton "_persist_map_badge"' in content:
                continue
                
            # Insert removal before addbutton
            lines = content.splitlines()
            new_lines = []
            modified = False
            
            for line in lines:
                if 'touch_addbutton "_persist_map_badge"' in line and not modified:
                    new_lines.append('touch_removebutton "_persist_map_badge"')
                    new_lines.append(line)
                    modified = True
                else:
                    new_lines.append(line)
            
            if modified:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(new_lines))
                processed += 1
                print(f"Updated {filename}")
    
    return processed

count = add_removal_to_persist_maps()
print(f"\nUpdated {count} map persistence files.")
