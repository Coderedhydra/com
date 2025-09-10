import os
import webbrowser
import time
import json

from flask import Flask, render_template, request

app = Flask(__name__)

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

def copy_template():
    """Copy template files to output directory"""
    import shutil
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Copy all files from output_template to output
    if os.path.exists('output_template'):
        for item in os.listdir('output_template'):
            src = os.path.join('output_template', item)
            dst = os.path.join('output', item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)
        print("Template files copied to output directory!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comic')
def comic():
    """Serve the comic page directly"""
    comic_path = os.path.join(os.getcwd(), 'output', 'page.html')
    if os.path.exists(comic_path):
        with open(comic_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    else:
        return "Comic not found. Please generate a comic first.", 404

def create_comic():
    start_time = time.time()
    print("Creating test comic data...")
    create_test_comic_data()
    copy_template()
    print("--- Execution time : %s seconds ---" % (time.time() - start_time))

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
        
        # For testing, just create a test comic
        create_comic()
        
        # Redirect to comic page
        return "Comic created Successfully! <a href='/comic'>Click here to view your comic</a>"

if __name__ == '__main__':
    print("Starting CineComic Flask application...")
    print("Open your browser and go to: http://localhost:5000")
    print("Comic will be available at: http://localhost:5000/comic")
    print("This is a simplified version for testing the UI functionality.")
    app.run(debug=True, host='0.0.0.0', port=5000)