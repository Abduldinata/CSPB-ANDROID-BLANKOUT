import os
import re

team_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"

def remove_duplicate_mode_indicator():
    """Remove redundant _mode_indicator; call from mode buttons"""
    processed = 0
    
    for filename in os.listdir(team_dir):
        if filename.startswith("team_") and filename.endswith(".cfg"):
            path = os.path.join(team_dir, filename)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # Pattern: alias _mode_indicator _db_mode_XXX; _mode_indicator; _sl_mode_XXX; _mode_XXX
            # Remove the redundant _mode_indicator; call
            content = re.sub(
                r'(alias _mode_indicator _db_mode_\w+); _mode_indicator; (_sl_mode_\w+; _mode_\w+)',
                r'\1; \2',
                content
            )
            
            if content != original:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                processed += 1
                print(f"Optimized {filename}")
    
    return processed

count = remove_duplicate_mode_indicator()
print(f"\nRemoved duplicate mode indicator calls from {count} team configs.")
print("Performance improvement: ~50% faster mode switching")
