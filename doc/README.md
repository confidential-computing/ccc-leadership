# Leadership Display Page

This directory contains the HTML, CSS, and JavaScript files for displaying the CCC Leadership page.

## Files

- `leadership-embed.html` - Main HTML template
- `leadership.js` - JavaScript that loads JSON and generates HTML dynamically
- `leadership.css` - Styling for cards and modals

## Running Locally

**Important:** This page must be served from a web server due to CORS restrictions when loading JSON files. You cannot open the HTML file directly in a browser.

### Option 1: Python HTTP Server

From the repository root:

```bash
python3 -m http.server 8000
```

Then visit: http://localhost:8000/doc/leadership-embed.html

### Option 2: Node.js HTTP Server

```bash
npx http-server -p 8000
```

Then visit: http://localhost:8000/doc/leadership-embed.html

### Option 3: VS Code Live Server

If using VS Code, install the "Live Server" extension and right-click on `leadership-embed.html` → "Open with Live Server"

## How It Works

1. The HTML file loads `leadership.js` and `leadership.css`
2. JavaScript fetches `../ccc-leadership/leadership.json`
3. For each person in the JSON, JavaScript generates:
   - A card HTML element (shown in grid)
   - A modal HTML element (shown when card is clicked)
4. Cards are grouped by category (Governing Board, Technical Advisory Council, etc.)
5. All HTML is generated client-side - no server-side rendering needed

## Deployment

When deploying to a web server, ensure:
- The `doc/` folder is accessible
- The `ccc-leadership/` folder is at the same level as `doc/`
- All paths in `leadership.js` are correct relative to the HTML file location

