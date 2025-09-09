#!/usr/bin/env python3
"""
Simple and Fast Cinecomic Runner
Optimized for speed without complex models
"""

import os
import sys
import time
from flask import Flask, render_template, request
import webbrowser

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def create_comic_simple():
    """Simplified comic creation process"""
    start_time = time.time()
    print("🚀 Starting fast comic creation...")
    
    try:
        # Import only when needed
        from backend.subtitles.subs import get_subtitles
        from backend.keyframes.keyframes import generate_keyframes, black_bar_crop
        from backend.panel_layout.layout_gen import generate_layout
        from backend.cartoonize.cartoonize import style_frames
        from backend.speech_bubble.bubble import bubble_create
        from backend.page_create import page_create, page_json
        from backend.utils import cleanup, copy_template
        
        video = 'video/uploaded.mp4'
        
        print("📝 Generating subtitles...")
        get_subtitles(video)
        
        print("🎬 Extracting keyframes (fast mode)...")
        generate_keyframes(video)
        
        print("📐 Generating layout (no cropping)...")
        black_x, black_y, _, _ = black_bar_crop()
        crop_coords, page_templates, panels = generate_layout()
        
        print("💬 Creating speech bubbles...")
        bubbles = bubble_create(video, crop_coords, black_x, black_y)
        
        print("📄 Creating pages...")
        pages = page_create(page_templates, panels, bubbles)
        page_json(pages)
        
        print("🎨 Applying cartoon style (fast)...")
        style_frames()
        
        print("📁 Copying template...")
        copy_template()
        
        execution_time = (time.time() - start_time) / 60
        print(f"✅ Comic created successfully in {execution_time:.2f} minutes!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating comic: {str(e)}")
        return False

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("📤 File upload received")
        f = request.files['file']
        
        # Clean up previous files
        from backend.utils import cleanup
        cleanup()
        
        # Save uploaded file
        f.save("video/uploaded.mp4")
        print(f"💾 Saved file: {f.filename}")
        
        # Create comic
        if create_comic_simple():
            copy_template()
            webbrowser.open('file:///' + os.getcwd() + '/output/page.html')
            return "✅ Comic created successfully! Check the output folder."
        else:
            return "❌ Error creating comic. Check console for details."

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print("🔗 Link received")
        link = request.form['link']
        
        # Clean up previous files
        from backend.utils import cleanup, download_video
        cleanup()
        
        # Download video
        download_video(link)
        print(f"⬇️ Downloaded video from: {link}")
        
        # Create comic
        if create_comic_simple():
            copy_template()
            webbrowser.open('file:///' + os.getcwd() + '/output/page.html')
            return "✅ Comic created successfully! Check the output folder."
        else:
            return "❌ Error creating comic. Check console for details."

if __name__ == '__main__':
    print("🎬 Cinecomic - Fast Mode")
    print("=" * 50)
    print("🚀 Starting Flask server...")
    print("📱 Open your browser to: http://127.0.0.1:5000")
    print("⚡ Optimized for speed - no complex models!")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)