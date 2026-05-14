import os
import re

# Categories to check for each character
subfolders = [
    '', # root of character folder
    'main', 'main2', 
    'secondary', 'secondary2', 
    'melee', 'melee2', 
    'explosive', 'explosive2', 
    'special', 'special2', 
    'character', 'character2'
]

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

# Patterns to replace IDs in touch_addbutton and its command string
# We use _sub suffix to avoid collision with main lobby buttons
back_pattern = re.compile(r'_lobby_back3\b')
out_pattern = re.compile(r'_lobby_out3\b')

for c in chars:
    for sub in subfolders:
        dir_path = os.path.join(base_path, c['team'], c['name'], sub)
        if not os.path.isdir(dir_path):
            continue
            
        for filename in os.listdir(dir_path):
            if filename.endswith('.cfg') and ('lobby_menu' not in filename): # Don't touch main lobby menus
                fp = os.path.join(dir_path, filename)
                with open(fp, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = back_pattern.sub('_lobby_back3_sub', content)
                new_content = out_pattern.sub('_lobby_out3_sub', new_content)
                
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f'Fixed Ghost IDs in: {fp}')

print('Ghost click IDs updated!')
