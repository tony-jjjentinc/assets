import os
import json

# Read colors.json
try:
    with open('utils/colors.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: utils/colors.json not found.")
    exit(1)

# Create directories
os.makedirs('css/dpt', exist_ok=True)
os.makedirs('css/sbdpt', exist_ok=True)

def get_hover_color(hex_color):
    """Simple function to slightly darken a color for hover state."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    else:
        return "#000000"
    
    # Darken by 15%
    factor = 0.85
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def generate_css_content(primary, text, theme):
    hover = get_hover_color(primary)
    
    if theme == "light":
        card_bg = '#F3F4F6'
    else:
        card_bg = '#1f1f1f'
        
    return f""":root {{
    --jjjei-primary-color: {primary};
    --jjjei-hover-color: {hover};
    --jjjei-text-color: {text};
    --jjjei-card-bg: {card_bg};
}}
"""

for dept_key, dept_data in data.get('departments', {}).items():
    # Write base color CSS
    base = dept_data.get('base', {})
    if base:
        css_content = generate_css_content(base['hex'], base['text'], base['theme'])
        with open(f"css/dpt/{dept_key}.css", "w", encoding="utf-8") as f:
            f.write(css_content)
            
    # Write shades CSS
    for shade_key, shade_data in dept_data.get('shades', {}).items():
        css_content = generate_css_content(shade_data['hex'], shade_data['text'], shade_data['theme'])
        with open(f"css/sbdpt/{dept_key}-shade-{shade_key}.css", "w", encoding="utf-8") as f:
            f.write(css_content)

print("Successfully generated all CSS files from colors.json.")
