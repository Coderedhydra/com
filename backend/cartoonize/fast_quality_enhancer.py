"""
Fast Quality Enhancer - Speed + Quality
Simple, fast, error-free quality enhancement
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

class FastQualityEnhancer:
    """Fast, reliable quality enhancement"""
    
    def __init__(self):
        print("⚡ Fast Quality Enhancer - Speed + Quality")
        self.gpu_available = self.check_gpu()
    
    def check_gpu(self):
        """Quick GPU check"""
        try:
            gpu_count = cv2.cuda.getCudaEnabledDeviceCount()
            if gpu_count > 0:
                print(f"🚀 GPU Available: {gpu_count} device(s)")
                return True
        except:
            pass
        print("💻 Using CPU with optimizations")
        return False
    
    def enhance_image(self, image_path, output_path=None):
        """Fast quality enhancement"""
        if output_path is None:
            output_path = image_path
        
        try:
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            h, w = img.shape[:2]
            
            # Fast quality enhancement pipeline
            if self.gpu_available:
                img = self.gpu_fast_enhance(img)
            else:
                img = self.cpu_fast_enhance(img)
            
            # Save with high quality
            success = cv2.imwrite(output_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 1])
            
            return success
                
        except Exception as e:
            print(f"⚠️ Fast enhancement failed: {e}")
            return False
    
    def gpu_fast_enhance(self, img):
        """GPU-accelerated fast enhancement"""
        try:
            print("🚀 GPU fast enhancement...")
            
            # Upload to GPU
            gpu_img = cv2.cuda_GpuMat()
            gpu_img.upload(img)
            
            # GPU bilateral filter (fastest quality improvement)
            gpu_result = cv2.cuda.bilateralFilter(gpu_img, -1, 40, 40)
            
            # Download result
            result = gpu_result.download()
            
            # Quick CPU finishing
            result = self.quick_cpu_finish(result)
            
            return result
            
        except Exception as e:
            print(f"⚠️ GPU enhancement failed: {e}, using CPU")
            return self.cpu_fast_enhance(img)
    
    def cpu_fast_enhance(self, img):
        """CPU-optimized fast enhancement"""
        print("💻 CPU fast enhancement...")
        
        # Fast bilateral filtering
        result = cv2.bilateralFilter(img, 5, 40, 40)
        
        # Quick finishing
        result = self.quick_cpu_finish(result)
        
        return result
    
    def quick_cpu_finish(self, img):
        """Quick CPU finishing touches"""
        # Fast color enhancement using PIL
        try:
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            # Quick enhancements
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.15)
            
            # Convert back
            result = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
            # Quick sharpening
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.1
            sharpened = cv2.filter2D(result, -1, kernel)
            result = cv2.addWeighted(result, 0.9, sharpened, 0.1, 0)
            
            return result
            
        except Exception as e:
            print(f"⚠️ Quick finish failed: {e}")
            return img
    
    def batch_enhance(self, input_dir):
        """Fast parallel batch enhancement"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            return False
        
        # Use more workers for speed
        max_workers = 8 if self.gpu_available else 6
        
        print(f"⚡ FAST Enhancement: {len(image_files)} images with {max_workers} workers")
        
        start_time = time.time()
        successful = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_file = {executor.submit(self.enhance_image, os.path.join(input_dir, img)): img 
                             for img in image_files}
            
            # Process results
            for future in as_completed(future_to_file):
                if future.result():
                    successful += 1
                
                # Progress update every 20 images
                if successful % 20 == 0:
                    elapsed = time.time() - start_time
                    rate = successful / elapsed if elapsed > 0 else 0
                    remaining = len(image_files) - successful
                    eta = remaining / rate if rate > 0 else 0
                    print(f"📊 Progress: {successful}/{len(image_files)} | Rate: {rate:.1f}/s | ETA: {eta:.0f}s")
        
        total_time = time.time() - start_time
        success_rate = (successful / len(image_files)) * 100
        
        print(f"\n🎉 FAST Enhancement Complete!")
        print(f"✅ Enhanced: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        print(f"⚡ Total time: {total_time:.1f}s | Speed: {successful/total_time:.1f} images/sec")
        
        return successful > 0

def enhance_frames_fast_quality(frames_dir="frames/final"):
    """Fast quality enhancement for all frames"""
    enhancer = FastQualityEnhancer()
    return enhancer.batch_enhance(frames_dir)

if __name__ == "__main__":
    enhancer = FastQualityEnhancer()
    
    if os.path.exists("frames/final"):
        enhance_frames_fast_quality()
    else:
        print("No frames directory found for testing")