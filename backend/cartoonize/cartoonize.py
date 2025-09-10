# Import necessary libraries
import cv2
import numpy as np
import os

def cartoonize(img_path):
    # Improved cartoonization that preserves image quality
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"Warning: Could not load image {img_path}")
        return
    
    # Light bilateral filter for subtle smoothing
    img_smooth = cv2.bilateralFilter(img, 9, 75, 75)
    
    # Light edge detection
    gray = cv2.cvtColor(img_smooth, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 30, 100)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Color reduction with more colors for better quality
    data = img_smooth.reshape((-1, 3))
    data = np.float32(data)
    K = 16  # More colors for better quality
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 5, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_smooth.shape)
    
    # Blend with original image to preserve quality
    cartoon = cv2.addWeighted(segmented_image, 0.7, img, 0.3, 0)
    
    # Light edge enhancement
    cartoon = cv2.addWeighted(cartoon, 0.9, edges, 0.1, 0)
    
    # Save the image with high quality
    cv2.imwrite(img_path, cartoon, [cv2.IMWRITE_PNG_COMPRESSION, 1])

# cartoonize()
    
def style_frames():
    for image in os.listdir("frames/final"):
        frame_path = os.path.join("frames",'final',image)
        cartoonize(frame_path)