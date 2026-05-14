import os
import glob
import re

# Paths
persist_map_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\map"
tga_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\image\map"

# List available TGAs (just the filenames without extensions for comparison)
available_tgas = {os.path.splitext(f)[0].lower(): f for f in os.listdir(tga_dir) if f.endswith(".tga")}

print(f"Available TGAs: {list(available_tgas.keys())}")

def fix_map_tga_paths():
    files = glob.glob(os.path.join(persist_map_dir, "*.cfg"))
    count = 0
    
    for file_path in files:
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
            
        # Extract the current TGA path from the cfg
        match = re.search(r'addons/neda/image/map/([^"]+\.tga)', content)
        if match:
            current_tga_full = match.group(1)
            current_tga_base = os.path.splitext(current_tga_full)[0].lower()
            
            # Check if it matches exactly
            if current_tga_full.lower() in [f.lower() for f in os.listdir(tga_dir)]:
                # Match found, check for case sensitivity or exact name
                actual_tga = [f for f in os.listdir(tga_dir) if f.lower() == current_tga_full.lower()][0]
                if current_tga_full != actual_tga:
                    new_content = content.replace(current_tga_full, actual_tga)
                    with open(file_path, "w", encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed case: {os.path.basename(file_path)} ({current_tga_full} -> {actual_tga})")
                    count += 1
            else:
                # No exact match. Try fuzzy matching (removing underscores, etc.)
                fuzzy_name = current_tga_base.replace("_", "")
                found = False
                for tga_base, tga_file in available_tgas.items():
                    if tga_base.replace("_", "") == fuzzy_name:
                        new_content = content.replace(current_tga_full, tga_file)
                        with open(file_path, "w", encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed mismatch: {os.path.basename(file_path)} ({current_tga_full} -> {tga_file})")
                        count += 1
                        found = True
                        break
                
                if not found:
                    print(f"WARNING: No TGA found for {os.path.basename(file_path)} (Path: {current_tga_full})")
                    
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    fix_map_tga_paths()
