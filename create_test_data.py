#!/usr/bin/env python3
"""
Create test data for comic panels
Ensures all 4 panels have different images for testing
"""

import os
import json
import shutil
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np

def create_test_images():
    """Create test images for all 4 panels"""
    frames_dir = "frames/final"
    os.makedirs(frames_dir, exist_ok=True)
    
    # Create 8 different test images for variety
    colors = [
        (255, 100, 100),  # Red
        (100, 255, 100),  # Green  
        (100, 100, 255),  # Blue
        (255, 255, 100),  # Yellow
        (255, 100, 255),  # Magenta
        (100, 255, 255),  # Cyan
        (255, 150, 100),  # Orange
        (150, 100, 255),  # Purple
    ]
    
    for i in range(8):
        # Create a 800x600 image with different colors
        img = np.zeros((600, 800, 3), dtype=np.uint8)
        img[:] = colors[i]
        
        # Add some pattern to make it interesting
        cv2.rectangle(img, (100, 100), (700, 500), (255, 255, 255), 3)
        cv2.circle(img, (400, 300), 150, (0, 0, 0), 5)
        
        # Add text to identify the panel
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f"Panel {i + 1}"
        cv2.putText(img, text, (300, 320), font, 2, (255, 255, 255), 3, cv2.LINE_AA)
        
        # Save the image
        filename = f"frame{i+1:03d}.png"
        filepath = os.path.join(frames_dir, filename)
        cv2.imwrite(filepath, img)
        print(f"Created test image: {filename}")
    
    print(f"✅ Created {len(colors)} test images in {frames_dir}")
    return len(colors)

def create_test_comic_data():
    """Create test comic data with 4 panels per page"""
    # Create test pages data with 4 different panels
    test_pages = [
        {
            "panels": [
                {
                    "image": "frame001",
                    "row_span": 1,
                    "col_span": 1
                },
                {
                    "image": "frame002", 
                    "row_span": 1,
                    "col_span": 1
                },
                {
                    "image": "frame003",
                    "row_span": 1,
                    "col_span": 1
                },
                {
                    "image": "frame004",
                    "row_span": 1,
                    "col_span": 1
                }
            ],
            "bubbles": [
                {
                    "dialog": "Panel 1: Top Left",
                    "emotion": "normal",
                    "bubble_offset_x": 50,
                    "bubble_offset_y": 50,
                    "tail_offset_x": 20,
                    "tail_offset_y": 30,
                    "tail_deg": 45
                },
                {
                    "dialog": "Panel 2: Top Right",
                    "emotion": "normal",
                    "bubble_offset_x": 50,
                    "bubble_offset_y": 50,
                    "tail_offset_x": 30,
                    "tail_offset_y": 40,
                    "tail_deg": 60
                },
                {
                    "dialog": "Panel 3: Bottom Left",
                    "emotion": "normal",
                    "bubble_offset_x": 50,
                    "bubble_offset_y": 50,
                    "tail_offset_x": 25,
                    "tail_offset_y": 35,
                    "tail_deg": 50
                },
                {
                    "dialog": "Panel 4: Bottom Right",
                    "emotion": "normal",
                    "bubble_offset_x": 50,
                    "bubble_offset_y": 50,
                    "tail_offset_x": 35,
                    "tail_offset_y": 45,
                    "tail_deg": 55
                }
            ]
        },
        # Second page with different images
        {
            "panels": [
                {
                    "image": "frame005",
                    "row_span": 1,
                    "col_span": 1
                },
                {
                    "image": "frame006", 
                    "row_span": 1,
                    "col_span": 1
                },
                {
                    "image": "frame007",
                    "row_span": 1,
                    "col_span": 1
                },
                {
                    "image": "frame008",
                    "row_span": 1,
                    "col_span": 1
                }
            ],
            "bubbles": [
                {
                    "dialog": "Page 2 - Panel 1",
                    "emotion": "normal",
                    "bubble_offset_x": 60,
                    "bubble_offset_y": 40,
                    "tail_offset_x": 20,
                    "tail_offset_y": 30,
                    "tail_deg": 45
                },
                {
                    "dialog": "Page 2 - Panel 2",
                    "emotion": "normal",
                    "bubble_offset_x": 70,
                    "bubble_offset_y": 60,
                    "tail_offset_x": 30,
                    "tail_offset_y": 40,
                    "tail_deg": 60
                },
                {
                    "dialog": "Page 2 - Panel 3",
                    "emotion": "normal",
                    "bubble_offset_x": 55,
                    "bubble_offset_y": 45,
                    "tail_offset_x": 25,
                    "tail_offset_y": 35,
                    "tail_deg": 50
                },
                {
                    "dialog": "Page 2 - Panel 4",
                    "emotion": "normal",
                    "bubble_offset_x": 65,
                    "bubble_offset_y": 55,
                    "tail_offset_x": 35,
                    "tail_offset_y": 45,
                    "tail_deg": 55
                }
            ]
        }
    ]
    
    # Write test data to page.js
    os.makedirs('output_template', exist_ok=True)
    with open('output_template/page.js', 'w') as f:
        f.write('var pages = ')
        json.dump(test_pages, f, indent=4)
    
    # Also copy to static directory for Flask
    os.makedirs('static/comic', exist_ok=True)
    with open('static/comic/page.js', 'w') as f:
        f.write('var pages = ')
        json.dump(test_pages, f, indent=4)
    
    print("✅ Created test comic data with 4 panels per page")
    print(f"✅ Page 1: {[p['image'] for p in test_pages[0]['panels']]}")
    print(f"✅ Page 2: {[p['image'] for p in test_pages[1]['panels']]}")
    
    return test_pages

def copy_test_files():
    """Copy test files to static directory"""
    # Copy frames to static directory
    if os.path.exists('frames/final'):
        os.makedirs('static/comic/frames/final', exist_ok=True)
        for item in os.listdir('frames/final'):
            if item.endswith('.png'):
                src = os.path.join('frames/final', item)
                dst = os.path.join('static/comic/frames/final', item)
                shutil.copy2(src, dst)
                print(f"Copied {item} to static directory")
    
    # Copy template files
    template_files = ['page.css', 'page_place.js', 'bubble.css']
    for file in template_files:
        src = os.path.join('output_template', file)
        if os.path.exists(src):
            dst = os.path.join('static/comic', file)
            shutil.copy2(src, dst)
            print(f"Copied {file} to static directory")
    
    print("✅ All test files copied to static directory")

def main():
    """Create complete test environment"""
    print("🎯 Creating Test Data for 4-Panel Comic Layout")
    print("=" * 50)
    
    # Create test images
    num_images = create_test_images()
    
    # Create test comic data
    pages = create_test_comic_data()
    
    # Copy files to static directory
    copy_test_files()
    
    print("\n🎉 Test Environment Ready!")
    print(f"📸 Created {num_images} test images")
    print(f"📄 Created {len(pages)} test pages")
    print("🌐 Files copied to static directory for Flask")
    print("\n🚀 You can now test the application:")
    print("   python3 start_app.py")
    print("   or")
    print("   python3 app.py")
    print("\n📍 Access at: http://localhost:5000")
    print("✅ All 4 panels should now show different images!")

if __name__ == "__main__":
    main()