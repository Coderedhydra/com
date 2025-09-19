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

def create_template_fit_test_page():
    """Create test page using template fitting approach"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n" + "="*70)
    print("🎯 TEMPLATE FIT TEST PAGE - RESIZE AND FIT ALL IMAGES")
    print("="*70)
    print("Starting template fit test page generation...")
    print("This properly resizes and fits all images to template dimensions!")
    
    # Step 1-3: Basic processing
    print("\n📹 Step 1: Processing subtitles...")
    get_subtitles(video)
    time.sleep(1)
    
    print("📹 Step 2: Extracting keyframes...")
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    print("📹 Step 3: Starting template fitting...")
    
    # Import and use the template fit enhancer
    from backend.template_fit_enhancer import TemplateFitEnhancer
    
    print("🔧 Using template fit enhancer (resize and fit to template)...")
    enhancer = TemplateFitEnhancer()
    test_success = enhancer.create_template_fit_test_page()
    
    if test_success:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 Template fit test page completed!")
        print(f"✅ All images properly fitted to template!")
        print(f"--- Generation time: {total_time:.1f} seconds ---")
        return True
    else:
        print("❌ Template fit test page generation failed")
        return False

def create_full_template_fit_comic():
    """Create full 12-page comic with template fitting"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n🎯 Full 12-Page Template Fit Comic Generation")
    print("Starting full comic with proper template fitting...")
    
    # Basic processing
    get_subtitles(video)
    time.sleep(2)
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    # Full comic generation with template fitting
    from backend.template_fit_enhancer import create_full_template_fit_comic
    success = create_full_template_fit_comic()
    
    if success:
        copy_to_static()
        total_time = time.time() - start_time
        print(f"\n🎉 Full 12-page template fit comic completed!")
        print(f"🔧 All images properly fitted to template dimensions!")
        print(f"--- Execution time: {total_time:.1f} seconds ({total_time/60:.2f} minutes) ---")
        return True
    else:
        print("❌ Full template fit comic generation failed")
        return False

@app.route('/generate_full_comic', methods=['POST'])
def generate_full_comic():
    """Generate full 12-page comic with template fitting"""
    try:
        print("🚀 Generating full 12-page template fit comic...")
        success = create_full_template_fit_comic()
        if success:
            return jsonify({'status': 'success', 'message': 'Full template fit comic generated successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Full template fit comic generation failed'}), 500
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
        
        # Use the template fit enhancer
        success = create_template_fit_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🎯 Template Fit Test Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Images properly resized and fitted to template dimensions!</p>
            <p style="font-size: 14px; color: #7f8c8d;">Based on resize-and-fit-all-images-to-template approach for optimal quality!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #e74c3c; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Template Fit Test Page</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create template fit test page", 500

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print(dict(request.form))  
        link = request.form['link']
        cleanup()
        download_video(link)
        
        # Use the template fit enhancer
        success = create_template_fit_test_page()
        copy_template()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🎯 Template Fit Test Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">Images properly resized and fitted to template dimensions!</p>
            <p style="font-size: 14px; color: #7f8c8d;">Based on resize-and-fit-all-images-to-template approach for optimal quality!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #e74c3c; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Template Fit Test Page</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create template fit test page", 500

if __name__ == '__main__':
    print("🎯 Starting Template Fit Comic Flask application...")
    print("This version properly resizes and fits all images to template!")
    print("Based on resize-and-fit-all-images-to-template approach!")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)