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

## 2. CSS Versioning

The build script automatically determines the version of the CSS files to generate based on the `version` field in `package.json`. 

* If your `package.json` version is `"1.0.0"`, all CSS files are generated into the `colors/v2/` directory.
* When you are ready to make breaking design changes, you can bump the version in `package.json` to `"2.0.0"`. The script will then output all new files into `colors/v2/`.

This ensures backwards compatibility. Your older web applications pointing to the `/v2/` path will remain safe and unaffected when you release version 2.

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
    
    <!-- 2. Add your custom theme overrides (jsDelivr Recommended) -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/v2/group_a.css">
    
    <!-- OR use GitHub Pages -->
    <!-- <link rel="stylesheet" href="https://tony-jjjentinc.github.io/assets/colors/v2/group_a.css"> -->
    
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
  var group = e.parameter.group || 'group_a'; 
  
  var template = HtmlService.createTemplateFromFile('Index');
  // jsDelivr (Recommended)
  template.groupCssUrl = `https://cdn.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/v2/${group}.css`;
  
  // OR GitHub Pages
  // template.groupCssUrl = `https://tony-jjjentinc.github.io/assets/colors/v2/${group}.css`;
  
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

**jsDelivr:** To force jsDelivr to clear its edge cache and fetch the newest version immediately, replace `cdn` with `purge` in the URL in your browser:
`https://purge.jsdelivr.net/gh/tony-jjjentinc/assets@main/colors/v2/group_a.css`

**GitHub Pages:** Note that GitHub Pages has a ~10-minute cache (`max-age=600`). When you push updates to your CSS repository, it may take up to 10 minutes for the changes to reflect globally across your GAS apps. You can bypass your browser's local cache by doing a hard refresh (`Ctrl + F5` or `Cmd + Shift + R`).
