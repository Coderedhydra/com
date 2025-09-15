"""
No-Gaps Quality Enhancer
Ensures images always fill panels completely with no gaps
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

class NoGapsQualityEnhancer:
    """Quality enhancement that prevents gaps by ensuring proper image sizing"""
    
    def __init__(self):
        print("📐 No-Gaps Quality Enhancer - Perfect Fit + High Quality")
        
    def enhance_image(self, image_path, output_path=None):
        """Quality enhancement ensuring no gaps in panels"""
        if output_path is None:
            output_path = image_path
        
        try:
            print(f"📐 NO-GAPS Enhancement: {os.path.basename(image_path)}")
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            h, w = img.shape[:2]
            print(f"📏 Original: {w}x{h}")
            
            # Step 1: Ensure proper aspect ratio for panels (400x540 = 0.74 ratio)
            target_ratio = 400.0 / 540.0  # Panel aspect ratio
            current_ratio = w / h
            
            if abs(current_ratio - target_ratio) > 0.1:  # If ratio is significantly different
                # Adjust to perfect panel ratio to prevent gaps
                if current_ratio > target_ratio:  # Too wide
                    new_w = int(h * target_ratio)
                    new_h = h
                else:  # Too tall
                    new_w = w
                    new_h = int(w / target_ratio)
                
                # Center crop to perfect ratio
                start_x = (w - new_w) // 2
                start_y = (h - new_h) // 2
                img = img[start_y:start_y+new_h, start_x:start_x+new_w]
                print(f"📐 Adjusted for perfect fit: {w}x{h} → {new_w}x{new_h}")
            
            # Step 2: Quality enhancement (without changing dimensions)
            img = self.quality_enhance_no_resize(img)
            
            # Step 3: Ensure minimum quality size for panels
            final_h, final_w = img.shape[:2]
            min_size = 800  # Minimum dimension for good quality
            
            if final_w < min_size or final_h < min_size:
                scale = min_size / min(final_w, final_h)
                new_w = int(final_w * scale)
                new_h = int(final_h * scale)
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
                print(f"📈 Quality upscale: {final_w}x{final_h} → {new_w}x{new_h}")
            
            # Save with maximum quality
            success = cv2.imwrite(output_path, img, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                final_h, final_w = img.shape[:2]
                print(f"✅ NO-GAPS Complete: {final_w}x{final_h} (perfect panel fit)")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ No-gaps enhancement failed: {e}")
            return False
    
    def quality_enhance_no_resize(self, img):
        """Quality enhancement without changing dimensions"""
        original_shape = img.shape
        
        # Fast but effective quality enhancement
        # Step 1: Noise reduction
        img = cv2.bilateralFilter(img, 5, 50, 50)
        
        # Step 2: Color enhancement using PIL (reliable)
        try:
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.2)
            
            # Enhance color
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.25)
            
            # Enhance brightness
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(1.05)
            
            # Convert back
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            print(f"⚠️ PIL enhancement failed: {e}")
        
        # Step 3: Sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.1
        sharpened = cv2.filter2D(img, -1, kernel)
        img = cv2.addWeighted(img, 0.9, sharpened, 0.1, 0)
        
        # Ensure exact same shape
        if img.shape != original_shape:
            img = cv2.resize(img, (original_shape[1], original_shape[0]), interpolation=cv2.INTER_CUBIC)
        
        return img
    
    def batch_enhance(self, input_dir):
        """Fast batch enhancement ensuring no gaps"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            return False
        
        print(f"📐 NO-GAPS Enhancement: {len(image_files)} images")
        print("🔥 Ensuring perfect panel fit with high quality")
        
        successful = 0
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(input_dir, filename)
            
            if self.enhance_image(image_path):
                successful += 1
            
            if i % 20 == 0 or i == len(image_files):
                progress = (i / len(image_files)) * 100
                print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | Success: {successful}")
        
        success_rate = (successful / len(image_files)) * 100
        print(f"\n🎉 NO-GAPS Enhancement Complete!")
        print(f"✅ Perfect fit: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        
        return successful > 0

def enhance_frames_no_gaps(frames_dir="frames/final"):
    """No-gaps enhancement for all frames"""
    enhancer = NoGapsQualityEnhancer()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = NoGapsQualityEnhancer()
    
    if os.path.exists("frames/final"):
        enhance_frames_no_gaps()
    else:
        print("No frames directory found for testing")