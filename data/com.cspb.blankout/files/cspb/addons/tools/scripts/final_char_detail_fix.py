import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\character'
char_db_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\char_db.cfg'

# Mapping from filename to char_db alias and pointer
# Based on char_db.cfg audit
char_meta = {
    'redbull': {'db': '_db_char_redbull', 'ptr': '_show_equip_char_redbull', 'img': 'redc1'},
    'acidpool': {'db': '_db_char_acidpool', 'ptr': '_show_equip_char_acidpool', 'img': 'bluec1'},
    'tarantula': {'db': '_db_char_tarantula', 'ptr': '_show_equip_char_tarantula', 'img': 'redc2'},
    'keeneyes': {'db': '_db_char_keeneyes', 'ptr': '_show_equip_char_keeneyes', 'img': 'bluec2'},
    'dfox': {'db': '_db_char_dfox', 'ptr': '_show_equip_char_dfox', 'img': 'redc3'},
    'leopard': {'db': '_db_char_leopard', 'ptr': '_show_equip_char_leopard', 'img': 'bluec3'},
    'viperred': {'db': '_db_char_viper', 'ptr': '_show_equip_char_viperred', 'img': 'redc4'},
    'hide': {'db': '_db_char_hide', 'ptr': '_show_equip_char_hide', 'img': 'bluec4'},
    'ricalopez': {'db': '_db_char_ricalopez', 'ptr': '_show_equip_char_ricalopez', 'img': 'redc5'},
    'judychou': {'db': '_db_char_judychou', 'ptr': '_show_equip_char_judychou', 'img': 'bluec5'},
    'queen': {'db': '_db_char_queen', 'ptr': '_show_equip_char_queen', 'img': 'bluec2'}, # Queen uses bluec2 in char_db? Let's check
    'natasha': {'db': '_db_char_natasha', 'ptr': '_show_equip_char_natasha', 'img': 'redc3'} # Natasha uses redc3?
}

def sweep_char_files():
    for page in ['page1', 'page2']:
        page_dir = os.path.join(root_dir, page)
        if not os.path.exists(page_dir): continue
        for file in os.listdir(page_dir):
            if file.endswith('.cfg'):
                name = file[:-4].lower()
                meta = char_meta.get(name)
                if not meta: continue
                
                filepath = os.path.join(page_dir, file)
                
                # Standardizing character detail file
                content = [
                    f'touch_addbutton "selected_char_img" "addons/neda/image/character/{meta["img"]}.tga" "" 0.460000 0.621582 0.620000 0.781990 255 255 255 255 4',
                    '',
                    f'touch_addbutton "equip_char_btn" "" "_tap_cnd_use; {meta["db"]}" 0.550000 0.760109 0.640000 0.821739 255 255 255 255 4',
                    '',
                    f'{meta["ptr"]}',
                    ''
                ]
                
                with open(filepath, 'w') as f:
                    f.write('\n'.join(content))
                print(f"  Standardized: {page}/{file}")

sweep_char_files()
