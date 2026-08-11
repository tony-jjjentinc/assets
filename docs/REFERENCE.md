# Assets Reference Guide

The assets directory are served via jsDelivr and Github Pages

## Base URL Configuration

To use these assets in your projects, it is highly recommended to use **jsDelivr**, a high-performance CDN for GitHub repositories.

**Recommended Base URL (jsDelivr):**
`https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/`

**Alternative Base URL (GitHub Pages):**
`https://tony-jjjentinc.github.io/assets/`

---

## 1. Styling Integration (CSS/Colors)

### Static Implementation
Include the default Bootstrap 5 CSS CDN link in your web projects, followed by the CDN URL pointing to the pre-compiled group CSS. You can use either the `latest` endpoint for auto-updating styles or a pinned version endpoint (e.g. `v3`).

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- jsDelivr (Latest - Recommended) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/latest/jjjei_admin:0.css">

<!-- jsDelivr (Version Pinned) -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/v3/jjjei_admin:0.css">
```

### Dynamic Implementation (Code.gs)
You can dynamically pass the appropriate group CSS URL to the frontend template, allowing one codebase to serve different themed groups based on URL parameters.

**Code.gs:**
```javascript
function doGet(e) {
  var group = e.parameter.group || 'jjjei_admin:0';
  var template = HtmlService.createTemplateFromFile('Index');
  // Use 'latest' to automatically inherit future theme updates
  template.cssUrl = 'https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/latest/' + group + '.css';
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
- **`.bg-primary-base`**: A custom background utility designed for page backgrounds. While `.bg-primary-subtle` uses a 25% tint of the specific sub-group's variant color (e.g., `jjjei_hr:2`), `.bg-primary-base` always uses a strong 60% tint of the **parent group's base color** (e.g., `jjjei_hr:0`). This ensures a consistent anchor background for the department, while the specific variant color is used for active UI elements. It automatically adapts to dark mode.

#### 2. The Full-Page Gradient Utility
- **`.bg-primary-gradient`**: A modern, responsive gradient utility designed to be applied to the `<body>` tag or main application wrapper. 
  - **Responsive Angles:** It flows vertically (`180deg`) on mobile and cleanly snaps horizontally (`90deg`) on desktop (`>=768px`).
  - **Colors:** It starts (top/left) with `$primary-bg-subtle` at 0% and fades into `$primary-bg-subtle` at 50% opacity (`rgba($primary-bg-subtle, 0.5)`) at 100%.
  - **Fixed Canvas:** It is locked in place with `background-attachment: fixed !important` to ensure a consistent presentation layer regardless of page scroll.

#### 3. Semantic Status Colors
The project dynamically injects semantic status colors into the standard Bootstrap theming engine. This means you have access to the full suite of Bootstrap utility classes for all defined custom statuses, including their accessible subtle variants!

Available status names are numeric keys from `0` to `9` (e.g., `status-0`, `status-1`, etc.).

**Available Utilities:**
- `.bg-status-#`, `.text-status-#`, `.border-status-#`
- `.bg-status-#-subtle`, `.border-status-#-subtle` (Uses the exact same 25% tint logic!)
- `.text-status-#-emphasis` (Automatically darkened to pass WCAG 4.5 contrast)

**Example Usage:**
```html
<div class="bg-primary-base p-3">
  <span class="badge bg-status-1 text-white">Urgent</span>
  <div class="alert bg-status-3-subtle text-status-3-emphasis border border-status-3-subtle mt-2">
    Awaiting review...
  </div>
</div>
```

### Included Bootstrap Components & Color Overrides
These custom CSS files include primary color overrides for all high color-impact Bootstrap 5 components:
- **Navigation & Layout:** `.nav`, `.nav-pills`, `.nav-tabs`, `.navbar`
- **Interactive Controls:** `.btn`, `.btn-group`, `.dropdown` (`.dropdown-item.active`), `.accordion` (`.accordion-button`)
- **Feedback & Content:** `.alert`, `.badge`, `.list-group`, `.progress`, `.spinners`, `.tables`, `.forms`, `.pagination`, `.breadcrumb`, `.carousel`

### Bootstrap JavaScript Bundle
This repository only serves customized CSS. For interactive Bootstrap components (like Modals, Dropdowns, or Offcanvases), you must manually include the standard Bootstrap JS bundle in your web projects `Index.html`:

```html
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
```

---

## 2. Fonts Usage

**Inter Font (Automatic):**
The primary `Inter` font is now **automatically injected** into your generated group CSS files. As long as you import your group's CSS file, the Inter font is ready to use!

**Gill Sans Nova (Manual):**
If you need to use the secondary `Gill Sans Nova` font, provide an explicit `@font-face` CSS declaration inside a `<style>` tag within your web project's HTML files.

```html
<style>
/* Gill Sans Nova Bold */
@font-face {
    font-family: 'Gill Sans Nova';
    src: url('https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/fonts/GillSansNova-Bold.woff2') format('woff2');
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
<img src="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/images/logo/marymart_horizontal.svg" alt="Marymart Logo" width="200" />
```

### Background Patterns (CSS Backgrounds)
Apply the provided SVGs as background textures to containers using CSS.

```html
<style>
.hero-section {
    background-color: #f0f0f0; /* Fallback/base color */
    background-image: url('https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/images/misc/background-pattern/topography.svg');
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

### Colors (`/colors/latest/` and `/colors/v3/`)
*(Note: CSS is available under both `/colors/latest/` for auto-updating apps and `/colors/v3/` for version-pinned apps)*
- `jjjei_admin:0.css` to `jjjei_admin:5.css`
- `jjjei_controller:0.css` to `jjjei_controller:2.css`
- `jjjei_facilities:0.css` to `jjjei_facilities:6.css`
- `jjjei_gmo:0.css` to `jjjei_gmo:3.css`
- `jjjei_hr:0.css` to `jjjei_hr:2.css`
- `jjjei_leasing:0.css` to `jjjei_leasing:3.css`
- `jjjei_procinv:0.css` to `jjjei_procinv:2.css`
- `jjjei_treasury:0.css` to `jjjei_treasury:3.css`
