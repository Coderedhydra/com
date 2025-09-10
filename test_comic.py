#!/usr/bin/env python3
"""
Test script to verify comic functionality
"""

import os
import json
from app import create_test_comic_data, copy_template

def test_comic_creation():
    """Test the comic creation process"""
    print("Testing comic creation...")
    
    # Create test comic data
    create_test_comic_data()
    
    # Copy template files
    copy_template()
    
    print("✅ Test comic data created successfully!")
    print("✅ Template files copied!")
    
    # Verify files exist
    files_to_check = [
        'output_template/page.js',
        'output_template/page.html',
        'output_template/page_place.js',
        'output_template/bubble.css',
        'output_template/page.css',
        'frames/final/test1.png',
        'frames/final/test2.png'
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
    
    print("\n🎉 Test setup complete!")
    print("You can now:")
    print("1. Run the Flask app: python app.py")
    print("2. Upload a video or enter a link")
    print("3. Test the print functionality")
    print("4. Test the image upload functionality")

if __name__ == "__main__":
    test_comic_creation()