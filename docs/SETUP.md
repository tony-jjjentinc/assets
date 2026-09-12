# Integration Guide: Google Apps Script

This guide explains how to integrate the custom generated Bootstrap CSS files into your Google Apps Script (GAS) web app projects.

## 1. Hosting the CSS (CDN Options)

The CSS files generated in this repository (`colors/v2/group_a.css`, etc.) act as lightweight themes and can be served via two methods:

### Option A: jsDelivr CDN (Recommended)
jsDelivr is a free, enterprise-grade CDN built specifically for public GitHub repositories. It provides faster global load times and better caching than GitHub Pages.
- **Base URL:** `https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/`

### Option B: GitHub Pages
Ensure this repository is pushed to GitHub and GitHub Pages is enabled in your repository settings:
- **Base URL:** `https://tony-jjjentinc.github.io/assets/`

## 2. CSS Versioning & Endpoints

JJJEI Core Assets supports modern Git tag/branch endpoints and maintains full backward compatibility with legacy directory-based endpoints. (See [Versioning Guide](VERSIONING.md) for full details).

1. **`@latest/colors/latest/` (Rolling Latest - Recommended):** Applications using this endpoint automatically inherit future theme enhancements, new color tokens, and accessibility fixes without manual code changes.
2. **`@vX.Y.Z/colors/latest/` (Immutable Release Pin):** Mission-critical production applications can pin to exact Git release tags (e.g. `@v4.0.0`) for permanent stability.
3. **`@main/colors/v4/` (Legacy Directory Pinned):** Pre-existing implementations referencing major version paths remain fully supported.

## 3. Setting up the HTML Template in GAS

Because the generated CSS files are lightweight overrides, you **must** include the official Bootstrap 5 CDN link for the core structural CSS (grid, layout), followed by the custom group CSS file.

In your GAS project's `Index.html` (or whichever file contains your `<head>` tags), link the CDN and the specific group CSS file.

### Example for Group A:

```html
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    <!-- 1. Include the standard Bootstrap 5 CDN link for layout/structure -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- 2. Add custom theme overrides (jsDelivr - Rolling Latest Recommended) -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@latest/colors/latest/jjjei_admin:0.css">
    
    <!-- OR Immutable Version Pinned -->
    <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@v4.0.0/colors/latest/jjjei_admin:0.css"> -->
    
    <!-- OR Legacy Directory Pinned -->
    <!-- <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/v4/jjjei_admin:0.css"> -->
  </head>
  <body>
    <div class="container mt-4">
      <h1 class="text-primary">Welcome to Group A</h1>
      <button class="btn btn-primary">Primary Action</button>
      <button class="btn btn-success">Success Action</button>
    </div>

    <!-- You still need the Bootstrap JS bundle if you are using interactive components like Modals or Dropdowns -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
```

## 4. Dynamic Injection (Optional)

If your GAS project serves multiple groups from the same codebase, you can pass the group name dynamically from `Code.gs` to your HTML template.

**Code.gs:**
```javascript
function doGet(e) {
  // Determine group dynamically, e.g., from query parameter: ?group=group_b
  var group = e.parameter.group || 'jjjei_admin:0'; 
  
  var template = HtmlService.createTemplateFromFile('Index');
  // jsDelivr (Rolling Latest - Recommended)
  template.groupCssUrl = `https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@latest/colors/latest/${group}.css`;
  
  return template.evaluate()
      .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}
```

**Index.html:**
```html
<!DOCTYPE html>
<html>
  <head>
    <base target="_top">
    <!-- Inject the URL dynamically -->
    <link rel="stylesheet" href="<?= groupCssUrl ?>">
  </head>
  <!-- ... body ... -->
</html>
```

## 5. Cache Purging

**jsDelivr:** When running `npm run release`, the edge cache is purged automatically for both `@latest` and `@main`. If you ever need to manually purge a specific file on jsDelivr, replace `cdn` with `purge` in the URL:
`https://purge.jsdelivr.net/gh/tony-jjjentinc/assets@latest/colors/latest/jjjei_admin:0.css`

## 6. Local Development & Releasing

For building assets locally and releasing new updates:
1. **Local Build:** Run `npm run build` (`python3 scripts/generator.py`) to compile all CSS files and generate the WCAG contrast audit.
2. **Visual Verification:** Open `index.html` in your web browser to test swatches, components, and dark mode.
3. **Automated Release:** Run `npm run release [patch | minor | major]` to bump semver, compile, tag, force-sync the `latest` branch, and purge CDN caches in one atomic step.

For full release lifecycle and semantic versioning rules, refer to the [Versioning & Release Guide](VERSIONING.md).
