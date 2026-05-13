import os

base_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\persist\character"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Page 1 Use Badges
for i in range(1, 10):
    with open(os.path.join(base_dir, f"use{i}.cfg"), "w") as f:
        f.write(f'touch_removebutton "_persist_char_badge"\n')
        f.write(f'touch_addbutton "_persist_char_badge" "addons/neda/image/select_char/{i}.tga" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 5\n')

# Page 1 Equip Badges
for i in range(1, 10):
    with open(os.path.join(base_dir, f"equip{i}.cfg"), "w") as f:
        f.write(f'touch_removebutton "_persist_char_equip_badge"\n')
        f.write(f'touch_addbutton "_persist_char_equip_badge" "addons/neda/image/select_char/equip/{i}.tga" "c" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 5\n')

print("Generated character persistence files.")
