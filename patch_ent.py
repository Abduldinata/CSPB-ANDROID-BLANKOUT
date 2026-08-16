import re

filepath = 'data/com.cspb.blankout/files/cspb/downloaded/maps/ent/pb_mstation.ent'

with open(filepath, 'r') as f:
    content = f.read()

# Remove the model lines for player models from spawn points
# We want to remove lines like: "model" "models/player/terror/terror.mdl"
content = re.sub(r'"model"\s+"models/player/[^"]+"', '', content)

with open(filepath, 'w') as f:
    f.write(content)

print("Patched pb_mstation.ent successfully.")
