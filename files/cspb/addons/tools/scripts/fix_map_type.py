import glob
import re

def fix_map_config_types():
    # Target all files in neda/persist/map/
    files = glob.glob(r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\map\*.cfg")
    
    count = 0
    for filepath in files:
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
        
        # Look for the touch_addbutton line ending in 5
        # Example: ... 255 255 255 255  4
        if re.search(r'255 5\s*$', content, re.MULTILINE):
            new_content = re.sub(r'(255 255 255 255) 5(\s*)$', r'\1 4\2', content, flags=re.MULTILINE)
            
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed type 5 -> 4 in: {filepath}")
            
    print(f"Total map files fixed: {count}")

if __name__ == "__main__":
    fix_map_config_types()
