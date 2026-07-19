#!/usr/bin/env python3
"""
generate_colors.py - Bootstrap 5 Primary Color CSS Generator
=============================================================
Generates department and theme variant color override CSS files
from the _template.css file.

Usage:
    python3 scripts/generate_colors.py

Output:
    css/colors/{dept}/{dept}.css
    css/colors/{dept}/{dept}-theme-variant-{1-8}.css
"""

import os
import sys
import json
import re
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "css", "colors", "_template.css")
COLORS_DIR = os.path.join(PROJECT_ROOT, "css", "colors")

# Department definitions with curated Light and Dark theme palettes
DEPARTMENTS = {
    "gmo": {
        "name": "GMO",
        "base": "#008000",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (GMO)",
                "color": "#008000",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Honeydew",
                "color": "#F0FFF0",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Mint Cream",
                "color": "#F5FFFA",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Pale Green",
                "color": "#98FB98",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Celadon",
                "color": "#ACE1AF",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Sea Green",
                "color": "#2E8B57",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Forest Green",
                "color": "#228B22",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Olive Drab",
                "color": "#6B8E23",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Dark Green",
                "color": "#006400",
                "theme": "dark"
            }
        ]
    },
    "admin": {
        "name": "Admin",
        "base": "#FFD700",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (Admin)",
                "color": "#FFD700",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Lemon Chiffon",
                "color": "#FFFACD",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Pale Goldenrod",
                "color": "#EEE8AA",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Khaki",
                "color": "#F0E68C",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Jasmine",
                "color": "#F8DE7E",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Goldenrod",
                "color": "#DAA520",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Dark Goldenrod",
                "color": "#B8860B",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Peru",
                "color": "#CD853F",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Saddle Brown",
                "color": "#8B4513",
                "theme": "dark"
            }
        ]
    },
    "facilities": {
        "name": "Facilities",
        "base": "#0000FF",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (Facilities)",
                "color": "#0000FF",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Alice Blue",
                "color": "#F0F8FF",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Powder Blue",
                "color": "#B0E0E6",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Baby Blue",
                "color": "#89CFF0",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Carolina Blue",
                "color": "#4B9CD3",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Steel Blue",
                "color": "#4682B4",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Independence",
                "color": "#4C516D",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Sapphire Blue",
                "color": "#0F52BA",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Oxford Blue",
                "color": "#002147",
                "theme": "dark"
            }
        ]
    },
    "leasing": {
        "name": "Leasing",
        "base": "#800000",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (Leasing)",
                "color": "#800000",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Misty Rose",
                "color": "#FFE4E1",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Pink Lace",
                "color": "#FFDDF4",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Salmon Pink",
                "color": "#FF91A4",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Indian Red",
                "color": "#CD5C5C",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Firebrick",
                "color": "#B22222",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Crimson",
                "color": "#DC143C",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Burgundy",
                "color": "#800020",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Dark Red",
                "color": "#8B0000",
                "theme": "dark"
            }
        ]
    },
    "hr": {
        "name": "HR",
        "base": "#800080",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (HR)",
                "color": "#800080",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Lavender",
                "color": "#E6E6FA",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Thistle",
                "color": "#D8BFD8",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Plum",
                "color": "#DDA0DD",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Orchid",
                "color": "#DA70D6",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Medium Purple",
                "color": "#9370DB",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Blue Violet",
                "color": "#8A2BE2",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Indigo",
                "color": "#4B0082",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Dark Magenta",
                "color": "#8B008B",
                "theme": "dark"
            }
        ]
    },
    "procurement-and-inventory": {
        "name": "Procurement and Inventory",
        "base": "#C08081",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (Procurement and Inventory)",
                "color": "#C08081",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Seashell",
                "color": "#FFF5EE",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Peach Puff",
                "color": "#FFDAB9",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Rosy Brown",
                "color": "#BC8F8F",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Light Coral",
                "color": "#F08080",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Chestnut",
                "color": "#954535",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Sienna",
                "color": "#A0522D",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Mahogany",
                "color": "#C04000",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Dark Brown",
                "color": "#654321",
                "theme": "dark"
            }
        ]
    },
    "controller": {
        "name": "Controller",
        "base": "#008080",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (Controller)",
                "color": "#008080",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Light Cyan",
                "color": "#E0FFFF",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Pale Turquoise",
                "color": "#AFEEEE",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Aquamarine",
                "color": "#7FFFD4",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Medium Aquamarine",
                "color": "#66CDAA",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Light Sea Green",
                "color": "#20B2AA",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Cadet Blue",
                "color": "#5F9EA0",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Dark Cyan",
                "color": "#008B8B",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Dark Slate Gray",
                "color": "#2F4F4F",
                "theme": "dark"
            }
        ]
    },
    "treasury": {
        "name": "Treasury",
        "base": "#F28500",
        "theme_variants": [
            {
                "suffix": "base",
                "name": "Base (Treasury)",
                "color": "#F28500",
                "theme": "base"
            },
            {
                "suffix": "light-1",
                "name": "Papaya Whip",
                "color": "#FFEFD5",
                "theme": "light"
            },
            {
                "suffix": "light-2",
                "name": "Moccasin",
                "color": "#FFE4B5",
                "theme": "light"
            },
            {
                "suffix": "light-3",
                "name": "Peach",
                "color": "#FFE5B4",
                "theme": "light"
            },
            {
                "suffix": "light-4",
                "name": "Sandy Brown",
                "color": "#F4A460",
                "theme": "light"
            },
            {
                "suffix": "dark-1",
                "name": "Coral",
                "color": "#FF7F50",
                "theme": "dark"
            },
            {
                "suffix": "dark-2",
                "name": "Tomato",
                "color": "#FF6347",
                "theme": "dark"
            },
            {
                "suffix": "dark-3",
                "name": "Orange Red",
                "color": "#FF4500",
                "theme": "dark"
            },
            {
                "suffix": "dark-4",
                "name": "Rust",
                "color": "#B7410E",
                "theme": "dark"
            }
        ]
    }
}



# ---------------------------------------------------------------------------
# Color Utility Functions
# ---------------------------------------------------------------------------

def hex_to_rgb(hex_color):
    """Convert a hex color string to an (r, g, b) tuple."""
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def rgb_to_hex(r, g, b):
    """Convert RGB values to a hex color string."""
    return f"#{int(round(r)):02x}{int(round(g)):02x}{int(round(b)):02x}"


def shade_color(rgb, weight):
    """
    Mix a color with black.
    Equivalent to Bootstrap's shade-color($color, $weight).
    shade-color = mix(black, color, weight) = color * (1 - weight)
    """
    r, g, b = rgb
    factor = 1.0 - weight
    return (r * factor, g * factor, b * factor)


def tint_color(rgb, weight):
    """
    Mix a color with white.
    Equivalent to Bootstrap's tint-color($color, $weight).
    tint-color = mix(white, color, weight) = color + (255 - color) * weight
    """
    r, g, b = rgb
    return (
        r + (255 - r) * weight,
        g + (255 - g) * weight,
        b + (255 - b) * weight,
    )


def relative_luminance(r, g, b):
    """Calculate WCAG 2.0 relative luminance."""
    def linearize(c):
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(l1, l2):
    """Calculate WCAG contrast ratio between two luminance values."""
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def text_color_on(rgb):
    """
    Determine whether white or dark text should be used on a given background.
    Uses WCAG contrast ratio to pick the higher-contrast option.
    """
    r, g, b = rgb
    lum = relative_luminance(r, g, b)
    white_contrast = contrast_ratio(1.0, lum)
    black_contrast = contrast_ratio(lum, 0.0)
    return "#fff" if white_contrast >= black_contrast else "#212529"


def format_rgb(rgb):
    """Format an RGB tuple as a CSS-friendly string like '0, 128, 0'."""
    r, g, b = rgb
    return f"{int(round(r))}, {int(round(g))}, {int(round(b))}"


# ---------------------------------------------------------------------------
# Template Processing
# ---------------------------------------------------------------------------

def compute_placeholders(base_rgb):
    """
    Given a base RGB color, compute all placeholder values needed
    by the _template.css file.
    """
    hover_rgb = shade_color(base_rgb, 0.20)
    active_rgb = shade_color(base_rgb, 0.25)
    active_border_rgb = shade_color(base_rgb, 0.30)
    text_emphasis_rgb = shade_color(base_rgb, 0.60)
    bg_subtle_rgb = tint_color(base_rgb, 0.80)
    border_subtle_rgb = tint_color(base_rgb, 0.60)
    focus_border_rgb = tint_color(base_rgb, 0.50)

    focus_border_hex = rgb_to_hex(*focus_border_rgb)

    # Dark mode variants (Bootstrap 5.3 dark theme formulas)
    dark_text_emphasis_rgb = tint_color(base_rgb, 0.40)
    dark_bg_subtle_rgb = shade_color(base_rgb, 0.80)
    dark_border_subtle_rgb = shade_color(base_rgb, 0.40)
    dark_link_hover_rgb = tint_color(base_rgb, 0.60)

    return {
        "{{PRIMARY}}":                      rgb_to_hex(*base_rgb),
        "{{PRIMARY_RGB}}":                  format_rgb(base_rgb),
        "{{TEXT_ON_PRIMARY}}":              text_color_on(base_rgb),
        "{{PRIMARY_HOVER}}":               rgb_to_hex(*hover_rgb),
        "{{PRIMARY_HOVER_RGB}}":           format_rgb(hover_rgb),
        "{{PRIMARY_ACTIVE}}":              rgb_to_hex(*active_rgb),
        "{{PRIMARY_ACTIVE_BORDER}}":       rgb_to_hex(*active_border_rgb),
        "{{PRIMARY_FOCUS_RGB}}":           format_rgb(base_rgb),
        "{{PRIMARY_TEXT_EMPHASIS}}":        rgb_to_hex(*text_emphasis_rgb),
        "{{PRIMARY_BG_SUBTLE}}":           rgb_to_hex(*bg_subtle_rgb),
        "{{PRIMARY_BORDER_SUBTLE}}":       rgb_to_hex(*border_subtle_rgb),
        "{{PRIMARY_FOCUS_BORDER}}":        focus_border_hex,
        "{{PRIMARY_FOCUS_BORDER_ENCODED}}": focus_border_hex.replace("#", "%23"),
        "{{DARK_PRIMARY_TEXT_EMPHASIS}}":     rgb_to_hex(*dark_text_emphasis_rgb),
        "{{DARK_PRIMARY_TEXT_EMPHASIS_RGB}}": format_rgb(dark_text_emphasis_rgb),
        "{{DARK_PRIMARY_BG_SUBTLE}}":        rgb_to_hex(*dark_bg_subtle_rgb),
        "{{DARK_PRIMARY_BORDER_SUBTLE}}":    rgb_to_hex(*dark_border_subtle_rgb),
        "{{DARK_PRIMARY_LINK_HOVER}}":       rgb_to_hex(*dark_link_hover_rgb),
        "{{DARK_PRIMARY_LINK_HOVER_RGB}}":   format_rgb(dark_link_hover_rgb),
    }


def generate_css(template, placeholders, dept_name, color_label, hex_color):
    """
    Generate a CSS file from the template by replacing all placeholders.
    Prepends a file header comment.
    """
    # Build header
    header = (
        f"/* ==========================================================================\n"
        f"   {dept_name} — {color_label}\n"
        f"   Primary Color: {hex_color}\n"
        f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"   ========================================================================== */\n\n"
    )

    # Strip the template's documentation header (everything before the first :root)
    content = template
    root_index = content.find(":root {")
    if root_index != -1:
        # Find the last comment block before :root
        section_marker = "/* ==========================================================================\n   Root-Level Variables"
        marker_index = content.find(section_marker)
        if marker_index != -1:
            content = content[marker_index:]

    # Replace all placeholders
    for placeholder, value in placeholders.items():
        content = content.replace(placeholder, value)

    return header + content


# ---------------------------------------------------------------------------
# File Generation
# ---------------------------------------------------------------------------

def generate_department_files(template):
    """Generate all CSS files for all departments and theme variants."""
    files_created = 0

    for folder, config in DEPARTMENTS.items():
        display_name = config["name"]
        hex_color = config["base"]
        
        dept_dir = os.path.join(COLORS_DIR, folder)
        
        # Clear out old generated CSS files to prevent orphaned files
        if os.path.exists(dept_dir):
            for file_name in os.listdir(dept_dir):
                if file_name.endswith('.css') and file_name != '_template.css':
                    file_path = os.path.join(dept_dir, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)

        os.makedirs(dept_dir, exist_ok=True)

        base_rgb = hex_to_rgb(hex_color)

        # --- Generate all files (Base and Variants) ---
        for sub_dept in config.get("theme_variants", []):
            suffix = sub_dept["suffix"]
            color_name = sub_dept["name"]
            sub_hex = sub_dept["color"]
            theme = sub_dept["theme"]

            sub_rgb = hex_to_rgb(sub_hex)
            placeholders = compute_placeholders(sub_rgb)
            
            css_content = generate_css(
                template, placeholders,
                display_name, color_name, sub_hex
            )
            
            filename = f"{folder}-{suffix}.css" if suffix != "base" else f"{folder}.css"
            output_path = os.path.join(dept_dir, filename)
            with open(output_path, "w") as f:
                f.write(css_content)
            files_created += 1

            sub_text_indicator = "◐" if text_color_on(sub_rgb) == "#212529" else "●"
            print(f"  {sub_text_indicator} {folder}/{filename}  →  {sub_hex}")

    return files_created



def generate_config_js():
    """Generates a config.js file for frontend theme configuration."""
    config_data = {"departments": []}
    
    for folder, config in DEPARTMENTS.items():
        dept_obj = {
            "folder": folder,
            "label": config["name"],
            "themeVariants": []
        }
        
        for sub in config.get("theme_variants", []):
            # Only use the suffix if it's not base, else use folder
            file_val = f"{folder}-{sub['suffix']}" if sub["suffix"] != "base" else folder
            dept_obj["themeVariants"].append({
                "file": file_val,
                "label": sub["name"],
                "theme": sub["theme"]
            })
            
        config_data["departments"].append(dept_obj)
        
    js_content = f"window.THEME_CONFIG = {json.dumps(config_data, indent=2)};\n"
    
    output_path = os.path.join(PROJECT_ROOT, "examples", "config.js")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(js_content)
        
    print(f"Generated {output_path}")


def update_index_html():
    """Updates the departments table in index.html with the latest colors."""
    index_path = os.path.join(PROJECT_ROOT, "index.html")
    
    if not os.path.exists(index_path):
        print(f"Warning: {index_path} not found.")
        return

    with open(index_path, "r") as f:
        html_content = f.read()

    # Generate the table rows
    rows = []
    for folder, config in DEPARTMENTS.items():
        name = config["name"]
        base_color = config["base"]
        row = f'                <tr><td>{name}</td><td><span class="badge" style="background:{base_color}">&nbsp;&nbsp;&nbsp;</span> {base_color}</td><td><code>css/colors/{folder}/{folder}.css</code></td></tr>'
        rows.append(row)
    
    rows_html = "\n".join(rows) + "\n                "

    # Replace the content between the markers using regex
    pattern = r'(<!-- DEPARTMENTS_TABLE_START -->\n)(.*?)(<!-- DEPARTMENTS_TABLE_END -->)'
    updated_html = re.sub(
        pattern, 
        f'\\g<1>{rows_html}\\g<3>', 
        html_content, 
        flags=re.DOTALL
    )

    with open(index_path, "w") as f:
        f.write(updated_html)
        
    print(f"Updated table in {index_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("Bootstrap 5 Primary Color CSS Generator")
    print("=" * 60)
    print()

    # Read template
    if not os.path.exists(TEMPLATE_PATH):
        print(f"ERROR: Template not found at {TEMPLATE_PATH}")
        sys.exit(1)

    with open(TEMPLATE_PATH, "r") as f:
        template = f.read()

    print(f"Template: {TEMPLATE_PATH}")
    print(f"Output:   {COLORS_DIR}/")
    print()
    print("Legend: ● = white text on primary  ◐ = dark text on primary")
    print("-" * 60)

    # Generate all files
    files_created = generate_department_files(template)

    print("-" * 60)
    print(f"Done! Generated {files_created} CSS files.")
    generate_config_js()
    update_index_html()
    print()


if __name__ == "__main__":
    main()
