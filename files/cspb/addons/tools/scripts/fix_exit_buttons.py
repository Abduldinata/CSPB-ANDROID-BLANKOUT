import os
import glob
import re

def fix_exit_buttons():
    base_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"
    patterns = ["*.cfg", "*/*.cfg", "*/*/*.cfg", "*/*/*/*.cfg"]
    
    files_to_process = []
    for pattern in patterns:
        files_to_process.extend(glob.glob(os.path.join(base_dir, pattern)))
    
    count = 0
    
    for file_path in files_to_process:
        try:
            with open(file_path, "r", encoding='utf-8') as f:
                lines = f.readlines()
        except:
            continue
            
        new_lines = []
        changed = False
        
        for line in lines:
            # Cari tombol _lobby_out
            if 'touch_addbutton "_lobby_out' in line:
                # Cek apakah sudah ada _rmv_persist_all atau _full_exit
                if '_rmv_persist_all' not in line and '_full_exit' not in line:
                    # Sisipkan _rmv_persist_all sebelum penutup command
                    # Format: touch_addbutton "name" "img" "command" ...
                    # Kita cari command string
                    parts = line.split('"')
                    if len(parts) >= 6:
                        command = parts[5]
                        # Tambahkan _rmv_persist_all di akhir command
                        new_command = command.strip()
                        if not new_command.endswith(';'):
                            new_command += '; '
                        new_command += '_rmv_persist_all'
                        
                        # Reconstruct line
                        new_line = line.replace(command, new_command)
                        new_lines.append(new_line)
                        changed = True
                        continue
            
            new_lines.append(line)
            
        if changed:
            with open(file_path, "w", encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Fixed exit button in: {os.path.basename(file_path)}")
            count += 1
            
    print(f"Total files fixed: {count}")

if __name__ == "__main__":
    fix_exit_buttons()
