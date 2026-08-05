# Integration Guide: Google Apps Script

This guide explains how to integrate the custom generated Bootstrap CSS files into your Google Apps Script (GAS) web app projects.

## 1. Hosting the CSS

The CSS files generated in this repository (`colors/v1/group_a.css`, etc.) act as lightweight themes and are designed to be served directly via GitHub Pages.

Ensure this repository is pushed to GitHub and GitHub Pages is enabled in your repository settings:
- **Repository:** `tony-jjjentinc/assets`
- **GitHub Pages URL:** `https://tony-jjjentinc.github.io/assets/`

## 2. Setting up the HTML Template in GAS

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
    <!-- 2. Add your custom Github Pages CDN link for the theme overrides -->
    <link rel="stylesheet" href="https://tony-jjjentinc.github.io/assets/colors/v1/group_a.css">
    
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

## 3. Dynamic Injection (Optional)

If your GAS project serves multiple groups from the same codebase, you can pass the group name dynamically from `Code.gs` to your HTML template.

**Code.gs:**
```javascript
function doGet(e) {
  // Determine group dynamically, e.g., from query parameter: ?group=group_b
  var group = e.parameter.group || 'group_a'; 
  
  var template = HtmlService.createTemplateFromFile('Index');
  template.groupCssUrl = `https://tony-jjjentinc.github.io/assets/colors/v1/${group}.css`;
  
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

## 4. Cache Purging

Note that GitHub Pages has a ~10-minute cache (`max-age=600`). When you push updates to your CSS repository, it may take up to 10 minutes for the changes to reflect globally across your GAS apps. You can bypass your browser's local cache by doing a hard refresh (`Ctrl + F5` or `Cmd + Shift + R`).
