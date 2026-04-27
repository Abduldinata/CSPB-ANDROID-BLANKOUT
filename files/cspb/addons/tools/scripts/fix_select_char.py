import os, glob, re

files = glob.glob(r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\select_character\select*.cfg')

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    # regex to match coordinates: e.g. "" 0.460000 0.205400 0.620000 0.349300 255 255 255 255 4
    content = re.sub(r'\"\" \d\.\d+ \d\.\d+ \d\.\d+ \d\.\d+ 255 255 255 255 4', '"" -0.020000 -0.000000 1.000000 1.000000 255 255 255 255 4', content)
    
    with open(f, 'w') as file:
        file.write(content)

print("Updated coordinates for character selection border.")
