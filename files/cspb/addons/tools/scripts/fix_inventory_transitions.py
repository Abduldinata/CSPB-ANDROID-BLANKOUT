import os
import re

base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons"

# 1. Update char_db.cfg - Remove inventory_character.cfg calls
char_db_path = os.path.join(base_path, "neda", "persist", "char_db.cfg")
if os.path.exists(char_db_path):
    with open(char_db_path, "r") as f:
        content = f.read()
    
    # We want to remove `exec addons/neda/.../inventory_character.cfg; ` from _db_char aliases
    new_content = re.sub(r'exec addons/neda/[a-z]+/[a-z]+/inventory_character\.cfg;\s*', '', content)
    
    with open(char_db_path, "w") as f:
        f.write(new_content)
    print("Fixed char_db.cfg (removed inventory_character.cfg from equip macro)")

# 2. Update cleanup.cfg to remove selected_char_img
cleanup_path = os.path.join(base_path, "neda", "persist", "cleanup.cfg")
if os.path.exists(cleanup_path):
    with open(cleanup_path, "r") as f:
        cleanup_lines = f.read().splitlines()
    
    if 'touch_removebutton "selected_char_img"' not in cleanup_lines:
        cleanup_lines.append('touch_removebutton "selected_char_img"')
        with open(cleanup_path, "w") as f:
            f.write("\n".join(cleanup_lines))
        print("Fixed cleanup.cfg (added touch_removebutton selected_char_img)")

# 3. Create a global page remover alias in inventory.cfg
inv_path = os.path.join(base_path, "inventory.cfg")
if os.path.exists(inv_path):
    with open(inv_path, "r") as f:
        inv_content = f.read()
        
    global_remover = 'alias _rmv_all_main_inv_pages "_rmv_wp_page1; _rmv_wp_page2; _rmv_wp_page3; _rmv_wp_page4; _rmv_wp_page5; _rmv_wp_page6; _rmv_wp_page7; _rmv_wp_page8; _rmv_wp_page9; _rmv_wp_page10; _rmv_scd_page1; _rmv_scd_page2; _rmv_ml_page1; _rmv_ml_page2; _rmv_ml_page3; _rmv_exp_page1; _rmv_spc_page1"'
    if "alias _rmv_all_main_inv_pages" not in inv_content:
        # insert it near the top or end
        inv_content += "\n// global pages remover\n" + global_remover + "\n"
        with open(inv_path, "w") as f:
            f.write(inv_content)
        print("Added _rmv_all_main_inv_pages to inventory.cfg")

# 4. Inject _rmv_all_main_inv_pages into all `_lobby_inventory_char1` commands
def patch_button_cmd(filepath, button_name, inject_cmd):
    with open(filepath, "r") as f:
        content = f.read()
        
    pattern = r'(touch_addbutton\s+"' + button_name + r'"\s+""\s+")([^"]+)(")'
    def replacer(match):
        cmd_str = match.group(2)
        if inject_cmd not in cmd_str:
            return f'{match.group(1)}{inject_cmd}; {cmd_str}{match.group(3)}'
        return match.group(0)
        
    new_content = re.sub(pattern, replacer, content)
    if new_content != content:
        with open(filepath, "w") as f:
            f.write(new_content)
        return True
    return False

patched_files = 0
for root, _, files in os.walk(base_path):
    for file in files:
        if file.endswith(".cfg"):
            p = os.path.join(root, file)
            if patch_button_cmd(p, "_lobby_inventory_char1", "_rmv_all_main_inv_pages"):
                patched_files += 1

print(f"Patched {patched_files} files for button bleed")

