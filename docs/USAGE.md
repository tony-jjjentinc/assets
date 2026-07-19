# Usage Guide

## Using in Google Apps Script

### Basic Setup

In your Google Apps Script project, create an HTML file and add the following to the `<head>`:

```html
<!DOCTYPE html>
<html>
<head>
  <base target="_top">
  <!-- 1. Bootstrap 5 CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">

  <!-- 2. Base style overrides -->
  <link href="https://{username}.github.io/assets/css/base.css" rel="stylesheet">

  <!-- 3. Department color (choose one) -->
  <link href="https://{username}.github.io/assets/css/colors/gmo/gmo.css" rel="stylesheet">
</head>
<body>

  <!-- Your content here — use standard Bootstrap classes -->
  <button class="btn btn-primary">Submit</button>

  <!-- Bootstrap 5 JS (at end of body) -->
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

> **Important:** The load order must be Bootstrap CSS → `base.css` → color file. Reversing this order will cause overrides to fail.

### Available Color Files

#### Department Base Colors

| Department | Path |
|---|---|
| GMO | `css/colors/gmo/gmo.css` |
| Admin | `css/colors/admin/admin.css` |
| Facilities | `css/colors/facilities/facilities.css` |
| Leasing | `css/colors/leasing/leasing.css` |
| HR | `css/colors/hr/hr.css` |
| Procurement and Inventory | `css/colors/procurement-and-inventory/procurement-and-inventory.css` |
| Controller | `css/colors/controller/controller.css` |
| Treasury | `css/colors/treasury/treasury.css` |

#### Theme Variant Themes

Each department has its own dynamically generated theme variants and theme variants (Light & Dark). Replace `{dept}` with the department folder name and `{theme-suffix}` with the specific theme variant suffix.

**Example** — HR Light Theme (Thistle):
```html
<link href="https://{username}.github.io/assets/css/colors/hr/hr-light-2.css" rel="stylesheet">
```
*Note: See `examples/config.js` or the interactive demo to view the available theme variants and their filenames for each department.*

### What Gets Overridden

When you include a color file, all Bootstrap components that use the "primary" color are automatically updated:

| Component | Bootstrap Class | What Changes |
|---|---|---|
| Buttons | `.btn-primary`, `.btn-outline-primary` | Background, border, hover/active states |
| Alerts | `.alert-primary` | Background, border, text color |
| Badges | `.badge.text-bg-primary` | Background color |
| Links | `<a>` | Link color, hover color |
| Link Utility | `.link-primary` | Link color, hover, underline color |
| Pagination | `.page-item.active` | Active page background |
| Nav Pills | `.nav-pills .nav-link.active` | Active pill background |
| Nav Tabs | `.nav-tabs .nav-link.active` | Active tab text color |
| List Group | `.list-group-item.active` | Active item background |
| Accordion | `.accordion-button` | Active state colors, focus ring |
| Form Inputs | `.form-control:focus` | Focus border, focus ring |
| Checkboxes | `.form-check-input:checked` | Checked background |
| Switches | `.form-switch .form-check-input:checked` | Checked background |
| Tables | `.table-primary` | Row background |
| Dropdowns | `.dropdown-item.active` | Active item background |
| Progress | `.progress-bar` | Bar color |
| Spinners | `.text-primary` | Spinner color |
| Utilities | `.text-primary`, `.bg-primary`, `.border-primary` | Color values |

### Google Apps Script Example

```javascript
// Code.gs
function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('My App')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}
```

```html
<!-- Index.html -->
<!DOCTYPE html>
<html>
<head>
  <base target="_top">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://{username}.github.io/assets/css/base.css" rel="stylesheet">
  <link href="https://{username}.github.io/assets/css/colors/gmo/gmo.css" rel="stylesheet">
</head>
<body>
  <div class="container mt-4">
    <h1>My GMO App</h1>
    <p>All Bootstrap components will use the GMO green color.</p>
    <button class="btn btn-primary" onclick="google.script.run.doSomething()">
      Submit
    </button>
    <div class="alert alert-primary mt-3">
      This alert uses the GMO green theme.
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
```

### ⚠️ Pale Color Contrast Limitation

**Important:** If you are using a Light Theme with pale colors (e.g., Alice Blue) as your primary or secondary theme colors, be cautious when using Bootstrap's text utility classes like `.text-primary`. 

Bootstrap applies the exact hex color of your theme variable to the text. On white or light backgrounds, these pale text colors will be nearly invisible and fail accessibility contrast standards. 

#### Best Practices & Workarounds

If you want to maintain your pale theme without sacrificing readability, consider the following approaches:

1. **Use Backgrounds Instead of Text Colors:** Apply your pale theme colors to background elements (e.g., `.bg-primary`) and pair them with high-contrast dark text (`.text-dark` or `.text-body`). This is the most effective way to showcase a light theme.
2. **Define Custom High-Contrast Text Classes:** If you absolutely need colored text that aligns with a pale theme, do not use `.text-primary`. Instead, create a custom CSS utility class (e.g., `.text-primary-dark`) that uses a darker, readable shade of your theme color specifically intended for text.
3. **Utilize Bootstrap's Built-in Dark Utilities:** Stick to `.text-dark`, `.text-muted`, or default body text for typography when working within pale-themed containers.

### Tips

1. **Only load one color file** — Loading multiple color files will cause the last one to win.
2. **Cache considerations** — GitHub Pages uses CDN caching. After pushing changes, it may take a few minutes for updates to propagate. Append a version query string to bust the cache if needed: `base.css?v=2`.
3. **No `<style>` conflicts** — If you add custom `<style>` blocks in your HTML, they will override the CDN styles (since inline styles load last). This is expected behavior and can be useful for page-specific tweaks.
4. **Dark mode** — The color files include `[data-bs-theme="dark"]` overrides. Add `data-bs-theme="dark"` to your `<html>` tag to use Bootstrap's dark mode with your department color.

### Live Demo

See all components in action with the [interactive sample page](../examples/sample.html). It includes a department/theme variant switcher to preview all color themes.

### Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Colors not changing | Wrong CSS load order | Ensure: Bootstrap → base.css → color file |
| Stale styles after update | GitHub Pages CDN cache | Append `?v=2` (or increment) to CSS URLs |
| Components still blue | Missing color override | Check that the color CSS file URL is correct and loading (browser DevTools → Network tab) |
| Fonts not loading | CSP restrictions | Google Apps Script allows fonts.googleapis.com by default; verify in browser console |
