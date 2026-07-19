#!/usr/bin/env python3
"""
generate_colors.py - Bootstrap 5 Primary Color CSS Generator
=============================================================
Generates department and sub-department color override CSS files
from the _template.css file.

Usage:
    python3 scripts/generate_colors.py

Output:
    css/colors/{dept}/{dept}.css
    css/colors/{dept}/{dept}-sub-dept-{1-8}.css
"""

import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "css", "colors", "_template.css")
COLORS_DIR = os.path.join(PROJECT_ROOT, "css", "colors")

# Department definitions: (folder_name, display_name, hex_color)
DEPARTMENTS = [
    ("gmo",                        "GMO",                        "#008000"),
    ("admin",                      "Admin",                      "#FFD700"),
    ("facilities",                 "Facilities",                 "#0000FF"),
    ("leasing",                    "Leasing",                    "#800000"),
    ("hr",                         "HR",                         "#800080"),
    ("procurement-and-inventory",  "Procurement and Inventory",  "#C08081"),
    ("controller",                 "Controller",                 "#008080"),
    ("treasury",                   "Treasury",                   "#F28500"),
]

# Sub-department shade definitions: (suffix, mode, weight)
# mode: "tint" = mix with white, "shade" = mix with black
# weight: percentage (0.0 to 1.0)
SUB_DEPARTMENTS = [
    ("sub-dept-1", "tint",  0.85),   # Lightest
    ("sub-dept-2", "tint",  0.70),   # Lighter
    ("sub-dept-3", "tint",  0.50),   # Light
    ("sub-dept-4", "tint",  0.30),   # Light-medium
    ("sub-dept-5", "tint",  0.15),   # Medium-dark
    ("sub-dept-6", "shade", 0.15),   # Dark
    ("sub-dept-7", "shade", 0.30),   # Darker
    ("sub-dept-8", "shade", 0.45),   # Darkest
]

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
    """Generate all CSS files for all departments and sub-departments."""
    files_created = 0

    for folder, display_name, hex_color in DEPARTMENTS:
        dept_dir = os.path.join(COLORS_DIR, folder)
        os.makedirs(dept_dir, exist_ok=True)

        base_rgb = hex_to_rgb(hex_color)

        # --- Generate base department file ---
        placeholders = compute_placeholders(base_rgb)
        css_content = generate_css(
            template, placeholders,
            display_name, "Base", hex_color
        )
        output_path = os.path.join(dept_dir, f"{folder}.css")
        with open(output_path, "w") as f:
            f.write(css_content)
        files_created += 1

        text_indicator = "◐" if text_color_on(base_rgb) == "#212529" else "●"
        print(f"  {text_indicator} {folder}/{folder}.css  →  {hex_color}")

        # --- Generate sub-department files ---
        for suffix, mode, weight in SUB_DEPARTMENTS:
            if mode == "tint":
                sub_rgb = tint_color(base_rgb, weight)
            else:
                sub_rgb = shade_color(base_rgb, weight)

            sub_hex = rgb_to_hex(*sub_rgb)
            placeholders = compute_placeholders(sub_rgb)
            css_content = generate_css(
                template, placeholders,
                display_name, suffix, sub_hex
            )
            filename = f"{folder}-{suffix}.css"
            output_path = os.path.join(dept_dir, filename)
            with open(output_path, "w") as f:
                f.write(css_content)
            files_created += 1

            sub_text_indicator = "◐" if text_color_on(sub_rgb) == "#212529" else "●"
            print(f"    {sub_text_indicator} {folder}/{filename}  →  {sub_hex}")

    return files_created


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
    print()


if __name__ == "__main__":
    main()
