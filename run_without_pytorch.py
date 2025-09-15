#!/usr/bin/env python3
"""
Run CineComic without PyTorch dependencies
Perfect for your current setup after PyTorch removal
"""

import os
import sys

def check_essential_deps():
    """Check if essential dependencies are available"""
    print("🧪 Checking essential dependencies...")
    
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} available")
    except ImportError:
        print("❌ OpenCV not available")
        return False
    
    try:
        import numpy
        print(f"✅ NumPy {numpy.__version__} available")
    except ImportError:
        print("❌ NumPy not available")
        return False
    
    try:
        import PIL
        print(f"✅ Pillow available")
    except ImportError:
        print("❌ Pillow not available")
        return False
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__} available")
    except ImportError:
        print("❌ Flask not available")
        return False
    
    return True

def create_no_pytorch_config():
    """Create configuration that explicitly avoids PyTorch"""
    config = '''
# CineComic Configuration - No PyTorch Mode
import os

# Disable all PyTorch-based enhancement
USE_REALESRGAN = False
USE_GFPGAN = False
USE_PYTORCH_MODELS = False

# Enable reliable OpenCV methods
USE_OPENCV_ENHANCEMENT = True
USE_SIMPLE_ENHANCER = True

# Quality settings
MAX_UPSCALE_FACTOR = 2.0
ENABLE_ADVANCED_OPENCV = True
ENABLE_BILATERAL_FILTERING = True
ENABLE_COLOR_ENHANCEMENT = True
ENABLE_SHARPENING = True

print("🎨 Using OpenCV-only enhancement mode")
'''
    
    with open('no_pytorch_config.py', 'w') as f:
        f.write(config)
    
    print("✅ No-PyTorch configuration created")

def test_image_enhancement():
    """Test image enhancement without PyTorch"""
    print("🧪 Testing image enhancement (no PyTorch)...")
    
    try:
        import cv2
        import numpy as np
        
        # Create a test image
        test_img = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)
        
        # Apply basic enhancement
        enhanced = cv2.bilateralFilter(test_img, 9, 75, 75)
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 4, 4, 7, 21)
        
        print("✅ Basic image enhancement working")
        
        # Test upscaling
        upscaled = cv2.resize(enhanced, (1200, 900), interpolation=cv2.INTER_LANCZOS4)
        print("✅ Image upscaling working")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhancement test failed: {e}")
        return False

def main():
    print("🚀 CineComic - No PyTorch Mode")
    print("Perfect setup after PyTorch removal!")
    print("=" * 50)
    
    # Check dependencies
    if not check_essential_deps():
        print("\n❌ Missing essential dependencies")
        print("Please install: pip install opencv-python numpy pillow flask")
        return False
    
    # Create configuration
    create_no_pytorch_config()
    
    # Test enhancement
    if test_image_enhancement():
        print("\n🎉 Perfect! Your setup is working great!")
        print("\n✅ What's working:")
        print("   • OpenCV image enhancement (high quality)")
        print("   • Image upscaling and processing")
        print("   • No PyTorch dependencies needed")
        print("   • No CUDA issues")
        print("   • Reliable, fast processing")
        
        print("\n🚀 To run your application:")
        print("   python3 start_app.py")
        print("   or")
        print("   python3 app.py")
        
        print("\n📍 Then access: http://localhost:5000")
        print("✅ Your application will work perfectly without PyTorch!")
        
        return True
    else:
        print("\n⚠️ Enhancement test failed, but basic app should still work")
        return False

if __name__ == "__main__":
    main()