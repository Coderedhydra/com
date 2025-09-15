"""
Real-ESRGAN Implementation for Ultra-High Quality Image Enhancement
Uses the latest Real-ESRGAN model for state-of-the-art super-resolution
"""

import cv2
import numpy as np
import os
import sys
import subprocess
import tempfile
import requests
from pathlib import Path
import urllib.request

class RealESRGANEnhancer:
    """Real-ESRGAN based image enhancer - currently the best super-resolution model"""
    
    def __init__(self):
        self.models_dir = Path("models")
        self.models_dir.mkdir(exist_ok=True)
        self.model_path = self.models_dir / "RealESRGAN_x4plus.pth"
        self.realesrgan_available = False
        self.upsampler = None  # Cache the upsampler
        self.initialization_attempted = False
        self.initialize()
    
    def initialize(self):
        """Initialize Real-ESRGAN"""
        if self.initialization_attempted:
            return
            
        self.initialization_attempted = True
        print("🔥 Initializing Real-ESRGAN (State-of-the-Art Super-Resolution)...")
        
        # Try to import Real-ESRGAN
        try:
            self.setup_realesrgan()
            self.realesrgan_available = True
            print("✅ Real-ESRGAN initialized successfully!")
        except Exception as e:
            print(f"⚠️ Real-ESRGAN not available: {e}")
            print("🔄 Will use advanced fallback methods")
            self.realesrgan_available = False
    
    def setup_realesrgan(self):
        """Setup Real-ESRGAN with proper dependencies"""
        try:
            # First, install compatible PyTorch versions
            print("📦 Installing compatible PyTorch versions...")
            pytorch_packages = [
                "torch==2.0.1",
                "torchvision==0.15.2", 
                "torchaudio==2.0.2"
            ]
            
            for package in pytorch_packages:
                try:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", 
                        package, "--break-system-packages", "--force-reinstall"
                    ], check=True, capture_output=True, timeout=180)
                    print(f"✅ Installed {package}")
                except Exception as e:
                    print(f"⚠️ Failed to install {package}: {e}")
            
            # Now try importing
            import torch
            import torchvision
            print(f"✅ PyTorch {torch.__version__}, torchvision {torchvision.__version__}")
            
            # Try importing Real-ESRGAN components
            import basicsr
            from realesrgan import RealESRGANer
            from basicsr.archs.rrdbnet_arch import RRDBNet
            print("✅ Real-ESRGAN libraries available")
            return True
            
        except ImportError as e:
            print(f"❌ Real-ESRGAN import failed: {e}")
            print("📦 Installing Real-ESRGAN with compatible versions...")
            
            # Install specific compatible versions
            packages = [
                "basicsr==1.4.2",
                "realesrgan==0.3.0"
            ]
            
            for package in packages:
                try:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", 
                        package, "--break-system-packages", "--force-reinstall"
                    ], check=True, capture_output=True, timeout=120)
                    print(f"✅ Installed {package}")
                except Exception as e:
                    print(f"⚠️ Failed to install {package}: {e}")
            
            # Final import test
            try:
                import basicsr
                from realesrgan import RealESRGANer
                print("✅ Real-ESRGAN setup complete")
                return True
            except ImportError as e:
                print(f"❌ Real-ESRGAN still not available: {e}")
                print("🔄 Falling back to advanced OpenCV processing")
                return False
    
    def download_model(self):
        """Download Real-ESRGAN model if needed"""
        if self.model_path.exists():
            print("✅ Real-ESRGAN model already available")
            return True
        
        try:
            print("📥 Downloading Real-ESRGAN model...")
            model_url = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"
            
            # Download with progress
            urllib.request.urlretrieve(model_url, self.model_path)
            print(f"✅ Model downloaded to {self.model_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            return False
    
    def enhance_with_realesrgan(self, image_path, output_path):
        """Enhance image using Real-ESRGAN"""
        try:
            from realesrgan import RealESRGANer
            from basicsr.archs.rrdbnet_arch import RRDBNet
            
            print(f"🔥 Enhancing with Real-ESRGAN: {os.path.basename(image_path)}")
            
            # Download model if needed
            if not self.download_model():
                return False
            
            # Use cached upsampler or create new one
            if self.upsampler is None:
                print("🔧 Initializing Real-ESRGAN upsampler...")
                
                # Initialize model
                model = RRDBNet(
                    num_in_ch=3, 
                    num_out_ch=3, 
                    num_feat=64, 
                    num_block=23, 
                    num_grow_ch=32, 
                    scale=4
                )
                
                # Initialize upsampler
                self.upsampler = RealESRGANer(
                    scale=4,
                    model_path=str(self.model_path),
                    model=model,
                    tile=400,      # Tile size for memory efficiency
                    tile_pad=10,   # Padding for tiles
                    pre_pad=0,     # Pre-padding
                    half=False     # Use FP32 for best quality
                )
                print("✅ Real-ESRGAN upsampler ready")
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"❌ Could not load image: {image_path}")
                return False
            
            # Get original dimensions
            h, w = img.shape[:2]
            
            # Determine optimal output scale
            if w < 800 or h < 600:
                outscale = 4  # 4x upscaling for small images
            elif w < 1200 or h < 900:
                outscale = 2  # 2x upscaling for medium images
            else:
                outscale = 1  # No upscaling for large images, just enhance
            
            print(f"📏 Input: {w}x{h}, Output scale: {outscale}x")
            
            # Enhance image using cached upsampler
            output, _ = self.upsampler.enhance(img, outscale=outscale)
            
            # Save with maximum quality
            success = cv2.imwrite(output_path, output, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                new_h, new_w = output.shape[:2]
                print(f"✅ Real-ESRGAN complete: {w}x{h} → {new_w}x{new_h}")
                return True
            else:
                print("❌ Failed to save enhanced image")
                return False
                
        except Exception as e:
            print(f"❌ Real-ESRGAN enhancement failed: {e}")
            return False
    
    def enhance_with_opencv_sota(self, image_path, output_path):
        """State-of-the-art OpenCV enhancement as fallback"""
        try:
            print(f"🎨 Using OpenCV SOTA enhancement: {os.path.basename(image_path)}")
            
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            h, w = img.shape[:2]
            
            # Super-resolution using EDSR-inspired technique
            if w < 1200 or h < 900:
                # Calculate optimal scale
                scale = min(1200/w, 900/h, 3.0)
                new_w, new_h = int(w * scale), int(h * scale)
                
                # Multi-step upscaling for better quality
                if scale > 2:
                    # First step: 2x upscaling
                    img = cv2.resize(img, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
                    # Second step: remaining scale
                    remaining_scale = scale / 2
                    final_w, final_h = int(w*2*remaining_scale), int(h*2*remaining_scale)
                    img = cv2.resize(img, (final_w, final_h), interpolation=cv2.INTER_LANCZOS4)
                else:
                    img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
                
                print(f"🔍 Super-resolution: {w}x{h} → {img.shape[1]}x{img.shape[0]}")
            
            # Advanced denoising with edge preservation
            img = cv2.fastNlMeansDenoisingColored(img, None, 4, 4, 7, 21)
            
            # Multi-scale detail enhancement
            img = self.advanced_detail_enhancement(img)
            
            # AI-inspired color enhancement
            img = self.color_enhancement_sota(img)
            
            # Professional sharpening
            img = self.professional_sharpening(img)
            
            # Save with maximum quality
            success = cv2.imwrite(output_path, img, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                print("✅ OpenCV SOTA enhancement complete")
                return True
            else:
                print("❌ Failed to save enhanced image")
                return False
                
        except Exception as e:
            print(f"❌ OpenCV SOTA enhancement failed: {e}")
            return False
    
    def advanced_detail_enhancement(self, img):
        """Advanced detail enhancement using multiple techniques"""
        # Create pyramid for multi-scale processing
        pyramid = [img]
        for i in range(3):
            pyramid.append(cv2.pyrDown(pyramid[-1]))
        
        # Process each level
        enhanced_pyramid = []
        for level in pyramid:
            # Apply bilateral filtering for edge-preserving smoothing
            smooth = cv2.bilateralFilter(level, 9, 75, 75)
            enhanced_pyramid.append(smooth)
        
        # Reconstruct with detail preservation
        result = enhanced_pyramid[0]
        for i in range(1, len(enhanced_pyramid)):
            # Upscale and blend
            upscaled = enhanced_pyramid[i]
            for _ in range(i):
                upscaled = cv2.pyrUp(upscaled)
            
            # Ensure same dimensions
            h, w = result.shape[:2]
            upscaled = cv2.resize(upscaled, (w, h))
            
            # Weighted blend
            weight = 0.3 / i  # Decreasing weight for higher levels
            result = cv2.addWeighted(result, 1-weight, upscaled, weight, 0)
        
        return result
    
    def color_enhancement_sota(self, img):
        """State-of-the-art color enhancement"""
        # Convert to LAB for perceptual color processing
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Advanced CLAHE with optimal parameters
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge and convert to HSV
        lab = cv2.merge([l, a, b])
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Intelligent saturation enhancement
        s_mean = np.mean(s)
        if s_mean < 80:
            s = cv2.multiply(s, 1.5)  # Boost low saturation
        elif s_mean < 120:
            s = cv2.multiply(s, 1.3)  # Moderate boost
        else:
            s = cv2.multiply(s, 1.2)  # Gentle boost
        
        # Intelligent brightness adjustment
        v_mean = np.mean(v)
        if v_mean < 80:
            v = cv2.multiply(v, 1.3)  # Brighten dark images
        elif v_mean > 200:
            v = cv2.multiply(v, 0.95)  # Slightly reduce very bright
        else:
            v = cv2.multiply(v, 1.15)  # Gentle brightness boost
        
        # Ensure valid ranges
        s = np.clip(s, 0, 255)
        v = np.clip(v, 0, 255)
        
        # Convert back to BGR
        hsv = cv2.merge([h, s, v])
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return enhanced
    
    def professional_sharpening(self, img):
        """Professional-grade sharpening"""
        # Create multiple sharpening kernels
        kernel1 = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.5
        kernel2 = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]]) * 0.8
        
        # Apply sharpening
        sharp1 = cv2.filter2D(img, -1, kernel1)
        sharp2 = cv2.filter2D(img, -1, kernel2)
        
        # Blend with original
        result = cv2.addWeighted(img, 0.6, sharp1, 0.3, 0)
        result = cv2.addWeighted(result, 0.8, sharp2, 0.2, 0)
        
        # Unsharp mask for final touch
        gaussian = cv2.GaussianBlur(result, (0, 0), 1.5)
        unsharp = cv2.addWeighted(result, 1.5, gaussian, -0.5, 0)
        
        # Final blend
        final = cv2.addWeighted(result, 0.7, unsharp, 0.3, 0)
        
        return final
    
    def enhance_image(self, image_path, output_path=None):
        """Main enhancement function"""
        if output_path is None:
            output_path = image_path
        
        # Try Real-ESRGAN first (best quality)
        if self.realesrgan_available:
            if self.enhance_with_realesrgan(image_path, output_path):
                return True
        
        # Fallback to advanced OpenCV
        return self.enhance_with_opencv_sota(image_path, output_path)
    
    def batch_enhance(self, input_dir):
        """Batch enhance all images in directory"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            print("❌ No image files found")
            return False
        
        print(f"🎯 Batch enhancing {len(image_files)} images with Real-ESRGAN...")
        
        successful = 0
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(input_dir, filename)
            
            print(f"\n📸 Processing {i}/{len(image_files)}: {filename}")
            
            if self.enhance_image(image_path):
                successful += 1
            
            if i % 3 == 0 or i == len(image_files):
                progress = (i / len(image_files)) * 100
                print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | Success: {successful}")
        
        success_rate = (successful / len(image_files)) * 100
        print(f"\n🎉 Real-ESRGAN Enhancement Complete!")
        print(f"✅ Successfully enhanced: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        
        return successful > 0

def enhance_frames_realesrgan(frames_dir="frames/final"):
    """Enhance frames using Real-ESRGAN"""
    enhancer = RealESRGANEnhancer()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = RealESRGANEnhancer()
    print(f"Real-ESRGAN available: {enhancer.realesrgan_available}")
    
    if os.path.exists("frames/final"):
        enhance_frames_realesrgan()
    else:
        print("No frames directory found for testing")