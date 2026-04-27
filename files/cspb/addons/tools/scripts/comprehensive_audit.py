import os
import re
import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
neda = os.path.join(root, "neda")

# Built-ins and engine commands to ignore
builtins = {
    'exec', 'alias', 'touch_addbutton', 'echo', 'say', 'quit', 'exit', 'restart', 
    'mp_gamemode', 'cl_mousegrab', 'set_sound_default', 'rmv_all_stat', 'wait', 
    'kill', 'name', 'bind', 'unbind', '+attack', '-attack', '+jump', '-jump',
    'inventory_primary', 'inventory_secondary', 'inventory_melee', 'inventory_explosive', 
    'inventory_special', 'inventory_character', 'rmv_all_menu', 'rmv_equip', 
    'rmv_all_sl_weap', 'rmv_all_sl_weap_cmd', 'touch_removebutton', 'cl_status',
    '_tap_cnd', '_tap_cnd_click', '_tap_cnd_switch', '_tap_cnd_back', '_tap_cnd_use'
}

all_files = glob.glob(os.path.join(root, "**/*.cfg"), recursive=True) + \
            glob.glob(os.path.join(root, "**/*.db"), recursive=True)

defined_aliases = set()
calls = [] # (source_file, call_name)
exec_calls = [] # (source_file, target_path)
tga_calls = [] # (source_file, target_path)

# Regex
re_alias = re.compile(r'alias\s+(\S+)')
re_exec = re.compile(r'exec\s+([\w\./\\-]+)')
re_tga = re.compile(r'"([\w\./\\ ]+?\.tga)"')
re_button = re.compile(r'touch_addbutton\s+".+?"\s+".*?"\s+"(.*?)"')


def normalize_exec_target(raw: str) -> str:
    target = raw.strip().replace('/', os.sep).replace('\\', os.sep)
    # In cfg alias strings, escaped quote often leaves a trailing backslash in regex capture.
    while target.endswith(os.sep):
        target = target[:-1]
    target = target.rstrip(';')
    return target

print(f"Auditing {len(all_files)} files...")

for filepath in all_files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
            # Definitions
            for m in re_alias.finditer(content):
                defined_aliases.add(m.group(1).lower())
            
            # Execs
            for m in re_exec.finditer(content):
                exec_calls.append((filepath, m.group(1)))
                
            # TGAs
            for m in re_tga.finditer(content):
                tga_calls.append((filepath, m.group(1)))
                
            # Calls in buttons
            for m in re_button.finditer(content):
                cmd_str = m.group(1)
                for part in cmd_str.split(';'):
                    tokens = part.strip().split()
                    if tokens:
                        calls.append((filepath, tokens[0].lower()))
            
            # Calls in lines
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('//') and not line.startswith('/*'):
                    tokens = line.split()
                    if tokens and tokens[0].lower() not in builtins:
                        if not tokens[0].startswith('alias') and not tokens[0].startswith('exec') and not tokens[0].startswith('touch_'):
                            calls.append((filepath, tokens[0].lower()))
    except Exception as e:
        print(f"Error {filepath}: {e}")

# Analysis
issues = []

# 1. Undefined Calls
for src, call in calls:
    if call not in defined_aliases and call not in builtins:
        if not call.startswith('_rmv_') and not call.startswith('rmv_'):
            issues.append(f"UNDEFINED ALIAS: '{call}' in {os.path.relpath(src, root)}")

# 2. Broken Execs
for src, target in exec_calls:
    # Normalize path
    p = normalize_exec_target(target)
    if not p.startswith('addons'): continue # Skip relative engine paths if any
    
    # Check absolute vs relative to project root
    # Most execs are relative to the game root (where e:\Games\PROJECT LOBBY CSPB is)
    # So 'addons/mode.cfg' is at 'e:\Games\PROJECT LOBBY CSPB\addons\mode.cfg'
    full_p = os.path.join(os.path.dirname(root), p)
    if not os.path.exists(full_p):
        issues.append(f"BROKEN EXEC: '{target}' in {os.path.relpath(src, root)}")

# 3. Broken TGAs
for src, target in tga_calls:
    p = target.replace('/', os.sep).replace('\\', os.sep)
    full_p = os.path.join(os.path.dirname(root), p)
    if not os.path.exists(full_p):
        # Retry with .tga if missing extension in path but regex caught it
        issues.append(f"BROKEN TGA: '{target}' in {os.path.relpath(src, root)}")

unique_issues = sorted(list(set(issues)))
if not unique_issues:
    print("\nOK: No major issues found.")
else:
    print(f"\nFound {len(unique_issues)} potential issues:")
    for issue in unique_issues[:40]:
        print(issue)
