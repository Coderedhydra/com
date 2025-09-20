#!/usr/bin/env python3
"""
Setup script for Text-to-Video Manim Generator
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    
    # Install requirements
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Install manim dependencies (might need system packages)
    print("🎬 Installing Manim...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "manim[dependencies]"])
    except:
        print("⚠️  Note: Some Manim dependencies might need to be installed separately")
        print("   On Ubuntu/Debian: sudo apt install ffmpeg")
        print("   On macOS: brew install ffmpeg")
    
    print("✅ Installation complete!")

def create_directories():
    """Create necessary directories."""
    os.makedirs("videos", exist_ok=True)
    os.makedirs("generated_code", exist_ok=True)
    print("📁 Created output directories")

def main():
    print("🎬 Setting up Text-to-Video Manim Generator...")
    print("=" * 50)
    
    create_directories()
    install_requirements()
    
    print("\n🎉 Setup complete!")
    print("\nTo use the generator:")
    print("  Interactive mode: python main.py -i")
    print("  Single generation: python main.py -t 'your description here'")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()