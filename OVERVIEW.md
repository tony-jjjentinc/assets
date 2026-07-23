# Project Overview

This repository contains an automated system to generate unified, pre-compiled Bootstrap 5 CSS files for different project "groups." 

By defining your color palette and design tokens in simple JSON files, a Python script orchestrates the official Sass compiler to generate fully themed Bootstrap CSS files. This ensures that all components, utilities, and hover states natively adopt your brand colors without writing manual CSS overrides.

## Repository Structure

```text
/
├── groupColors.json       # Defines the base (primary) color for each group
├── systemColors.json      # Defines standard UI colors (success, danger, etc.)
├── designTokens.json      # Defines global styling (fonts, border radius, shadows)
├── generator.py           # The Python build script
├── package.json           # Node.js configuration to manage Bootstrap & Sass
├── node_modules/          # Source files for Bootstrap and dart-sass
└── colors/                # 📂 Output directory containing the compiled .css files
```

---

## How to Modify the Styling

All theming configuration is driven by three JSON files. You **do not** need to edit any CSS manually.

### 1. Adding or Modifying a Group (Primary Colors)
To change the primary brand color of an existing group or to add a completely new group, edit `groupColors.json`:

```json
{
  "group_a": "#BDEA68",
  "group_b": "#228B22",
  "group_c": "#FF5733"  // <-- Just add a new line!
}
```

### 2. Modifying System Colors
To change the secondary, success, danger, or warning colors that apply across *all* groups, edit `systemColors.json`:

```json
{
  "secondary": "#848B92",
  "success": "#00E936",
  "warning": "#F9E500",
  ...
}
```

### 3. Modifying Unified Design Tokens
To change global design elements like typography, corner rounding, or shadows, edit `designTokens.json`:

```json
{
  "font-family": "'Inter', sans-serif",
  "font-url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
  "border-radius": "0.5rem",
  "box-shadow": "0 0.5rem 1rem rgba(0, 0, 0, 0.15)",
  "enable-shadows": "true"
}
```

---

## How to Re-generate the CSS Files

Whenever you make a change to the `.json` files, you must run the Python generator to rebuild the CSS files.

### Prerequisites
Make sure you have Node.js and Python installed. If this is a fresh clone of the repository, you need to install the dependencies first:
```bash
npm install
```

### Generating the Output
To generate or update the CSS files, run the Python script from the root of the project:

```bash
python3 generator.py
```

**What the script does:**
1. Reads your `.json` configurations.
2. For each group in `groupColors.json`, it creates a temporary Sass (`.scss`) file.
3. It injects your colors and variables into the Sass file.
4. It imports the official Bootstrap source code from `node_modules/`.
5. It compiles everything into a highly compressed, standalone CSS file in the `colors/` directory (e.g., `colors/group_a.css`).
6. It cleans up the temporary files.

Once the script finishes successfully, simply commit your changes and push to GitHub!
