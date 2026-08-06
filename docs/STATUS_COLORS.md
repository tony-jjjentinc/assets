# Dashboard Status Colors

This project includes a dedicated configuration file `config/statusColors.json` that defines 10 highly-semantic status indicators. These statuses generate custom utility classes in Bootstrap independent of the standard `success`, `warning`, and `danger` utilities.

## Configuration File

The `statusColors.json` maps numeric status concepts to hex colors.

```json
{
  "0": "#28A745",
  "1": "#0D6EFD",
  "2": "#17A2B8",
  "3": "#FFC107",
  "4": "#FD7E14",
  "5": "#DC3545",
  "6": "#6F42C1",
  "7": "#8B5E3C",
  "8": "#6C757D",
  "9": "#343A40"
}
```

## How It Works

During the build process (`npm run build`), the generator script dynamically reads `statusColors.json`, automatically prepends the `status-` namespace to all the keys (e.g. `status-0`), and injects these colors into Bootstrap's internal `$theme-colors` map.

Because they are recognized natively by Bootstrap, they automatically generate the complete suite of utility classes and components, including:
- Backgrounds (`.bg-status-0`)
- Text colors (`.text-status-1`)
- Borders (`.border-status-2`)
- Subtle variants (`.bg-status-3-subtle`)
- Interactive components (`.btn-status-4`, `.alert-status-5`)

## Usage Guide

To use these in your dashboards, write semantic HTML class names matching the numeric status codes.

### Examples

**1. Green Utilities (0) - #28A745**
Use for: Completed, Resolved, Successful
```html
<div class="bg-status-0 text-white">Process Finished</div>
<span class="badge bg-status-0">Success</span>
```

**2. Blue Utilities (1) - #0D6EFD**
Use for: Assigned, Information, Action Required
```html
<div class="alert alert-status-1">Please update your profile.</div>
```

**3. Cyan Utilities (2) - #17A2B8**
Use for: Processing
```html
<span class="text-status-2">Processing...</span>
```

**4. Yellow Utilities (3) - #FFC107**
Use for: Warning, Pending Approval
```html
<p class="text-status-3">Awaiting Manager Review...</p>
```

**5. Orange Utilities (4) - #FD7E14**
Use for: In Progress, Due Soon
```html
<div class="border border-status-4">Task Container</div>
```

**6. Red Utilities (5) - #DC3545**
Use for: Urgent, Delayed, Error
```html
<button class="btn btn-status-5">Address Immediately</button>
```

**7. Purple Utilities (6) - #6F42C1**
Use for: Pending Verification
```html
<span class="badge bg-status-6">Verifying...</span>
```

**8. Brown Utilities (7) - #8B5E3C**
Use for: On Hold
```html
<div class="bg-status-7-subtle text-status-7-emphasis">Hold</div>
```

**9. Gray Utilities (8) - #6C757D**
Use for: Not Started, Read Only
```html
<input class="form-control border-status-8" readonly />
```

**10. Dark Gray Utilities (9) - #343A40**
Use for: Cancelled / Void
```html
<div class="alert alert-status-9">This order has been voided.</div>
```

### Extending Status Colors
To add more semantic statuses, simply append a new numeric key to `config/statusColors.json`, assign a valid hex color, and re-run the build script!
