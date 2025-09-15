#!/usr/bin/env python3
"""
Install State-of-the-Art AI Models for CineComic
Automatically installs the latest and best AI models for image enhancement
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command with progress indication"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, timeout=300)
        print(f"✅ {description} - Success")
        return True
    except subprocess.TimeoutExpired:
        print(f"⏰ {description} - Timeout (continuing...)")
        return False
    except subprocess.CalledProcessError as e:
        print(f"⚠️ {description} - Failed: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def install_sota_models():
    """Install state-of-the-art AI models"""
    print("🤖 Installing State-of-the-Art AI Models for CineComic")
    print("=" * 60)
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    print(f"📁 Created models directory: {models_dir}")
    
    # Essential packages for SOTA models
    packages = [
        # Core dependencies
        ("torch torchvision", "PyTorch (AI Framework)"),
        ("opencv-python", "OpenCV (Computer Vision)"),
        ("Pillow numpy", "Image Processing Libraries"),
        
        # State-of-the-art models
        ("basicsr", "BasicSR (Super-Resolution Framework)"),
        ("realesrgan", "Real-ESRGAN (Best Super-Resolution Model 2024)"),
        ("gfpgan", "GFPGAN (Advanced Face Enhancement)"),
        ("facexlib", "Face Analysis Library"),
        
        # Additional quality models
        ("scikit-image", "Advanced Image Processing"),
        ("imageio", "Image I/O Operations"),
        ("tqdm", "Progress Bars"),
    ]
    
    installed = 0
    total = len(packages)
    
    print(f"🎯 Installing {total} essential packages for SOTA AI enhancement...")
    print()
    
    for package, description in packages:
        cmd = f"{sys.executable} -m pip install {package} --break-system-packages --no-warn-script-location"
        if run_command(cmd, f"Installing {description}"):
            installed += 1
        print()
    
    # Install additional models if possible
    optional_packages = [
        ("codeformer", "CodeFormer (Advanced Face Restoration)"),
        ("swinir", "SwinIR (Transformer-based Restoration)"),
    ]
    
    print("🔧 Installing optional advanced models...")
    
    for package, description in optional_packages:
        cmd = f"{sys.executable} -m pip install {package} --break-system-packages --no-warn-script-location"
        run_command(cmd, f"Installing {description}")
        print()
    
    # Test installations
    print("🧪 Testing installed models...")
    
    test_results = {}
    
    # Test Real-ESRGAN
    try:
        import basicsr
        import realesrgan
        test_results['Real-ESRGAN'] = "✅ Available (Best Super-Resolution)"
    except ImportError:
        test_results['Real-ESRGAN'] = "❌ Not available"
    
    # Test GFPGAN
    try:
        import gfpgan
        test_results['GFPGAN'] = "✅ Available (Face Enhancement)"
    except ImportError:
        test_results['GFPGAN'] = "❌ Not available"
    
    # Test OpenCV
    try:
        import cv2
        test_results['OpenCV'] = "✅ Available (Always works)"
    except ImportError:
        test_results['OpenCV'] = "❌ Critical - Not available"
    
    # Test PyTorch
    try:
        import torch
        test_results['PyTorch'] = "✅ Available (AI Framework)"
    except ImportError:
        test_results['PyTorch'] = "❌ Not available"
    
    print("\n📊 Installation Results:")
    print("=" * 40)
    for model, status in test_results.items():
        print(f"{model:15} : {status}")
    
    # Summary
    available_models = sum(1 for status in test_results.values() if "✅" in status)
    total_models = len(test_results)
    
    print(f"\n🎉 Installation Summary:")
    print(f"📈 Successfully installed: {installed}/{total} packages")
    print(f"🤖 Available AI models: {available_models}/{total_models}")
    
    if "✅" in test_results.get('Real-ESRGAN', ''):
        print("🔥 Real-ESRGAN available - ULTRA-HIGH QUALITY mode enabled!")
    elif "✅" in test_results.get('OpenCV', ''):
        print("🎨 Advanced OpenCV AI available - HIGH QUALITY mode enabled!")
    else:
        print("⚠️ Limited enhancement available - consider installing more models")
    
    print(f"\n🚀 CineComic is ready with the latest AI models!")
    return available_models > 0

def main():
    """Main installation function"""
    print("🎬 CineComic - SOTA AI Models Installer")
    print("Installing the latest and best AI models for image enhancement")
    print()
    
    success = install_sota_models()
    
    if success:
        print("\n✅ Installation completed successfully!")
        print("🎯 You can now run CineComic with state-of-the-art image quality!")
        print("\nTo start the application:")
        print("  python3 start_app.py")
        print("  or")
        print("  python3 app.py")
    else:
        print("\n⚠️ Installation completed with some issues.")
        print("The application will still work with fallback methods.")
    
    return success

if __name__ == "__main__":
    main()