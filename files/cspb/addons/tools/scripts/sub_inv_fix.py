import os

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

loader_block = """

// Full Persistence Loaders
_map_p1_indicator
_map_p2_indicator
_map_p3_indicator
_weap_p1_indicator
_weap_p2_indicator
_weap_p3_indicator
_weap_p4_indicator
_weap_p5_indicator
_weap_p6_indicator
_weap_p7_indicator
_weap_p8_indicator
_weap_p9_indicator
_sec_p1_indicator
_melee_p1_indicator
_exp_p1_indicator
_special_p1_indicator
"""

# Targets: inventory_secondary, inventory_melee, inventory_explosive, inventory_special, inventory_character
# Both Version 1 and Version 2 (if any)
prefixes = ["inventory_secondary", "inventory_melee", "inventory_explosive", "inventory_special", "inventory_character"]

count = 0
for team in ["blueteam", "redteam"]:
    team_dir = os.path.join(root_dir, team)
    if not os.path.exists(team_dir): continue
    for char in os.listdir(team_dir):
        char_dir = os.path.join(team_dir, char)
        if os.path.isdir(char_dir):
            for f in os.listdir(char_dir):
                # Match any of the sub-inventory patterns
                if any(f.startswith(p) for p in prefixes) and f.endswith(".cfg"):
                    filepath = os.path.join(char_dir, f)
                    with open(filepath, 'r') as file_obj:
                        content = file_obj.read()
                    
                    if "_map_p1_indicator" not in content:
                        with open(filepath, 'a') as file_obj:
                            file_obj.write(loader_block)
                        count += 1

print(f"Sub-inventory consistency fix complete for {count} files.")
