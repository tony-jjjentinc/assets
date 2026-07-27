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
Replace the default Bootstrap 5 CSS CDN link in your web projects with the GitHub Pages URL pointing to the pre-compiled group CSS. These files bundle both the Bootstrap 5 core and the custom theme.

```html
<link rel="stylesheet" href="https://tony-jjjentinc.github.io/assets/colors/admin.css">
```

### Dynamic Implementation (Code.gs)
You can dynamically pass the appropriate group CSS URL to the frontend template, allowing one codebase to serve different themed groups based on URL parameters.

**Code.gs:**
```javascript
function doGet(e) {
  var group = e.parameter.group || 'admin';
  var template = HtmlService.createTemplateFromFile('Index');
  template.cssUrl = 'https://tony-jjjentinc.github.io/assets/colors/' + group + '.css';
  return template.evaluate();
}
```

**Index.html:**
```html
<link rel="stylesheet" href="<?= cssUrl ?>">
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
- `logo.svg`
- `marymart_compact.svg`
- `marymart_horizontal.svg`

### Background Patterns (`/images/misc/background-pattern/`)
- `bubbles.svg`
- `circuit-board.svg`
- `diagonal-lines.svg`
- `diagonal-stripes.svg`
- `hexagons.svg`
- `texture.svg`
- `topography.svg`

### Colors (`/colors/`)
*(Note: Group variations now use a colon `:` separator instead of an underscore `_`)*
- `admin.css`, `admin:1.css`, `admin:2.css`, `admin:3.css`, `admin:4.css`, `admin:5.css`, `admin:6.css`
- `controller.css`, `controller:1.css`, `controller:2.css`, `controller:3.css`, `controller:4.css`, `controller:5.css`, `controller:6.css`, `controller:7.css`
- `facilities.css`, `facilities:1.css`, `facilities:2.css`, `facilities:3.css`, `facilities:4.css`, `facilities:5.css`, `facilities:6.css`, `facilities:7.css`, `facilities:8.css`
- `gmo.css`, `gmo:1.css`, `gmo:2.css`, `gmo:3.css`, `gmo:4.css`, `gmo:5.css`, `gmo:6.css`, `gmo:7.css`, `gmo:8.css`
- `hr.css`, `hr:1.css`, `hr:2.css`, `hr:3.css`, `hr:4.css`, `hr:5.css`, `hr:6.css`, `hr:7.css`, `hr:8.css`
- `leasing.css`, `leasing:1.css`, `leasing:2.css`, `leasing:3.css`, `leasing:4.css`, `leasing:5.css`, `leasing:6.css`, `leasing:7.css`, `leasing:8.css`
- `procurement.css`, `procurement:1.css`, `procurement:2.css`, `procurement:3.css`
- `treasury.css`, `treasury:1.css`, `treasury:2.css`, `treasury:3.css`, `treasury:4.css`
