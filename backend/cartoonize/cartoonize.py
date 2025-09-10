# Import necessary libraries
import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def cartoonize(img_path):
    # Balanced cartoon-style processing with good visual quality
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"Warning: Could not load image {img_path}")
        return
    
    try:
        # Get original dimensions
        original_height, original_width = img.shape[:2]
        
        # Resize for consistent processing if needed
        if original_width > 1920 or original_height > 1080:
            # Downscale large images for speed
            scale_factor = min(1920/original_width, 1080/original_height)
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
            resized = True
        else:
            resized = False
        
        # Step 1: Bilateral filtering for smooth cartoon look (2 passes for quality)
        smooth = cv2.bilateralFilter(img, 9, 80, 80)
        smooth = cv2.bilateralFilter(smooth, 9, 80, 80)
        
        # Step 2: Create strong edges for cartoon effect
        gray = cv2.cvtColor(smooth, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Dilate edges to make them more prominent (cartoon style)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        edges = cv2.dilate(edges, kernel, iterations=1)
        edges = cv2.erode(edges, kernel, iterations=1)
        
        # Convert edges to 3-channel
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        
        # Step 3: Color quantization for cartoon effect
        data = smooth.reshape((-1, 3))
        data = np.float32(data)
        
        # Use 12 colors for good cartoon effect
        K = 12
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 15, 1.0)
        _, labels, centers = cv2.kmeans(data, K, None, criteria, 8, cv2.KMEANS_PP_CENTERS)
        
        centers = np.uint8(centers)
        segmented_data = centers[labels.flatten()]
        segmented_image = segmented_data.reshape(smooth.shape)
        
        # Step 4: Combine for cartoon effect
        # Blend quantized colors with original for detail retention
        cartoon = cv2.addWeighted(segmented_image, 0.75, img, 0.25, 0)
        
        # Add strong edges for cartoon look
        cartoon = cv2.addWeighted(cartoon, 0.85, edges, 0.15, 0)
        
        # Step 5: Enhance colors for vibrant comic look
        hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
        
        # Boost saturation and slightly increase brightness
        hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.3)  # Saturation boost
        hsv[:, :, 2] = cv2.multiply(hsv[:, :, 2], 1.1)  # Brightness boost
        
        # Ensure values stay in valid range
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)
        
        cartoon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        # Resize back to original dimensions if we downscaled
        if resized:
            cartoon = cv2.resize(cartoon, (original_width, original_height), interpolation=cv2.INTER_CUBIC)
        
        # Save with good quality
        cv2.imwrite(img_path, cartoon, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # No compression for quality
        
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