import os

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\image\select_char'

for root, dirs, files in os.walk(root_dir):
    print(f"\nDirectory: {root}")
    for file in files:
        print(f"  - {file}")
