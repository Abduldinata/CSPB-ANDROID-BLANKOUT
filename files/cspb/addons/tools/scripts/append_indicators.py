import os
import glob

def append_indicators():
    base_dir = r"e:\Games\PROJECT LOBBY CSPB\addons\neda\team"
    pattern = "team_*_class*.cfg"
    
    files = glob.glob(os.path.join(base_dir, pattern))
    
    for file_path in files:
        with open(file_path, "r", encoding='utf-8') as f:
            content = f.read()
            
        if "_add_indicators" not in content[-50:]: # Check end of file
            with open(file_path, "a", encoding='utf-8') as f:
                f.write("\n_add_indicators\n")
            print(f"Appended _add_indicators to {os.path.basename(file_path)}")
        else:
            print(f"Skipped {os.path.basename(file_path)}")

if __name__ == "__main__":
    append_indicators()
