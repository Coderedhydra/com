import os
import webbrowser
import time

from flask import Flask, render_template,request
from backend.subtitles.subs import get_subtitles
from backend.keyframes.keyframes import generate_keyframes, black_bar_crop
from backend.panel_layout.layout_gen import generate_layout
from backend.cartoonize.cartoonize import style_frames
from backend.speech_bubble.bubble import bubble_create
from backend.page_create import page_create,page_json
from backend.utils import cleanup, download_video
from backend.utils import copy_template
import json

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

@app.route('/')
def index():
    return render_template('index.html')


def create_comic():
    start_time = time.time()
    video = 'video/uploaded.mp4'
    
    # COMMENTED OUT FOR TESTING - Heavy processing steps
    # get_subtitles(video)
    # time.sleep(3)
    # generate_keyframes(video)
    # black_x, black_y, _, _ = black_bar_crop()
    # crop_coords, page_templates, panels = generate_layout()
    # bubbles = bubble_create(video, crop_coords, black_x, black_y)
    # pages  = page_create(page_templates,panels,bubbles)
    # page_json(pages)
    # style_frames()
    
    # SIMPLIFIED FOR TESTING - Create basic test data
    print("Creating test comic data...")
    create_test_comic_data()
    
    print("--- Execution time : %s minutes ---" % ((time.time() - start_time) / 60))

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
    


