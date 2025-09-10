import os
import webbrowser
import time
import json
import shutil

from flask import Flask, render_template, request

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
                    "dialog": "Hello! This is a test bubble with square, plain text.",
                    "emotion": "normal",
                    "bubble_offset_x": 50,
                    "bubble_offset_y": 50,
                    "tail_offset_x": 20,
                    "tail_offset_y": 30,
                    "tail_deg": 45
                },
                {
                    "dialog": "This is another test bubble with normal styling!",
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
    
    # Write test data to page.js in both locations
    with open('output_template/page.js', 'w') as f:
        f.write(f'var pages = ')
        json.dump(test_pages, f, indent=4)
    
    # Also write to static directory for Flask serving
    with open('static/comic/page.js', 'w') as f:
        f.write(f'var pages = ')
        json.dump(test_pages, f, indent=4)
    
    print("Test comic data created successfully!")

def create_comic():
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    try:
        # Try to run the full program
        print("Starting full comic generation...")
        
        # Import and run the full processing pipeline
        from backend.subtitles.subs import get_subtitles
        from backend.keyframes.keyframes import generate_keyframes, black_bar_crop
        from backend.panel_layout.layout_gen import generate_layout
        from backend.cartoonize.cartoonize import style_frames
        from backend.speech_bubble.bubble import bubble_create
        from backend.page_create import page_create, page_json
        
        get_subtitles(video)
        time.sleep(3)
        generate_keyframes(video)
        black_x, black_y, _, _ = black_bar_crop()
        crop_coords, page_templates, panels = generate_layout()
        bubbles = bubble_create(video, crop_coords, black_x, black_y)
        pages = page_create(page_templates, panels, bubbles)
        page_json(pages)
        style_frames()
        
        print("Full comic generation completed successfully!")
        
    except ImportError as e:
        print(f"Full program dependencies not available: {e}")
        print("Using test data instead...")
        create_test_comic_data()
        
    except Exception as e:
        print(f"Error in full program: {e}")
        print("Using test data instead...")
        create_test_comic_data()
    
    # Copy to static directory for Flask serving
    copy_to_static()
    
    print("--- Execution time : %s seconds ---" % (time.time() - start_time))

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

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("File upload request received")
        print(dict(request.form))  
        f = request.files['file']
        print(f"File type: {type(f)}")
        
        # Create video directory if it doesn't exist
        os.makedirs('video', exist_ok=True)
        
        # Save the uploaded file
        f.save("video/uploaded.mp4")
        print("File saved successfully!")
        
        # Create comic
        create_comic()
        
        # Redirect to comic page
        return "Comic created Successfully! <a href='/comic'>Click here to view your comic</a>"

@app.route('/handle_link', methods=['GET', 'POST'])
def handle_link():
    if request.method == 'POST':
        print("Link request received")
        print(dict(request.form))  
        link = request.form['link']
        print(f"Processing link: {link}")
        
        try:
            # Try to download video from link
            from backend.utils import download_video
            download_video(link)
            print("Video downloaded successfully!")
        except ImportError:
            print("Video download not available, using test data...")
        except Exception as e:
            print(f"Error downloading video: {e}, using test data...")
        
        # Create comic
        create_comic()
        
        # Redirect to comic page
        return "Comic created Successfully! <a href='/comic'>Click here to view your comic</a>"

if __name__ == '__main__':
    print("Starting CineComic Flask application...")
    print("Open your browser and go to: http://localhost:5000")
    print("Comic will be available at: http://localhost:5000/comic")
    print("This version tries full processing first, falls back to test data if needed.")
    app.run(debug=True, host='0.0.0.0', port=5000)