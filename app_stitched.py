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
    stitched_path = os.path.join(os.getcwd(), 'static', 'stitched_comic_page.png')
    if os.path.exists(stitched_path):
        return f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Stitched Comic Page</title>
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
                    border: 2px solid #333;
                    border-radius: 8px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }}
                .buttons {{
                    margin-top: 20px;
                }}
                .button {{
                    margin: 0 10px;
                    padding: 10px 20px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    text-decoration: none;
                    display: inline-block;
                }}
                .button:hover {{
                    background: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div class="comic-container">
                <h2>🔲 Stitched Comic Page</h2>
                <p>4 panels combined into single square image with bubbles</p>
                <img src="/static/stitched_comic_page.png" alt="Stitched Comic Page" class="comic-image">
                <div class="buttons">
                    <a href="/download_stitched" class="button">Download Image</a>
                    <button onclick="generateFullStitched()" class="button">Generate 12 Stitched Pages</button>
                </div>
            </div>
            
            <script>
            function generateFullStitched() {{
                if (confirm('Generate 12 stitched comic pages?\\n\\nThis will create 12 separate image files.')) {{
                    fetch('/generate_full_stitched', {{
                        method: 'POST'
                    }})
                    .then(response => response.json())
                    .then(data => {{
                        if (data.status === 'success') {{
                            alert('✅ 12 stitched pages generated successfully!\\nCheck the static folder for all images.');
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
        return "Stitched comic not found. Please generate a comic first.", 404

@app.route('/download_stitched')
def download_stitched():
    """Download the stitched comic image"""
    stitched_path = os.path.join(os.getcwd(), 'static', 'stitched_comic_page.png')
    if os.path.exists(stitched_path):
        return send_file(stitched_path, as_attachment=True, download_name='comic_page_stitched.png')
    else:
        return "Stitched image not found", 404

def create_stitched_test_page():
    """Create stitched test page - no HTML template"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n" + "="*70)
    print("🔲 STITCHED COMIC PAGE - NO HTML TEMPLATE")
    print("="*70)
    print("Creating single image with 4 panels + bubbles stitched together!")
    
    # Step 1-3: Basic processing
    print("\n📹 Step 1: Processing subtitles...")
    get_subtitles(video)
    time.sleep(1)
    
    print("📹 Step 2: Extracting keyframes...")
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    print("📹 Step 3: Enhancing frames with professional quality...")
    
    # Use professional enhancer first
    from backend.professional_comic_enhancer import ProfessionalComicEnhancer
    enhancer = ProfessionalComicEnhancer()
    test_success = enhancer.create_professional_comic_test_page()
    
    if not test_success:
        print("❌ Failed to create enhanced frames")
        return False
    
    # Step 4: Stitch panels into single image
    print("\n🔲 Step 4: Stitching panels into single image...")
    
    from backend.image_stitcher import ImageStitcher
    stitcher = ImageStitcher()
    
    # Create stitched image
    stitch_success = stitcher.stitch_comic_page("static/stitched_comic_page.png")
    
    if stitch_success:
        total_time = time.time() - start_time
        print(f"\n🎉 Stitched comic page completed!")
        print(f"✅ Single image with 4 panels + bubbles!")
        print(f"🔲 No HTML template needed!")
        print(f"--- Generation time: {total_time:.1f} seconds ---")
        return True
    else:
        print("❌ Stitching failed")
        return False

def create_full_stitched_comic():
    """Create full 12 stitched comic pages"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("\n🔲 Full 12 Stitched Comic Pages Generation")
    print("Creating 12 separate stitched image files...")
    
    # Basic processing
    get_subtitles(video)
    time.sleep(2)
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    
    # Create full comic with professional enhancement
    from backend.professional_comic_enhancer import ProfessionalComicEnhancer
    enhancer = ProfessionalComicEnhancer()
    
    # Generate full comic data first
    frames_dir = "frames/final"
    frame_files = [f for f in os.listdir(frames_dir) 
                  if f.lower().endswith('.png') and f.startswith('frame')]
    frame_files.sort()
    
    if not frame_files:
        print("❌ No frames found")
        return False
    
    # Process frames professionally
    processed_count = 0
    panels_needed = 48  # 12 pages × 4 panels
    
    if len(frame_files) >= panels_needed:
        step = len(frame_files) // panels_needed
        selected_frames = [frame_files[i * step] for i in range(panels_needed)]
    else:
        selected_frames = frame_files.copy()
        while len(selected_frames) < panels_needed:
            selected_frames.extend(frame_files)
        selected_frames = selected_frames[:panels_needed]
    
    # Enhance all frames
    for i, frame_file in enumerate(selected_frames, 1):
        frame_path = os.path.join('frames/final', frame_file)
        if os.path.exists(frame_path):
            if enhancer.process_frame_professional(frame_path):
                processed_count += 1
    
    # Create 12 stitched pages
    from backend.image_stitcher import ImageStitcher
    stitcher = ImageStitcher()
    
    stitched_count = 0
    for page_num in range(12):
        # Create page data for this page
        start_idx = page_num * 4
        end_idx = start_idx + 4
        page_frames = selected_frames[start_idx:end_idx]
        
        if len(page_frames) == 4:
            # Create temporary page data
            page_data = {
                "panels": [{"image": frame.replace('.png', '')} for frame in page_frames],
                "bubbles": [
                    {"dialog": f"Page {page_num+1} Panel 1", "bubble_offset_x": 50, "bubble_offset_y": 50},
                    {"dialog": f"Page {page_num+1} Panel 2", "bubble_offset_x": 50, "bubble_offset_y": 50},
                    {"dialog": f"Page {page_num+1} Panel 3", "bubble_offset_x": 50, "bubble_offset_y": 50},
                    {"dialog": f"Page {page_num+1} Panel 4", "bubble_offset_x": 50, "bubble_offset_y": 50}
                ]
            }
            
            # Save temporary page data
            with open('output_template/page.js', 'w') as f:
                f.write('var pages = ')
                json.dump([page_data], f, indent=4)
            
            with open('static/comic/page.js', 'w') as f:
                f.write('var pages = ')
                json.dump([page_data], f, indent=4)
            
            # Copy frames to static
            for frame in page_frames:
                src = os.path.join('frames/final', frame)
                dst = os.path.join('static/comic/frames/final', frame)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
            
            # Stitch this page
            output_file = f"static/stitched_comic_page_{page_num+1:02d}.png"
            if stitcher.stitch_comic_page(output_file):
                stitched_count += 1
                print(f"✅ Created page {page_num+1}: {output_file}")
    
    total_time = time.time() - start_time
    
    if stitched_count > 0:
        print(f"\n🎉 Full stitched comic completed!")
        print(f"🔲 Created {stitched_count} stitched image files")
        print(f"📁 Files saved in static/ folder")
        print(f"--- Execution time: {total_time:.1f} seconds ({total_time/60:.2f} minutes) ---")
        return True
    else:
        print("❌ No stitched pages created")
        return False

@app.route('/generate_full_stitched', methods=['POST'])
def generate_full_stitched():
    """Generate full 12 stitched comic pages"""
    try:
        print("🚀 Generating 12 stitched comic pages...")
        success = create_full_stitched_comic()
        if success:
            return jsonify({'status': 'success', 'message': 'Full stitched comic generated successfully!'})
        else:
            return jsonify({'status': 'error', 'message': 'Stitched comic generation failed'}), 500
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
        
        # Create stitched comic page
        success = create_stitched_test_page()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🔲 Stitched Comic Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">4 panels + bubbles combined into single square image!</p>
            <p style="font-size: 14px; color: #7f8c8d;">No HTML template - direct image with perfect quality!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Stitched Comic</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create stitched comic page", 500

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print(dict(request.form))  
        link = request.form['link']
        cleanup()
        download_video(link)
        
        # Create stitched comic page
        success = create_stitched_test_page()
        
        if success:
            return '''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f0f0f0;">
            <h2 style="color: #2c3e50;">🔲 Stitched Comic Page Created!</h2>
            <p style="font-size: 16px; margin: 20px 0;">4 panels + bubbles combined into single square image!</p>
            <p style="font-size: 14px; color: #7f8c8d;">No HTML template - direct image with perfect quality!</p>
            <a href="/comic" target="_blank" style="display: inline-block; padding: 12px 24px; background: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px;">View Stitched Comic</a>
            <script>
            setTimeout(function() {
                window.open('/comic', '_blank');
            }, 1000);
            </script>
            </body>
            </html>
            '''
        else:
            return "Failed to create stitched comic page", 500

if __name__ == '__main__':
    print("🔲 Starting Stitched Comic Flask application...")
    print("Creates single image with 4 panels + bubbles - no HTML template!")
    print("Perfect square with 4 equal parts!")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)