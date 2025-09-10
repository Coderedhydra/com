import os
import webbrowser
import time
import subprocess
import base64

from flask import Flask, render_template, request, jsonify, send_file
from backend.subtitles.subs import get_subtitles
from backend.keyframes.keyframes import generate_keyframes, black_bar_crop
from backend.panel_layout.layout_gen import generate_layout
from backend.cartoonize.cartoonize import style_frames, style_frames_fast
from backend.speech_bubble.bubble import bubble_create
from backend.page_create import page_create,page_json
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

@app.route('/export_hq_png', methods=['POST'])
def export_hq_png():
    """Export high-quality PNG using server-side rendering"""
    try:
        data = request.get_json()
        page_number = data.get('page', 0)
        
        # Create a high-quality export using wkhtmltopdf/wkhtmltoimage
        # This is a server-side alternative that produces better quality
        
        # Generate the HTML content for the specific page
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="static/comic/page.css">
            <link rel="stylesheet" href="static/comic/bubble.css">
            <style>
                body {{ 
                    margin: 0; 
                    padding: 0; 
                    background: white;
                    width: 800px;
                    height: 1080px;
                }}
                .wrapper {{
                    border-radius: 0 !important;
                    box-shadow: none !important;
                }}
                .grid-item {{
                    image-rendering: -webkit-optimize-contrast;
                    image-rendering: crisp-edges;
                }}
            </style>
            <script src="static/comic/page.js"></script>
        </head>
        <body>
            <div class="wrapper">
                <div class="grid-container">
                    <div class="grid-item" id="_1"></div>
                    <div class="grid-item" id="_2"></div>
                </div>
            </div>
            <script>
                // Load specific page content
                if (typeof pages !== 'undefined' && pages[{page_number}]) {{
                    // Simplified version of placeDialogs for server-side rendering
                    const page = pages[{page_number}];
                    const gridItems = document.querySelectorAll('.grid-item');
                    
                    page.panels.forEach(function (panel, index) {{
                        if (gridItems[index]) {{
                            const gridItem = gridItems[index];
                            gridItem.style.backgroundImage = `url("static/comic/frames/final/${{panel.image}}.png")`;
                            
                            if (page.bubbles[index] && page.bubbles[index].dialog !== "((action-scene))") {{
                                const bubble = document.createElement('div');
                                bubble.className = 'bubble';
                                bubble.innerHTML = page.bubbles[index].dialog;
                                bubble.style.transform = `translate(${{page.bubbles[index].bubble_offset_x}}px, ${{page.bubbles[index].bubble_offset_y}}px)`;
                                gridItem.appendChild(bubble);
                            }}
                        }}
                    }});
                }}
            </script>
        </body>
        </html>
        '''
        
        # Save temporary HTML file
        temp_html_path = f'/tmp/comic_page_{page_number}.html'
        with open(temp_html_path, 'w') as f:
            f.write(html_content)
        
        # Use wkhtmltoimage for high-quality PNG export
        output_path = f'/tmp/comic_page_{page_number}_HQ.png'
        
        # Command for high-quality image generation
        cmd = [
            'wkhtmltoimage',
            '--width', '800',
            '--height', '1080',
            '--format', 'png',
            '--quality', '100',
            '--disable-smart-width',
            '--enable-local-file-access',
            temp_html_path,
            output_path
        ]
        
        # Try to run wkhtmltoimage
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Send the high-quality PNG file
            return send_file(output_path, as_attachment=True, download_name=f'comic_page_{page_number + 1}_HQ.png')
            
        except subprocess.CalledProcessError:
            # Fallback: Return JSON response for client-side processing
            return jsonify({
                'status': 'fallback',
                'message': 'Server-side rendering not available. Using client-side method.',
                'html_content': html_content
            })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_comic():
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    # FULL PROGRAM - All processing steps enabled
    print("Starting optimized comic generation...")
    get_subtitles(video)
    time.sleep(3)
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    crop_coords, page_templates, panels = generate_layout()
    bubbles = bubble_create(video, crop_coords, black_x, black_y)
    pages  = page_create(page_templates,panels,bubbles)
    page_json(pages)
    
    # Use optimized parallel styling for faster processing
    print("Step 6: Styling frames with optimized parallel processing...")
    style_frames()
    
    # Copy to static directory for Flask serving
    copy_to_static()
    
    total_time = time.time() - start_time
    print(f"Full comic generation completed successfully!")
    print(f"Generated {len(pages) if 'pages' in locals() else 'unknown'} comic pages from video!")
    print(f"--- Execution time : {total_time:.1f} seconds ({total_time/60:.2f} minutes) ---")

def create_comic_fast():
    """Ultra-fast comic generation - minimal styling"""
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    print("Starting FAST comic generation (minimal styling)...")
    get_subtitles(video)
    time.sleep(1)  # Reduced wait time
    generate_keyframes(video)
    black_x, black_y, _, _ = black_bar_crop()
    crop_coords, page_templates, panels = generate_layout()
    bubbles = bubble_create(video, crop_coords, black_x, black_y)
    pages  = page_create(page_templates,panels,bubbles)
    page_json(pages)
    
    # Skip styling entirely for maximum speed
    print("Step 6: Skipping frame styling for maximum speed...")
    print("Using original frames without cartoon styling")
    
    # Copy to static directory for Flask serving
    copy_to_static()
    
    total_time = time.time() - start_time
    print(f"FAST comic generation completed!")
    print(f"Generated {len(pages) if 'pages' in locals() else 'unknown'} comic pages from video!")
    print(f"--- Execution time : {total_time:.1f} seconds ({total_time/60:.2f} minutes) ---")

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(dict(request.form))  
        f = request.files['file']  #we got the file as file storage object from frontend
        print(type(f))
        cleanup()
        f.save("video/uploaded.mp4")
        create_comic()
        copy_template()
        webbrowser.open('file:///'+os.getcwd()+'/' + 'output/page.html')
        return "Comic created Successfully"
    

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print(dict(request.form))  
        link = request.form['link']
        cleanup()
        download_video(link)
        create_comic()
        copy_template()
        webbrowser.open('file:///'+os.getcwd()+'/' + 'output/page.html')
        return "Comic created Successfully"
    

if __name__ == '__main__':
    print("Starting CineComic Flask application...")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
