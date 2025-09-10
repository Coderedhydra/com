# Import necessary libraries
import cv2
import numpy as np
import os

def cartoonize(img_path):
    # High-quality cartoonization with advanced AI techniques
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    
    if img is None:
        print(f"Warning: Could not load image {img_path}")
        return
    
    # Get original dimensions for high-quality processing
    original_height, original_width = img.shape[:2]
    
    # Upscale for better processing if image is small
    if original_width < 1920 or original_height < 1080:
        scale_factor = max(1920/original_width, 1080/original_height)
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Advanced bilateral filtering for high-quality smoothing
    # Multiple passes for better quality
    img_smooth = cv2.bilateralFilter(img, 15, 80, 80)
    img_smooth = cv2.bilateralFilter(img_smooth, 15, 80, 80)
    img_smooth = cv2.bilateralFilter(img_smooth, 15, 80, 80)
    
    # Advanced edge detection with multiple scales
    gray = cv2.cvtColor(img_smooth, cv2.COLOR_BGR2GRAY)
    
    # Multi-scale edge detection for better quality
    edges1 = cv2.Canny(gray, 50, 150)
    edges2 = cv2.Canny(gray, 100, 200)
    edges = cv2.bitwise_or(edges1, edges2)
    
    # Morphological operations to clean edges
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)
    
    # Convert edges back to BGR
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # High-quality color quantization with more colors
    data = img_smooth.reshape((-1, 3))
    data = np.float32(data)
    K = 16  # More colors for better quality
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)
    
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_smooth.shape)
    
    # Advanced blending for cartoon effect
    # Preserve more original detail
    cartoon = cv2.addWeighted(segmented_image, 0.6, img, 0.4, 0)
    
    # Enhance edges with better blending
    cartoon = cv2.addWeighted(cartoon, 0.85, edges, 0.15, 0)
    
    # Color enhancement for vibrant comic look
    # Convert to HSV for better color manipulation
    hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], 1.3)  # Increase saturation
    hsv[:, :, 2] = cv2.multiply(hsv[:, :, 2], 1.1)  # Slightly increase brightness
    cartoon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Resize back to original dimensions if we upscaled
    if original_width < 1920 or original_height < 1080:
        cartoon = cv2.resize(cartoon, (original_width, original_height), interpolation=cv2.INTER_LANCZOS4)
    
    # Save with maximum quality PNG settings
    cv2.imwrite(img_path, cartoon, [cv2.IMWRITE_PNG_COMPRESSION, 0])  # No compression for best quality

# cartoonize()
    
def style_frames():
    for image in os.listdir("frames/final"):
        frame_path = os.path.join("frames",'final',image)
        cartoonize(frame_path)