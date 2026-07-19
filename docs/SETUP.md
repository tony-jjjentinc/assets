# Setup Guide

## Prerequisites

- A GitHub account
- Git installed locally
- Python 3.6+ (only needed if regenerating color files)

## Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/{username}/assets_v2.git
cd assets_v2
```

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **Deploy from a branch**
4. Under **Branch**, select `main` and `/ (root)`
5. Click **Save**

GitHub Pages will deploy your site at:
```
https://{username}.github.io/assets_v2/
```

### 3. Verify Deployment

After a few minutes, verify the CSS files are accessible:

```
https://{username}.github.io/assets_v2/css/base.css
https://{username}.github.io/assets_v2/css/colors/gmo/gmo.css
```

## Project Structure

```
assets_v2/
├── css/
│   ├── base.css                       # Font + component style overrides
│   └── colors/
│       ├── _template.css              # Template (not served to end users)
│       ├── gmo/                       # 1 base + 8 sub-dept files
│       ├── admin/
│       ├── facilities/
│       ├── leasing/
│       ├── hr/
│       ├── procurement-and-inventory/
│       ├── controller/
│       └── treasury/
├── docs/                              # Documentation
├── examples/
│   └── sample.html                    # Interactive demo with theme switcher
├── index.html                         # Landing page (GitHub Pages root)
├── .nojekyll                          # Prevents Jekyll processing
└── scripts/
    └── generate_colors.py             # Color file generator (dev tool)
```

## Regenerating Color Files

If you need to change department colors or add new departments:

### 1. Edit the Configuration

Open `scripts/generate_colors.py` and modify the `DEPARTMENTS` list:

```python
DEPARTMENTS = [
    ("folder-name", "Display Name", "#HexColor"),
    # ... add or modify entries
]
```

### 2. Run the Generator

```bash
python3 scripts/generate_colors.py
```

This will regenerate all CSS files in `css/colors/`.

### 3. Commit and Push

```bash
git add css/colors/
git commit -m "Regenerate color files"
git push
```

GitHub Pages will automatically redeploy.

## Adding a New Department

1. Add the department to the `DEPARTMENTS` list in `scripts/generate_colors.py`
2. Run the generator: `python3 scripts/generate_colors.py`
3. The new folder and files will be created automatically
4. Commit and push

## Verifying Changes

After making any changes, use the [interactive sample page](../examples/sample.html) to visually verify all components render correctly with the new colors. The sample includes a department/sub-department theme switcher.

## Customizing Base Styles

Edit `css/base.css` directly. Changes apply to all departments.

Common customizations:
- **Font**: Change the Google Fonts `@import` URL and `--bs-body-font-family`
- **Border radius**: Adjust `--bs-border-radius` and related variables
- **Shadows**: Modify `box-shadow` values on `.card`, `.modal-content`, etc.

## Customizing the Color Template

If you need to override additional Bootstrap components:

1. Edit `css/colors/_template.css`
2. Add the new CSS rules using `{{PLACEHOLDER}}` tokens
3. Regenerate all color files: `python3 scripts/generate_colors.py`
