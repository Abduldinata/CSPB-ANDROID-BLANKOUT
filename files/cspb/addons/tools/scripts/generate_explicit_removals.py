import os

def generate_explicit_removals():
    commands = []
    
    # Weapons, Secondary, Melee, Explosive, Special (s1 to s6)
    prefixes = ['_w_badge_s', '_s_badge_s', '_m_badge_s', '_e_badge_s', '_p_badge_s']
    for prefix in prefixes:
        for i in range(1, 7):
            commands.append(f'touch_removebutton {prefix}{i}')
            
    # Characters
    # Persist use configs for characters are use1.cfg up to use9.cfg, and use1_p2.cfg, etc.
    # Let's check persist/character directory explicitly to find the exact button names.
    char_persist_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\character'
    if os.path.exists(char_persist_dir):
        for f in os.listdir(char_persist_dir):
            if f.startswith('use') and f.endswith('.cfg'):
                with open(os.path.join(char_persist_dir, f), 'r') as file:
                    for line in file:
                        if 'touch_addbutton' in line:
                            parts = line.split('"')
                            if len(parts) >= 2:
                                btn_name = parts[1]
                                if btn_name.startswith('_c_badge'):
                                    commands.append(f'touch_removebutton {btn_name}')
                                    
    # Explicit single badges
    commands.append('touch_removebutton selected_char_img')
    commands.append('touch_removebutton equip_char_btn')
    commands.append('touch_removebutton _char_equip_status_badge')
    commands.append('touch_removebutton _weap_equip_status_badge')
    
    return commands

cmds = generate_explicit_removals()
chunk_size = 15 # Grouping aliases to not hit character limits
file_lines = []

for i in range(0, len(cmds), chunk_size):
    chunk = cmds[i:i+chunk_size]
    file_lines.append(f"alias _rmv_inv_badges_{i//chunk_size} \"{'; '.join(chunk)}\"")

master_alias = "alias _rmv_inv_badges \"" + "; ".join([f"_rmv_inv_badges_{i//chunk_size}" for i in range(0, len(cmds), chunk_size)]) + "\""

file_path = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\remove_inv_badges.cfg'
with open(file_path, 'w') as f:
    f.write("\n".join(file_lines) + "\n\n" + master_alias + "\n")
    
print(f"Generated explicit removal script at {file_path}")
