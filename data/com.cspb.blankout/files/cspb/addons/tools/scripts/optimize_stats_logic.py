import os
import re

root_dir = r'e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda'

# Patterns to replace stat loadings and removal
stat_exec_pattern = re.compile(r'exec\s+addons/neda/stat/([a-zA-Z0-9_]+)\.cfg', re.IGNORECASE)
rmv_stat_pattern = re.compile(r'exec\s+addons/neda/stat/remove_all_stat\.cfg', re.IGNORECASE)

count = 0
for root, dirs, files in os.walk(root_dir):
    for f in files:
        if f.lower().endswith('.cfg'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                
                # Replace specific weapon stat execs with aliases
                # e.g. exec addons/neda/stat/ak47.cfg -> stat_ak47
                def stat_replace(match):
                    weapon = match.group(1).lower()
                    if weapon == 'remove_all_stat':
                        return 'rmv_all_stat'
                    return f'stat_{weapon}'

                new_content = stat_exec_pattern.sub(stat_replace, new_content)
                new_content = rmv_stat_pattern.sub('rmv_all_stat', new_content)
                
                if new_content != content:
                    with open(fp, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    count += 1
            except:
                pass

print(f'Done! Optimized {count} additional files by consolidating statistics logic.')
