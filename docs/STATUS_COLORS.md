# Dashboard Status Colors

This project includes a dedicated configuration file `config/statusColors.json` that defines 20 highly-semantic status indicators. These statuses generate custom utility classes in Bootstrap independent of the standard `success`, `warning`, and `danger` utilities.

## Configuration File

The `statusColors.json` maps specific dashboard concepts to hex colors.

```json
{
  "completed": "#28A745",
  "resolved": "#28A745",
  "successful": "#28A745",
  "assigned": "#0D6EFD",
  "information": "#0D6EFD",
  "action-required": "#0D6EFD",
  ...
}
```

## How It Works

During the build process (`npm run build`), the generator script dynamically reads `statusColors.json`, automatically prepends the `status-` namespace to all the keys (to ensure they never collide with Bootstrap's core utilities), and injects these colors into Bootstrap's internal `$theme-colors` map.

Because they are recognized natively by Bootstrap, they automatically generate the complete suite of utility classes and components, including:
- Backgrounds (`.bg-status-completed`)
- Text colors (`.text-status-urgent`)
- Borders (`.border-status-pending-approval`)
- Subtle variants (`.bg-status-processing-subtle`)
- Interactive components (`.btn-status-error`, `.alert-status-information`)

## Usage Guide

To use these in your dashboards, write semantic HTML class names that perfectly match your desired intent, avoiding the need to remember which specific hex code applies.

### Examples

**1. Green Utilities (#28A745)**
Use for: Completed, Resolved, Successful
```html
<div class="bg-status-completed text-white">Process Finished</div>
<span class="badge bg-status-successful">Success</span>
```

**2. Blue Utilities (#0D6EFD)**
Use for: Assigned, Information, Action Required
```html
<div class="alert alert-status-action-required">Please update your profile.</div>
```

**3. Yellow Utilities (#FFC107)**
Use for: Warning, Pending Approval
```html
<p class="text-status-pending-approval">Awaiting Manager Review...</p>
```

**4. Orange Utilities (#FD7E14)**
Use for: In Progress, Due Soon
```html
<div class="border border-status-in-progress">Task Container</div>
```

**5. Red Utilities (#DC3545)**
Use for: Urgent, Delayed, Error
```html
<button class="btn btn-status-urgent">Address Immediately</button>
```

**6. Purple Utilities (#6F42C1)**
Use for: Pending Verification
```html
<span class="badge bg-status-pending-verification">Verifying...</span>
```

**7. Gray Utilities (#6C757D)**
Use for: Not Started, Read Only
```html
<input class="form-control border-status-read-only" readonly />
```

**8. Brown Utilities (#8B5E3C)**
Use for: On Hold
```html
<div class="bg-status-on-hold-subtle text-status-on-hold-emphasis">Hold</div>
```

**9. Cyan Utilities (#17A2B8)**
Use for: Processing
```html
<span class="text-status-processing">Processing...</span>
```

**10. Dark Gray Utilities (#343A40)**
Use for: Cancelled / Void
```html
<div class="alert alert-status-void">This order has been voided.</div>
```

### Extending Status Colors
To add more semantic statuses, simply append a new key to `config/statusColors.json` starting with `status-`, assign a valid hex color, and re-run the build script!
