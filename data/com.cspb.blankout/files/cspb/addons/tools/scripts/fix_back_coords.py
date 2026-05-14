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
pattern = re.compile(r'(touch_addbutton \"_lobby_back2\".+?)\s+0\.900000 0\.819775 0\.980000 0\.906067 255 255 255 255 6', re.IGNORECASE)
replacement = r'\1 0.720000 0.821739 0.770000 0.883370 255 255 255 255 6'

for c in chars:
    fp = os.path.join(base_path, c['team'], c['name'], 'lobby_menu3.cfg')
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = pattern.sub(replacement, content)
        if new_content != content:
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Fixed: {fp}')
        else:
            print(f'No change needed or pattern mismatch in: {fp}')
    else:
        print(f'File not found: {fp}')

print('Done!')
