import json
import os
import shutil
import subprocess
from datetime import datetime

# Dynamically set working directory to project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(PROJECT_ROOT)

# WCAG 2.1 Contrast Constants
WHITE = '#ffffff'
DARK_TEXT_DEFAULT = '#212529'
MIN_CONTRAST_RATIO_DEFAULT = 4.5

# ─────────────────────────────────────────────
# Contrast Utility Functions
# ─────────────────────────────────────────────

def relative_luminance(hex_color):
    """Calculate WCAG 2.1 relative luminance from a hex color string."""
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

    def linearize(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast_ratio(hex1, hex2):
    """Calculate WCAG contrast ratio between two hex colors."""
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def shade_color(hex_color, weight):
    """Darken a color by mixing with black (mirrors Bootstrap's shade-color()).
    Weight is a percentage (0-100). Higher weight = darker result."""
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    factor = 1 - (weight / 100)
    r, g, b = int(r * factor), int(g * factor), int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def tint_color(hex_color, weight):
    """Lighten a color by mixing with white (mirrors Bootstrap's tint-color()).
    Weight is a percentage (0-100). Higher weight = lighter result."""
    hex_color = hex_color.lstrip('#')
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    factor = weight / 100
    r = int(r + (255 - r) * factor)
    g = int(g + (255 - g) * factor)
    b = int(b + (255 - b) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

def find_accessible_shade(hex_color, background, min_ratio, start_weight=40, max_weight=90, step=5):
    """Find the minimum shade weight that achieves the target contrast ratio against a background.
    Returns (shaded_hex, weight) or (None, None) if no weight works."""
    for weight in range(start_weight, max_weight + 1, step):
        shaded = shade_color(hex_color, weight)
        ratio = contrast_ratio(shaded, background)
        if ratio >= min_ratio:
            return shaded, weight
    return shade_color(hex_color, max_weight), max_weight

# ─────────────────────────────────────────────
# Pre-Validation & Contrast Report
# ─────────────────────────────────────────────

def validate_color_contrast(group_name, primary_color, min_ratio, dark_text):
    """Validate a primary color's contrast and generate corrective SCSS overrides if needed.

    Returns a dict with:
        - 'status': 'PASS', 'WARN', or 'FAIL'
        - 'ratio_vs_white': contrast ratio against white
        - 'ratio_vs_dark': contrast ratio against dark text
        - 'scss_overrides': list of SCSS variable override strings
        - 'fixes_applied': list of human-readable fix descriptions
    """
    ratio_vs_white = contrast_ratio(primary_color, WHITE)
    ratio_vs_dark = contrast_ratio(primary_color, dark_text)

    result = {
        'group': group_name,
        'primary': primary_color,
        'ratio_vs_white': ratio_vs_white,
        'ratio_vs_dark': ratio_vs_dark,
        'status': 'PASS',
        'scss_overrides': [],
        'fixes_applied': []
    }

    # Check if primary color is too light for text on white backgrounds
    if ratio_vs_white < min_ratio:
        result['status'] = 'WARN'

        # Generate a darkened shade for text emphasis
        text_emphasis, weight = find_accessible_shade(primary_color, WHITE, min_ratio)
        text_emphasis_ratio = contrast_ratio(text_emphasis, WHITE)

        result['scss_overrides'].append(f"$primary-text-emphasis: {text_emphasis};")
        result['scss_overrides'].append(f"$link-color: {text_emphasis};")
        result['fixes_applied'].append(
            f"text-emphasis darkened (shade {weight}%) to {text_emphasis} (ratio: {text_emphasis_ratio:.2f}:1)"
        )


    return result

# ─────────────────────────────────────────────
# Report Generation
# ─────────────────────────────────────────────

def generate_contrast_report(results, min_ratio):
    """Generate a Markdown contrast report from validation results."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lines = [
        f"# Contrast Report",
        f"",
        f"**Generated:** {now}  ",
        f"**WCAG Threshold:** {min_ratio}:1 (Level AA)  ",
        f"**Total Groups:** {len(results)}  ",
        f"",
    ]

    # Summary counts
    pass_count = sum(1 for r in results if r['status'] == 'PASS')
    warn_count = sum(1 for r in results if r['status'] == 'WARN')
    lines.append(f"**Results:** ✅ {pass_count} Pass | ⚠️ {warn_count} Auto-Fixed")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Table header
    lines.append("| Group | Primary | vs White | vs Dark | Status | Auto-Fix Applied |")
    lines.append("|:------|:--------|:---------|:--------|:-------|:-----------------|")

    for r in results:
        white_indicator = "✅" if r['ratio_vs_white'] >= min_ratio else "⚠️"
        dark_indicator = "✅" if r['ratio_vs_dark'] >= min_ratio else "⚠️"

        fixes_str = ", ".join(r['fixes_applied']) if r['fixes_applied'] else "—"
        status_str = "✅ PASS" if r['status'] == 'PASS' else "⚠️ AUTO-FIXED"

        lines.append(
            f"| {r['group']} | `{r['primary']}` | "
            f"{r['ratio_vs_white']:.2f}:1 {white_indicator} | "
            f"{r['ratio_vs_dark']:.2f}:1 {dark_indicator} | "
            f"{status_str} | {fixes_str} |"
        )

    lines.append("")
    return "\n".join(lines)

# ─────────────────────────────────────────────
# JSON Loader
# ─────────────────────────────────────────────

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# ─────────────────────────────────────────────
# Main Generation Pipeline
# ─────────────────────────────────────────────

def generate_css():
    print("Loading configurations...")
    try:
        group_colors = load_json('config/groupColors.json')
        system_colors = load_json('config/systemColors.json')
        design_tokens = load_json('config/designTokens.json')
        status_colors = load_json('config/statusColors.json')
        loaders_config = load_json('config/loaders.json') if os.path.exists('config/loaders.json') else {}
        patterns_config = load_json('config/backgroundPatterns.json') if os.path.exists('config/backgroundPatterns.json') else {}
    except Exception as e:
        print(f"Error loading JSON configurations: {e}")
        return

    # Read contrast settings from design tokens (with defaults)
    min_ratio = float(design_tokens.get('min-contrast-ratio', MIN_CONTRAST_RATIO_DEFAULT))
    dark_text = design_tokens.get('color-contrast-dark', DARK_TEXT_DEFAULT)
    light_text = design_tokens.get('color-contrast-light', WHITE)

    bg_tint = float(design_tokens.get('subtle-bg-tint-weight', 75))
    border_tint = float(design_tokens.get('subtle-border-tint-weight', 75))
    bg_shade = float(design_tokens.get('subtle-bg-shade-weight', 75))
    border_shade = float(design_tokens.get('subtle-border-shade-weight', 75))

    faint_bg_tint = float(design_tokens.get('faint-bg-tint-weight', 20))
    faint_border_tint = float(design_tokens.get('faint-border-tint-weight', 20))
    faint_bg_shade = float(design_tokens.get('faint-bg-shade-weight', 20))
    faint_border_shade = float(design_tokens.get('faint-border-shade-weight', 20))

    shaded_bg_shade = float(design_tokens.get('shaded-bg-shade-weight', 35))
    shaded_border_shade = float(design_tokens.get('shaded-border-shade-weight', 35))
    
    base_bg_tint_strength = float(design_tokens.get('base-bg-tint-strength', 40))
    base_bg_shade_strength = float(design_tokens.get('base-bg-shade-strength', 40))

    override_spinner = design_tokens.get('override-bootstrap-spinner', False)

    def generate_subtle_overrides(name, hex_color):
        overrides = [
            f"${name}-bg-subtle: {tint_color(hex_color, bg_tint)};",
            f"${name}-border-subtle: {tint_color(hex_color, border_tint)};",
            f"${name}-bg-subtle-dark: {shade_color(hex_color, bg_shade)};",
            f"${name}-border-subtle-dark: {shade_color(hex_color, border_shade)};",

            f"${name}-bg-faint: {tint_color(hex_color, faint_bg_tint)};",
            f"${name}-border-faint: {tint_color(hex_color, faint_border_tint)};",
            f"${name}-bg-faint-dark: {shade_color(hex_color, faint_bg_shade)};",
            f"${name}-border-faint-dark: {shade_color(hex_color, faint_border_shade)};",

            f"${name}-bg-shaded: {shade_color(hex_color, shaded_bg_shade)};",
            f"${name}-border-shaded: {shade_color(hex_color, shaded_border_shade)};"
        ]
        return "\n".join(overrides)

    try:
        package_info = load_json('package.json')
        version_major = package_info.get('version', '4.0.0').split('.')[0]
    except Exception as e:
        print(f"Error loading package.json: {e}")
        version_major = '4'
        
    output_dirs = [f'colors/v{version_major}', 'colors/latest']
    output_dir = output_dirs[0]
    
    # Ensure output directories exist
    for d in output_dirs:
        os.makedirs(d, exist_ok=True)

    # Collect contrast validation results for the report
    contrast_results = []

    print(f"\n{'='*60}")
    print(f"  WCAG Contrast Pre-Validation (threshold: {min_ratio}:1)")
    print(f"{'='*60}")

    for group_key, primary_color in group_colors.items():
        print(f"\nProcessing {group_key}...")

        base_group_key = group_key.split(':')[0]
        # Look for the exact base group key, otherwise fallback to the ':0' variant (the standard base color), otherwise fallback to the primary color itself
        base_group_color = group_colors.get(base_group_key, group_colors.get(f"{base_group_key}:0", primary_color))
        base_bg_light = tint_color(base_group_color, base_bg_tint_strength)
        base_bg_dark = shade_color(base_group_color, base_bg_shade_strength)

        # ── Phase 1: Pre-Validation ──
        validation = validate_color_contrast(group_key, primary_color, min_ratio, dark_text)
        contrast_results.append(validation)

        if validation['status'] == 'WARN':
            print(f"  ⚠️  Contrast warning for {primary_color} (vs white: {validation['ratio_vs_white']:.2f}:1)")
            for fix in validation['fixes_applied']:
                print(f"      → Auto-fix: {fix}")
        else:
            print(f"  ✅  Contrast OK (vs white: {validation['ratio_vs_white']:.2f}:1, vs dark: {validation['ratio_vs_dark']:.2f}:1)")

        safe_filename = group_key.replace(":", "-")
        # ── Phase 2: Build SCSS ──
        temp_scss_file = f"_temp_{safe_filename}.scss"
        temp_output_css_file = f"{output_dir}/{safe_filename}.css"
        final_output_css_file = f"{output_dir}/{group_key}.css"

        scss_content = []

        # 1. Fonts
        if 'font-url' in design_tokens and design_tokens['font-url']:
            scss_content.append(f"@import url('{design_tokens['font-url']}');")
            
        if 'font-face-url' in design_tokens and 'font-family-raw' in design_tokens:
            scss_content.append("@font-face {")
            scss_content.append(f"  font-family: '{design_tokens['font-family-raw']}';")
            scss_content.append(f"  src: url('{design_tokens['font-face-url']}') format('woff2');")
            scss_content.append("  font-weight: normal;")
            scss_content.append("  font-style: normal;")
            scss_content.append("}")

        # 2. Contrast Configuration
        scss_content.append(f"$min-contrast-ratio: {min_ratio};")
        scss_content.append(f'$color-contrast-dark: {dark_text};')
        scss_content.append(f'$color-contrast-light: {light_text};')

        # 3. System Variables Override
        scss_content.append(f"$primary: {primary_color};")
        scss_content.append(generate_subtle_overrides("primary", primary_color))

        theme_colors_entries = ['"primary": $primary']

        for name, color in system_colors.items():
            scss_content.append(f"${name}: {color};")
            scss_content.append(generate_subtle_overrides(name, color))
            theme_colors_entries.append(f'"{name}": ${name}')

        for name, color in status_colors.items():
            full_name = f"status-{name}"
            scss_content.append(f"${full_name}: {color};")
            scss_content.append(generate_subtle_overrides(full_name, color))
            theme_colors_entries.append(f'"{full_name}": ${full_name}')

        scss_content.append("")
        scss_content.append("$theme-colors: (")
        scss_content.append("  " + ",\n  ".join(theme_colors_entries))
        scss_content.append(");")

        # 4. Design Tokens
        if 'font-family' in design_tokens:
            scss_content.append(f"$font-family-sans-serif: {design_tokens['font-family']};")
        if 'border-radius' in design_tokens:
            scss_content.append(f"$border-radius: {design_tokens['border-radius']};")
        if 'box-shadow' in design_tokens:
            scss_content.append(f"$box-shadow: {design_tokens['box-shadow']};")
        if 'btn-box-shadow' in design_tokens:
            scss_content.append(f"$btn-box-shadow: {design_tokens['btn-box-shadow']};")
        if 'enable-shadows' in design_tokens:
            scss_content.append(f"$enable-shadows: {design_tokens['enable-shadows']};")

        # 5. Inject contrast auto-fix overrides (if any)
        if validation['scss_overrides']:
            scss_content.append("")
            scss_content.append("// Auto-generated contrast fixes")
            for override in validation['scss_overrides']:
                scss_content.append(override)

        # 6. Selectively Import Bootstrap (Lightweight Overrides)
        scss_content.append("")
        scss_content.append('// Core variables and mixins')
        scss_content.append('@import "node_modules/bootstrap/scss/functions";')
        scss_content.append('@import "node_modules/bootstrap/scss/variables";')
        scss_content.append('@import "node_modules/bootstrap/scss/variables-dark";')
        scss_content.append('@import "node_modules/bootstrap/scss/maps";')
        scss_content.append('')
        scss_content.append('// Bootstrap does not automatically populate subtle maps for new theme colors. We must merge them:')
        scss_content.append('@each $color, $value in $theme-colors {')
        scss_content.append('  @if not map-has-key($theme-colors-bg-subtle, $color) {')
        scss_content.append(f'    $theme-colors-bg-subtle: map-merge($theme-colors-bg-subtle, ($color: mix(#fff, $value, {bg_tint}%)));')
        scss_content.append('  }')
        scss_content.append('  @if not map-has-key($theme-colors-border-subtle, $color) {')
        scss_content.append(f'    $theme-colors-border-subtle: map-merge($theme-colors-border-subtle, ($color: mix(#fff, $value, {border_tint}%)));')
        scss_content.append('  }')
        scss_content.append('  @if not map-has-key($theme-colors-text, $color) {')
        scss_content.append('    $theme-colors-text: map-merge($theme-colors-text, ($color: color-contrast($value)));')
        scss_content.append('  }')
        scss_content.append('}')
        scss_content.append('')
        scss_content.append('@import "node_modules/bootstrap/scss/mixins";')
        scss_content.append('@import "node_modules/bootstrap/scss/utilities";')
        scss_content.append('')
        scss_content.append('// Populate utility maps after utilities.scss defines them:')
        scss_content.append('@each $color, $value in $theme-colors {')
        scss_content.append('  @if not map-has-key($utilities-bg-subtle, $color + "-subtle") {')
        scss_content.append('    $utilities-bg-subtle: map-merge($utilities-bg-subtle, (#{$color}-subtle: var(--#{$prefix}#{$color}-bg-subtle)));')
        scss_content.append('  }')
        scss_content.append('  @if not map-has-key($utilities-border-subtle, $color + "-subtle") {')
        scss_content.append('    $utilities-border-subtle: map-merge($utilities-border-subtle, (#{$color}-subtle: var(--#{$prefix}#{$color}-border-subtle)));')
        scss_content.append('  }')
        scss_content.append('  @if not map-has-key($utilities-text-emphasis-colors, $color + "-emphasis") {')
        scss_content.append('    $utilities-text-emphasis-colors: map-merge($utilities-text-emphasis-colors, (#{$color}-emphasis: var(--#{$prefix}#{$color}-text-emphasis)));')
        scss_content.append('  }')
        scss_content.append('}')
        scss_content.append('')
        scss_content.append('// Update $utilities map with expanded values so Bootstrap API generates all subtle utility classes')
        scss_content.append('$subtle-bg-config: map-get($utilities, "subtle-background-color");')
        scss_content.append('$subtle-bg-config: map-merge($subtle-bg-config, (values: $utilities-bg-subtle));')
        scss_content.append('$subtle-border-config: map-get($utilities, "subtle-border-color");')
        scss_content.append('$subtle-border-config: map-merge($subtle-border-config, (values: $utilities-border-subtle));')
        scss_content.append('$text-color-config: map-get($utilities, "text-color");')
        scss_content.append('$text-color-vals: map-get($text-color-config, "values");')
        scss_content.append('$text-color-vals: map-merge($text-color-vals, $utilities-text-emphasis-colors);')
        scss_content.append('$text-color-config: map-merge($text-color-config, (values: $text-color-vals));')
        scss_content.append('$utilities: map-merge($utilities, (')
        scss_content.append('  "subtle-background-color": $subtle-bg-config,')
        scss_content.append('  "subtle-border-color": $subtle-border-config,')
        scss_content.append('  "text-color": $text-color-config')
        scss_content.append('));')
        scss_content.append('')
        scss_content.append('// Components that depend on colors')
        scss_content.append('@import "node_modules/bootstrap/scss/root";')
        scss_content.append('@import "node_modules/bootstrap/scss/buttons";')
        scss_content.append('@import "node_modules/bootstrap/scss/button-group";')
        scss_content.append('@import "node_modules/bootstrap/scss/badge";')
        scss_content.append('@import "node_modules/bootstrap/scss/alert";')
        scss_content.append('@import "node_modules/bootstrap/scss/list-group";')
        scss_content.append('@import "node_modules/bootstrap/scss/progress";')
        scss_content.append('@import "node_modules/bootstrap/scss/spinners";')
        scss_content.append('@import "node_modules/bootstrap/scss/tables";')
        scss_content.append('@import "node_modules/bootstrap/scss/forms";')
        scss_content.append('@import "node_modules/bootstrap/scss/pagination";')
        scss_content.append('@import "node_modules/bootstrap/scss/nav";')
        scss_content.append('@import "node_modules/bootstrap/scss/navbar";')
        scss_content.append('@import "node_modules/bootstrap/scss/accordion";')
        scss_content.append('@import "node_modules/bootstrap/scss/dropdown";')
        scss_content.append('@import "node_modules/bootstrap/scss/breadcrumb";')
        scss_content.append('@import "node_modules/bootstrap/scss/carousel";')
        
        scss_content.append('// Configure utilities to only generate color-related utilities to save space')
        scss_content.append('$utilities: (')
        scss_content.append('  "color": map-get($utilities, "color"),')
        scss_content.append('  "text-opacity": map-get($utilities, "text-opacity"),')
        scss_content.append('  "text-color": map-get($utilities, "text-color"),')
        scss_content.append('  "link-opacity": map-get($utilities, "link-opacity"),')
        scss_content.append('  "link-offset": map-get($utilities, "link-offset"),')
        scss_content.append('  "link-underline": map-get($utilities, "link-underline"),')
        scss_content.append('  "link-underline-opacity": map-get($utilities, "link-underline-opacity"),')
        scss_content.append('  "background-color": map-get($utilities, "background-color"),')
        scss_content.append('  "bg-opacity": map-get($utilities, "bg-opacity"),')
        scss_content.append('  "subtle-background-color": map-get($utilities, "subtle-background-color"),')
        scss_content.append('  "gradient": map-get($utilities, "gradient"),')
        scss_content.append('  "border-color": map-get($utilities, "border-color"),')
        scss_content.append('  "subtle-border-color": map-get($utilities, "subtle-border-color"),')
        scss_content.append('  "border-opacity": map-get($utilities, "border-opacity")')
        scss_content.append(');')
        
        scss_content.append('// Generate utilities')
        scss_content.append('@import "node_modules/bootstrap/scss/utilities/api";')

        # 7. Inject Custom Utilities & Color Variants
        scss_content.append("")
        scss_content.append("// Custom Utility: bg-primary-base")
        scss_content.append(".bg-primary-base {")
        scss_content.append(f"  background-color: {base_bg_light} !important;")
        scss_content.append("}")
        scss_content.append('[data-bs-theme="dark"] .bg-primary-base {')
        scss_content.append(f"  background-color: {base_bg_dark} !important;")
        scss_content.append("}")
        scss_content.append("")
        
        # Color Variant Utilities (-gradient 45deg, -gradient-subtle 45deg, -shaded, -faint)
        scss_content.append("// 45deg Gradient Utilities (Primary, System & Status colors)")
        scss_content.append("@each $color, $value in $theme-colors {")
        scss_content.append("  .bg-#{$color}-gradient {")
        scss_content.append("    background: linear-gradient(45deg, $value 0%, var(--#{$prefix}#{$color}-bg-subtle, mix(#fff, $value, 75%)) 100%) !important;")
        scss_content.append("  }")
        scss_content.append("  [data-bs-theme=\"dark\"] .bg-#{$color}-gradient {")
        scss_content.append("    background: linear-gradient(45deg, $value 0%, var(--#{$prefix}#{$color}-bg-subtle-dark, mix(#000, $value, 75%)) 100%) !important;")
        scss_content.append("  }")
        scss_content.append("")
        scss_content.append("  .bg-#{$color}-gradient-subtle {")
        scss_content.append("    background: linear-gradient(45deg, var(--#{$prefix}#{$color}-bg-subtle, mix(#fff, $value, 75%)) 0%, color-mix(in srgb, var(--#{$prefix}#{$color}-bg-subtle, mix(#fff, $value, 75%)) 50%, transparent) 100%) !important;")
        scss_content.append("  }")
        scss_content.append("  [data-bs-theme=\"dark\"] .bg-#{$color}-gradient-subtle {")
        scss_content.append("    background: linear-gradient(45deg, var(--#{$prefix}#{$color}-bg-subtle-dark, mix(#000, $value, 75%)) 0%, color-mix(in srgb, var(--#{$prefix}#{$color}-bg-subtle-dark, mix(#000, $value, 75%)) 50%, transparent) 100%) !important;")
        scss_content.append("  }")
        scss_content.append("")
        scss_content.append("  .bg-#{$color}-shaded {")
        scss_content.append("    background-color: mix(#000, $value, 35%) !important;")
        scss_content.append("  }")
        scss_content.append("  .border-#{$color}-shaded {")
        scss_content.append("    border-color: mix(#000, $value, 35%) !important;")
        scss_content.append("  }")
        scss_content.append("")
        scss_content.append("  .bg-#{$color}-faint {")
        scss_content.append("    background-color: mix(#fff, $value, 20%) !important;")
        scss_content.append("  }")
        scss_content.append("  .border-#{$color}-faint {")
        scss_content.append("    border-color: mix(#fff, $value, 20%) !important;")
        scss_content.append("  }")
        scss_content.append("  [data-bs-theme=\"dark\"] .bg-#{$color}-faint {")
        scss_content.append("    background-color: mix(#000, $value, 20%) !important;")
        scss_content.append("  }")
        scss_content.append("  [data-bs-theme=\"dark\"] .border-#{$color}-faint {")
        scss_content.append("    border-color: mix(#000, $value, 20%) !important;")
        scss_content.append("  }")
        scss_content.append("}")
        scss_content.append("")

        # 8. Inject Custom Keyframe Loaders
        scss_content.append("// Custom Loader Animation Utilities")
        scss_content.append("@keyframes loader-spin {")
        scss_content.append("  to { transform: rotate(360deg); }")
        scss_content.append("}")
        scss_content.append("@keyframes loader-pulse {")
        scss_content.append("  0%, 100% { transform: scale(0.8); opacity: 0.5; }")
        scss_content.append("  50% { transform: scale(1.2); opacity: 1; }")
        scss_content.append("}")
        scss_content.append("@keyframes loader-dots {")
        scss_content.append("  0%, 20% { transform: translateY(0); }")
        scss_content.append("  50% { transform: translateY(-6px); }")
        scss_content.append("  80%, 100% { transform: translateY(0); }")
        scss_content.append("}")
        scss_content.append("")
        
        loader_target_selector = ".loader, .spinner-border" if override_spinner else ".loader"
        scss_content.append(f"{loader_target_selector} {{")
        scss_content.append("  display: inline-block;")
        scss_content.append("  width: 2rem;")
        scss_content.append("  height: 2rem;")
        scss_content.append("  vertical-align: -0.125em;")
        scss_content.append("  border: 0.2em solid currentColor;")
        scss_content.append("  border-right-color: transparent;")
        scss_content.append("  border-radius: 50%;")
        scss_content.append("  animation: loader-spin 0.75s linear infinite;")
        scss_content.append("}")
        scss_content.append(".loader-pulse {")
        scss_content.append("  display: inline-block;")
        scss_content.append("  width: 2rem;")
        scss_content.append("  height: 2rem;")
        scss_content.append("  vertical-align: -0.125em;")
        scss_content.append("  border: none !important;")
        scss_content.append("  background-color: currentColor;")
        scss_content.append("  border-radius: 50%;")
        scss_content.append("  animation: loader-pulse 1s ease-in-out infinite !important;")
        scss_content.append("}")
        scss_content.append(".loader-dots {")
        scss_content.append("  display: inline-block;")
        scss_content.append("  vertical-align: -0.125em;")
        scss_content.append("  border: none !important;")
        scss_content.append("  border-radius: 0 !important;")
        scss_content.append("  animation: loader-dots 1.2s ease-in-out infinite !important;")
        scss_content.append("}")
        scss_content.append("")
        scss_content.append("// Loader Color Variants")
        scss_content.append(".loader-primary { color: var(--#{$prefix}primary) !important; }")
        scss_content.append(".loader-light { color: var(--#{$prefix}light) !important; }")
        scss_content.append(".loader-dark { color: var(--#{$prefix}dark) !important; }")
        scss_content.append("@each $color, $value in $theme-colors {")
        scss_content.append("  .loader-#{$color} { color: var(--#{$prefix}#{$color}, $value) !important; }")
        scss_content.append("}")
        scss_content.append("")

        # 9. Inject Background Patterns
        scss_content.append("// Configurable Background Patterns")
        if isinstance(patterns_config, dict):
            for p_name, p_data in patterns_config.items():
                if isinstance(p_data, dict) and 'svg' in p_data:
                    scss_content.append(f".bg-pattern-{p_name} {{")
                    scss_content.append(f"  background-image: url(\"{p_data['svg']}\") !important;")
                    if 'background-size' in p_data:
                        scss_content.append(f"  background-size: {p_data['background-size']} !important;")
                    if 'background-repeat' in p_data:
                        scss_content.append(f"  background-repeat: {p_data['background-repeat']} !important;")
                    scss_content.append("}")

        # Write to temporary file
        with open(temp_scss_file, 'w') as f:
            f.write("\n".join(scss_content))

        # ── Phase 3: Compile ──
        print(f"  Compiling {temp_scss_file} to {final_output_css_file}...")
        try:
            subprocess.run(
                ["npx", "sass", temp_scss_file, temp_output_css_file, "--style=compressed", "--no-source-map"],
                check=True
            )
            if temp_output_css_file != final_output_css_file:
                if os.path.exists(temp_output_css_file):
                    if os.path.exists(final_output_css_file):
                        os.remove(final_output_css_file)
                    os.rename(temp_output_css_file, final_output_css_file)
            
            # Sync generated file to latest directory
            for d in output_dirs[1:]:
                shutil.copy2(final_output_css_file, f"{d}/{group_key}.css")

            print(f"  Successfully generated {final_output_css_file}")
        except subprocess.CalledProcessError as e:
            print(f"  Error compiling {group_key}: {e}")
        finally:
            # Clean up temporary file
            if os.path.exists(temp_scss_file):
                os.remove(temp_scss_file)

    # ── Phase 4: Generate Contrast Report ──
    print(f"\n{'='*60}")
    print(f"  Generating Contrast Report")
    print(f"{'='*60}")

    report = generate_contrast_report(contrast_results, min_ratio)
    for d in output_dirs:
        report_path = f'{d}/contrast-report.md'
        with open(report_path, 'w') as f:
            f.write(report)

    pass_count = sum(1 for r in contrast_results if r['status'] == 'PASS')
    warn_count = sum(1 for r in contrast_results if r['status'] == 'WARN')
    print(f"\n  Reports saved to: {', '.join([f'{d}/contrast-report.md' for d in output_dirs])}")
    print(f"  Summary: ✅ {pass_count} Pass | ⚠️ {warn_count} Auto-Fixed | {len(contrast_results)} Total")
    print(f"\n{'='*60}")
    print(f"  Build Complete!")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    generate_css()
