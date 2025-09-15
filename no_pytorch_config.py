
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
