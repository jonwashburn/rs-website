#!/usr/bin/env python3
"""
SAFER version of template application script
This version is more careful about preserving content
"""

import os
import re
from pathlib import Path
import shutil
from datetime import datetime

# Create backup directory
BACKUP_DIR = f"backups/template-rollout-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

def create_backup(file_path):
    """Create a backup of the file before modifying"""
    backup_path = Path(BACKUP_DIR) / file_path.relative_to('.')
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, backup_path)
    return backup_path

def update_css_links_safely(content, filename):
    """Safely update CSS links without breaking content"""
    lines = content.split('\n')
    new_lines = []
    template_css_added = False
    
    for line in lines:
        # Keep main.css but remove other old CSS files
        if re.search(r'<link[^>]+href="[^"]*(?:academic-style\.css|encyclopedia\.css)[^"]*"[^>]*>', line):
            continue
        
        # Add template CSS after main.css and before </head>
        if '</head>' in line and not template_css_added and 'site-template.css' not in content:
            new_lines.append('  <link rel="stylesheet" href="/assets/css/site-template.css">')
            template_css_added = True
        
        new_lines.append(line)
    
    return '\n'.join(new_lines)

def apply_class_updates(content):
    """Apply class updates more safely"""
    # Add template- prefix to avoid conflicts
    updates = [
        # Hero sections
        (r'<section\s+class="hero">', '<section class="template-hero template-hero-framed">'),
        (r'<section\s+class="cosmic-hero">', '<section class="template-hero template-hero-framed">'),
        (r'class="hero-content"', 'class="template-hero-content"'),
        (r'class="hero-title"', 'class="template-hero-title"'),
        (r'class="hero-lead"', 'class="template-hero-lead"'),
        
        # Content sections
        (r'<section\s+class="content-section">', '<section class="template-section">'),
        (r'<section\s+class="page-section">', '<section class="template-section">'),
        
        # Containers
        (r'class="wrapper"', 'class="template-container"'),
        (r'class="content-wrapper"', 'class="template-container"'),
        (r'class="container"', 'class="template-container"'),
        
        # Titles
        (r'class="section-title"', 'class="template-section-title"'),
        (r'class="page-title"', 'class="template-section-title"'),
        
        # Content blocks
        (r'class="content-block"', 'class="template-reading"'),
        (r'class="reading"', 'class="template-reading"'),
        
        # Body class
        (r'<body class="academic-page">', '<body class="template-page">'),
        (r'<body>', '<body class="template-page">'),
    ]
    
    for old, new in updates:
        content = re.sub(old, new, content)
    
    return content

def should_skip_file(file_path):
    """Skip certain files that shouldn't be modified"""
    skip_patterns = [
        'constants.html',  # This is our template!
        'constants-styles.css',
        '_includes/header.html',
        '_includes/footer.html'
    ]
    
    return any(pattern in str(file_path) for pattern in skip_patterns)

def process_file_safely(file_path):
    """Process a file with safety checks"""
    if should_skip_file(file_path):
        print(f"⏭️  Skipped (template file): {file_path}")
        return False
    
    try:
        # Read original content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Verify we have actual content
        if len(original_content) < 100 or '<body' not in original_content:
            print(f"⚠️  Skipped (too small or no body): {file_path}")
            return False
        
        # Create backup
        backup_path = create_backup(file_path)
        
        # Apply changes
        content = original_content
        content = update_css_links_safely(content, file_path.name)
        content = apply_class_updates(content)
        
        # Safety check: ensure content wasn't truncated
        if len(content) < len(original_content) * 0.9:  # Lost more than 10%
            print(f"❌ ERROR: Content would be truncated! Skipping {file_path}")
            return False
        
        # Write changes
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated: {file_path}")
            return True
        else:
            print(f"  No changes: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False

def main():
    """Main function"""
    # Create backup directory
    Path(BACKUP_DIR).mkdir(parents=True, exist_ok=True)
    print(f"📁 Created backup directory: {BACKUP_DIR}\n")
    
    # Find HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        if any(skip in root for skip in ['node_modules', '.git', '_site', 'assets', 'backups']):
            continue
        
        for file in files:
            if file.endswith('.html') and not file.startswith('._'):
                html_files.append(Path(root) / file)
    
    print(f"Found {len(html_files)} HTML files\n")
    
    # Process files
    updated_count = 0
    for file_path in sorted(html_files):
        if process_file_safely(file_path):
            updated_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  Total files: {len(html_files)}")
    print(f"  Updated: {updated_count}")
    print(f"  Skipped/No changes: {len(html_files) - updated_count}")
    print(f"\nBackups saved to: {BACKUP_DIR}")
    print(f"\nTo restore a file:")
    print(f"  cp {BACKUP_DIR}/path/to/file.html path/to/file.html")

if __name__ == "__main__":
    main()
