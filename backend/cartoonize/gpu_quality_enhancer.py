"""
GPU-Accelerated Quality Enhancer
Fast GPU processing while maintaining the same excellent quality
"""

import cv2
import numpy as np
import os
from PIL import Image, ImageEnhance
from concurrent.futures import ThreadPoolExecutor
import time

class GPUQualityEnhancer:
    """GPU-accelerated quality enhancement for speed"""
    
    def __init__(self):
        print("🚀 GPU Quality Enhancer - High Speed + High Quality")
        self.gpu_available = self.check_gpu_support()
        
    def check_gpu_support(self):
        """Check if GPU acceleration is available"""
        try:
            # Check if OpenCV was built with GPU support
            gpu_count = cv2.cuda.getCudaEnabledDeviceCount()
            if gpu_count > 0:
                print(f"✅ GPU Support Available: {gpu_count} CUDA device(s)")
                return True
            else:
                print("⚠️ No CUDA devices found, using CPU with optimizations")
                return False
        except:
            print("⚠️ OpenCV not built with CUDA support, using CPU optimizations")
            return False
    
    def enhance_image_gpu(self, image_path, output_path=None):
        """GPU-accelerated image enhancement"""
        if output_path is None:
            output_path = image_path
        
        try:
            print(f"🚀 GPU QUALITY Enhancement: {os.path.basename(image_path)}")
            
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_COLOR)
            if img is None:
                return False
            
            h, w = img.shape[:2]
            print(f"📐 Processing: {w}x{h} (no resizing)")
            
            if self.gpu_available:
                img = self.gpu_enhancement_pipeline(img)
            else:
                img = self.optimized_cpu_pipeline(img)
            
            # Save with maximum quality
            success = cv2.imwrite(output_path, img, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            if success:
                print(f"✅ GPU QUALITY Complete: {w}x{h}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ GPU enhancement failed: {e}")
            return False
    
    def gpu_enhancement_pipeline(self, img):
        """GPU-accelerated enhancement pipeline"""
        print("🔥 Using GPU acceleration...")
        
        try:
            # Upload image to GPU
            gpu_img = cv2.cuda_GpuMat()
            gpu_img.upload(img)
            
            # GPU-accelerated bilateral filtering (fastest denoising)
            gpu_bilateral = cv2.cuda.bilateralFilter(gpu_img, -1, 50, 50)
            
            # GPU-accelerated Gaussian blur for unsharp mask
            gpu_gaussian = cv2.cuda.GaussianBlur(gpu_bilateral, (5, 5), 1.5)
            
            # Download back to CPU for operations not available on GPU
            bilateral_result = gpu_bilateral.download()
            gaussian_result = gpu_gaussian.download()
            
            # CPU operations for final enhancement
            # Unsharp masking
            unsharp = cv2.addWeighted(bilateral_result, 1.5, gaussian_result, -0.5, 0)
            
            # Color enhancement using PIL (fast and reliable)
            result = self.fast_color_enhancement(unsharp)
            
            # Final sharpening
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]) * 0.1
            sharpened = cv2.filter2D(result, -1, kernel)
            result = cv2.addWeighted(result, 0.8, sharpened, 0.2, 0)
            
            print("✅ GPU acceleration complete")
            return result
            
        except Exception as e:
            print(f"⚠️ GPU acceleration failed: {e}, using CPU")
            return self.optimized_cpu_pipeline(img)
    
    def optimized_cpu_pipeline(self, img):
        """Optimized CPU pipeline for speed"""
        print("⚡ Using optimized CPU processing...")
        
        # Fast but high-quality CPU processing
        
        # Step 1: Fast bilateral filtering (single pass)
        img = cv2.bilateralFilter(img, 5, 50, 50)
        
        # Step 2: Fast unsharp masking
        gaussian = cv2.GaussianBlur(img, (3, 3), 1.0)
        unsharp = cv2.addWeighted(img, 1.3, gaussian, -0.3, 0)
        
        # Step 3: Fast color enhancement
        img = self.fast_color_enhancement(unsharp)
        
        # Step 4: Fast final sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.1
        sharpened = cv2.filter2D(img, -1, kernel)
        result = cv2.addWeighted(img, 0.9, sharpened, 0.1, 0)
        
        print("✅ Optimized CPU processing complete")
        return result
    
    def fast_color_enhancement(self, img):
        """Fast color enhancement using PIL"""
        try:
            # Convert to PIL for fast color operations
            pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            # Fast enhancement
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.15)
            
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.2)
            
            enhancer = ImageEnhance.Brightness(pil_img)
            pil_img = enhancer.enhance(1.05)
            
            # Convert back
            result = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            return result
            
        except Exception as e:
            print(f"⚠️ Fast color enhancement failed: {e}")
            return img
    
    def batch_enhance_parallel(self, input_dir, max_workers=4):
        """Parallel batch enhancement for maximum speed"""
        image_files = [f for f in os.listdir(input_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        if not image_files:
            return False
        
        print(f"🚀 GPU/PARALLEL Enhancement: {len(image_files)} images")
        print(f"⚡ Using {max_workers} parallel workers")
        
        start_time = time.time()
        successful = 0
        
        # Process in parallel for maximum speed
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = []
            
            for filename in image_files:
                image_path = os.path.join(input_dir, filename)
                future = executor.submit(self.enhance_image_gpu, image_path)
                futures.append((future, filename))
            
            # Collect results
            for i, (future, filename) in enumerate(futures, 1):
                try:
                    if future.result():
                        successful += 1
                    
                    if i % 10 == 0 or i == len(image_files):
                        elapsed = time.time() - start_time
                        progress = (i / len(image_files)) * 100
                        avg_time = elapsed / i
                        eta = avg_time * (len(image_files) - i)
                        print(f"📊 Progress: {i}/{len(image_files)} ({progress:.1f}%) | "
                              f"Success: {successful} | ETA: {eta:.1f}s")
                        
                except Exception as e:
                    print(f"⚠️ Error processing {filename}: {e}")
        
        total_time = time.time() - start_time
        success_rate = (successful / len(image_files)) * 100
        avg_time_per_image = total_time / len(image_files)
        
        print(f"\n🎉 GPU/PARALLEL Enhancement Complete!")
        print(f"✅ Enhanced: {successful}/{len(image_files)} ({success_rate:.1f}%)")
        print(f"⚡ Total time: {total_time:.1f}s | Avg: {avg_time_per_image:.2f}s per image")
        
        return successful > 0

def enhance_frames_gpu_accelerated(frames_dir="frames/final"):
    """GPU-accelerated enhancement for all frames"""
    enhancer = GPUQualityEnhancer()
    return enhancer.batch_enhance_parallel(frames_dir, max_workers=6)  # More workers for speed

if __name__ == "__main__":
    enhancer = GPUQualityEnhancer()
    
    if os.path.exists("frames/final"):
        enhance_frames_gpu_accelerated()
    else:
        print("No frames directory found for testing")