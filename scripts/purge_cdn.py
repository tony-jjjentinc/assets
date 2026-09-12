import os
import urllib.request
import urllib.error
import json

def purge_jsdelivr_cache():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Read the version from package.json
    package_json_path = os.path.join(project_root, 'package.json')
    try:
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)
            version_major = package_data.get('version', '4.0.0').split('.')[0]
            output_dir_name = f'v{version_major}'
    except Exception:
        output_dir_name = 'v4'

    latest_dir = os.path.join(project_root, 'colors', 'latest')
    if not os.path.exists(latest_dir):
        print(f"Directory {latest_dir} does not exist.")
        return

    # Endpoints to purge:
    # 1. @latest/colors/latest/<file> (Modern rolling release)
    # 2. @main/colors/latest/<file>   (Main branch latest)
    # 3. @main/colors/vX/<file>       (Legacy directory)
    endpoint_templates = [
        "https://purge.jsdelivr.net/gh/tony-jjjentinc/assets@latest/colors/latest/{file}",
        "https://purge.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/latest/{file}",
        f"https://purge.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/{output_dir_name}/{{file}}",
    ]

    print("============================================================")
    print("  Purging jsDelivr Edge Cache")
    print("  Endpoints: @latest/colors/latest, @main/colors/latest, @main/colors/" + output_dir_name)
    print("============================================================")
    
    css_files = [f for f in os.listdir(latest_dir) if f.endswith(".css")]
    success_count = 0
    fail_count = 0

    for file in css_files:
        for tmpl in endpoint_templates:
            purge_url = tmpl.format(file=file)
            print(f"Purging {purge_url.replace('https://purge.jsdelivr.net/gh/tony-jjjentinc/assets@', '@')}...", end=" ")
            try:
                req = urllib.request.Request(purge_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    if response.status == 200:
                        print("✅")
                        success_count += 1
                    else:
                        print(f"❌ ({response.status})")
                        fail_count += 1
            except urllib.error.URLError as e:
                print(f"❌ ({e.reason})")
                fail_count += 1

    print("\n============================================================")
    print(f"  Purge Complete! ✅ {success_count} Successful | ❌ {fail_count} Failed")
    print("============================================================")

if __name__ == "__main__":
    purge_jsdelivr_cache()
