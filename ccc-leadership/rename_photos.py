#!/usr/bin/env python3
"""
Script to rename photos to match the person's name from the JSON file.
"""
import json
import os
import re
from urllib.parse import urlparse

def sanitize_filename(name):
    """Convert a name to a safe filename."""
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and special characters with hyphens
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name

def rename_photos():
    """Rename photos to match person names."""
    json_path = os.path.join(os.path.dirname(__file__), 'leadership.json')
    photos_dir = os.path.join(os.path.dirname(__file__), 'leadership-photos')
    
    # Read the JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        leadership = json.load(f)
    
    renamed = 0
    skipped = 0
    
    for person in leadership:
        avatar_path = person.get('avatar', '')
        if not avatar_path:
            continue
        
        # Extract current filename
        if avatar_path.startswith('./'):
            current_filename = avatar_path.replace('./leadership-photos/', '')
        else:
            # If it's still a URL, extract filename
            parsed = urlparse(avatar_path)
            current_filename = os.path.basename(parsed.path)
        
        current_path = os.path.join(photos_dir, current_filename)
        
        if not os.path.exists(current_path):
            print(f"Warning: File not found for {person['name']}: {current_filename}")
            skipped += 1
            continue
        
        # Get file extension
        _, ext = os.path.splitext(current_filename)
        
        # Create new filename from person's name
        person_name = person.get('name', '')
        new_filename = f"{sanitize_filename(person_name)}{ext}"
        new_path = os.path.join(photos_dir, new_filename)
        
        # Skip if already renamed
        if current_filename == new_filename:
            print(f"⊘ Already named correctly: {person_name}")
            continue
        
        # Check if target file already exists (different person with same name?)
        if os.path.exists(new_path) and current_path != new_path:
            # Add ID to make it unique
            person_id = person.get('id', '')
            new_filename = f"{sanitize_filename(person_name)}-{person_id}{ext}"
            new_path = os.path.join(photos_dir, new_filename)
        
        # Rename the file
        try:
            os.rename(current_path, new_path)
            print(f"✓ Renamed: {current_filename} → {new_filename} ({person_name})")
            
            # Update JSON with new path
            person['avatar'] = f"./leadership-photos/{new_filename}"
            renamed += 1
        except Exception as e:
            print(f"✗ Failed to rename {current_filename}: {e}")
            skipped += 1
    
    # Write updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(leadership, f, indent=2, ensure_ascii=False)
    
    print(f"\nSummary: {renamed} renamed, {skipped} skipped")

if __name__ == '__main__':
    rename_photos()

