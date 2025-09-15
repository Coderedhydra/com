"""
Reliable Quality Enhancer - No Errors, Just Great Quality
Simple but highly effective image quality enhancement without resizing
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance

class ReliableQualityEnhancer:
    """Reliable quality enhancement without complex operations that can fail"""
    
    def __init__(self):
        print("🎨 Reliable Quality Enhancer - Error-Free Excellence")
    
    def enhance_image(self, image_path, output_path=None):
        """Reliable quality enhancement without resizing"""
        if output_path is None:
            output_path = image_path
        
        try:
            print(f"🔥 RELIABLE QUALITY Enhancement: {os.path.basename(image_path)}")
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                print(f"❌ Could not load image: {image_path}")
                return False
            
            h, w = img.shape[:2]
            print(f"📐 Original size: {w}x{h} (preserving exactly)")
            
            # Step 1: Reliable noise reduction
            img = self.reliable_noise_reduction(img)
            
            # Step 2: Reliable detail enhancement
            img = self.reliable_detail_enhancement(img)
            
            # Step 3: Reliable color enhancement
            img = self.reliable_color_enhancement(img)
            
            # Step 4: Reliable sharpening
            img = self.reliable_sharpening(img)
            
            # Step 5: Final quality pass
            img = self.reliable_final_pass(img)
            
            # Save with maximum quality
            success = cv2.imwrite(output_path, img, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                print(f"✅ RELIABLE QUALITY Complete: {w}x{h} (same size, enhanced quality)")
                return True
            else:
                print("❌ Failed to save enhanced image")
                return False
                
        except Exception as e:
            print(f"❌ Reliable quality enhancement failed: {e}")
            return False
    
    def reliable_noise_reduction(self, img):
        """Reliable noise reduction using proven methods"""
        print("🧹 Reliable noise reduction...")
        
        try:
            # Use fastNlMeansDenoising - most reliable method
            denoised = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)
            
            # Add bilateral filtering for extra smoothness
            bilateral = cv2.bilateralFilter(denoised, 5, 50, 50)
            
            # Combine both methods
            result = cv2.addWeighted(denoised, 0.7, bilateral, 0.3, 0)
            
            return result
        except Exception as e:
            print(f"⚠️ Noise reduction failed, using original: {e}")
            return img
    
    def reliable_detail_enhancement(self, img):
        """Reliable detail enhancement using safe methods"""
        print("🔬 Reliable detail enhancement...")
        
        try:
            # Method 1: Unsharp masking (very reliable)
            gaussian = cv2.GaussianBlur(img, (0, 0), 1.5)
            unsharp = cv2.addWeighted(img, 1.5, gaussian, -0.5, 0)
            
            # Method 2: Simple sharpening kernel
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.1
            kernel_sharp = cv2.filter2D(img, -1, kernel)
            
            # Combine methods safely
            result = cv2.addWeighted(img, 0.6, unsharp, 0.3, 0)
            result = cv2.addWeighted(result, 0.9, kernel_sharp, 0.1, 0)
            
            return result
        except Exception as e:
            print(f"⚠️ Detail enhancement failed, using original: {e}")
            return img
    
    def reliable_color_enhancement(self, img):
        """Reliable color enhancement using PIL and OpenCV"""
        print("🎨 Reliable color enhancement...")
        
        try:
            # Use PIL for reliable color enhancement
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.2)
            
            # Enhance color saturation
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.3)
            
            # Enhance brightness slightly
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(1.05)
            
            # Convert back to OpenCV
            result = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
            return result
        except Exception as e:
            print(f"⚠️ Color enhancement failed, using original: {e}")
            return img
    
    def reliable_sharpening(self, img):
        """Reliable sharpening without complex operations"""
        print("⚡ Reliable sharpening...")
        
        try:
            # Simple but effective sharpening kernel
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.2
            sharpened = cv2.filter2D(img, -1, kernel)
            
            # Blend with original
            result = cv2.addWeighted(img, 0.7, sharpened, 0.3, 0)
            
            return result
        except Exception as e:
            print(f"⚠️ Sharpening failed, using original: {e}")
            return img
    
    def reliable_final_pass(self, img):
        """Reliable final quality pass"""
        print("🌟 Reliable final pass...")
        
        try:
            # Simple but effective final enhancement
            # Light bilateral filtering for smooth finish
            result = cv2.bilateralFilter(img, 3, 25, 25)
            
            # Very light final sharpening
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.05
            final_sharp = cv2.filter2D(result, -1, kernel)
            result = cv2.addWeighted(result, 0.95, final_sharp, 0.05, 0)
            
            return result
        except Exception as e:
            print(f"⚠️ Final pass failed, using previous: {e}")
            return img
    
    def batch_enhance(self, input_dir):
        """Batch enhance with reliable methods"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            return False
        
        print(f"🎯 RELIABLE QUALITY Enhancement: {len(image_files)} images")
        print("🔥 Error-free quality enhancement without resizing")
        
        successful = 0
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(input_dir, filename)
            
            if self.enhance_image(image_path):
                successful += 1
            
            if i % 10 == 0 or i == len(image_files):
                progress = (i / len(image_files)) * 100
                print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | Success: {successful}")
        
        success_rate = (successful / len(image_files)) * 100
        print(f"\n🎉 RELIABLE QUALITY Complete!")
        print(f"✅ Error-free enhancement: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        
        return successful > 0

def enhance_frames_reliable_quality(frames_dir="frames/final"):
    """Reliable quality enhancement for all frames"""
    enhancer = ReliableQualityEnhancer()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = ReliableQualityEnhancer()
    
    if os.path.exists("frames/final"):
        enhance_frames_reliable_quality()
    else:
        print("No frames directory found for testing")