import os
import re

chars = [
    {'team':'blueteam', 'name':'acidpool'},
    {'team':'blueteam', 'name':'keeneyes'},
    {'team':'blueteam', 'name':'leopard'},
    {'team':'blueteam', 'name':'hide'},
    {'team':'blueteam', 'name':'judychou'},
    {'team':'redteam', 'name':'redbull'},
    {'team':'redteam', 'name':'tarantula'},
    {'team':'redteam', 'name':'dfox'},
    {'team':'redteam', 'name':'viper'},
    {'team':'redteam', 'name':'ricalopez'}
]

base_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'

# Exit replacement
exit_repl = '//Exit\ntouch_addbutton "_lobby_out3" "" "touch_removebutton _lobby_out3; _tap_cnd_back; _hapus; _rmv_persist_all; rmv_all_stat" 0.940000 0.906067 0.980000 0.992360 255 255 255 255 6'

for c in chars:
    c_dir = os.path.join(base_path, c['team'], c['name'])
    if not os.path.isdir(c_dir): continue
    for f in os.listdir(c_dir):
        if f.startswith('inventory_') and f.endswith('.cfg'):
            fp = os.path.join(c_dir, f)
            with open(fp, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            new_lines = []
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.strip() == '//Exit':
                    new_lines.append('//Exit\n')
                    new_lines.append('touch_addbutton "_lobby_out3" "" "touch_removebutton _lobby_out3; _tap_cnd_back; _hapus; _rmv_persist_all; rmv_all_stat" 0.940000 0.906067 0.980000 0.992360 255 255 255 255 6\n')
                    if i+1 < len(lines) and 'touch_addbutton "_lobby_out3"' in lines[i+1]:
                        i += 1
                elif line.strip() == '//Back':
                    new_lines.append('//Back\n')
                    if f.endswith('2.cfg'):
                        new_lines.append(f'touch_addbutton "_lobby_back3" "" "touch_removebutton _lobby_back3; _tap_cnd_back; _hapus; _rmv_persist_all; rmv_all_stat; _back_4_{c["name"]}" 0.900000 0.819775 0.980000 0.906067 255 255 255 255 6\n')
                    else:
                        new_lines.append(f'touch_addbutton "_lobby_back2" "" "touch_removebutton _lobby_back2; _tap_cnd_back; _hapus; _rmv_persist_all; rmv_all_stat; _back_3_{c["name"]}" 0.900000 0.819775 0.980000 0.906067 255 255 255 255 6\n')
                    
                    # skip all touch_addbutton lines following //Back until empty line or comment
                    j = i + 1
                    while j < len(lines) and ('touch_addbutton "_lobby_back' in lines[j] or lines[j].strip() == ''):
                        if lines[j].strip() == '':
                            pass # keep it? no, will add a newline below if needed
                        j += 1
                    i = j - 1
                else:
                    new_lines.append(line)
                i += 1

            with open(fp, 'w', encoding='utf-8') as file:
                file.writelines(new_lines)

print("Done")
