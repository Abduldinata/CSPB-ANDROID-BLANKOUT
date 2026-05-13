import os

root_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda"

# Target files: character lobbies and team selection
target_files = []

# Character Lobby Menus
for team in ["blueteam", "redteam"]:
    team_dir = os.path.join(root_dir, team)
    if not os.path.exists(team_dir): continue
    for char in os.listdir(team_dir):
        char_dir = os.path.join(team_dir, char)
        if os.path.isdir(char_dir):
            for f in os.listdir(char_dir):
                if f.startswith("lobby_menu") and f.endswith(".cfg"):
                    target_files.append(os.path.join(char_dir, f))

# Team Selection Files (Lobby 4)
team_dir = os.path.join(root_dir, "team")
if os.path.exists(team_dir):
    for f in os.listdir(team_dir):
        if f.startswith("team_") and "class" in f and f.endswith(".cfg"):
            target_files.append(os.path.join(team_dir, f))

# Add mode indicator to persistence loaders
count = 0
for filepath in target_files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check if mode indicator is missing
    if "_mode_indicator" not in content and "_map_p1_indicator" in content:
        # Add after the last indicator line
        lines = content.split('\n')
        new_lines = []
        for line in lines:
            new_lines.append(line)
            # Add mode indicator after special_p1_indicator
            if "_special_p1_indicator" in line:
                new_lines.append("_mode_indicator")
        
        with open(filepath, 'w') as f:
            f.write('\n'.join(new_lines))
        count += 1

print(f"Mode persistence integrated into {count} lobby files.")
