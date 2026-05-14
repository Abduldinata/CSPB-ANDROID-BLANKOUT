import os

reset_files = [
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\weapon\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\secondary\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\melee\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\explosive\reset_indicators.cfg",
    r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_main\special\reset_indicators.cfg"
]

for reset_file in reset_files:
    if os.path.exists(reset_file):
        with open(reset_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove _equipped_item line
        content = content.replace('alias _equipped_item ""\n', '')
        content = content.replace('alias _equipped_item ""\r\n', '')
        
        with open(reset_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Cleaned {os.path.basename(reset_file)}")

print("Reset scripts cleaned.")
