import os

directory = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\persist\map'
files = [f for f in os.listdir(directory) if f.endswith('.cfg')]

# Reverting coordinates
# From: -0.350000 1.000000 0.650000
# To:   -0.000000 1.000000 1.000000

for filename in files:
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace coordinates back to original
    new_content = content.replace('-0.350000 1.000000 0.650000', '-0.000000 1.000000 1.000000')
    
    with open(filepath, 'w') as f:
        f.write(new_content)

print(f"Reverted {len(files)} map badge files to original coordinates.")
