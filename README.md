# Bootstrap 5 Custom Color CDN

A GitHub Pages-hosted CDN providing custom Bootstrap 5 style and color overrides for web apps deployed via Google Apps Script.

## Quick Start

Add these three lines to your Google Apps Script HTML file:

```html
<!-- 1. Bootstrap 5 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

<!-- 2. Base style overrides (fonts, shadows, border-radius) -->
<link href="https://{username}.github.io/assets_v2/css/base.css" rel="stylesheet">

<!-- 3. Department color override (pick one) -->
<link href="https://{username}.github.io/assets_v2/css/colors/gmo/gmo.css" rel="stylesheet">
```

And the Bootstrap JS at the end of `<body>`:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

## Available Departments

| Department | Color | Folder |
|---|---|---|
| GMO | Green (`#008000`) | `css/colors/gmo/` |
| Admin | Gold (`#FFD700`) | `css/colors/admin/` |
| Facilities | Blue (`#0000FF`) | `css/colors/facilities/` |
| Leasing | Maroon (`#800000`) | `css/colors/leasing/` |
| HR | Purple (`#800080`) | `css/colors/hr/` |
| Procurement and Inventory | Rose Gold (`#C08081`) | `css/colors/procurement-and-inventory/` |
| Controller | Teal (`#008080`) | `css/colors/controller/` |
| Treasury | Tangerine (`#F28500`) | `css/colors/treasury/` |

Each department folder contains a base color file and 8 sub-department shade variants (`sub-dept-1` to `sub-dept-8`).

All color files include `[data-bs-theme="dark"]` overrides for Bootstrap 5.3 dark mode support.

## Documentation

- [Architecture Overview](docs/OVERVIEW.md)
- [Setup Guide](docs/SETUP.md)
- [Usage Guide](docs/USAGE.md)
- [Color Reference](docs/COLORS.md)

## Project Structure

```
css/
├── base.css                           # Font + component style overrides
└── colors/
    ├── _template.css                  # Template for creating new color files
    ├── gmo/                           # GMO department (green)
    │   ├── gmo.css                    # Base color
    │   ├── gmo-sub-dept-1.css         # Lightest shade
    │   └── ...                        # sub-dept-2 through sub-dept-8
    ├── admin/                         # Admin department (gold)
    ├── facilities/                    # Facilities department (blue)
    ├── leasing/                       # Leasing department (maroon)
    ├── hr/                            # HR department (purple)
    ├── procurement-and-inventory/     # Procurement & Inventory (rose gold)
    ├── controller/                    # Controller department (teal)
    └── treasury/                      # Treasury department (tangerine)
examples/
└── sample.html                        # Interactive demo with theme switcher
index.html                             # Landing page (GitHub Pages root)
.nojekyll                              # Prevents Jekyll processing
```
