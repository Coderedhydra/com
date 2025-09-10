# Import necessary libraries
import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def cartoonize(img_path):
    # Optimized cartoonization - balanced quality and speed
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"Warning: Could not load image {img_path}")
        return
    
    # Get original dimensions
    original_height, original_width = img.shape[:2]
    
    # Only upscale if image is very small (avoid unnecessary processing)
    if original_width < 800 or original_height < 600:
        scale_factor = max(800/original_width, 600/original_height)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    # Optimized bilateral filtering - single pass with good parameters
    img_smooth = cv2.bilateralFilter(img, 9, 75, 75)
    
    # Efficient edge detection
    gray = cv2.cvtColor(img_smooth, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # Simple edge cleanup
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Optimized color quantization - fewer colors for speed
    data = img_smooth.reshape((-1, 3))
    data = np.float32(data)
    K = 12  # Good balance of quality and speed
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_smooth.shape)
    
    # Efficient blending
    cartoon = cv2.addWeighted(segmented_image, 0.7, img, 0.3, 0)
    cartoon = cv2.addWeighted(cartoon, 0.9, edges, 0.1, 0)
    
    # Quick color enhancement
    hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.2)  # Moderate saturation boost
    cartoon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Resize back if we upscaled
    if original_width < 800 or original_height < 600:
        cartoon = cv2.resize(cartoon, (original_width, original_height), interpolation=cv2.INTER_LINEAR)
    
    # Save with good quality but faster compression
    cv2.imwrite(img_path, cartoon, [cv2.IMWRITE_PNG_COMPRESSION, 1])  # Light compression for speed

# cartoonize()
    
def style_frames():
    """Optimized parallel frame styling with progress tracking"""
    frames_dir = "frames/final"
    if not os.path.exists(frames_dir):
        print("No frames directory found!")
        return
    
    image_files = [f for f in os.listdir(frames_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_frames = len(image_files)
    
    if total_frames == 0:
        print("No image files found in frames directory!")
        return
    
    print(f"Starting optimized styling for {total_frames} frames...")
    start_time = time.time()
    
    def process_single_frame(image_file):
        """Process a single frame"""
        try:
            frame_path = os.path.join(frames_dir, image_file)
            cartoonize(frame_path)
            return f"Processed: {image_file}"
        except Exception as e:
            return f"Error processing {image_file}: {str(e)}"
    
    # Use parallel processing with optimal number of workers
    max_workers = min(4, os.cpu_count() or 1)  # Limit to 4 to avoid memory issues
    processed = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_file = {executor.submit(process_single_frame, img): img for img in image_files}
        
        # Process results as they complete
        for future in as_completed(future_to_file):
            processed += 1
            elapsed_time = time.time() - start_time
            
            # Progress reporting every 10 frames or at key milestones
            if processed % 10 == 0 or processed == total_frames:
                avg_time_per_frame = elapsed_time / processed
                remaining_frames = total_frames - processed
                estimated_remaining = avg_time_per_frame * remaining_frames
                
                print(f"Progress: {processed}/{total_frames} frames ({processed/total_frames*100:.1f}%) "
                      f"- Elapsed: {elapsed_time:.1f}s - ETA: {estimated_remaining:.1f}s")
    
    total_time = time.time() - start_time
    print(f"Frame styling completed! Processed {total_frames} frames in {total_time:.1f} seconds "
          f"(avg: {total_time/total_frames:.2f}s per frame)")

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