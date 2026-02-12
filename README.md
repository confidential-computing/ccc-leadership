# Confidential Computing Consortium Leadership

This repository contains the leadership data and display components for the Confidential Computing Consortium (CCC) leadership page.

## Structure

- `ccc-leadership/` - Main directory containing leadership data and scripts
  - `leadership.json` - JSON file containing all leadership information (Governing Board, Technical Advisory Council, Committee Chairs, and Staff)
  - `leadership-photos/` - Directory containing leadership member photos
  - `rename_photos.py` - Script to rename photos to match person names
  - `update_local_paths.py` - Script to update JSON to use local photo paths
- `doc/` - Source HTML/CSS/JS files for development
- `docs/` - Generated static HTML for GitHub Pages (auto-generated)
- `generate-static-html.py` - Script to generate static HTML from JSON

## Data Source

Leadership data is extracted from: https://confidentialcomputing.io/about/leadership/

## JSON Structure

Each entry in `ccc-leadership/leadership.json` contains:
- `id` - Unique identifier (slug format, e.g., "john-doe")
- `name` - Full name
- `role` - Role/title within CCC
- `organization` - Company/organization name
- `title` - Job title
- `category` - One of: "Governing Board", "Technical Advisory Council", "Committee Chairs", "Staff"
- `avatar` - Path to photo (relative path to `leadership-photos/` directory, e.g., "./leadership-photos/john-doe.jpg")
- `bio` - Biography text

All photos are stored in the `ccc-leadership/leadership-photos/` directory and referenced in `leadership.json` using local paths.

To update JSON paths after adding or renaming photos:
```bash
python3 ccc-leadership/update_local_paths.py
```

## Workflow: PR to Website Deployment

### 1. Making Changes

When adding or updating leadership members:

1. **Update `ccc-leadership/leadership.json`**
   - Add new person entry with all required fields:
     - `id` - Unique identifier (slug format, e.g., "john-doe")
     - `name` - Full name
     - `role` - Role/title within CCC
     - `organization` - Company/organization name
     - `title` - Job title
     - `category` - One of: "Governing Board", "Technical Advisory Council", "Committee Chairs", "Staff"
     - `avatar` - Path to photo (e.g., "./leadership-photos/john-doe.jpg")
     - `bio` - Biography text

2. **Add Photo** (if new person)
   - Add photo to `ccc-leadership/leadership-photos/`
   - Name it using the person's name (e.g., `john-doe.jpg`)
   - Run `python3 ccc-leadership/update_local_paths.py` to update JSON paths if needed

3. **Update HTML/CSS/JS** (if needed)
   - Modify files in `doc/` directory for layout/styling changes

### 2. Creating a Pull Request

1. Create a branch: `git checkout -b add-new-leadership-member`
2. Make your changes
3. Commit: `git commit -m "Add John Doe to Governing Board"`
4. Push: `git push origin add-new-leadership-member`
5. Create PR on GitHub

### 3. Automated Validation (on PR)

When a PR is created or updated, GitHub Actions automatically runs:

- ✅ **Validate JSON** (`validate-json.yml`)
  - Checks JSON is valid
  - Verifies all required fields are present
  - Runs on: PRs that modify `ccc-leadership/leadership.json`

- ✅ **Check Photos** (`check-photos.yml`)
  - Verifies all photos referenced in JSON exist
  - Runs on: PRs that modify JSON or photos

- ✅ **Lint JSON** (`lint-json.yml`)
  - Checks JSON formatting
  - Runs on: PRs that modify `ccc-leadership/leadership.json`

### 4. PR Review

- Reviewers check the PR
- Validation checks must pass (green checkmarks)
- Code review and approval

### 5. Merge to Main

Once approved and merged:
- Changes are in the `main` branch
- **Deployment workflow automatically triggers**

### 6. Generate Static HTML & Deploy to GitHub Pages

When changes are merged to `main`, the deployment workflow automatically:

1. **Validates** the JSON and checks all photos exist
2. **Generates** a static HTML file (`docs/index.html`) from the JSON data
   - Embeds CSS inline
   - Pre-renders all HTML (no client-side JSON fetching needed)
   - Includes all modals
3. **Deploys** to GitHub Pages
   - The static HTML file is published to GitHub Pages
   - Available at: `https://[org].github.io/[repo]/`
   - Updates within 1-2 minutes after merge

### 7. Website Integration

The main CCC website can then:
- **Embed** the GitHub Pages page using an iframe
- **Link** to the GitHub Pages page
- **Proxy** the content (if needed for branding)

## Benefits of This Approach

✅ **No CORS issues** - Static HTML, no JSON fetching  
✅ **Faster loading** - Pre-rendered HTML  
✅ **Works without JavaScript** - Fully static  
✅ **Simple deployment** - GitHub Pages handles hosting  
✅ **Automatic updates** - Every merge triggers deployment  
✅ **Easy to embed** - Main website can iframe or link to it  

## GitHub Pages Setup

To enable GitHub Pages:

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` (or use GitHub Actions)
4. The workflow uses GitHub Actions to deploy, so ensure Pages is enabled

The page will be available at: `https://[org].github.io/[repo]/`

## Local Testing

### Test Static HTML Generation

```bash
python3 generate-static-html.py
# Then open docs/index.html in a browser
```

### Test Development Version

The `doc/` folder contains the development version that loads JSON dynamically:

```bash
# From repository root
python3 -m http.server 8000
# Then visit: http://localhost:8000/doc/leadership-embed.html
```

## Quick Start

1. Navigate to the `ccc-leadership/` directory
2. Review the `leadership.json` file for leadership data
3. Photos are stored in `leadership-photos/` directory
4. See workflow above for adding new members
