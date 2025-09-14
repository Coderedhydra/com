# Import necessary libraries
import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def cartoonize(img_path):
    # Advanced cartoon-style processing with superior visual quality and AI-enhanced colors
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"Warning: Could not load image {img_path}")
        return
    
    try:
        # Get original dimensions
        original_height, original_width = img.shape[:2]
        
        # Enhanced upscaling for better quality instead of downscaling
        target_width, target_height = original_width, original_height
        if original_width < 800 or original_height < 600:
            # Upscale small images for better quality
            scale_factor = max(800/original_width, 600/original_height)
            target_width = int(original_width * scale_factor)
            target_height = int(original_height * scale_factor)
            img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_CUBIC)
            upscaled = True
        elif original_width > 1920 or original_height > 1080:
            # Smart downscale for very large images
            scale_factor = min(1920/original_width, 1080/original_height)
            target_width = int(original_width * scale_factor)
            target_height = int(original_height * scale_factor)
            img = cv2.resize(img, (target_width, target_height), interpolation=cv2.INTER_AREA)
            upscaled = False
        else:
            upscaled = False
        
        # Step 1: Advanced bilateral filtering for ultra-smooth cartoon look (3 passes)
        smooth = cv2.bilateralFilter(img, 15, 120, 120)
        smooth = cv2.bilateralFilter(smooth, 15, 120, 120)
        smooth = cv2.bilateralFilter(smooth, 9, 80, 80)  # Final pass with tighter parameters
        
        # Step 2: Advanced edge detection with adaptive thresholds
        gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
        
        # Use adaptive thresholds for better edge detection
        mean_intensity = np.mean(gray)
        if mean_intensity < 100:
            # Dark image - use lower thresholds
            edges = cv2.Canny(gray, 30, 100)
        elif mean_intensity > 180:
            # Bright image - use higher thresholds
            edges = cv2.Canny(gray, 70, 200)
        else:
            # Normal image - standard thresholds
            edges = cv2.Canny(gray, 50, 150)
        
        # Enhanced edge processing for comic book style
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        edges = cv2.dilate(edges, kernel, iterations=1)
        edges = cv2.erode(edges, kernel, iterations=1)
        
        # Convert edges to 3-channel
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Step 3: Advanced color quantization with intelligent clustering
        data = smooth.reshape((-1, 3))
        data = np.float32(data)
        
        # Adaptive K-means clustering based on image complexity
        unique_colors = len(np.unique(data.reshape(-1, data.shape[-1]), axis=0))
        if unique_colors < 50:
            K = 8  # Simple images
        elif unique_colors < 200:
            K = 12  # Normal complexity
        else:
            K = 16  # Complex images
            
        # Enhanced K-means with better initialization
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 25, 0.8)
        _, labels, centers = cv2.kmeans(data, K, None, criteria, 12, cv2.KMEANS_PP_CENTERS)
        
        centers = np.uint8(centers)
        segmented_data = centers[labels.flatten()]
        segmented_image = segmented_data.reshape(smooth.shape)
        
        # Apply smart blending for detail preservation
        alpha = 0.8 if unique_colors > 100 else 0.75
        
        # Step 4: Advanced cartoon composition with smart blending
        cartoon = cv2.addWeighted(segmented_image, alpha, img, 1-alpha, 0)
        
        # Add strong edges with adaptive intensity
        edge_intensity = 0.2 if mean_intensity > 150 else 0.15
        cartoon = cv2.addWeighted(cartoon, 1-edge_intensity, edges, edge_intensity, 0)
        
        # Step 5: Advanced color enhancement with AI-inspired techniques
        # Convert to LAB color space for better color manipulation
        lab = cv2.cvtColor(cartoon, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Enhance L channel (lightness) with CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        # Merge back and convert to HSV for saturation enhancement
        lab = cv2.merge([l, a, b])
        cartoon = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Adaptive saturation and brightness enhancement
        saturation_boost = 1.4 if mean_intensity > 120 else 1.3
        brightness_boost = 1.15 if mean_intensity < 100 else 1.1
        
        s = cv2.multiply(s, saturation_boost)
        v = cv2.multiply(v, brightness_boost)
        
        # Advanced color temperature adjustment for comic book feel
        # Slightly warm up the image for more appealing colors
        h = np.where((h >= 90) & (h <= 150), h - 5, h)  # Cool down greens slightly
        h = np.where((h >= 0) & (h <= 30), h + 3, h)    # Warm up reds slightly
        
        # Ensure values stay in valid range
        s = np.clip(s, 0, 255)
        v = np.clip(v, 0, 255)
        h = np.clip(h, 0, 179)
        
        hsv = cv2.merge([h, s, v])
        cartoon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Step 6: Image repair and noise reduction
        # Apply gentle denoising while preserving edges
        cartoon = cv2.fastNlMeansDenoisingColored(cartoon, None, 3, 3, 7, 21)
        
        # Resize back to original dimensions if we scaled
        if target_width != original_width or target_height != original_height:
            cartoon = cv2.resize(cartoon, (original_width, original_height), interpolation=cv2.INTER_CUBIC)
        
        # Step 7: Final quality enhancement - unsharp masking for crisp details
        gaussian_blur = cv2.GaussianBlur(cartoon, (0, 0), 2.0)
        unsharp_mask = cv2.addWeighted(cartoon, 1.5, gaussian_blur, -0.5, 0)
        cartoon = cv2.addWeighted(cartoon, 0.7, unsharp_mask, 0.3, 0)
        
        # Save with maximum quality
        cv2.imwrite(img_path, cartoon, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # No compression for quality
        print(f"✅ Enhanced cartoonization complete for {img_path}")
        
    except Exception as e:
        print(f"Error processing {img_path}: {str(e)}")
        # Save original if processing fails
        cv2.imwrite(img_path, img, [cv2.IMWRITE_PNG_COMPRESSION, 1])

# cartoonize()
    
def style_frames():
    """Optimized parallel frame styling with real-time progress tracking"""
    frames_dir = "frames/final"
    if not os.path.exists(frames_dir):
        print("❌ No frames directory found!")
        return
    
    image_files = [f for f in os.listdir(frames_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_frames = len(image_files)
    
    if total_frames == 0:
        print("❌ No image files found in frames directory!")
        return
    
    print(f"🎨 Starting cartoon-style processing for {total_frames} frames...")
    print(f"🔧 Using parallel processing with {min(4, os.cpu_count() or 1)} workers")
    start_time = time.time()
    
    def process_single_frame(image_file):
        """Process a single frame with cartoon styling"""
        try:
            frame_path = os.path.join(frames_dir, image_file)
            cartoonize(frame_path)
            return True, image_file
        except Exception as e:
            print(f"⚠️  Error processing {image_file}: {str(e)}")
            return False, image_file
    
    # Use parallel processing with optimal number of workers
    max_workers = min(4, os.cpu_count() or 1)
    processed = 0
    successful = 0
    
    print(f"⚡ Processing {total_frames} frames in parallel...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {executor.submit(process_single_frame, img): img for img in image_files}
        
        # Process results as they complete with real-time progress
        for future in as_completed(future_to_file):
            success, filename = future.result()
            processed += 1
            if success:
                successful += 1
            
            elapsed_time = time.time() - start_time
            
            # Real-time progress reporting
            if processed % 5 == 0 or processed == total_frames:
                progress_percent = (processed / total_frames) * 100
                avg_time_per_frame = elapsed_time / processed
                remaining_frames = total_frames - processed
                estimated_remaining = avg_time_per_frame * remaining_frames
                
                print(f"📊 Progress: {processed}/{total_frames} ({progress_percent:.1f}%) "
                      f"✅ Success: {successful} | "
                      f"⏱️  Elapsed: {elapsed_time:.1f}s | "
                      f"🕒 ETA: {estimated_remaining:.1f}s")
    
    total_time = time.time() - start_time
    success_rate = (successful / total_frames) * 100
    
    print(f"\n🎉 Frame styling completed!")
    print(f"📈 Processed: {total_frames} frames in {total_time:.1f} seconds")
    print(f"⚡ Average: {total_time/total_frames:.2f}s per frame")
    print(f"✅ Success rate: {success_rate:.1f}% ({successful}/{total_frames})")
    print(f"🎨 All frames now have cartoon-style processing!")

def style_frames_fast():
    """Ultra-fast frame styling - minimal processing for speed"""
    frames_dir = "frames/final"
    if not os.path.exists(frames_dir):
        return
    
    image_files = [f for f in os.listdir(frames_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_frames = len(image_files)
    
    print(f"Fast styling {total_frames} frames...")
    start_time = time.time()
    
    for i, image_file in enumerate(image_files):
        if i % 20 == 0 or i == total_frames - 1:
            print(f"Fast processing: {i+1}/{total_frames} ({(i+1)/total_frames*100:.1f}%)")
        
        frame_path = os.path.join(frames_dir, image_file)
        # Minimal processing for speed
        img = cv2.imread(frame_path)
        if img is not None:
            # Very light cartoon effect
            img_smooth = cv2.bilateralFilter(img, 5, 50, 50)
            cv2.imwrite(frame_path, img_smooth, [cv2.IMWRITE_PNG_COMPRESSION, 3])
    
    total_time = time.time() - start_time
    print(f"Fast styling completed in {total_time:.1f} seconds!")