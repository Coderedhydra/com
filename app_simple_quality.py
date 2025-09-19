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

def create_simple_quality_test_page():
    """Create test page with professional quality but simple template"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n" + "="*70)
    print("🎯 SIMPLE QUALITY TEST PAGE - PROFESSIONAL ENHANCEMENT")
    print("="*70)
    print("Professional quality enhancement with simplified HTML template!")
    print("Images will show their full size and quality properly!")
    
    # Step 1-3: Basic processing
    print("\n📹 Step 1: Processing subtitles...")
    get_subtitles(video)
    time.sleep(1)
    
    print("📹 Step 2: Extracting keyframes...")
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    print("📹 Step 3: Starting professional enhancement with simple template...")
    
    # Import and use the professional enhancer
    from backend.professional_comic_enhancer import ProfessionalComicEnhancer
    
    print("🎨 Using Professional Enhancement + Simple Template...")
    enhancer = ProfessionalComicEnhancer()
    test_success = enhancer.create_professional_comic_test_page()
    
    if test_success:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 Simple quality test page completed!")
        print(f"✅ Professional quality with simple template!")
        print(f"🎯 Images will show full size and quality!")
        print(f"--- Generation time: {total_time:.1f} seconds ---")
        return True
    else:
        print("❌ Simple quality test page generation failed")
        return False

def create_full_simple_quality_comic():
    """Create full 12-page comic with professional quality and simple template"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n🎯 Full 12-Page Simple Quality Comic Generation")
    print("Starting full comic with professional quality + simple template...")
    
    # Basic processing
    get_subtitles(video)
    time.sleep(2)
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    # Full comic generation
    from backend.professional_comic_enhancer import ProfessionalComicEnhancer
    enhancer = ProfessionalComicEnhancer()
    
    # Create full comic
    print("🎨 Creating full comic with simple quality template...")
    
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
    
    print(f"📋 Selected {len(selected_frames)} frames for simple quality comic")
    
    # Process all frames
    processed_count = 0
    for i, frame_file in enumerate(selected_frames, 1):
        frame_path = os.path.join('frames/final', frame_file)
        
        if os.path.exists(frame_path):
            if i % 8 == 1:
                print(f"Processing frames {i}-{min(i+7, len(selected_frames))}...")
            
            if enhancer.process_frame_professional(frame_path):
                processed_count += 1
    
    # Create pages
    pages = []
    for page_num in range(12):
        start_idx = page_num * 4
        end_idx = start_idx + 4
        page_frames = selected_frames[start_idx:end_idx]
        
        if page_frames:
            page = create_simple_quality_page(page_frames, page_num + 1)
            pages.append(page)
    
    # Save full comic
    save_full_simple_quality_comic(pages, selected_frames)
    
    if processed_count > 0:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 Full 12-page simple quality comic completed!")
        print(f"🎯 All {processed_count} panels with professional quality!")
        print(f"📺 Simple template shows full image size and quality!")
        print(f"--- Execution time: {total_time:.1f} seconds ({total_time/60:.2f} minutes) ---")
        return True
    else:
        print("❌ Full simple quality comic generation failed")
        return False

def create_simple_quality_page(page_frames, page_number):
    """Create simple quality comic page"""
    page = {
        "panels": [],
        "bubbles": [],
        "metadata": {
            "page_number": page_number,
            "quality": "Simple Quality",
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
            "quality": "Simple Quality"
        })
        
        # Bubble
        page["bubbles"].append({
            "dialog": f"Page {page_number} Panel {i+1}",
            "emotion": "normal",
            "bubble_offset_x": 50,
            "bubble_offset_y": 50,
            "tail_offset_x": 20,
            "tail_offset_y": 25,
            "tail_deg": 45
        })
    
    return page

def save_full_simple_quality_comic(pages, selected_frames):
    """Save full simple quality comic"""
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
    """Generate full 12-page comic with simple quality template"""
    try:
        print("🚀 Generating full 12-page simple quality comic...")
        success = create_full_simple_quality_comic()
        if success:
            return jsonify({'status': 'success', 'message': 'Full simple quality comic generated successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Simple quality comic generation failed'}), 500
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
        
        # Use the simple quality enhancer
        success = create_simple_quality_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5;">
            <h2 style="color: #2c3e50;">🎯 Simple Quality Test Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Professional quality enhancement with simplified template!</p>
            <p style="font-size: 14px; color: #7f8c8d;">Images will show their full size and quality properly - no thin appearance!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Simple Quality Test</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create simple quality test page", 500

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print(dict(request.form))  
        link = request.form['link']
        cleanup()
        download_video(link)
        
        # Use the simple quality enhancer
        success = create_simple_quality_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5;">
            <h2 style="color: #2c3e50;">🎯 Simple Quality Test Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Professional quality enhancement with simplified template!</p>
            <p style="font-size: 14px; color: #7f8c8d;">Images will show their full size and quality properly - no thin appearance!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Simple Quality Test</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create simple quality test page", 500

if __name__ == '__main__':
    print("🎯 Starting Simple Quality Comic Flask application...")
    print("Professional enhancement + Simplified template!")
    print("Images will show full size and quality - no thin appearance!")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)