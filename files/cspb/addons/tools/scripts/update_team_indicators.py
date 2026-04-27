import os
import glob

# Directory for team files
team_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"
files = glob.glob(os.path.join(team_dir, "team_*.cfg"))

def update_team_files():
    count = 0
    for file_path in files:
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
            
        # Replace _mode_indicator with _add_indicators
        if "_mode_indicator" in content:
            new_content = content.replace("_mode_indicator", "_add_indicators")
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(file_path)}")
            count += 1
        elif "_add_indicators" not in content:
            # If neither is present, append to the end
            with open(file_path, "a", encoding='utf-8') as f:
                f.write("\n_add_indicators\n")
            print(f"Appended _add_indicators to {os.path.basename(file_path)}")
            count += 1
            
    print(f"Total files processed: {count}")

if __name__ == "__main__":
    update_team_files()
