import os

def update_char_db_instant():
    char_db = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg"
    
    with open(char_db, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if line.startswith("alias _db_char_") and "_char_inventory" in line:
            # Check which character (p1 or p2)
            if "_char_p2_badge" in line:
                badge = "_char_p2_badge"
            else:
                badge = "_char_p1_badge"
                
            if badge not in line.split(";")[-1]: # Don't add twice
                line = line.strip().rstrip(';') + f"; {badge}" + "\n"
        new_lines.append(line)
        
    with open(char_db, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("char_db.cfg updated with instant badge logic.")

if __name__ == "__main__":
    update_char_db_instant()
