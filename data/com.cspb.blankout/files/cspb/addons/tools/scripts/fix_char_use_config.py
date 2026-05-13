import glob
import re

def fix_char_use_configs():
    # Target all files in neda/persist/character/
    files = glob.glob(r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\character\*.cfg")
    
    count = 0
    for filepath in files:
        with open(filepath, "r", encoding='utf-8') as f:
            content = f.read()
            
        # Look for touch_addbutton ... "" -0.02
        # Change "" to "c"
        if '"" -0.02' in content:
            new_content = content.replace('"" -0.02', '"c" -0.02')
            
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(new_content)
            count += 1
            print(f"Fixed '\"\"' -> '\"c\"' in: {filepath}")
            
    print(f"Total character use files fixed: {count}")

if __name__ == "__main__":
    fix_char_use_configs()
