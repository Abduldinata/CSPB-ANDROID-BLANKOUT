import os

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons"

# Map char lobby file to its character suffix
char_lobbies = {
    "lobby_acidpool.cfg": "acidpool",
    "lobby_dfox.cfg": "dfox",
    "lobby_hide.cfg": "hide",
    "lobby_judychou.cfg": "judychou",
    "lobby_keeneyes.cfg": "keeneyes",
    "lobby_leopard.cfg": "leopard",
    "lobby_redbull.cfg": "redbull",
    "lobby_ricalopez.cfg": "ricalopez",
    "lobby_tarantula.cfg": "tarantula",
    "lobby_viper.cfg": "viper"
}

generic_aliases = [
    "_main_inventory", "_rmv_main_inventory",
    "_second_inventory", "_rmv_second_inventory",
    "_melee_inventory", "_rmv_melee_inventory",
    "_explosive_inventory", "_rmv_explosive_inventory",
    "_special_inventory", "_rmv_special_inventory",
    "_char_inventory", "_rmv_char_inventory"
]

count = 0
for filename, char_suffix in char_lobbies.items():
    filepath = os.path.join(root_dir, filename)
    if not os.path.exists(filepath): continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Add redirection block if not present
    if "// Generic Redirection" not in content:
        redirection_block = "\n// Generic Redirection\n"
        for alias in generic_aliases:
            redirection_block += f'alias {alias} "{alias}_{char_suffix}"\n'
        
        # Insert after sv_cheats or at the end of the initial block
        if "sv_cheats" in content:
            content = content.replace('sv_cheats "1"', 'sv_cheats "1"' + redirection_block)
        else:
            content = redirection_block + content
            
        with open(filepath, 'w') as f:
            f.write(content)
        count += 1

print(f"Generic redirection added to {count} character lobby files.")
