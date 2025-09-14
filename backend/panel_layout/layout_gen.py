import os
from os import listdir
from backend.panel_layout.cam import get_coordinates, dump_CAM_data
from backend.utils import crop_image
from backend.panel_layout.layout.page import get_templates,panel_create
from backend.utils import get_panel_type, types
from PIL import Image


def centroid_crop(index, panel_type, cam_coords, img_w, img_h):
    # Enhanced cropping to preserve full image content
    frame_path = os.path.join("frames",'final',f"frame{index+1:03d}.png")
    
    # Ensure we use the full image dimensions without cropping
    # This prevents the lower part of images from being cut off
    crop_coords = (0, img_w, 0, img_h)
    
    # Verify image exists and get actual dimensions
    try:
        from PIL import Image
        if os.path.exists(frame_path):
            with Image.open(frame_path) as img:
                actual_w, actual_h = img.size
                crop_coords = (0, actual_w, 0, actual_h)
                print(f"Frame {index+1}: Using full dimensions {actual_w}x{actual_h}")
    except Exception as e:
        print(f"Warning: Could not verify dimensions for frame {index+1}: {e}")
    
    return crop_coords


def generate_layout():
    # Simplified layout generation for speed
    input_seq = ""
    cam_coords = []
    
    # Get dimensions of first image
    try:
        img = Image.open(os.path.join("frames",'final',f"frame001.png"))
        width, height = img.size
    except:
        width, height = 800, 600  # Default dimensions
    
    # Simple panel type assignment (no complex analysis)
    folder_dir = "frames/final"
    frame_count = 0
    for image in sorted(os.listdir(folder_dir)):
        if image.endswith('.png'):
            frame_count += 1
            # Simple panel type - just use '1' for all panels
            input_seq += "1"
            # Use full image coordinates
            cam_coords.append((0, width, 0, height))
    
    # Ensure we have multiples of 4 frames for 2x2 grid
    while len(input_seq) % 4 != 0:
        input_seq += "1"
        cam_coords.append((0, width, 0, height))
    
    page_templates = get_templates(input_seq)
    print(f"Generated {len(page_templates)} page templates")
    
    # Generate crop coordinates (no cropping)
    crop_coords = []
    for i in range(len(cam_coords)):
        crop_coords.append((0, width, 0, height))
    
    panels = panel_create(page_templates)
    dump_CAM_data()
    return crop_coords, page_templates, panels