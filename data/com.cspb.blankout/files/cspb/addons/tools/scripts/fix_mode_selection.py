import os

mode_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda\mode'

for file in os.listdir(mode_dir):
    if file.endswith('.cfg') and file not in ['mode_db.cfg', 'remove_mode_all.cfg', 'reset_indicators.cfg']:
        filepath = os.path.join(mode_dir, file)
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Replace the pointer alias
        updated = content.replace('alias _mode_indicator _db_mode_', 'alias _mode_p1_indicator _db_mode_')
        # Ensure _mode_p1_indicator is called instead of _mode_indicator for state storage
        updated = updated.replace('_mode_indicator;', '_mode_p1_indicator;')
        
        with open(filepath, 'w') as f:
            f.write(updated)

print("Mode selection files updated.")
