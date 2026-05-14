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

# Broad patterns for back/out buttons across all categories (1-5)
# We append _sub to ensure they are unique relative to the main lobby buttons
patterns = [
    (re.compile(r'_lobby_back(?![_\d]*_sub)\b'), '_lobby_back_sub'),
    (re.compile(r'_lobby_back(\d+)(?![_\d]*_sub)\b'), r'_lobby_back\1_sub'),
    (re.compile(r'_lobby_out(?![_\d]*_sub)\b'), '_lobby_out_sub'),
    (re.compile(r'_lobby_out(\d+)(?![_\d]*_sub)\b'), r'_lobby_out\1_sub'),
]

# Files that should NOT be modified because they are "Main" layers
protected_files = [
    'lobby_menu.cfg', 'lobby_menu2.cfg', 'lobby_menu3.cfg', 
    'lobby_menu4.cfg', 'lobby_menu5.cfg', 'lobby_menu4_load.cfg',
    'team_blue.cfg', 'team_blue2.cfg', 'team_red.cfg', 'team_red2.cfg',
    'team_blue_class', 'team_red_class' # partial match for class files
]

for c in chars:
    for sub in subfolders:
        dir_path = os.path.join(base_path, c['team'], c['name'], sub)
        if not os.path.isdir(dir_path):
            continue
            
        for filename in os.listdir(dir_path):
            if not filename.endswith('.cfg'):
                continue
                
            is_protected = False
            for p in protected_files:
                if p in filename:
                    is_protected = True
                    break
            
            if is_protected:
                continue
                
            fp = os.path.join(dir_path, filename)
            with open(fp, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            for pattern, replacement in patterns:
                new_content = pattern.sub(replacement, new_content)
            
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f'Fixed Ghost IDs in: {fp}')

print('Comprehensive Ghost Click IDs updated!')
