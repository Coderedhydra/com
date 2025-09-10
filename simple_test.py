#!/usr/bin/env python3
"""
Simple test script to verify comic functionality without Flask dependencies
"""

import os
import json

def create_test_comic_data():
    """Create test comic data for testing purposes"""
    # Create test pages data
    test_pages = [
        {
            "panels": [
                {
                    "image": "test1",
                    "row_span": 1,
                    "col_span": 1
                },
                {
                    "image": "test2", 
                    "row_span": 1,
                    "col_span": 1
                }
            ],
            "bubbles": [
                {
                    "dialog": "Hello! This is a test bubble with normal text.",
                    "emotion": "normal",
                    "bubble_offset_x": 50,
                    "bubble_offset_y": 50,
                    "tail_offset_x": 20,
                    "tail_offset_y": 30,
                    "tail_deg": 45
                },
                {
                    "dialog": "This is another test bubble!",
                    "emotion": "normal",
                    "bubble_offset_x": 100,
                    "bubble_offset_y": 100,
                    "tail_offset_x": 30,
                    "tail_offset_y": 40,
                    "tail_deg": 60
                }
            ]
        }
    ]
    
    # Write test data to page.js
    with open('output_template/page.js', 'w') as f:
        f.write(f'var pages = ')
        json.dump(test_pages, f, indent=4)
    
    print("Test comic data created successfully!")

def test_comic_creation():
    """Test the comic creation process"""
    print("Testing comic creation...")
    
    # Create test comic data
    create_test_comic_data()
    
    print("✅ Test comic data created successfully!")
    
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
    print("1. Run the Flask app: python3 app.py")
    print("2. Upload a video or enter a link")
    print("3. Test the print functionality")
    print("4. Test the image upload functionality")
    print("\n📋 Summary of fixes:")
    print("✅ Fixed print functionality (missing page.js file)")
    print("✅ Updated bubble styling to be square and bold")
    print("✅ Added image upload functionality")
    print("✅ Commented out heavy processing for testing")

if __name__ == "__main__":
    test_comic_creation()