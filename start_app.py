#!/usr/bin/env python3
"""
CineComic Application Launcher
Automatically detects and runs the best version of the application
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if essential dependencies are available"""
    try:
        import flask
        import cv2
        import numpy
        import PIL
        print("✅ All essential dependencies available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing essential dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_essential.txt", "--break-system-packages"], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("⚠️ Could not install dependencies automatically")
            return False

def main():
    print("🎬 CineComic Application Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install dependencies manually:")
        print("pip3 install -r requirements_essential.txt --break-system-packages")
        return
    
    # Check which app version to run
    if os.path.exists("app.py"):
        print("🚀 Starting full-featured CineComic application...")
        print("📍 Access at: http://localhost:5000")
        print("🔧 Features: Full video processing + AI enhancement")
        print("\nStarting server...")
        
        try:
            # Import and run the main app
            sys.path.insert(0, os.getcwd())
            from app import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"❌ Error starting main app: {e}")
            print("Trying simplified version...")
            
            if os.path.exists("app_simple.py"):
                from app_simple import app
                app.run(debug=True, host='0.0.0.0', port=5000)
    
    elif os.path.exists("app_simple.py"):
        print("🚀 Starting simplified CineComic application...")
        print("📍 Access at: http://localhost:5000")
        print("🔧 Features: Basic functionality for testing")
        print("\nStarting server...")
        
        try:
            sys.path.insert(0, os.getcwd())
            from app_simple import app
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e:
            print(f"❌ Error starting app: {e}")
    
    else:
        print("❌ No application file found!")
        print("Please ensure app.py or app_simple.py exists in the current directory.")

if __name__ == "__main__":
    main()