import os

# Base directory for character selection files
select_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\select_character\character"

# Mapping: filename -> full_alias
mapping = {
    "page1/redbull.cfg": "_db_char_redbull_full",
    "page1/acidpool.cfg": "_db_char_acidpool_full",
    "page1/tarantula.cfg": "_db_char_tarantula_full",
    "page1/keeneyes.cfg": "_db_char_keeneyes_full",
    "page1/dfox.cfg": "_db_char_dfox_full",
    "page1/leopard.cfg": "_db_char_leopard_full",
    "page1/viperred.cfg": "_db_char_viperred_full",
    "page1/hide.cfg": "_db_char_hide_full",
    "page1/ricalopez.cfg": "_db_char_ricalopez_full",
    "page2/judychou.cfg": "_db_char_judychou_full",
}

for rel_path, alias in mapping.items():
    path = os.path.join(select_dir, rel_path)
    if not os.path.exists(path):
        print(f"Skipping {path} (not found)")
        continue
        
    with open(path, "r", encoding='utf-8') as f:
        lines = f.readlines()
        
    new_lines = []
    for line in lines:
        if 'touch_addbutton "equip_' in line or 'touch_addbutton "equip_' in line:
            # Replace the command part
            # Pattern: touch_addbutton "ID" "IMAGE" "CMD" ...
            import re
            fixed_line = re.sub(r'("[^"]*"\s+"[^"]*"\s+)"[^"]*"', r'\1"' + f'_tap_cnd_use; {alias}' + r'"', line)
            new_lines.append(fixed_line)
        else:
            new_lines.append(line)
            
    with open(path, "w", encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Updated {rel_path}")
