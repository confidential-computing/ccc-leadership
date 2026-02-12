#!/usr/bin/env python3
"""
Script to update leadership.json to use local photo paths instead of URLs.
"""
import json
import os
from urllib.parse import urlparse

def update_to_local_paths():
    """Update avatar URLs to local paths."""
    json_path = os.path.join(os.path.dirname(__file__), 'leadership.json')
    photos_dir = os.path.join(os.path.dirname(__file__), 'leadership-photos')
    
    # Read the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        leadership = json.load(f)
    
    # Update each entry
    updated = 0
    for person in leadership:
        avatar_url = person.get('avatar', '')
        if not avatar_url:
            continue
        
        # Extract filename from URL
        parsed = urlparse(avatar_url)
        filename = os.path.basename(parsed.path)
        
        # Check if file exists locally
        local_path = os.path.join(photos_dir, filename)
        if os.path.exists(local_path):
            # Update to relative path
            person['avatar'] = f"./leadership-photos/{filename}"
            updated += 1
        else:
            print(f"Warning: Local file not found for {person['name']}: {filename}")
    
    # Write updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(leadership, f, indent=2, ensure_ascii=False)
    
    print(f"Updated {updated} avatar paths to local files.")

if __name__ == '__main__':
    update_to_local_paths()

