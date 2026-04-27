import os
import re

# Base directory for character selection files
select_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_character\character"

# Mapping: filename -> theme alias
mapping = {
    "page1/redbull.cfg": "_db_char_redbull",
    "page1/acidpool.cfg": "_db_char_acidpool",
    "page1/tarantula.cfg": "_db_char_tarantula",
    "page1/keeneyes.cfg": "_db_char_keeneyes",
    "page1/dfox.cfg": "_db_char_dfox",
    "page1/leopard.cfg": "_db_char_leopard",
    "page1/viperred.cfg": "_db_char_viper",
    "page1/hide.cfg": "_db_char_hide",
    "page1/ricalopez.cfg": "_db_char_ricalopez",
    "page2/judychou.cfg": "_db_char_judychou",
    "page2/natasha.cfg": "_db_char_natasha",
    "page2/queen.cfg": "_db_char_queen",
}

def update_character_buttons():
    count = 0
    for rel_path, theme_alias in mapping.items():
        path = os.path.join(select_dir, rel_path)
        if not os.path.exists(path):
            print(f"Skipping {path} (not found)")
            continue
            
        with open(path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            
        new_lines = []
        for line in lines:
            # Cari tombol equip karakter
            if 'touch_addbutton "equip_' in line:
                # Ganti perintahnya (CMD) menjadi _tap_cnd_use; THEME_ALIAS
                # Pattern: touch_addbutton "ID" "IMAGE" "CMD" ...
                # Menggunakan re.sub untuk mengganti partisi ketiga (CMD)
                fixed_line = re.sub(r'("[^"]*"\s+"[^"]*"\s+)"[^"]*"', r'\1"' + f'_tap_cnd_use; {theme_alias}' + r'"', line)
                new_lines.append(fixed_line)
            else:
                new_lines.append(line)
        
        with open(path, "w", encoding='utf-8') as f:
            f.writelines(new_lines)
        count += 1
        print(f"Updated {rel_path} to use {theme_alias}")
    
    print(f"Total files updated: {count}")

update_character_buttons()
