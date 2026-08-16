import re
with open('data/com.cspb.blankout/files/cspb/downloaded/maps/pb_mstation.bsp', 'rb') as f:
    bsp = f.read()
match = re.search(br'\{[^{}]*?models/player/terror/terror\.mdl[^{}]*?\}', bsp)
if match:
    print(match.group(0).decode('ascii', errors='ignore'))
else:
    print('Not found')
