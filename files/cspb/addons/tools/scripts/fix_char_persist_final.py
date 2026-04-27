import os

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'
char_persist_dir = os.path.join(root_dir, 'persist', 'character')

if not os.path.exists(char_persist_dir): os.makedirs(char_persist_dir)

# Coordinate Map for Character Slots 1-9 (Page 1 & 2 share similar grid)
char_slots = {
    1: "0.460000 0.205400 0.620000 0.349300",
    2: "0.620000 0.205400 0.780000 0.349300",
    3: "0.780000 0.205400 0.940000 0.349300",
    4: "0.460000 0.349300 0.620000 0.485300",
    5: "0.620000 0.349300 0.780000 0.485300",
    6: "0.780000 0.349300 0.940000 0.485300",
    7: "0.460000 0.472500 0.620000 0.616300",
    8: "0.620000 0.472500 0.780000 0.616300",
    9: "0.780000 0.472500 0.940000 0.616300"
}

def generate_char_persist():
    # P1 (Part 1 / Red)
    for i in range(1, 10):
        filename = f'use{i}.cfg'
        filepath = os.path.join(char_persist_dir, filename)
        badge_id = f'_c_badge_p1_s{i}'
        coord = char_slots[i]
        content = f'touch_addbutton "{badge_id}" "addons/neda/image/select_char/equip/{i}.tga" "c" {coord} 255 255 255 255 4\n'
        with open(filepath, 'w') as f: f.write(content)
    
    # P2 (Part 2 / Blue)
    for i in range(1, 10):
        filename = f'use{i}_p2.cfg'
        filepath = os.path.join(char_persist_dir, filename)
        badge_id = f'_c_badge_p2_s{i}'
        coord = char_slots[i]
        content = f'touch_addbutton "{badge_id}" "addons/neda/image/select_char/equip/{i}.tga" "c" {coord} 255 255 255 255 4\n'
        with open(filepath, 'w') as f: f.write(content)

    print("Character persistence files standardized.")

generate_char_persist()
