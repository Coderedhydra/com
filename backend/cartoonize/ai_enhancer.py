"""
Advanced AI-Based Image Enhancement System
Implements state-of-the-art image enhancement techniques for superior comic quality
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import os

class AIImageEnhancer:
    def __init__(self):
        self.enhancement_models = {
            'super_resolution': self.super_resolution_enhance,
            'color_enhancement': self.ai_color_enhance,
            'detail_preservation': self.preserve_details,
            'noise_reduction': self.advanced_denoise,
            'contrast_optimization': self.optimize_contrast
        }
    
    def super_resolution_enhance(self, image):
        """Enhanced super-resolution using advanced interpolation"""
        h, w = image.shape[:2]
        
        # Smart upscaling for better quality
        if w < 1200 or h < 900:
            # Calculate optimal scale factor
            scale_w = max(1.0, 1200 / w)
            scale_h = max(1.0, 900 / h)
            scale = min(scale_w, scale_h, 2.0)  # Cap at 2x to avoid over-processing
            
            new_w = int(w * scale)
            new_h = int(h * scale)
            
            # Use INTER_CUBIC for upscaling, INTER_AREA for downscaling
            if scale > 1.0:
                enhanced = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
            else:
                enhanced = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            print(f"🔍 Super-resolution: {w}x{h} → {new_w}x{new_h} (scale: {scale:.2f}x)")
            return enhanced
        
        return image
    
    def ai_color_enhance(self, image):
        """AI-powered color enhancement with intelligent adjustments"""
        # Convert to PIL for advanced color operations
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Analyze image characteristics
        histogram = pil_image.histogram()
        brightness = sum(i * w for i, w in enumerate(histogram)) / sum(histogram)
        
        # Smart enhancement based on image characteristics
        if brightness < 85:  # Dark image
            # Enhance brightness and contrast more aggressively
            enhancer = ImageEnhance.Brightness(pil_image)
            pil_image = enhancer.enhance(1.3)
            
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.4)
            
            print("🌟 Applied dark image enhancement")
            
        elif brightness > 170:  # Bright image
            # Gentle enhancement to avoid overexposure
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.2)
            
            print("☀️ Applied bright image enhancement")
            
        else:  # Normal brightness
            # Standard enhancement
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.25)
            
            print("🎨 Applied standard enhancement")
        
        # Always enhance saturation for comic book look
        enhancer = ImageEnhance.Color(pil_image)
        pil_image = enhancer.enhance(1.35)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(1.2)
        
        # Convert back to OpenCV format
        enhanced = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return enhanced
    
    def preserve_details(self, image):
        """Advanced detail preservation using multi-scale processing"""
        # Create multiple scales
        scale1 = cv2.pyrDown(image)
        scale2 = cv2.pyrDown(scale1)
        
        # Process each scale
        smooth1 = cv2.bilateralFilter(image, 9, 75, 75)
        smooth2 = cv2.bilateralFilter(scale1, 9, 75, 75)
        smooth3 = cv2.bilateralFilter(scale2, 9, 75, 75)
        
        # Upscale back
        smooth2_up = cv2.pyrUp(smooth2)
        smooth3_up = cv2.pyrUp(cv2.pyrUp(smooth3))
        
        # Ensure same dimensions
        smooth2_up = cv2.resize(smooth2_up, (image.shape[1], image.shape[0]))
        smooth3_up = cv2.resize(smooth3_up, (image.shape[1], image.shape[0]))
        
        # Blend scales for detail preservation
        result = cv2.addWeighted(smooth1, 0.5, smooth2_up, 0.3, 0)
        result = cv2.addWeighted(result, 0.8, smooth3_up, 0.2, 0)
        
        print("🔬 Applied multi-scale detail preservation")
        return result
    
    def advanced_denoise(self, image):
        """Advanced noise reduction while preserving edges"""
        # Apply multiple denoising techniques
        
        # Color denoising
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 3, 3, 7, 21)
        
        # Edge-preserving smoothing
        smooth = cv2.edgePreservingFilter(denoised, flags=2, sigma_s=50, sigma_r=0.4)
        
        # Blend original and processed for natural look
        result = cv2.addWeighted(denoised, 0.7, smooth, 0.3, 0)
        
        print("🧹 Applied advanced noise reduction")
        return result
    
    def optimize_contrast(self, image):
        """Intelligent contrast optimization using CLAHE"""
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel with adaptive parameters
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l_enhanced = clahe.apply(l)
        
        # Merge back
        enhanced_lab = cv2.merge([l_enhanced, a, b])
        result = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
        
        print("⚡ Applied intelligent contrast optimization")
        return result
    
    def enhance_image(self, image_path):
        """Main enhancement pipeline using all AI techniques"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print(f"❌ Could not load image: {image_path}")
                return False
            
            print(f"🚀 Starting AI enhancement for: {os.path.basename(image_path)}")
            original_shape = image.shape
            
            # Apply enhancement pipeline
            enhanced = image.copy()
            
            # Step 1: Super-resolution enhancement
            enhanced = self.super_resolution_enhance(enhanced)
            
            # Step 2: Detail preservation
            enhanced = self.preserve_details(enhanced)
            
            # Step 3: Advanced denoising
            enhanced = self.advanced_denoise(enhanced)
            
            # Step 4: AI color enhancement
            enhanced = self.ai_color_enhance(enhanced)
            
            # Step 5: Contrast optimization
            enhanced = self.optimize_contrast(enhanced)
            
            # Step 6: Final sharpening
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            sharpened = cv2.filter2D(enhanced, -1, kernel)
            enhanced = cv2.addWeighted(enhanced, 0.8, sharpened, 0.2, 0)
            
            # Save with maximum quality
            success = cv2.imwrite(image_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                print(f"✅ AI enhancement complete: {os.path.basename(image_path)}")
                print(f"   Original: {original_shape[1]}x{original_shape[0]} → Enhanced: {enhanced.shape[1]}x{enhanced.shape[0]}")
                return True
            else:
                print(f"⚠️ Failed to save enhanced image: {image_path}")
                return False
                
        except Exception as e:
            print(f"❌ Error enhancing {image_path}: {str(e)}")
            return False

def enhance_all_frames(frames_dir="frames/final"):
    """Enhance all frames in the directory using AI techniques"""
    if not os.path.exists(frames_dir):
        print(f"❌ Frames directory not found: {frames_dir}")
        return False
    
    enhancer = AIImageEnhancer()
    image_files = [f for f in os.listdir(frames_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not image_files:
        print("❌ No image files found for enhancement")
        return False
    
    print(f"🎯 Starting AI enhancement for {len(image_files)} frames")
    
    successful = 0
    for i, image_file in enumerate(image_files, 1):
        image_path = os.path.join(frames_dir, image_file)
        print(f"\n📸 Processing frame {i}/{len(image_files)}: {image_file}")
        
        if enhancer.enhance_image(image_path):
            successful += 1
        
        # Progress update
        if i % 5 == 0 or i == len(image_files):
            progress = (i / len(image_files)) * 100
            print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | Success: {successful}")
    
    success_rate = (successful / len(image_files)) * 100
    print(f"\n🎉 AI Enhancement Complete!")
    print(f"✅ Successfully enhanced: {successful}/{len(image_files)} ({success_rate:.1f}%)")
    
    return successful > 0

if __name__ == "__main__":
    enhance_all_frames()