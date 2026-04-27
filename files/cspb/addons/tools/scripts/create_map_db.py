import os
import glob

def create_map_db():
    # Find all map files in persist/map/
    map_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\map"
    map_files = glob.glob(os.path.join(map_dir, "*.cfg"))
    
    output_file = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_map\map_db.cfg"
    
    with open(output_file, "w", encoding='utf-8') as f:
        f.write("// Map Persistence Database\n")
        f.write("// This file defines all map persistence aliases\n\n")
        
        # Define reset alias
        f.write("// Badge Reset\n")
        f.write('alias _reset_map_indicators "touch_removebutton _persist_map_badge"\n\n')
        
        for map_file in sorted(map_files):
            map_name = os.path.splitext(os.path.basename(map_file))[0]
            
            # Create alias for this map
            f.write(f'alias _db_map_{map_name} "_reset_map_indicators; alias _map_indicator \\\"exec addons/neda/persist/map/{map_name}.cfg\\\"; _map_indicator"\n')
        
        f.write("\n// Default\n")
        f.write('alias _map_indicator "_blank"\n')
    
    print(f"Created {output_file} with {len(map_files)} maps")
    
    # Now update map.cfg to load this file
    map_cfg = r"e:\Games\PROJECT LOBBY CSPB\addons\map.cfg"
    with open(map_cfg, "r", encoding='utf-8') as f:
        content = f.read()
    
    if "exec addons/neda/select_map/map_db.cfg" not in content:
        with open(map_cfg, "a", encoding='utf-8') as f:
            f.write("\n// Load Map Persistence System\n")
            f.write("exec addons/neda/select_map/map_db.cfg\n")
        print("Added load map_db to map.cfg")

if __name__ == "__main__":
    create_map_db()
