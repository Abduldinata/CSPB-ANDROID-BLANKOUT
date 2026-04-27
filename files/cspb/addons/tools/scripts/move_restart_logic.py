import glob
import os
import re

def move_restart_logic():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
    
    # 1. Remove 'restart' from mode/cmd/*.cfg
    mode_cmd_path = os.path.join(base_path, "mode", "cmd")
    mode_files = glob.glob(os.path.join(mode_cmd_path, "*.cfg"))
    
    for filepath in mode_files:
        if "remove" in filepath: continue # Skip remove scripts
        
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
            
        # Replace 'restart;' or 'restart' with nothing
        # Case insensitive regex
        new_content = re.sub(r';?\s*restart\s*;?', '', content, flags=re.IGNORECASE)
        
        if content != new_content:
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(new_content)
            print(f"Removed restart from: {os.path.basename(filepath)}")

    # 2. Add 'restart' to Start Buttons in team/team_*.cfg
    team_path = os.path.join(base_path, "team")
    team_files = glob.glob(os.path.join(team_path, "team_*.cfg"))
    
    # Patterns for start buttons
    # touch_addbutton "_lobby_start_blue1" ... "_team_blue1"
    # We want to append "; restart" after "_team_blue1" or at end of command string
    
    # Regex to find the start button line
    # Looks for _lobby_start_... and captures the third argument (command string)
    # The command string is inside quotes.
    
    for filepath in team_files:
        with open(filepath, "r", encoding='utf-8') as f:
            lines = f.readlines()
            
        modified = False
        new_lines = []
        
        for line in lines:
            if "_lobby_start_" in line and "touch_addbutton" in line:
                # Basic check if restart is already there
                if "restart" in line:
                    new_lines.append(line)
                    continue

                # We need to insert '; restart' before the closing quote of the command string
                # The line format: touch_addbutton "name" "image" "command" x y x y r g b a t
                # We can split by quotes.
                parts = line.split('"')
                if len(parts) >= 6:
                    command_str = parts[5] # 0=pre, 1=name, 2=gap, 3=image, 4=gap, 5=command
                    # Append restart to command
                    if command_str.strip().endswith(";"):
                         new_command = command_str + " restart"
                    else:
                         new_command = command_str + "; restart"
                    
                    parts[5] = new_command
                    new_line = '"'.join(parts)
                    new_lines.append(new_line)
                    modified = True
                    print(f"Added restart to: {os.path.basename(filepath)}")
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
        
        if modified:
            with open(filepath, "w", encoding='utf-8') as f:
                f.writelines(new_lines)

if __name__ == "__main__":
    move_restart_logic()
