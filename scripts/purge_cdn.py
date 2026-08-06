import os
import urllib.request
import urllib.error
import json

def purge_jsdelivr_cache():
    # Base URL for jsDelivr purge API
    base_purge_url = "https://purge.jsdelivr.net/gh/tony-jjjentinc/assets@main/"
    
    # Locate the output directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Read the version from package.json to determine the directory (e.g. v1)
    package_json_path = os.path.join(project_root, 'package.json')
    try:
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            version_major = package_data.get('version', '1.0.0').split('.')[0]
            output_dir_name = f'v{version_major}'
    except Exception:
        output_dir_name = 'v1'

    colors_dir = os.path.join(project_root, 'colors', output_dir_name)
    
    if not os.path.exists(colors_dir):
        print(f"Directory {colors_dir} does not exist.")
        return

    print("============================================================")
    print("  Purging jsDelivr Edge Cache")
    print("============================================================")
    
    success_count = 0
    fail_count = 0

    for root, dirs, files in os.walk(colors_dir):
        for file in files:
            if file.endswith(".css"):
                # Construct the relative path from the repository root
                # Since we know it's in colors/vX/filename
                rel_path = f"colors/{output_dir_name}/{file}"
                purge_url = base_purge_url + rel_path
                
                print(f"Purging {rel_path}...", end=" ")
                try:
                    req = urllib.request.Request(purge_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req) as response:
                        if response.status == 200:
                            print("✅ Success")
                            success_count += 1
                        else:
                            print(f"❌ Failed (Status {response.status})")
                            fail_count += 1
                except urllib.error.URLError as e:
                    print(f"❌ Failed ({e.reason})")
                    fail_count += 1

    print("\n============================================================")
    print(f"  Purge Complete! ✅ {success_count} Successful | ❌ {fail_count} Failed")
    print("============================================================")

if __name__ == "__main__":
    purge_jsdelivr_cache()
