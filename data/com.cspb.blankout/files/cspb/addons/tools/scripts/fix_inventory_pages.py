import glob
import os

def fix_inventory_pages():
    base_path = r"e:\Games\PROJECT LOBBY CSPB\com.cspb.m\files\cspb\addons\neda"
    
    # Categories and their subfolders
    categories = {
        "weapons": "weapons",
        "secondary": "secondary",
        "melee": "melee",
        "explosive": "explosive",
        "special": "special",
        "character": "character"
    }

    total_fixed = 0

    for cat_name, subfolder in categories.items():
        folder_path = os.path.join(base_path, subfolder)
        if not os.path.exists(folder_path):
            print(f"Skipping {cat_name}: {folder_path} not found")
            continue
            
        # Find all page*.cfg files
        pattern = os.path.join(folder_path, "page*.cfg")
        files = glob.glob(pattern)
        
        for filepath in files:
            with open(filepath, "r", encoding='utf-8') as f:
                content = f.read()
            
            # Check if _add_indicators is already there
            if "_add_indicators" in content:
                # Optional: Ensure it's at the end or near end?
                # For now, assume if it exists, it's fine.
                # But wait, page1.cfg had "_weap_p1_indicator".
                # We should append it if it's not explicitly calling the global loader.
                if "_add_indicators" in content.splitlines()[-1]:
                     print(f"Skipping {filepath}: already has _add_indicators")
                     continue

            # Append it
            new_content = content.strip() + "\n\n// Restore Persistence Badges\n_add_indicators\n"
            
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Fixed: {filepath}")
            total_fixed += 1

    print(f"Total inventory pages fixed: {total_fixed}")

if __name__ == "__main__":
    fix_inventory_pages()
