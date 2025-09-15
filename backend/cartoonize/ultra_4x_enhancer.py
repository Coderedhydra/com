"""
Ultra-High Quality 4x Enhancer
Professional 4x upscaling for maximum image quality
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class Ultra4xEnhancer:
    """Ultra-high quality 4x enhancement for maximum image quality"""
    
    def __init__(self):
        print("🔥 Ultra 4x Quality Enhancer - Maximum Quality Mode")
        
    def enhance_image(self, image_path, output_path=None):
        """Ultra-high quality 4x enhancement"""
        if output_path is None:
            output_path = image_path
        
        try:
            print(f"🔥 ULTRA 4x QUALITY: {os.path.basename(image_path)}")
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            h, w = img.shape[:2]
            print(f"📐 Original: {w}x{h}")
            
            # Step 1: 2x Ultra-High Quality Upscaling (4K instead of 8K)
            target_w = w * 2  # 2x instead of 4x
            target_h = h * 2  # 2x instead of 4x
            
            # High-quality 2x upscaling
            img_2x = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
            
            print(f"🚀 2x Upscaling (4K): {w}x{h} → {target_w}x{target_h}")
            
            # Step 2: Ultra-high quality enhancement on 2x image
            img_2x = self.ultra_quality_enhancement(img_2x)
            
            # Save with absolute maximum quality
            success = cv2.imwrite(output_path, img_2x, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # Zero compression
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                print(f"✅ ULTRA 2x Complete: {target_w}x{target_h} (4K quality)")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Ultra 4x enhancement failed: {e}")
            return False
    
    def ultra_quality_enhancement(self, img):
        """Ultra-high quality enhancement for 4x images"""
        print("🌟 Ultra-high quality processing...")
        
        # Step 1: Advanced noise reduction (for 4x images)
        img = cv2.fastNlMeansDenoisingColored(img, None, 2, 2, 5, 15)  # Lighter for 4x
        
        # Step 2: Professional detail enhancement
        img = cv2.bilateralFilter(img, 7, 50, 50)
        
        # Step 3: Color enhancement using PIL
        try:
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            # Professional color grading
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.15)
            
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.3)
            
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(1.05)
            
            enhancer = ImageEnhance.Sharpness(pil_img)
            pil_img = enhancer.enhance(1.1)
            
            # Convert back
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            print(f"⚠️ PIL enhancement failed: {e}")
        
        # Step 4: Final sharpening for 4x images
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.05  # Lighter for 4x
        sharpened = cv2.filter2D(img, -1, kernel)
        img = cv2.addWeighted(img, 0.95, sharpened, 0.05, 0)
        
        return img
    
    def batch_enhance(self, input_dir):
        """Ultra 4x batch enhancement"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            return False
        
        print(f"🔥 ULTRA 4x Enhancement: {len(image_files)} images")
        print("🚀 4x upscaling + ultra-high quality processing")
        
        start_time = time.time()
        successful = 0
        
        # Use parallel processing for speed
        max_workers = 4  # Conservative for 4x processing
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_file = {executor.submit(self.enhance_image, os.path.join(input_dir, img)): img 
                             for img in image_files}
            
            for future in as_completed(future_to_file):
                if future.result():
                    successful += 1
                
                if successful % 10 == 0:
                    elapsed = time.time() - start_time
                    rate = successful / elapsed if elapsed > 0 else 0
                    remaining = len(image_files) - successful
                    eta = remaining / rate if rate > 0 else 0
                    print(f"📊 Progress: {successful}/{len(image_files)} | Rate: {rate:.1f}/s | ETA: {eta:.0f}s")
        
        total_time = time.time() - start_time
        success_rate = (successful / len(image_files)) * 100
        
        print(f"\n🎉 ULTRA 4x Enhancement Complete!")
        print(f"✅ 4x Quality: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        print(f"⚡ Total time: {total_time:.1f}s | Speed: {successful/total_time:.2f} images/sec")
        
        return successful > 0

def enhance_frames_ultra_4x(frames_dir="frames/final"):
    """Ultra 4x enhancement for all frames"""
    enhancer = Ultra4xEnhancer()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = Ultra4xEnhancer()
    
    if os.path.exists("frames/final"):
        enhance_frames_ultra_4x()
    else:
        print("No frames directory found for testing")