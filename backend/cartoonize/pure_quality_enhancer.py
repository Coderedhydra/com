"""
Pure Quality Enhancement - No Resizing, Just Superior Quality
Focuses on dramatically improving image quality without changing dimensions
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

class PureQualityEnhancer:
    """Pure quality enhancement without resizing"""
    
    def __init__(self):
        print("🎨 Pure Quality Enhancer - No Resize, Just Excellence")
    
    def enhance_image(self, image_path, output_path=None):
        """Dramatically improve image quality without resizing"""
        if output_path is None:
            output_path = image_path
        
        try:
            print(f"🔥 PURE QUALITY Enhancement: {os.path.basename(image_path)}")
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            h, w = img.shape[:2]
            print(f"📐 Original size: {w}x{h} (preserving dimensions)")
            
            # Step 1: Advanced noise reduction (preserve all details)
            img = self.advanced_noise_reduction(img)
            
            # Step 2: Professional detail enhancement
            img = self.professional_detail_enhancement(img)
            
            # Step 3: Superior color enhancement
            img = self.superior_color_enhancement(img)
            
            # Step 4: Professional edge enhancement
            img = self.professional_edge_enhancement(img)
            
            # Step 5: Final quality optimization
            img = self.final_quality_optimization(img)
            
            # Save with absolute maximum quality
            success = cv2.imwrite(output_path, img, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # Zero compression
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                final_h, final_w = img.shape[:2]
                print(f"✅ PURE QUALITY Complete: {final_w}x{final_h} (same size, superior quality)")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Pure quality enhancement failed: {e}")
            return False
    
    def advanced_noise_reduction(self, img):
        """Advanced noise reduction while preserving all details"""
        print("🧹 Advanced noise reduction (detail-preserving)...")
        
        # Multi-stage noise reduction
        # Stage 1: Color noise reduction with edge preservation
        denoised1 = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)
        
        # Stage 2: Edge-preserving smoothing
        denoised2 = cv2.edgePreservingFilter(img, flags=2, sigma_s=50, sigma_r=0.4)
        
        # Stage 3: Bilateral filtering for texture preservation
        denoised3 = cv2.bilateralFilter(img, 5, 50, 50)
        
        # Combine all stages for optimal result
        result = cv2.addWeighted(denoised1, 0.4, denoised2, 0.3, 0)
        result = cv2.addWeighted(result, 0.7, denoised3, 0.3, 0)
        
        return result
    
    def professional_detail_enhancement(self, img):
        """Professional detail enhancement without resizing"""
        print("🔬 Professional detail enhancement...")
        
        # Create multiple detail layers
        # Layer 1: Fine details
        fine_details = cv2.bilateralFilter(img, 3, 30, 30)
        
        # Layer 2: Medium details  
        medium_details = cv2.bilateralFilter(img, 5, 40, 40)
        
        # Layer 3: Large structures
        large_structures = cv2.bilateralFilter(img, 9, 60, 60)
        
        # Combine layers for optimal detail preservation
        result = cv2.addWeighted(fine_details, 0.5, medium_details, 0.3, 0)
        result = cv2.addWeighted(result, 0.8, large_structures, 0.2, 0)
        
        # Detail enhancement using unsharp mask
        gaussian = cv2.GaussianBlur(result, (0, 0), 1.0)
        unsharp = cv2.addWeighted(result, 1.5, gaussian, -0.5, 0)
        result = cv2.addWeighted(result, 0.7, unsharp, 0.3, 0)
        
        return result
    
    def superior_color_enhancement(self, img):
        """Superior color enhancement for professional results"""
        print("🎨 Superior color enhancement...")
        
        # Convert to PIL for advanced color operations
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Professional color enhancement
        # Step 1: Enhance contrast intelligently
        enhancer = ImageEnhance.Contrast(pil_img)
        pil_img = enhancer.enhance(1.2)
        
        # Step 2: Enhance color saturation
        enhancer = ImageEnhance.Color(pil_img)
        pil_img = enhancer.enhance(1.3)
        
        # Step 3: Enhance brightness subtly
        enhancer = ImageEnhance.Brightness(pil_img)
        pil_img = enhancer.enhance(1.1)
        
        # Step 4: Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_img)
        pil_img = enhancer.enhance(1.2)
        
        # Convert back to OpenCV
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        
        # Additional OpenCV color enhancement
        # LAB color space enhancement
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge back
        lab = cv2.merge([l, a, b])
        img = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return img
    
    def professional_edge_enhancement(self, img):
        """Professional edge enhancement for crisp images"""
        print("⚡ Professional edge enhancement...")
        
        # Multiple edge enhancement techniques
        # Technique 1: Laplacian sharpening
        laplacian = cv2.Laplacian(img, cv2.CV_64F)
        laplacian = np.uint8(np.absolute(laplacian))
        laplacian = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR) if len(laplacian.shape) == 2 else laplacian
        
        # Technique 2: Sobel edge detection
        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)
        sobel = np.sqrt(sobelx**2 + sobely**2)
        sobel = np.uint8(sobel)
        sobel = cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR) if len(sobel.shape) == 2 else sobel
        
        # Technique 3: Custom sharpening kernel
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.1
        custom_sharp = cv2.filter2D(img, -1, kernel)
        
        # Combine edge enhancements
        edge_enhanced = cv2.addWeighted(img, 0.7, laplacian, 0.1, 0)
        edge_enhanced = cv2.addWeighted(edge_enhanced, 0.9, sobel, 0.1, 0)
        edge_enhanced = cv2.addWeighted(edge_enhanced, 0.8, custom_sharp, 0.2, 0)
        
        return edge_enhanced
    
    def final_quality_optimization(self, img):
        """Final quality optimization for professional results"""
        print("🌟 Final quality optimization...")
        
        # Convert to float for precision processing
        img_float = img.astype(np.float32) / 255.0
        
        # Gamma correction for better contrast
        gamma = 1.05
        img_float = np.power(img_float, 1.0/gamma)
        
        # Convert back to uint8
        img = (img_float * 255).astype(np.uint8)
        
        # Final bilateral filtering for smooth quality
        img = cv2.bilateralFilter(img, 3, 25, 25)
        
        # Final sharpening pass
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.05
        final_sharp = cv2.filter2D(img, -1, kernel)
        img = cv2.addWeighted(img, 0.9, final_sharp, 0.1, 0)
        
        return img
    
    def batch_enhance(self, input_dir):
        """Batch enhance all images with pure quality focus"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            return False
        
        print(f"🎯 PURE QUALITY Enhancement: {len(image_files)} images")
        print("🔥 Focus: Superior quality without resizing")
        
        successful = 0
        for i, filename in enumerate(image_files, 1):
            image_path = os.path.join(input_dir, filename)
            
            if self.enhance_image(image_path):
                successful += 1
            
            if i % 10 == 0 or i == len(image_files):
                progress = (i / len(image_files)) * 100
                print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | Success: {successful}")
        
        success_rate = (successful / len(image_files)) * 100
        print(f"\n🎉 PURE QUALITY Enhancement Complete!")
        print(f"✅ Superior quality: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        
        return successful > 0

def enhance_frames_pure_quality(frames_dir="frames/final"):
    """Enhance frames with pure quality focus (no resizing)"""
    enhancer = PureQualityEnhancer()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = PureQualityEnhancer()
    
    if os.path.exists("frames/final"):
        enhance_frames_pure_quality()
    else:
        print("No frames directory found for testing")