#!/usr/bin/env python3
"""
Generate static HTML file from leadership.json
This creates a fully self-contained HTML file that can be deployed to GitHub Pages.
"""
import json
import os
import re

def escape_html(text):
    """Escape HTML special characters."""
    if not text:
        return ""
    return (str(text)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#x27;"))

def nl2br(text):
    """Convert newlines to <br> tags."""
    if not text:
        return ""
    return escape_html(text).replace("\n", "<br>")

def generate_html():
    """Generate static HTML from JSON."""
    json_path = os.path.join('ccc-leadership', 'leadership.json')
    output_path = os.path.join('docs', 'index.html')
    
    # Read JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        people = json.load(f)
    
    # Sort by name
    people.sort(key=lambda x: x.get('name', '').lower())
    
    # Group by category
    category_order = [
        {'key': 'Governing Board', 'label': 'Governing Board'},
        {'key': 'Committee Chairs', 'label': 'Outreach'},
        {'key': 'Technical Advisory Council', 'label': 'Technical Advisory Council'},
        {'key': 'Staff', 'label': 'Staff'}
    ]
    
    categories = {}
    for person in people:
        cat = person.get('category', 'Other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(person)
    
    # Read CSS
    css_path = os.path.join('doc', 'leadership.css')
    with open(css_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    
    # Generate HTML
    html_parts = []
    
    # Header
    html_parts.append('''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Leadership - Confidential Computing Consortium</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700&subset=latin,latin-ext" rel="stylesheet">
<link href="https://fonts.googleapis.com/css?family=Fira+Sans:300,300italic,400,400italic,500,500italic,700,700italic&subset=latin" rel="stylesheet">

<style>
''')
    html_parts.append(css_content)
    html_parts.append('''
</style>
</head>
<body>

  <div id="page-content">
    <div id="leadership-grid">
''')
    
    # Generate category sections
    for cat_info in category_order:
        cat_key = cat_info['key']
        cat_label = cat_info['label']
        
        if cat_key not in categories or not categories[cat_key]:
            continue
        
        html_parts.append(f'''      <div class="category-section">
        <h2>{escape_html(cat_label)}</h2>
        <div class="leadership-grid">
''')
        
        for person in categories[cat_key]:
            person_id = person.get('id', '')
            name = person.get('name', '')
            role = person.get('role', '')
            organization = person.get('organization', '')
            title = person.get('title', '')
            avatar = person.get('avatar', '').replace('./leadership-photos/', 'ccc-leadership/leadership-photos/')
            
            html_parts.append(f'''          <div class="leadership-card" data-id="{escape_html(person_id)}" data-category="{escape_html(cat_key)}">
            <img class="avatar" src="{escape_html(avatar)}" alt="{escape_html(name)}" width="140" height="140" loading="lazy" />
            <h3 class="name">{escape_html(name)}</h3>
            <p class="role">{escape_html(role) if role else "—"}</p>
            <p class="organization">{escape_html(organization) if organization else "—"}</p>
            <p class="title">{escape_html(title) if title else "—"}</p>
          </div>
''')
        
        html_parts.append('''        </div>
      </div>
''')
    
    # Generate modals
    html_parts.append('''    </div>
  </div>

''')
    
    for person in people:
        person_id = person.get('id', '')
        name = person.get('name', '')
        role = person.get('role', '')
        organization = person.get('organization', '')
        title = person.get('title', '')
        category = person.get('category', '')
        bio = person.get('bio', '')
        avatar = person.get('avatar', '').replace('./leadership-photos/', 'ccc-leadership/leadership-photos/')
        
        html_parts.append(f'''  <section id="{escape_html(person_id)}-modal" class="modal" role="dialog" aria-modal="true" aria-labelledby="{escape_html(person_id)}-title">
    <a href="#" class="modal__backdrop" aria-hidden="true"></a>
    <div class="modal__card">
      <a href="#" class="modal__close" aria-label="Close">×</a>

      <div class="modal__avatar-wrap">
        <img class="modal__avatar" src="{escape_html(avatar)}" alt="{escape_html(name)}" width="140" height="140" />
      </div>

      <div class="modal__header">
        <h3 id="{escape_html(person_id)}-title">{escape_html(name)}</h3>
        <p class="role">{escape_html(role) if role else "—"}</p>
        <p class="organization">{escape_html(organization) if organization else "—"}</p>
        <p class="title">{escape_html(title) if title else "—"}</p>
        <p class="category">{escape_html(category) if category else "—"}</p>
      </div>
      <div class="bio">{nl2br(bio) if bio else "—"}</div>
    </div>
  </section>

''')
    
    # Add JavaScript for modal behavior
    html_parts.append('''  <script>
    (function () {
      function syncModalOpenClass() {
        if (location.hash && document.querySelector(location.hash + '.modal')) {
          document.body.classList.add('modal-open');
        } else {
          document.body.classList.remove('modal-open');
        }
      }
      window.addEventListener('hashchange', syncModalOpenClass);
      document.addEventListener('DOMContentLoaded', syncModalOpenClass);

      // Open/close modal behavior
      document.addEventListener('click', function(e) {
        const card = e.target.closest('.leadership-card');
        if (card) {
          const id = card.getAttribute('data-id');
          location.hash = id + '-modal';
          syncModalOpenClass();
          return;
        }
        
        if (e.target.closest('.modal__backdrop') || e.target.closest('.modal__close')) {
          location.hash = '';
          syncModalOpenClass();
        }
      });

      document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && location.hash) {
          location.hash = '';
          syncModalOpenClass();
        }
      });

      // Initial state
      syncModalOpenClass();
    })();
  </script>

</body>
</html>
''')
    
    # Write HTML file
    os.makedirs('docs', exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(''.join(html_parts))
    
    print(f"✅ Generated static HTML: {output_path}")
    print(f"   Contains {len(people)} leadership entries")

if __name__ == '__main__':
    generate_html()

