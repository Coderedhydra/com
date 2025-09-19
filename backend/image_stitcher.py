"""
Image Stitcher - Combine 4 panels with bubbles into single image
No HTML template - direct image creation
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json

class ImageStitcher:
    """Stitch 4 panels with bubbles into single image"""
    
    def __init__(self):
        print("🔲 Image Stitcher - Combine 4 Panels + Bubbles")
        # Square dimensions for 4 equal parts - NO GAPS
        self.output_size = 2048  # Square size (2048x2048)
        self.panel_size = 1024   # Each panel (1024x1024)
        self.gap_size = 0        # No gaps for perfect fit
        
    def load_panel_images(self, frames_dir="frames/final"):
        """Load the 4 panel images"""
        print(f"\n📸 LOADING PANEL IMAGES")
        print("=" * 40)
        
        # Get page data to know which frames to use
        page_js_path = "static/comic/page.js"
        if not os.path.exists(page_js_path):
            page_js_path = "output_template/page.js"
        
        if not os.path.exists(page_js_path):
            print("❌ No page.js found")
            return None, None
        
        # Read page data
        with open(page_js_path, 'r') as f:
            content = f.read()
            # Extract JSON from "var pages = {...}"
            json_start = content.find('[')
            json_end = content.rfind(']') + 1
            pages_data = json.loads(content[json_start:json_end])
        
        if not pages_data or len(pages_data) == 0:
            print("❌ No page data found")
            return None, None
        
        page = pages_data[0]  # First page
        panels = page.get('panels', [])
        bubbles = page.get('bubbles', [])
        
        print(f"📋 Found {len(panels)} panels and {len(bubbles)} bubbles")
        
        # Load panel images
        panel_images = []
        for i, panel in enumerate(panels):
            frame_name = panel['image']
            frame_path = os.path.join(frames_dir, f"{frame_name}.png")
            
            if os.path.exists(frame_path):
                img = cv2.imread(frame_path)
                if img is not None:
                    panel_images.append(img)
                    print(f"   ✅ Loaded panel {i+1}: {frame_name}.png")
                else:
                    print(f"   ❌ Failed to load: {frame_name}.png")
            else:
                print(f"   ❌ Not found: {frame_path}")
        
        return panel_images, bubbles
    
    def resize_panel_to_square(self, image):
        """Resize panel to square maintaining aspect ratio"""
        h, w = image.shape[:2]
        
        # Make it square by cropping to center
        if w > h:
            # Wider image - crop width
            start_x = (w - h) // 2
            cropped = image[:, start_x:start_x + h]
        elif h > w:
            # Taller image - crop height
            start_y = (h - w) // 2
            cropped = image[start_y:start_y + w, :]
        else:
            # Already square
            cropped = image
        
        # Resize to panel size
        resized = cv2.resize(cropped, (self.panel_size, self.panel_size), 
                           interpolation=cv2.INTER_LANCZOS4)
        
        return resized
    
    def create_stitched_image(self, panel_images, bubbles):
        """Create single stitched image with 4 panels and bubbles"""
        print(f"\n🔲 STITCHING 4 PANELS INTO SINGLE IMAGE")
        print("=" * 50)
        
        if len(panel_images) < 4:
            print(f"❌ Need 4 panels, got {len(panel_images)}")
            return None
        
        # Create square canvas
        canvas_size = self.output_size
        canvas = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
        canvas.fill(255)  # White background
        
        # Resize panels to squares
        resized_panels = []
        for i, panel_img in enumerate(panel_images[:4]):
            resized = self.resize_panel_to_square(panel_img)
            resized_panels.append(resized)
            print(f"   ✅ Resized panel {i+1} to {self.panel_size}x{self.panel_size}")
        
        # Position panels in 2x2 grid - NO GAPS
        positions = [
            (0, 0),                    # Top-left
            (self.panel_size, 0),      # Top-right
            (0, self.panel_size),      # Bottom-left
            (self.panel_size, self.panel_size)  # Bottom-right
        ]
        
        # Place panels on canvas
        for i, (panel, (x, y)) in enumerate(zip(resized_panels, positions)):
            canvas[y:y + self.panel_size, x:x + self.panel_size] = panel
            print(f"   📍 Placed panel {i+1} at position ({x}, {y})")
        
        # Convert to PIL for bubble drawing
        canvas_pil = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        
        # Add bubbles
        canvas_with_bubbles = self.add_bubbles_to_image(canvas_pil, bubbles)
        
        # Convert back to OpenCV format
        final_image = cv2.cvtColor(np.array(canvas_with_bubbles), cv2.COLOR_RGB2BGR)
        
        print(f"✅ Created stitched image: {canvas_size}x{canvas_size}")
        return final_image
    
    def add_bubbles_to_image(self, image, bubbles):
        """Add speech bubbles directly to the image"""
        print(f"\n💬 ADDING {len(bubbles)} BUBBLES TO IMAGE")
        print("=" * 40)
        
        draw = ImageDraw.Draw(image)
        
        # Try to load a font
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Panel positions for bubble placement - NO GAPS
        panel_positions = [
            (0, 0),                    # Top-left
            (self.panel_size, 0),      # Top-right
            (0, self.panel_size),      # Bottom-left
            (self.panel_size, self.panel_size)  # Bottom-right
        ]
        
        # Add each bubble
        for i, bubble in enumerate(bubbles[:4]):  # Only first 4 bubbles
            if i >= len(panel_positions):
                break
            
            panel_x, panel_y = panel_positions[i]
            
            # Calculate bubble position relative to panel
            bubble_x = panel_x + bubble.get('bubble_offset_x', 50)
            bubble_y = panel_y + bubble.get('bubble_offset_y', 50)
            
            # Draw bubble
            self.draw_bubble(draw, bubble_x, bubble_y, bubble.get('dialog', ''), font)
            print(f"   💬 Added bubble {i+1}: '{bubble.get('dialog', '')[:20]}...'")
        
        return image
    
    def draw_bubble(self, draw, x, y, text, font):
        """Draw a speech bubble on the image"""
        if not text or text == "((action-scene))":
            return
        
        # Calculate text size
        if font:
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
        else:
            text_width = len(text) * 8
            text_height = 16
        
        # Bubble dimensions
        padding = 15
        bubble_width = text_width + padding * 2
        bubble_height = text_height + padding * 2
        
        # Ensure bubble stays within bounds
        max_x = self.output_size - bubble_width
        max_y = self.output_size - bubble_height
        x = min(max(x, 0), max_x)
        y = min(max(y, 0), max_y)
        
        # Draw bubble background
        bubble_rect = [x, y, x + bubble_width, y + bubble_height]
        draw.ellipse(bubble_rect, fill='white', outline='black', width=2)
        
        # Draw text
        text_x = x + padding
        text_y = y + padding
        
        if font:
            draw.text((text_x, text_y), text, fill='black', font=font)
        else:
            draw.text((text_x, text_y), text, fill='black')
    
    def stitch_comic_page(self, output_path="stitched_comic_page.png"):
        """Stitch complete comic page with bubbles"""
        print("\n🔲 STITCHING COMPLETE COMIC PAGE")
        print("=" * 60)
        
        # Load panel images and bubble data
        panel_images, bubbles = self.load_panel_images()
        
        if panel_images is None or len(panel_images) < 4:
            print("❌ Could not load 4 panel images")
            return False
        
        # Create stitched image
        stitched_image = self.create_stitched_image(panel_images, bubbles)
        
        if stitched_image is None:
            print("❌ Failed to create stitched image")
            return False
        
        # Save stitched image
        cv2.imwrite(output_path, stitched_image, [
            cv2.IMWRITE_PNG_COMPRESSION, 0,  # No compression
        ])
        
        file_size = os.path.getsize(output_path) / (1024*1024)
        
        print(f"\n🎉 STITCHED COMIC PAGE COMPLETED!")
        print("=" * 50)
        print(f"✅ Combined 4 panels into single square image")
        print(f"💬 Added speech bubbles directly to image")
        print(f"🔲 Output: {self.output_size}x{self.output_size} square")
        print(f"💾 File: {output_path} ({file_size:.1f}MB)")
        print(f"📺 No HTML template needed!")
        
        return True

def stitch_comic_page():
    """Stitch comic page into single image"""
    stitcher = ImageStitcher()
    return stitcher.stitch_comic_page()

if __name__ == "__main__":
    stitch_comic_page()