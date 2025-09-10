# Import necessary libraries
import cv2
import numpy as np
import os

def cartoonize(img_path):
    # Enhanced cartoonization with superior color quality
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"Warning: Could not load image {img_path}")
        return
    
    # Enhanced color processing
    # Convert to LAB color space for better color preservation
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    
    # Merge channels back
    lab = cv2.merge([l, a, b])
    img_enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Enhanced bilateral filter for better smoothing while preserving edges
    img_smooth = cv2.bilateralFilter(img_enhanced, 15, 80, 80)
    
    # Improved edge detection
    gray = cv2.cvtColor(img_smooth, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 20, 80)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Enhanced color quantization with more colors
    data = img_smooth.reshape((-1, 3))
    data = np.float32(data)
    K = 32  # Increased colors for better quality
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_smooth.shape)
    
    # Enhanced blending with original for superior color quality
    cartoon = cv2.addWeighted(segmented_image, 0.6, img_enhanced, 0.4, 0)
    
    # Subtle edge enhancement
    cartoon = cv2.addWeighted(cartoon, 0.95, edges, 0.05, 0)
    
    # Color saturation boost
    hsv = cv2.cvtColor(cartoon, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = hsv[:,:,1] * 1.2  # Increase saturation
    hsv[:,:,1] = np.clip(hsv[:,:,1], 0, 255)
    cartoon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    
    # Save with maximum quality
    cv2.imwrite(img_path, cartoon, [cv2.IMWRITE_PNG_COMPRESSION, 0])

# cartoonize()
    
def style_frames():
    for image in os.listdir("frames/final"):
        frame_path = os.path.join("frames",'final',image)
        cartoonize(frame_path)