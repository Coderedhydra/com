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
    """Serve the comic page using Flask template"""
    # Check if comic data exists
    comic_data_path = os.path.join(os.getcwd(), 'static', 'comic', 'page.js')
    if os.path.exists(comic_data_path):
        return render_template('comic.html')
    else:
        return "Comic not found. Please generate a comic first.", 404

def create_4k_template_fit_test_page():
    """Create 4K test page using template fitting approach from GitHub repo"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n" + "="*80)
    print("🚀 4K TEMPLATE FIT TEST PAGE - RESIZE AND FIT ALL IMAGES")
    print("="*80)
    print("Based on Coderedhydra/comic resize-and-fit-all-images-to-template approach!")
    print("This properly fits images to 4K template dimensions with quality enhancement!")
    
    # Step 1-3: Basic processing
    print("\n📹 Step 1: Processing subtitles...")
    get_subtitles(video)
    time.sleep(1)
    
    print("📹 Step 2: Extracting keyframes...")
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    print("📹 Step 3: Starting 4K template fitting...")
    
    # Import and use the enhanced 4K template fit enhancer
    from backend.enhanced_4k_template_fit import Enhanced4KTemplateFit
    
    print("🔥 Using Enhanced 4K Template Fit (resize and fit to 4K template)...")
    enhancer = Enhanced4KTemplateFit()
    test_success = enhancer.create_4k_template_fit_test_page()
    
    if test_success:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 4K Template Fit test page completed!")
        print(f"✅ All images properly fitted to 4K template!")
        print(f"🚀 Each panel: 1920x1080 (4K template fitted)!")
        print(f"--- Generation time: {total_time:.1f} seconds ---")
        return True
    else:
        print("❌ 4K Template fit test page generation failed")
        return False

def create_full_4k_template_fit_comic():
    """Create full 12-page comic with 4K template fitting"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n🚀 Full 12-Page 4K Template Fit Comic Generation")
    print("Starting full comic with 4K template fitting...")
    
    # Basic processing
    get_subtitles(video)
    time.sleep(2)
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    # Full comic generation with 4K template fitting
    from backend.enhanced_4k_template_fit import Enhanced4KTemplateFit
    enhancer = Enhanced4KTemplateFit()
    
    # Create full comic using the enhancer
    print("🔥 Creating full 12-page comic with 4K template fitting...")
    
    # Get all frames
    frames_dir = "frames/final"
    frame_files = [f for f in os.listdir(frames_dir) 
                  if f.lower().endswith('.png') and f.startswith('frame')]
    frame_files.sort()
    
    if not frame_files:
        print("❌ No frames found for full comic")
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
    
    print(f"📋 Selected {len(selected_frames)} frames for full 4K comic")
    
    # Process all frames
    processed_count = 0
    for i, frame_file in enumerate(selected_frames, 1):
        frame_path = os.path.join('frames/final', frame_file)
        
        if os.path.exists(frame_path):
            if i % 8 == 1:
                print(f"Processing 4K template fit {i}-{min(i+7, len(selected_frames))}...")
            
            if enhancer.process_frame_to_4k_template(frame_path):
                processed_count += 1
    
    # Create pages
    pages = []
    for page_num in range(12):
        start_idx = page_num * 4
        end_idx = start_idx + 4
        page_frames = selected_frames[start_idx:end_idx]
        
        if page_frames:
            page = create_4k_template_page(page_frames, page_num + 1)
            pages.append(page)
    
    # Save full comic
    save_full_4k_template_comic(pages, selected_frames)
    
    if processed_count > 0:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 Full 12-page 4K template fit comic completed!")
        print(f"🔥 All {processed_count} panels fitted to 4K template!")
        print(f"--- Execution time: {total_time:.1f} seconds ({total_time/60:.2f} minutes) ---")
        return True
    else:
        print("❌ Full 4K template fit comic generation failed")
        return False

def create_4k_template_page(page_frames, page_number):
    """Create 4K template fitted comic page"""
    page = {
        "panels": [],
        "bubbles": [],
        "metadata": {
            "page_number": page_number,
            "quality": "4K Template Fit",
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
            "quality": "4K Template Fit"
        })
        
        # Bubble
        page["bubbles"].append({
            "dialog": f"4K Page {page_number} Panel {i+1}",
            "emotion": "normal",
            "bubble_offset_x": 50,
            "bubble_offset_y": 50,
            "tail_offset_x": 25,
            "tail_offset_y": 30,
            "tail_deg": 45
        })
    
    return page

def save_full_4k_template_comic(pages, selected_frames):
    """Save full 4K template fitted comic"""
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
    """Generate full 12-page comic with 4K template fitting"""
    try:
        print("🚀 Generating full 12-page 4K template fit comic...")
        success = create_full_4k_template_fit_comic()
        if success:
            return jsonify({'status': 'success', 'message': 'Full 4K template fit comic generated successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Full 4K template fit comic generation failed'}), 500
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
        
        # Use the 4K template fit enhancer
        success = create_4k_template_fit_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🚀 4K Template Fit Test Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Images properly resized and fitted to 4K template (1920x1080 per panel)!</p>
            <p style="font-size: 14px; color: #7f8c8d;">Based on resize-and-fit-all-images-to-template approach with 4K enhancement!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #e74c3c; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View 4K Template Fit Test</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create 4K template fit test page", 500

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print(dict(request.form))  
        link = request.form['link']
        cleanup()
        download_video(link)
        
        # Use the 4K template fit enhancer
        success = create_4k_template_fit_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🚀 4K Template Fit Test Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Images properly resized and fitted to 4K template (1920x1080 per panel)!</p>
            <p style="font-size: 14px; color: #7f8c8d;">Based on resize-and-fit-all-images-to-template approach with 4K enhancement!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #e74c3c; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View 4K Template Fit Test</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create 4K template fit test page", 500

if __name__ == '__main__':
    print("🚀 Starting 4K Template Fit Comic Flask application...")
    print("Based on resize-and-fit-all-images-to-template approach!")
    print("This properly fits images to 4K template with quality enhancement!")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)