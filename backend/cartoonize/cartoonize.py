# Import necessary libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

def cartoonize(img_path):
    # Opens an image with cv2
    img = cv2.imread(img_path)
    
    # Enhanced preprocessing for better quality
    # Apply bilateral filter for noise reduction while preserving edges
    img_bf = cv2.bilateralFilter(img, 9, 75, 75)
    
    # Apply edge-preserving filter for smoother cartoon effect
    img_epf = cv2.edgePreservingFilter(img_bf, flags=1, sigma_s=50, sigma_r=0.4)
    
    # Enhanced edge detection using Canny
    gray = cv2.cvtColor(img_epf, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    
    # Adaptive threshold for better edge detection
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    # Morphological operations to clean up edges
    kernel = np.ones((2,2), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    edges = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)
    
    # Invert edges for cartoon effect
    edges = cv2.bitwise_not(edges)
    
    # Enhanced color quantization using K-means with more colors for better quality
    data = img_epf.reshape((-1, 3))
    data = np.float32(data)
    
    # Increased number of colors for better quality
    K = 32
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    
    # Convert back to uint8
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_epf.shape)
    
    # Convert edges to 3-channel
    edges_3ch = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Combine segmented image with edges
    cartoon = cv2.bitwise_and(segmented_image, edges_3ch)
    
    # Apply final enhancement
    cartoon = cv2.bilateralFilter(cartoon, 5, 50, 50)
    
    # Save the enhanced image
    cv2.imwrite(img_path, cartoon)

# cartoonize()
    
def style_frames():
    for image in os.listdir("frames/final"):
        frame_path = os.path.join("frames",'final',image)
        cartoonize(frame_path)