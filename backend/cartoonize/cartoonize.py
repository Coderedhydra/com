# Import necessary libraries
import cv2
import numpy as np
import os

def cartoonize(img_path):
    # Fast and simple cartoonization
    img = cv2.imread(img_path)
    
    # Simple bilateral filter for basic smoothing
    img_smooth = cv2.bilateralFilter(img, 5, 50, 50)
    
    # Simple edge detection
    gray = cv2.cvtColor(img_smooth, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Simple color reduction (fast)
    data = img_smooth.reshape((-1, 3))
    data = np.float32(data)
    K = 8  # Reduced colors for speed
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 5, 1.0)
    _, labels, centers = cv2.kmeans(data, K, None, criteria, 3, cv2.KMEANS_RANDOM_CENTERS)
    
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_smooth.shape)
    
    # Simple combination
    cartoon = cv2.bitwise_and(segmented_image, edges)
    
    # Save the image
    cv2.imwrite(img_path, cartoon)

# cartoonize()
    
def style_frames():
    for image in os.listdir("frames/final"):
        frame_path = os.path.join("frames",'final',image)
        cartoonize(frame_path)