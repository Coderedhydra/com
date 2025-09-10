import os
from os import listdir
from backend.panel_layout.cam import get_coordinates, dump_CAM_data
from backend.utils import crop_image
from backend.panel_layout.layout.page import get_templates,panel_create
from backend.utils import get_panel_type, types
from PIL import Image


def centroid_crop(index, panel_type, cam_coords, img_w, img_h):
    # Skip complex cropping - just return the original image coordinates
    frame_path = os.path.join("frames",'final',f"frame{index+1:03d}.png")
    
    # Return full image coordinates (no cropping)
    crop_coords = (0, img_w, 0, img_h)
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
    for image in sorted(os.listdir(folder_dir)):
        if image.endswith('.png'):
            # Simple panel type - just use '1' for all panels
            input_seq += "1"
            # Use full image coordinates
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