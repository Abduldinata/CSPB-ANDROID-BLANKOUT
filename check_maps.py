import glob
import os
import re

for map_path in glob.glob('C:/CSPB_PROJECT/CSPBV16-BASE-BILLFLX/files/cstrike/downloaded/maps/*.bsp'):
    name = os.path.basename(map_path)
    with open(map_path, 'rb') as f:
        data = f.read()
    
    wad_match = re.search(rb'"wad"\s*"([^"]+)"', data)
    wads = wad_match.group(1).decode('ascii', errors='ignore') if wad_match else 'None'
    
    t_spawns = len(re.findall(rb'"classname"\s*"info_player_deathmatch"', data))
    ct_spawns = len(re.findall(rb'"classname"\s*"info_player_start"', data))
    coop_spawns = len(re.findall(rb'"classname"\s*"info_player_coop"', data))
    
    print(f'Map: {name}')
    print(f'  Wads: {wads}')
    print(f'  Terrorist (Red) Spawns (info_player_deathmatch): {t_spawns}')
    print(f'  CT (Blue) Spawns (info_player_start): {ct_spawns}')
    print(f'  Coop Spawns: {coop_spawns}')
    print('-'*50)
