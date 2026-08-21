# CSS Override & Custom Colors Reference Guide

This document provides a comprehensive reference for the custom CSS stylesheets compiled and distributed by **JJJEI Core Assets**. It details how to import the assets, primary color modifications, custom brand color tokens, and semantic status color utilities.

---

## 1. Basic Description

The **JJJEI Core Assets** system provides pre-compiled, theme-specific Bootstrap 5 stylesheets. Instead of maintaining cumbersome manual CSS overrides across multiple Google Apps Script web apps and web portals, brand styling is centralized through JSON tokens.

When compiled, each group stylesheet (e.g. `jjjei_admin:0.css`, `jjjei_facilities:1.css`) packages:
- The base department/group **primary color** and its variations.
- Selective color overrides for all core Bootstrap 5 components.
- Custom non-Bootstrap brand color classes (`jjjei-primary`, `jjjei-secondary`).
- Custom numeric dashboard status colors (`status-0` through `status-9`).
- Custom extended color variants (gradient, faint, shaded, and subtle utilities).
- Automated WCAG 2.1 AA accessibility contrast adjustments.

---

## 2. Import Setup to Project (via jsDelivr)

Assets are served via the **jsDelivr** global CDN for fast delivery, CORS compatibility in Google Apps Script iframes, and caching.

### Standard HTML Integration

Include the base Bootstrap 5 CSS stylesheet followed by the desired group theme stylesheet:

```html
<!-- 1. Bootstrap 5 Base CSS (Required) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" crossorigin="anonymous">

<!-- 2. JJJEI Group Theme Stylesheet Override -->

<!-- Option A: Latest (Recommended - auto-updates with releases) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/latest/jjjei_admin:0.css">

<!-- Option B: Pinned Major Version (e.g., v4) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/v4/jjjei_admin:0.css">
```

### Dynamic Multi-Tenant Setup (Google Apps Script)

You can pass the group CSS dynamically via URL parameters in Google Apps Script:

**Code.gs:**
```javascript
function doGet(e) {
  var group = e.parameter.group || 'jjjei_admin:0';
  var template = HtmlService.createTemplateFromFile('Index');
  template.cssUrl = 'https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/latest/' + group + '.css';
  return template.evaluate().setTitle('JJJEI Portal');
}
```

**Index.html:**
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="<?= cssUrl ?>">
```

### Interactive Components (Bootstrap JS)
If using interactive elements like modals, dropdowns, tooltips, or offcanvases, include the Bootstrap JavaScript bundle before the closing `</body>` tag:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
```

---

## 3. Overrides on the Primary Color

Importing a group's theme stylesheet replaces Bootstrap's default primary color (`#0d6efd`) with the group's assigned brand color and automatically regenerates associated component styles and custom utilities.

### Standard Bootstrap Component Overrides
All components that leverage `$primary` adopt the active group color:
- **Buttons:** `.btn-primary`, `.btn-outline-primary`, `.btn-check:checked + .btn-primary`
- **Badges:** `.badge.bg-primary`, `.text-bg-primary`
- **Alerts:** `.alert-primary`
- **Navs & Navigation:** `.nav-pills .nav-link.active`, `.nav-tabs .nav-link.active`, `.navbar`
- **Forms & Inputs:** Focus borders, check/radio active states, switches (`.form-check-input:checked`)
- **Tables & Lists:** `.table-primary`, `.list-group-item-primary`, `.list-group-item.active`
- **Feedback & Progress:** `.progress-bar.bg-primary`, `.spinner-border.text-primary`
- **Interactive Containers:** `.accordion-button:not(.collapsed)`, `.dropdown-item.active`, `.pagination .page-item.active .page-link`
- **And More...**

### Custom Primary Utilities

| Utility Class | Description |
|:---|:---|
| `.bg-primary` | Standard primary background color. |
| `.text-primary` | Standard primary text color. |
| `.border-primary` | Standard primary border color. |
| `.bg-primary-subtle` | Light tint (25% color / 75% white in light mode; 75% shade in dark mode) derived from the specific variant color. |
| `.border-primary-subtle` | Border matching the subtle tint weight. |
| `.text-primary-emphasis` | Primary color auto-darkened to achieve WCAG 4.5:1 AA contrast against white backgrounds. |
| `.bg-primary-base` | Anchor page background using a 60% tint of the department's parent base color (`:0`), ensuring brand continuity. |
| `.bg-primary-gradient` | 45-degree linear gradient transitioning from the primary color to subtle primary tint. |
| `.bg-primary-gradient-subtle` | 45-degree linear gradient transitioning from subtle primary tint to 50% opacity subtle primary tint. |
| `.bg-primary-faint` | 20% faint tint background (`mix(#fff, $primary, 20%)` in light mode; `mix(#000, $primary, 20%)` in dark mode). |
| `.border-primary-faint` | 20% faint border. |
| `.bg-primary-shaded` | 35% shaded background (`mix(#000, $primary, 35%)`). |
| `.border-primary-shaded` | 35% shaded border. |
| `.loader-primary` | Colorizes animated custom loaders (`.loader`, `.loader-pulse`, `.loader-dots`) to the primary color. |

---

## 4. Custom Colors (Non-Bootstrap Brand Classes)

The theme system injects custom non-Bootstrap brand color tokens into Bootstrap's `$theme-colors` map:

- **`jjjei-primary`** (`#184421` - JJJEI Forest Green)
- **`jjjei-secondary`** (`#918F90` - JJJEI Neutral Gray)

### Available Class Variants for Custom Colors

Each custom brand color generates a complete family of Bootstrap-compatible classes:

#### For `jjjei-primary`:
- **Backgrounds:**
  - `.bg-jjjei-primary` — Solid background
  - `.bg-jjjei-primary-subtle` — Light subtle background
  - `.bg-jjjei-primary-gradient` — 45° gradient
  - `.bg-jjjei-primary-faint` — 20% faint tint
  - `.bg-jjjei-primary-shaded` — 35% darkened shade
- **Text & Borders:**
  - `.text-jjjei-primary` — Text color
  - `.text-jjjei-primary-emphasis` — High-contrast text emphasis
  - `.border-jjjei-primary` — Solid border
  - `.border-jjjei-primary-subtle` — Subtle border
  - `.border-jjjei-primary-faint` — Faint border
  - `.border-jjjei-primary-shaded` — Shaded border
- **Components & Loaders:**
  - `.btn-jjjei-primary`, `.btn-outline-jjjei-primary`
  - `.alert-jjjei-primary`
  - `.badge.bg-jjjei-primary`, `.text-bg-jjjei-primary`
  - `.table-jjjei-primary`
  - `.list-group-item-jjjei-primary`
  - `.loader-jjjei-primary`

#### For `jjjei-secondary`:
- Same structure: `.bg-jjjei-secondary`, `.bg-jjjei-secondary-subtle`, `.bg-jjjei-secondary-gradient`, `.bg-jjjei-secondary-faint`, `.bg-jjjei-secondary-shaded`, `.text-jjjei-secondary`, `.text-jjjei-secondary-emphasis`, `.border-jjjei-secondary`, `.border-jjjei-secondary-subtle`, `.border-jjjei-secondary-faint`, `.border-jjjei-secondary-shaded`, `.btn-jjjei-secondary`, `.btn-outline-jjjei-secondary`, `.alert-jjjei-secondary`, `.loader-jjjei-secondary`, `.table-jjjei-secondary`, `.list-group-item-jjjei-secondary`.

#### Example Usage:
```html
<div class="card border-jjjei-primary">
  <div class="card-header bg-jjjei-primary text-white">
    JJJEI Official Header
  </div>
  <div class="card-body bg-jjjei-primary-faint">
    <p class="text-jjjei-primary-emphasis">Departmental notice using brand tokens.</p>
    <button class="btn btn-jjjei-primary">Submit Report</button>
    <button class="btn btn-outline-jjjei-secondary">Cancel</button>
  </div>
</div>
```

---

## 5. Custom Status Colors

The system defines 10 numeric status tokens (`0` through `9`) specifically for data tables, status badges, pipeline indicators, and dashboards.

### Status Color Palette Mapping

| Code | Hex Code | Color Name | Intended Semantic Meaning |
|:---:|:---:|:---|:---|
| `0` | `#28A745` | Green | Completed, Resolved, Successful |
| `1` | `#0D6EFD` | Blue | Assigned, Information, Action Required |
| `2` | `#17A2B8` | Cyan | Processing, Under Review |
| `3` | `#FFC107` | Yellow | Warning, Pending Approval |
| `4` | `#FD7E14` | Orange | In Progress, Due Soon |
| `5` | `#DC3545` | Red | Urgent, Delayed, Error, Rejected |
| `6` | `#6F42C1` | Purple | Pending Verification, Escalated |
| `7` | `#8B5E3C` | Brown | On Hold, Suspended |
| `8` | `#6C757D` | Gray | Not Started, Draft, Read Only |
| `9` | `#343A40` | Dark Gray | Cancelled, Archived, Void |

### Available Status Class Variants

Replace `#` with the status number (`0` to `9`):

- **Background Utilities:**
  - `.bg-status-#` — Full status background
  - `.bg-status-#-subtle` — 25% subtle background tint (dark-mode aware)
  - `.bg-status-#-gradient` — 45° linear gradient
  - `.bg-status-#-gradient-subtle` — 45° linear gradient from subtle tint to 50% opacity subtle tint
  - `.bg-status-#-faint` — 20% faint background tint
  - `.bg-status-#-shaded` — 35% shaded background
- **Text & Emphasis Utilities:**
  - `.text-status-#` — Status color text
  - `.text-status-#-emphasis` — WCAG-compliant high-contrast status text
- **Border Utilities:**
  - `.border-status-#` — Solid status border
  - `.border-status-#-subtle` — Subtle status border
  - `.border-status-#-faint` — Faint status border
  - `.border-status-#-shaded` — Shaded status border
- **Component Classes:**
  - `.btn-status-#`, `.btn-outline-status-#` — Status button styles
  - `.alert-status-#` — Status alert banner
  - `.table-status-#` — Highlighted table row / cell
  - `.list-group-item-status-#` — Highlighted list item
  - `.loader-status-#` — Colored loader spinner

### Example Dashboard Status Usage:

```html
<!-- 1. Badges -->
<span class="badge bg-status-0">Completed</span>
<span class="badge bg-status-4 text-dark">In Progress</span>
<span class="badge bg-status-5">Urgent</span>

<!-- 2. Subtle Status Alert / Notice -->
<div class="alert alert-status-3 d-flex align-items-center">
  <span class="text-status-3-emphasis">Pending manager sign-off.</span>
</div>

<!-- 3. Soft Status Card Container -->
<div class="p-3 bg-status-2-subtle border border-status-2-subtle rounded">
  <h6 class="text-status-2-emphasis fw-bold">Processing Order #4092</h6>
  <p class="mb-0 text-secondary">The invoice is currently being matched.</p>
</div>

<!-- 4. Table Row Status -->
<table class="table">
  <tbody>
    <tr class="table-status-0">
      <td>TX-1001</td>
      <td>Payment Received</td>
      <td>$1,200.00</td>
    </tr>
    <tr class="table-status-5">
      <td>TX-1002</td>
      <td>Payment Failed</td>
      <td>$450.00</td>
    </tr>
  </tbody>
</table>
```
