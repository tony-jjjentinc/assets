# Project Overview

This repository contains an automated system to generate unified, pre-compiled Bootstrap 5 CSS files for different project "groups." 

By defining your color palette and design tokens in simple JSON files, a Python script orchestrates the official Sass compiler to generate fully themed Bootstrap CSS files. This ensures that all components, utilities, and hover states natively adopt your brand colors without writing manual CSS overrides.

## Repository Structure

```text
/
├── config/
│   ├── groupColors.json       # Defines the base (primary) color for each group
│   ├── systemColors.json      # Defines standard UI colors (success, danger, etc.) and custom brand colors
│   ├── statusColors.json      # Defines custom semantic status colors for dashboards
│   └── designTokens.json      # Defines global styling (fonts, border radius, shadows, contrast, subtle strengths)
├── scripts/
│   └── generator.py           # The Python build script
├── package.json           # Node.js configuration to manage Bootstrap & Sass
├── node_modules/          # Source files for Bootstrap and dart-sass
└── colors/                # 📂 Output directory
    └── v1/                # 📂 Versioned CSS files and accessibility reports
```

---

## How to Modify the Styling

All theming configuration is driven by three JSON files. You **do not** need to edit any CSS manually.

### 1. Adding or Modifying a Group (Primary Colors)
To change the primary brand color of an existing group or to add a completely new group, edit `config/groupColors.json`:

```json
{
  "group:variant_1": "#BDEA68",
  "group:variant_2": "#228B22",
  "new_group:variant": "#FF5733"  // <-- Use group:variant naming format!
}
```

### 2. Modifying System Colors
To change the secondary, success, danger, or warning colors that apply across *all* groups, edit `config/systemColors.json`:

```json
{
  "jjjei-primary": "#YOURHEX",
  "jjjei-secondary": "#YOURHEX",
  "secondary": "#848B92",
  "success": "#00E936",
  ...
}
```

### 3. Modifying Unified Design Tokens
To change global design elements like typography, corner rounding, shadows, or **color contrast accessibility settings**, edit `config/designTokens.json`:

```json
{
  "font-family": "'Inter', sans-serif",
  "font-url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
  "border-radius": "0.5rem",
  "enable-shadows": "true",
  "min-contrast-ratio": "4.5",
  "color-contrast-dark": "#212529",
  "color-contrast-light": "#ffffff",
  "base-bg-tint-strength": 90,
  "base-bg-shade-strength": 90
}
```

#### Contrast & Subtle Accessibility Settings

| Token | Default | Description |
|:------|:--------|:------------|
| `min-contrast-ratio` | `4.5` | WCAG minimum contrast ratio. Use `4.5` for AA compliance, `7.0` for AAA. |
| `color-contrast-dark` | `#212529` | Dark text color used on light backgrounds (Bootstrap's gray-900). |
| `color-contrast-light` | `#ffffff` | Light text color used on dark backgrounds. |
| `base-bg-tint-strength` | `90` | Tint mix percentage for the custom `.bg-primary-base` utility in light mode. |
| `base-bg-shade-strength` | `90` | Shade mix percentage for the custom `.bg-primary-base` utility in dark mode. |
| `subtle-bg-tint-weight` | `80` | Tint mix percentage for primary subtle backgrounds in light mode (lower = stronger color). |
| `subtle-border-tint-weight`| `60` | Tint mix percentage for primary subtle borders. |
| `subtle-bg-shade-weight` | `80` | Shade mix percentage for primary subtle backgrounds in dark mode. |
| `subtle-border-shade-weight`| `40` | Shade mix percentage for primary subtle borders in dark mode. |

The build script automatically detects primary colors that fail WCAG contrast thresholds and applies corrective overrides (darkened text emphasis, tinted subtle backgrounds) so that text and icons remain readable.

---

## How to Re-generate the CSS Files

Whenever you make a change to the `.json` files, you must run the build command to rebuild the CSS files.

### Prerequisites
Make sure you have Node.js and Python installed. If this is a fresh clone of the repository, you need to install the dependencies first:
```bash
npm install
```

### Generating the Output
To generate or update the CSS files, run the build command:

```bash
npm run build
```

*(Note: You can also manually run `python3 scripts/generator.py`. Because the script automatically resolves its root directory, you can safely execute it from anywhere in the project!)*

**What the script does:**
1. Reads your `.json` configurations.
2. **Pre-validates** each group's primary color against WCAG contrast thresholds.
3. For colors that fail validation, it **auto-generates** corrective SCSS overrides (darkened text emphasis, accessible link colors, tinted subtle backgrounds and borders).
4. For each group in `config/groupColors.json`, it creates a temporary Sass (`.scss`) file with contrast-safe variables injected.
5. It selectively imports ONLY the Bootstrap components that rely on color (e.g. buttons, badges) to create lightweight overrides.
6. It compiles everything into a highly compressed CSS file in a versioned directory (e.g., `colors/v1/group_a.css`).
7. It cleans up the temporary files.
8. It generates a **contrast accessibility report** at `colors/v1/contrast-report.md` summarizing pass/fail status and auto-fixes applied per group.

Once the script finishes successfully, simply commit your changes and push to GitHub!
