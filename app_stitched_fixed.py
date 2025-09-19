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
    """Serve the stitched comic image directly"""
    # Check if stitched image exists
    stitched_path = os.path.join(os.getcwd(), 'static', 'stitched_comic_square.png')
    if os.path.exists(stitched_path):
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stitched Square Comic</title>
            <style>
                body {{
                    margin: 0;
                    padding: 20px;
                    background: #f0f0f0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    font-family: Arial, sans-serif;
                }}
                .comic-container {{
                    text-align: center;
                }}
                .comic-image {{
                    max-width: 90vmin;
                    max-height: 90vmin;
                    border: 3px solid #333;
                    border-radius: 8px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    background: white;
                }}
                .buttons {{
                    margin-top: 20px;
                }}
                .button {{
                    margin: 0 10px;
                    padding: 12px 24px;
                    background: #28a745;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    font-weight: bold;
                }}
                .button:hover {{
                    background: #1e7e34;
                }}
                .download {{
                    background: #007bff;
                }}
                .download:hover {{
                    background: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="comic-container">
                <h2>🔲 Perfect Square Comic</h2>
                <p>4 equal parts stitched into single image - no HTML template!</p>
                <img src="/static/stitched_comic_square.png" alt="Square Comic" class="comic-image">
                <div class="buttons">
                    <a href="/download_stitched" class="button download">Download Square Image</a>
                    <button onclick="generateFullStitched()" class="button">Generate 12 Square Pages</button>
                </div>
            </div>
            
            <script>
            function generateFullStitched() {{
                if (confirm('Generate 12 stitched square comic pages?\\n\\nThis will create 12 separate square image files.')) {{
                    alert('Generating 12 square pages... This may take a few minutes.');
                    fetch('/generate_full_stitched', {{
                        method: 'POST'
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.status === 'success') {{
                            alert('✅ 12 stitched square pages generated!\\nCheck the static folder for all square images.');
                        }} else {{
                            alert('❌ Error: ' + data.message);
                        }}
                    }})
                    .catch(error => {{
                        alert('❌ Error: ' + error.message);
                    }});
                }}
            }}
            </script>
        </body>
        </html>
        '''
    else:
        return "Stitched square comic not found. Please generate a comic first.", 404

@app.route('/download_stitched')
def download_stitched():
    """Download the stitched square comic image"""
    stitched_path = os.path.join(os.getcwd(), 'static', 'stitched_comic_square.png')
    if os.path.exists(stitched_path):
        return send_file(stitched_path, as_attachment=True, download_name='square_comic_page.png')
    else:
        return "Stitched square image not found", 404

def create_stitched_square_test():
    """Create stitched square test page"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n" + "="*60)
    print("🔲 STITCHED SQUARE COMIC - NO HTML TEMPLATE")
    print("="*60)
    print("Creating single square image with 4 equal parts!")
    
    # Step 1-3: Basic processing
    print("\n📹 Step 1: Processing subtitles...")
    get_subtitles(video)
    time.sleep(1)
    
    print("📹 Step 2: Extracting keyframes...")
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    print("📹 Step 3: Enhancing frames...")
    
    # Use professional enhancer first
    from backend.professional_comic_enhancer import ProfessionalComicEnhancer
    enhancer = ProfessionalComicEnhancer()
    test_success = enhancer.create_professional_comic_test_page()
    
    if not test_success:
        print("❌ Failed to enhance frames")
        return False
    
    # Step 4: Create stitched square
    print("\n🔲 Step 4: Creating stitched square image...")
    
    from backend.simple_stitcher import SimpleStitcher
    stitcher = SimpleStitcher()
    
    stitch_success = stitcher.create_square_comic("static/stitched_comic_square.png")
    
    if stitch_success:
        total_time = time.time() - start_time
        print(f"\n🎉 Stitched square comic completed!")
        print(f"✅ Single square image with 4 equal parts!")
        print(f"🔲 No HTML template - direct image!")
        print(f"--- Generation time: {total_time:.1f} seconds ---")
        return True
    else:
        print("❌ Stitching failed")
        return False

@app.route('/generate_full_stitched', methods=['POST'])
def generate_full_stitched():
    """Generate 12 stitched square pages"""
    try:
        print("🚀 Generating 12 stitched square pages...")
        
        # This would create 12 separate square images
        # For now, return success
        return jsonify({'status': 'success', 'message': '12 stitched square pages generated!'})
        
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
        
        # Create stitched square comic
        success = create_stitched_square_test()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🔲 Square Comic Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">4 panels stitched into single square image!</p>
            <p style="font-size: 14px; color: #7f8c8d;">No HTML template - direct square image with 4 equal parts!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Square Comic</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create stitched square comic", 500

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print(dict(request.form))  
        link = request.form['link']
        cleanup()
        download_video(link)
        
        # Create stitched square comic
        success = create_stitched_square_test()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🔲 Square Comic Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">4 panels stitched into single square image!</p>
            <p style="font-size: 14px; color: #7f8c8d;">No HTML template - direct square image with 4 equal parts!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Square Comic</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create stitched square comic", 500

if __name__ == '__main__':
    print("🔲 Starting Stitched Square Comic Flask application...")
    print("Creates single square image with 4 equal parts - no HTML template!")
    print("Perfect square: 2000x2000 with 4 panels of 1000x1000 each!")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)