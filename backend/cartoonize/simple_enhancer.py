"""
Simple but High-Quality Image Enhancer
Reliable fallback when Real-ESRGAN fails
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter

class SimpleHighQualityEnhancer:
    """Simple but effective image enhancer that always works"""
    
    def __init__(self):
        self.name = "Simple High-Quality Enhancer"
        print(f"🎨 Initialized {self.name}")
    
    def enhance_image(self, image_path, output_path=None):
        """Enhance image with reliable, high-quality processing"""
        if output_path is None:
            output_path = image_path
            
        try:
            print(f"🎨 Enhancing with {self.name}: {os.path.basename(image_path)}")
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"❌ Could not load image: {image_path}")
                return False
            
            h, w = img.shape[:2]
            
            # Step 1: Smart upscaling if needed
            if w < 1200 or h < 900:
                scale = min(1200/w, 900/h, 2.5)  # Cap at 2.5x
                new_w, new_h = int(w * scale), int(h * scale)
                
                # Use LANCZOS for best quality upscaling
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
                print(f"📈 Upscaled: {w}x{h} → {new_w}x{new_h} ({scale:.1f}x)")
            
            # Step 2: Advanced noise reduction
            img = cv2.fastNlMeansDenoisingColored(img, None, 4, 4, 7, 21)
            
            # Step 3: Multi-scale bilateral filtering for smoothing
            smooth1 = cv2.bilateralFilter(img, 9, 75, 75)
            smooth2 = cv2.bilateralFilter(smooth1, 7, 50, 50)
            img = cv2.addWeighted(smooth1, 0.7, smooth2, 0.3, 0)
            
            # Step 4: Enhanced color processing
            img = self.enhance_colors(img)
            
            # Step 5: Professional sharpening
            img = self.sharpen_image(img)
            
            # Step 6: Final quality optimization
            img = self.final_optimization(img)
            
            # Save with maximum quality
            success = cv2.imwrite(output_path, img, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                final_h, final_w = img.shape[:2]
                print(f"✅ Enhancement complete: {final_w}x{final_h}")
                return True
            else:
                print("❌ Failed to save enhanced image")
                return False
                
        except Exception as e:
            print(f"❌ Enhancement failed: {e}")
            return False
    
    def enhance_colors(self, img):
        """Enhanced color processing"""
        # Convert to LAB for better color manipulation
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge back and convert to HSV
        lab = cv2.merge([l, a, b])
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Smart saturation enhancement
        s_mean = np.mean(s)
        if s_mean < 100:
            s = cv2.multiply(s, 1.4)  # Boost low saturation
        else:
            s = cv2.multiply(s, 1.2)  # Gentle boost
        
        # Smart brightness adjustment
        v_mean = np.mean(v)
        if v_mean < 100:
            v = cv2.multiply(v, 1.2)  # Brighten dark images
        elif v_mean > 200:
            v = cv2.multiply(v, 0.95)  # Slightly reduce very bright
        else:
            v = cv2.multiply(v, 1.1)   # Gentle brightness boost
        
        # Ensure valid ranges
        s = np.clip(s, 0, 255)
        v = np.clip(v, 0, 255)
        
        # Convert back
        hsv = cv2.merge([h, s, v])
        enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return enhanced
    
    def sharpen_image(self, img):
        """Professional sharpening"""
        # Create unsharp mask
        gaussian = cv2.GaussianBlur(img, (0, 0), 1.5)
        unsharp = cv2.addWeighted(img, 1.5, gaussian, -0.5, 0)
        
        # Additional edge enhancement
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.15
        sharpened = cv2.filter2D(img, -1, kernel)
        
        # Blend for natural result
        result = cv2.addWeighted(img, 0.6, unsharp, 0.3, 0)
        result = cv2.addWeighted(result, 0.85, sharpened, 0.15, 0)
        
        return result
    
    def final_optimization(self, img):
        """Final quality optimization"""
        # Convert to float for precision
        img_float = img.astype(np.float32) / 255.0
        
        # Gentle gamma correction
        gamma = 1.05
        img_float = np.power(img_float, 1.0/gamma)
        
        # Convert back
        img = (img_float * 255).astype(np.uint8)
        
        # Final light denoising
        img = cv2.bilateralFilter(img, 3, 30, 30)
        
        return img
    
    def batch_enhance(self, input_dir):
        """Batch enhance all images in directory"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            print("❌ No image files found")
            return False
        
        print(f"🎯 Batch enhancing {len(image_files)} images with {self.name}...")
        
        successful = 0
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(input_dir, filename)
            
            print(f"\n📸 Processing {i}/{len(image_files)}: {filename}")
            
            if self.enhance_image(image_path):
                successful += 1
            
            if i % 10 == 0 or i == len(image_files):
                progress = (i / len(image_files)) * 100
                print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | Success: {successful}")
        
        success_rate = (successful / len(image_files)) * 100
        print(f"\n🎉 Simple Enhancement Complete!")
        print(f"✅ Successfully enhanced: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        
        return successful > 0

def enhance_frames_simple(frames_dir="frames/final"):
    """Simple but reliable enhancement for all frames"""
    enhancer = SimpleHighQualityEnhancer()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = SimpleHighQualityEnhancer()
    
    if os.path.exists("frames/final"):
        enhance_frames_simple()
    else:
        print("No frames directory found for testing")