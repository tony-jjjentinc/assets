import json
import os
import subprocess

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def generate_css():
    print("Loading configurations...")
    try:
        group_colors = load_json('groupColors.json')
        system_colors = load_json('systemColors.json')
        design_tokens = load_json('designTokens.json')
    except Exception as e:
        print(f"Error loading JSON configurations: {e}")
        return

    # Ensure output directory exists
    os.makedirs('colors', exist_ok=True)

    for group, primary_color in group_colors.items():
        print(f"\nProcessing {group}...")
        temp_scss_file = f"_temp_{group}.scss"
        output_css_file = f"colors/{group}.css"
        
        # Build the SCSS content
        scss_content = []
        
        # 1. Fonts
        if 'font-url' in design_tokens:
            scss_content.append(f"@import url('{design_tokens['font-url']}');")
        
        # 2. System Variables Override
        scss_content.append(f"$primary: {primary_color};")
        
        for name, color in system_colors.items():
            scss_content.append(f"${name}: {color};")
            
        # 3. Design Tokens
        if 'font-family' in design_tokens:
            scss_content.append(f"$font-family-sans-serif: {design_tokens['font-family']};")
        if 'border-radius' in design_tokens:
            scss_content.append(f"$border-radius: {design_tokens['border-radius']};")
        if 'box-shadow' in design_tokens:
            scss_content.append(f"$box-shadow: {design_tokens['box-shadow']};")
        if 'enable-shadows' in design_tokens:
            scss_content.append(f"$enable-shadows: {design_tokens['enable-shadows']};")
            
        # 4. Import Bootstrap
        scss_content.append('@import "node_modules/bootstrap/scss/bootstrap";')
        
        # Write to temporary file
        with open(temp_scss_file, 'w') as f:
            f.write("\n".join(scss_content))
            
        # Compile using Sass
        print(f"Compiling {temp_scss_file} to {output_css_file}...")
        try:
            # Using npx sass so it runs the locally installed sass from node_modules
            subprocess.run(
                ["npx", "sass", temp_scss_file, output_css_file, "--style=compressed", "--no-source-map"],
                check=True
            )
            print(f"Successfully generated {output_css_file}")
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {group}: {e}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_scss_file):
                os.remove(temp_scss_file)

if __name__ == "__main__":
    generate_css()
