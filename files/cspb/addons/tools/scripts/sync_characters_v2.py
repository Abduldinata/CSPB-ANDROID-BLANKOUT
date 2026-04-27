import os

# Base directory
team_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"

# Mapping: filename -> correct character name
identity_map = {
    "team_red_class1.cfg": "redbull",
    "team_red_class2.cfg": "tarantula",
    "team_red_class3.cfg": "dfox",
    "team_red_class4.cfg": "viper",
    "team_red_class5.cfg": "ricalopez",
    "team_blue_class1.cfg": "acidpool",
    "team_blue_class2.cfg": "keeneyes",
    "team_blue_class3.cfg": "leopard",
    "team_blue_class4.cfg": "hide",
    "team_blue_class5.cfg": "judychou"
}

def sync_identities():
    count = 0
    for filename, char in identity_map.items():
        path = os.path.join(team_dir, filename)
        if not os.path.exists(path):
            continue
            
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
        
        new_lines = []
        for line in lines:
            line_str = line.strip()
            if not line_str:
                new_lines.append(line)
                continue
                
            # 1. Fix lobby exec (e.g., exec addons/lobby_acidpool.cfg)
            if line_str.startswith("exec addons/lobby_"):
                new_lines.append(f"exec addons/lobby_{char}.cfg\n")
                continue
                
            # 2. Fix image path (e.g., touch_addbutton "_lobby_teamblue_class1" "addons/neda/image/blue/acidpool.tga" ...)
            if 'addons/neda/image' in line_str and '.tga"' in line_str:
                import re
                # Replaces the filename after the last slash and before .tga
                fixed_line = re.sub(r'(/)[^/]+\.tga"', r'/' + char + r'.tga"', line)
                new_lines.append(fixed_line)
                continue

            # 3. Fix other prefixed commands (Massive identity sync)
            # This is complex to do with simple string replace because characters overlap (e.g. viper and viperred)
            # But here we only have the TARGET character 'char'. 
            # I will use a regex that looks specifically for character-suffixed aliases.
            import re
            # List of known suffixes we might have used or found
            old_chars = ["redbull", "tarantula", "dfox", "viper", "viperred", "ricalopez", "acidpool", "keeneyes", "leopard", "hide", "judychou", "natasha", "queen"]
            
            new_line = line
            for old in old_chars:
                if old != char:
                    # Replace only when it's at the end of a command part or followed by a ; or "
                    # Example: _back_3_dfox -> _back_3_redbull
                    new_line = re.sub(r'([a-z0-9_]+_)' + old + r'([; "\n])', r'\1' + char + r'\2', new_line)
            
            new_lines.append(new_line)
            
        with open(path, "w", encoding='utf-8') as f:
            f.writelines(new_lines)
        count += 1
        print(f"Synchronized {filename} to {char}")

    print(f"Total files synchronized: {count}")

sync_identities()
