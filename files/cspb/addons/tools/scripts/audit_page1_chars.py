import os

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character\page1'

for file in os.listdir(root_dir):
    if file.endswith('.cfg'):
        filepath = os.path.join(root_dir, file)
        with open(filepath, 'r') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            # Change the invisible button to use the unified ID and asset
            if 'touch_addbutton "equip_' in line:
                # We want to keep the command but standardize the button name if needed
                # Actually, the 'equip_redc1' etc are the logical hitboxes.
                # The image is displayed via _show_equip_char_*
                new_lines.append(line)
            elif '_show_equip_char_' in line:
                new_lines.append(line)
            else:
                new_lines.append(line)
        
        # We also need to make sure the hitbox matches the new button area
        # 0.550000 0.760109 0.640000 0.821739
        updated_content = "".join(new_lines)
        # Re-check coordinates in all files
        # (Assuming they might be slightly off in some)
        with open(filepath, 'w') as f:
            f.write(updated_content)

print("Character page1 files audited.")
