#!/usr/bin/env python3
"""
Test Page Display - Debug the white page issue
"""

import os
import json

def check_comic_files():
    """Check if all comic files are present"""
    print("🔍 Checking Comic Files...")
    print("=" * 40)
    
    files_to_check = [
        'static/comic/page.js',
        'static/comic/page.css', 
        'static/comic/page_place.js',
        'static/comic/bubble.css',
        'static/comic/frames/final/frame001.png',
        'static/comic/frames/final/frame002.png',
        'static/comic/frames/final/frame003.png',
        'static/comic/frames/final/frame004.png'
    ]
    
    all_present = True
    for file_path in files_to_check:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} - MISSING")
            all_present = False
    
    return all_present

def check_page_data():
    """Check the page.js data structure"""
    print("\n📄 Checking Page Data...")
    print("=" * 40)
    
    try:
        with open('static/comic/page.js', 'r') as f:
            content = f.read()
        
        print(f"📊 page.js size: {len(content)} characters")
        
        # Extract JSON data
        if 'var pages = ' in content:
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            if json_start >= 0 and json_end > json_start:
                json_data = content[json_start:json_end]
                pages = json.loads(json_data)
                
                print(f"📚 Pages found: {len(pages)}")
                
                for i, page in enumerate(pages):
                    panels = page.get('panels', [])
                    bubbles = page.get('bubbles', [])
                    print(f"   Page {i+1}: {len(panels)} panels, {len(bubbles)} bubbles")
                    
                    for j, panel in enumerate(panels):
                        image_name = panel.get('image', 'unknown')
                        image_path = f"static/comic/frames/final/{image_name}.png"
                        exists = "✅" if os.path.exists(image_path) else "❌"
                        print(f"      Panel {j+1}: {image_name} {exists}")
                
                return True
            else:
                print("❌ Could not extract JSON from page.js")
                return False
        else:
            print("❌ page.js doesn't contain 'var pages ='")
            return False
            
    except Exception as e:
        print(f"❌ Error reading page.js: {e}")
        return False

def create_simple_test_page():
    """Create a simple test page that should definitely work"""
    print("\n🛠️ Creating Simple Test Page...")
    print("=" * 40)
    
    # Simple test data
    simple_page = [{
        "panels": [
            {"image": "frame001", "row_span": 1, "col_span": 1},
            {"image": "frame002", "row_span": 1, "col_span": 1},
            {"image": "frame003", "row_span": 1, "col_span": 1},
            {"image": "frame004", "row_span": 1, "col_span": 1}
        ],
        "bubbles": [
            {"dialog": "Test 1", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 20, "tail_offset_y": 30, "tail_deg": 45},
            {"dialog": "Test 2", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 30, "tail_offset_y": 40, "tail_deg": 60},
            {"dialog": "Test 3", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 25, "tail_offset_y": 35, "tail_deg": 50},
            {"dialog": "Test 4", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 35, "tail_offset_y": 45, "tail_deg": 55}
        ]
    }]
    
    # Write simple test page
    os.makedirs('static/comic', exist_ok=True)
    with open('static/comic/page.js', 'w') as f:
        f.write('var pages = ')
        json.dump(simple_page, f, indent=4)
    
    print("✅ Simple test page created")
    print("📄 1 page with 4 panels")
    print("🌐 Try accessing: http://localhost:5000/comic")
    
    return True

def main():
    print("🔍 Debugging White Page Issue")
    print("=" * 50)
    
    # Check files
    files_ok = check_comic_files()
    
    # Check data
    data_ok = check_page_data()
    
    if not files_ok or not data_ok:
        print("\n🛠️ Issues found, creating simple test page...")
        create_simple_test_page()
    
    print("\n🎯 Debugging Summary:")
    print(f"   Files present: {'✅' if files_ok else '❌'}")
    print(f"   Data structure: {'✅' if data_ok else '❌'}")
    
    print("\n🌐 Test your comic at: http://localhost:5000/comic")
    print("🔧 If still white, check browser console for errors")

if __name__ == "__main__":
    main()