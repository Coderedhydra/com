"""
Ultra-High Quality Enhancement Without Resizing
Professional-grade image quality improvement while preserving original dimensions
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter
import scipy.ndimage

class UltraQualityNoResize:
    """Ultra-high quality enhancement without any resizing"""
    
    def __init__(self):
        print("🔥 Ultra-High Quality Enhancer (No Resize, Pure Quality)")
    
    def enhance_image(self, image_path, output_path=None):
        """Ultra-high quality enhancement preserving original size"""
        if output_path is None:
            output_path = image_path
        
        try:
            print(f"🎨 ULTRA-HIGH QUALITY (No Resize): {os.path.basename(image_path)}")
            
            # Load image with maximum quality
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            h, w = img.shape[:2]
            print(f"📐 Preserving original: {w}x{h} (no resizing)")
            
            # Professional quality enhancement pipeline
            img = self.professional_noise_reduction(img)
            img = self.professional_detail_enhancement(img)
            img = self.professional_color_grading(img)
            img = self.professional_sharpening(img)
            img = self.professional_final_pass(img)
            
            # Save with absolute maximum quality settings
            success = cv2.imwrite(output_path, img, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # Zero compression for maximum quality
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT,
                cv2.IMWRITE_PNG_BILEVEL, 0
            ])
            
            if success:
                print(f"✅ ULTRA-HIGH QUALITY Complete: {w}x{h} (preserved, enhanced)")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Ultra-high quality enhancement failed: {e}")
            return False
    
    def professional_noise_reduction(self, img):
        """Professional-grade noise reduction"""
        print("🧹 Professional noise reduction...")
        
        # Stage 1: Advanced color denoising
        denoised = cv2.fastNlMeansDenoisingColored(img, None, 4, 4, 7, 21)
        
        # Stage 2: Edge-preserving bilateral filtering
        bilateral = cv2.bilateralFilter(img, 9, 75, 75)
        
        # Stage 3: Combine for optimal noise reduction
        result = cv2.addWeighted(denoised, 0.6, bilateral, 0.4, 0)
        
        return result
    
    def professional_detail_enhancement(self, img):
        """Professional detail enhancement using advanced techniques"""
        print("🔬 Professional detail enhancement...")
        
        # Technique 1: Unsharp masking (professional standard)
        gaussian = cv2.GaussianBlur(img, (0, 0), 1.5)
        unsharp = cv2.addWeighted(img, 1.5, gaussian, -0.5, 0)
        
        # Technique 2: Detail enhancement filter
        detail_enhanced = cv2.detailEnhance(img, sigma_s=20, sigma_r=0.15)
        
        # Technique 3: Edge enhancement
        edges = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 50, 150)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        edge_enhanced = cv2.addWeighted(img, 0.9, edges, 0.1, 0)
        
        # Combine all techniques
        result = cv2.addWeighted(unsharp, 0.4, detail_enhanced, 0.4, 0)
        result = cv2.addWeighted(result, 0.8, edge_enhanced, 0.2, 0)
        
        return result
    
    def professional_color_grading(self, img):
        """Professional color grading for superior visual quality"""
        print("🎨 Professional color grading...")
        
        # Convert to LAB color space for professional color work
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Professional CLAHE for contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge back and convert to HSV for saturation work
        lab = cv2.merge([l, a, b])
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        # HSV color enhancement
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Professional saturation enhancement
        s = cv2.multiply(s, 1.25)  # 25% saturation boost
        s = np.clip(s, 0, 255)
        
        # Professional brightness optimization
        v = cv2.multiply(v, 1.1)   # 10% brightness boost
        v = np.clip(v, 0, 255)
        
        # Merge back to BGR
        hsv = cv2.merge([h, s, v])
        result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return result
    
    def professional_sharpening(self, img):
        """Professional sharpening for crisp, clear images"""
        print("⚡ Professional sharpening...")
        
        # Multiple sharpening techniques
        # Technique 1: Custom sharpening kernel (most reliable)
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.15
        kernel_sharp = cv2.filter2D(img, -1, kernel)
        
        # Technique 2: High-pass filter sharpening
        gaussian = cv2.GaussianBlur(img, (0, 0), 2.0)
        high_pass = cv2.addWeighted(img, 2.0, gaussian, -1.0, 0)
        
        # Technique 3: Unsharp mask (professional standard)
        gaussian2 = cv2.GaussianBlur(img, (0, 0), 1.0)
        unsharp = cv2.addWeighted(img, 1.3, gaussian2, -0.3, 0)
        
        # Combine sharpening techniques safely
        result = cv2.addWeighted(img, 0.6, kernel_sharp, 0.25, 0)
        result = cv2.addWeighted(result, 0.85, high_pass, 0.15, 0)
        result = cv2.addWeighted(result, 0.9, unsharp, 0.1, 0)
        
        return result
    
    def professional_final_pass(self, img):
        """Professional final pass for ultimate quality"""
        print("🌟 Professional final pass...")
        
        # Final quality optimization
        # Convert to float for precision
        img_float = img.astype(np.float32) / 255.0
        
        # Subtle gamma correction
        gamma = 1.02
        img_float = np.power(img_float, 1.0/gamma)
        
        # Convert back
        img = (img_float * 255).astype(np.uint8)
        
        # Final edge-preserving smoothing
        result = cv2.bilateralFilter(img, 3, 20, 20)
        
        # Final micro-sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.02
        micro_sharp = cv2.filter2D(result, -1, kernel)
        result = cv2.addWeighted(result, 0.95, micro_sharp, 0.05, 0)
        
        return result
    
    def batch_enhance(self, input_dir):
        """Batch enhance with pure quality focus"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            return False
        
        print(f"🎯 ULTRA-HIGH QUALITY (No Resize): {len(image_files)} images")
        print("🔥 Professional-grade enhancement without size changes")
        
        successful = 0
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(input_dir, filename)
            
            if self.enhance_image(image_path):
                successful += 1
            
            if i % 5 == 0 or i == len(image_files):
                progress = (i / len(image_files)) * 100
                print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | Success: {successful}")
        
        success_rate = (successful / len(image_files)) * 100
        print(f"\n🎉 ULTRA-HIGH QUALITY Complete!")
        print(f"✅ Professional quality: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        
        return successful > 0

def enhance_frames_ultra_quality_no_resize(frames_dir="frames/final"):
    """Ultra-high quality enhancement without resizing"""
    enhancer = UltraQualityNoResize()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = UltraQualityNoResize()
    
    if os.path.exists("frames/final"):
        enhance_frames_ultra_quality_no_resize()
    else:
        print("No frames directory found for testing")