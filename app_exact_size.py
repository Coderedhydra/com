import os
import webbrowser
import time
import subprocess
import base64

from flask import Flask, render_template, request, jsonify, send_file
from backend.subtitles.subs import get_subtitles
from backend.keyframes.keyframes import generate_keyframes, black_bar_crop
from backend.utils import cleanup, download_video
from backend.utils import copy_template
import json
import shutil

app = Flask(__name__)

def copy_to_static():
    """Copy generated comic files to static directory for Flask serving"""
    # Create static/comic directory if it doesn't exist
    os.makedirs('static/comic', exist_ok=True)
    
    # Copy all files from output_template to static/comic
    if os.path.exists('output_template'):
        for item in os.listdir('output_template'):
            src = os.path.join('output_template', item)
            dst = os.path.join('static/comic', item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
    
    # Copy frames to static directory
    if os.path.exists('frames/final'):
        os.makedirs('static/comic/frames/final', exist_ok=True)
        for item in os.listdir('frames/final'):
            src = os.path.join('frames/final', item)
            dst = os.path.join('static/comic/frames/final', item)
            shutil.copy2(src, dst)
    
    print("Comic files copied to static directory for Flask serving!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comic')
def comic():
    """Serve the exact size comic page"""
    # Check if comic data exists
    comic_data_path = os.path.join(os.getcwd(), 'static', 'comic', 'page.js')
    if os.path.exists(comic_data_path):
        return render_template('comic.html')
    else:
        return "Comic not found. Please generate a comic first.", 404

def create_exact_size_test_page():
    """Create test page with exact 400×540 panels"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n" + "="*70)
    print("📐 EXACT SIZE TEST PAGE - 400×540 per panel")
    print("="*70)
    print("Creating test page with exact dimensions for perfect template fit!")
    print("Template: 800×1080 | Each panel: 400×540 | No gaps!")
    
    # Step 1-3: Basic processing
    print("\n📹 Step 1: Processing subtitles...")
    get_subtitles(video)
    time.sleep(1)
    
    print("📹 Step 2: Extracting keyframes...")
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    print("📹 Step 3: Enhancing to exact 400×540 size...")
    
    # Use exact size enhancer
    from backend.exact_size_enhancer import ExactSizeEnhancer
    
    print("📐 Using Exact Size Enhancer (400×540 per panel)...")
    enhancer = ExactSizeEnhancer()
    test_success = enhancer.create_exact_size_test_page()
    
    if test_success:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 Exact size test page completed!")
        print(f"✅ Perfect template fit: 800×1080 with 400×540 panels!")
        print(f"📐 Zero gaps - exact dimensions!")
        print(f"--- Generation time: {total_time:.1f} seconds ---")
        return True
    else:
        print("❌ Exact size test page generation failed")
        return False

def create_full_exact_size_comic():
    """Create full 12-page comic with exact 400×540 panels"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n📐 Full 12-Page Exact Size Comic Generation")
    print("Starting full comic with 400×540 panels...")
    
    # Basic processing
    get_subtitles(video)
    time.sleep(2)
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    # Full comic generation with exact sizes
    from backend.exact_size_enhancer import ExactSizeEnhancer
    enhancer = ExactSizeEnhancer()
    
    # Get all frames
    frames_dir = "frames/final"
    frame_files = [f for f in os.listdir(frames_dir) 
                  if f.lower().endswith('.png') and f.startswith('frame')]
    frame_files.sort()
    
    if not frame_files:
        print("❌ No frames found")
        return False
    
    # Select frames for 12 pages (48 panels)
    panels_needed = 48
    if len(frame_files) >= panels_needed:
        step = len(frame_files) // panels_needed
        selected_frames = [frame_files[i * step] for i in range(panels_needed)]
    else:
        selected_frames = frame_files.copy()
        while len(selected_frames) < panels_needed:
            selected_frames.extend(frame_files)
        selected_frames = selected_frames[:panels_needed]
    
    print(f"📋 Selected {len(selected_frames)} frames for exact size comic")
    
    # Process all frames to exact size
    processed_count = 0
    for i, frame_file in enumerate(selected_frames, 1):
        frame_path = os.path.join('frames/final', frame_file)
        
        if os.path.exists(frame_path):
            if i % 8 == 1:
                print(f"Processing exact size frames {i}-{min(i+7, len(selected_frames))}...")
            
            if enhancer.enhance_to_exact_size(frame_path):
                processed_count += 1
    
    # Create pages
    pages = []
    for page_num in range(12):
        start_idx = page_num * 4
        end_idx = start_idx + 4
        page_frames = selected_frames[start_idx:end_idx]
        
        if page_frames:
            page = create_exact_size_page(page_frames, page_num + 1)
            pages.append(page)
    
    # Save full comic
    save_full_exact_size_comic(pages, selected_frames)
    
    if processed_count > 0:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 Full 12-page exact size comic completed!")
        print(f"📐 All {processed_count} panels exactly 400×540!")
        print(f"🔲 Perfect 800×1080 template fit with zero gaps!")
        print(f"--- Execution time: {total_time:.1f} seconds ({total_time/60:.2f} minutes) ---")
        return True
    else:
        print("❌ Full exact size comic generation failed")
        return False

def create_exact_size_page(page_frames, page_number):
    """Create exact size comic page"""
    page = {
        "panels": [],
        "bubbles": [],
        "metadata": {
            "page_number": page_number,
            "quality": "400×540 Exact",
            "panel_count": len(page_frames)
        }
    }
    
    for i, frame_file in enumerate(page_frames):
        frame_name = frame_file.replace('.png', '')
        
        # Panel
        page["panels"].append({
            "image": frame_name,
            "row_span": 1,
            "col_span": 1,
            "quality": "400×540 Exact"
        })
        
        # Bubble
        page["bubbles"].append({
            "dialog": f"Page {page_number}.{i+1}",
            "emotion": "normal",
            "bubble_offset_x": 50,
            "bubble_offset_y": 50,
            "tail_offset_x": 20,
            "tail_offset_y": 25,
            "tail_deg": 45
        })
    
    return page

def save_full_exact_size_comic(pages, selected_frames):
    """Save full exact size comic"""
    # Save pages
    os.makedirs('output_template', exist_ok=True)
    with open('output_template/page.js', 'w') as f:
        f.write('var pages = ')
        json.dump(pages, f, indent=4)
    
    os.makedirs('static/comic', exist_ok=True)
    with open('static/comic/page.js', 'w') as f:
        f.write('var pages = ')
        json.dump(pages, f, indent=4)

@app.route('/generate_full_comic', methods=['POST'])
def generate_full_comic():
    """Generate full 12-page exact size comic"""
    try:
        print("🚀 Generating full 12-page exact size comic...")
        success = create_full_exact_size_comic()
        if success:
            return jsonify({'status': 'success', 'message': 'Full exact size comic generated successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Exact size comic generation failed'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(dict(request.form))  
        f = request.files['file']
        print(type(f))
        cleanup()
        f.save("video/uploaded.mp4")
        
        # Create exact size test page
        success = create_exact_size_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #2c3e50; color: white;">
            <h2 style="color: #ecf0f1;">📐 Exact Size Comic Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Perfect 800×1080 template with 400×540 panels!</p>
            <p style="font-size: 14px; color: #bdc3c7;">Zero gaps - exact dimensions for perfect fit!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #27ae60; color: white; text-decoration: none; border-radius: 8px; margin: 20px;">View Exact Size Comic</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create exact size comic", 500

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print(dict(request.form))  
        link = request.form['link']
        cleanup()
        download_video(link)
        
        # Create exact size test page
        success = create_exact_size_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #2c3e50; color: white;">
            <h2 style="color: #ecf0f1;">📐 Exact Size Comic Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Perfect 800×1080 template with 400×540 panels!</p>
            <p style="font-size: 14px; color: #bdc3c7;">Zero gaps - exact dimensions for perfect fit!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #27ae60; color: white; text-decoration: none; border-radius: 8px; margin: 20px;">View Exact Size Comic</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create exact size comic", 500

if __name__ == '__main__':
    print("📐 Starting Exact Size Comic Flask application...")
    print("Perfect 800×1080 template with 400×540 panels!")
    print("Zero gaps - exact dimensions for perfect image fit!")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)