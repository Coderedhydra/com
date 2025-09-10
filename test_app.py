#!/usr/bin/env python3

import os
import sys

# Test if all imports work
try:
    from flask import Flask, render_template, request, jsonify, send_file
    print("✅ Flask imports successful")
except ImportError as e:
    print(f"❌ Flask import error: {e}")
    sys.exit(1)

try:
    from backend.cartoonize.cartoonize import style_frames, style_frames_fast
    print("✅ Cartoonize imports successful")
except ImportError as e:
    print(f"❌ Cartoonize import error: {e}")

try:
    from backend.subtitles.subs import get_subtitles
    from backend.keyframes.keyframes import generate_keyframes, black_bar_crop
    from backend.panel_layout.layout_gen import generate_layout
    from backend.speech_bubble.bubble import bubble_create
    from backend.page_create import page_create, page_json
    from backend.utils import cleanup, download_video, copy_template
    print("✅ All backend imports successful")
except ImportError as e:
    print(f"❌ Backend import error: {e}")

# Create test Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head><title>CineComic - Test</title></head>
    <body>
    <h1>🎬 CineComic Test Server</h1>
    <p>✅ Flask server is running!</p>
    <p><a href="/comic">Test Comic Viewer</a></p>
    <p><a href="/test">Test Route</a></p>
    </body>
    </html>
    '''

@app.route('/test')
def test():
    return jsonify({
        "status": "working",
        "message": "Test route is functional",
        "comic_files_exist": os.path.exists('static/comic'),
        "templates_exist": os.path.exists('templates')
    })

@app.route('/comic')
def comic():
    """Test comic page"""
    comic_data_path = os.path.join(os.getcwd(), 'static', 'comic', 'page.js')
    if os.path.exists(comic_data_path):
        try:
            return render_template('comic.html')
        except Exception as e:
            return f"Error loading comic template: {str(e)}"
    else:
        return f"Comic not found. Looking for: {comic_data_path}"

if __name__ == '__main__':
    print("🚀 Starting CineComic Test Server...")
    print("📍 Server will be available at: http://localhost:5000")
    print("🎯 Comic viewer will be at: http://localhost:5000/comic")
    
    # Check directories
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"📁 Static directory exists: {os.path.exists('static')}")
    print(f"📁 Templates directory exists: {os.path.exists('templates')}")
    
    app.run(debug=True, host='0.0.0.0', port=5000)