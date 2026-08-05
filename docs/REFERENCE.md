# Assets Reference Guide

The assets directory are served via Github Pages

## Base URL Configuration

To use these assets in your projects, you must construct the base URL for the GitHub Pages deployment. 
Based on this repository, the base URL is:
`https://tony-jjjentinc.github.io/assets/`

You can define this base URL dynamically in web projects (e.g., passing it to the HTML template) or hardcode it in the frontend code.

---

## 1. Styling Integration (CSS/Colors)

### Static Implementation
Include the default Bootstrap 5 CSS CDN link in your web projects, followed by the GitHub Pages URL pointing to the pre-compiled group CSS. These custom files are lightweight and only override the Bootstrap 5 core theme colors and components.

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://tony-jjjentinc.github.io/assets/colors/v1/admin.css">
```

### Dynamic Implementation (Code.gs)
You can dynamically pass the appropriate group CSS URL to the frontend template, allowing one codebase to serve different themed groups based on URL parameters.

**Code.gs:**
```javascript
function doGet(e) {
  var group = e.parameter.group || 'admin';
  var template = HtmlService.createTemplateFromFile('Index');
  template.cssUrl = 'https://tony-jjjentinc.github.io/assets/colors/v1/' + group + '.css';
  return template.evaluate();
}
```

**Index.html:**
```html
<link rel="stylesheet" href="<?= cssUrl ?>">
```

### Custom Theme Colors & Utilities

Beyond the standard Bootstrap 5 color classes (`primary`, `secondary`, `success`, etc.), these compiled CSS files include custom colors and utilities specifically built for this project:

#### 1. The Base Background Utility
- **`.bg-primary-base`**: A custom background utility designed for page backgrounds. While `.bg-primary-subtle` uses a subtle tint of the specific sub-group's color (e.g., `hr:hr_operations`), `.bg-primary-base` always uses a subtle tint of the **parent group's base color** (e.g., `hr`). This ensures a consistent, non-overwhelming background while the specific variant color is used for active UI elements. It automatically adapts to dark mode.

#### 2. Semantic Status Colors
The project dynamically injects semantic status colors into the standard Bootstrap theming engine. This means you have access to the full suite of Bootstrap utility classes (like `.bg-*`, `.text-*`, `.border-*`, `.btn-*`, etc.) for all defined custom statuses. 

Available status names include: `status-completed`, `status-resolved`, `status-successful`, `status-assigned`, `status-information`, `status-action-required`, `status-warning`, `status-pending-approval`, `status-in-progress`, `status-due-soon`, `status-urgent`, `status-delayed`, `status-error`, `status-pending-verification`, `status-not-started`, `status-read-only`, `status-on-hold`, `status-processing`, `status-cancelled`, and `status-void`.

**Example Usage:**
```html
<div class="bg-primary-base p-3">
  <span class="badge bg-status-urgent text-white">Urgent</span>
  <div class="alert alert-status-pending-approval mt-2">Awaiting review...</div>
</div>
```

### Bootstrap JavaScript Bundle
This repository only serves customized CSS. For interactive Bootstrap components (like Modals, Dropdowns, or Offcanvases), you must manually include the standard Bootstrap JS bundle in your web projects `Index.html`:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

---

## 2. Fonts Usage

Provide explicit `@font-face` CSS declarations inside a `<style>` tag within the web projects HTML files.

```html
<style>
/* Inter Font */
@font-face {
    font-family: 'Inter';
    src: url('https://tony-jjjentinc.github.io/assets/fonts/Inter.woff2') format('woff2');
    font-weight: normal;
    font-style: normal;
}

/* Gill Sans Nova Bold */
@font-face {
    font-family: 'Gill Sans Nova';
    src: url('https://tony-jjjentinc.github.io/assets/fonts/GillSansNova-Bold.woff2') format('woff2');
    font-weight: bold;
    font-style: normal;
}
</style>
```
*Note: `.woff2` is fully supported by modern browsers and offers optimal compression.*

---

## 3. Images Usage

Since web projects serves the UI in a sandboxed iframe (`IFRAME` mode), referencing external `https` URLs hosted on GitHub Pages works seamlessly and circumvents inline SVG sanitization issues.

### Logos (HTML Embedding)
Use `<img>` tags for logos in the application header or footer.

```html
<img src="https://tony-jjjentinc.github.io/assets/images/logo/marymart_horizontal.svg" alt="Marymart Logo" width="200" />
```

### Background Patterns (CSS Backgrounds)
Apply the provided SVGs as background textures to containers using CSS.

```html
<style>
.hero-section {
    background-color: #f0f0f0; /* Fallback/base color */
    background-image: url('https://tony-jjjentinc.github.io/assets/images/misc/background-pattern/topography.svg');
    background-repeat: repeat;
}
</style>
```

---

## Specific Considerations

- **CORS Requirements:** GitHub Pages automatically handles CORS headers (`Access-Control-Allow-Origin: *`), which allows fonts and SVGs to load correctly inside the `googleusercontent.com` sandbox that web projects uses.
- **Security Restrictions:** web projects sanitizes HTML; using these assets as direct URL references bypasses any inline SVG sanitization issues, making external references the preferred method.
- **Caching Note:** GitHub Pages uses aggressive caching (`max-age=600`). web projects deployments may not see CSS or asset updates for up to 10 minutes after a push, requiring a hard refresh or cache-busting (e.g., adding a query string like `?v=123` to the URL) during active development.

---

## 4. Currently Served Assets

### Fonts (`/fonts/`)
- `GillSansNova-Bold.woff2`
- `Inter.woff2`

### Logos (`/images/logo/`)
- `.gitkeep`
- `base-dark.svg`
- `base-light.svg`
- `base.svg`
- `jjjei_horizontal.svg`
- `jjjei_stacked.svg`
- `logo.svg`
- `marymart_horizontal.svg`
- `marymart_stacked.svg`

### Background Patterns (`/images/misc/background-pattern/`)
- `bubbles.svg`
- `circuit-board.svg`
- `diagonal-lines.svg`
- `diagonal-stripes.svg`
- `hexagons.svg`
- `texture.svg`
- `texture2.svg`
- `topography.svg`

### Colors (`/colors/v1/`)
*(Note: CSS is now versioned and group variations use a colon `:` separator)*
- `admin.css`, `admin:admin_supervisor.css`, `admin:bla.css`, `admin:compliance.css`, `admin:it.css`, `admin:legal.css`, `admin:om.css`
- `controller.css`, `controller:compliance_tax_and_payroll_coordinator.css`, `controller:department_head.css`, `controller:payables.css`, `controller:receivables.css`
- `facilities.css`, `facilities:acs.css`, `facilities:ee.css`, `facilities:mp.css`, `facilities:pjt.css`
- `gmo.css`, `gmo:1.css`, `gmo:2.css`, `gmo:3.css`, `gmo:4.css`
- `hr.css`, `hr:assistant.css`, `hr:department_head.css`, `hr:payroll_and_benefits_coordinator.css`, `hr:supervisor.css`
- `leasing.css`, `leasing:admin.css`, `leasing:events.css`, `leasing:sales.css`, `leasing:supervisor.css`, `leasing:tenant_relations.css`
- `procinv.css`, `procinv:admin_staff.css`, `procinv:inventory_and_warehouse staff.css`, `procinv:staff.css`, `procinv:supervisor.css`
- `treasury.css`, `treasury:billing.css`, `treasury:collection.css`, `treasury:department_head.css`, `treasury:disbursment.css`, `treasury:supervisor.css`
