"""
Simple Image Stitcher - Robust 4-panel combination
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import json

class SimpleStitcher:
    """Simple, robust image stitcher"""
    
    def __init__(self):
        print("🔲 Simple Stitcher - 4 Equal Square Parts")
        self.square_size = 2000  # Total square size
        self.panel_size = 1000   # Each panel size (square_size / 2)
        
    def get_latest_frames(self, count=4):
        """Get the latest generated frames"""
        frames_dir = "frames/final"
        
        if not os.path.exists(frames_dir):
            print(f"❌ Frames directory not found: {frames_dir}")
            return []
        
        # Get all frame files
        frame_files = [f for f in os.listdir(frames_dir) 
                      if f.lower().endswith('.png') and f.startswith('frame')]
        frame_files.sort()
        
        if len(frame_files) < count:
            print(f"❌ Need {count} frames, found {len(frame_files)}")
            return []
        
        # Take first 4 frames
        selected = frame_files[:count]
        print(f"📋 Selected frames: {selected}")
        
        return selected
    
    def load_and_resize_panel(self, frame_file, frames_dir="frames/final"):
        """Load and resize panel to square"""
        frame_path = os.path.join(frames_dir, frame_file)
        
        # Load image
        img = cv2.imread(frame_path)
        if img is None:
            print(f"❌ Could not load: {frame_file}")
            return None
        
        h, w = img.shape[:2]
        print(f"   Loading {frame_file}: {w}x{h}")
        
        # Resize to square panel
        resized = cv2.resize(img, (self.panel_size, self.panel_size), 
                           interpolation=cv2.INTER_LANCZOS4)
        
        print(f"   Resized to: {self.panel_size}x{self.panel_size}")
        return resized
    
    def create_square_comic(self, output_path="static/stitched_comic_square.png"):
        """Create square comic with 4 panels"""
        print(f"\n🔲 CREATING SQUARE COMIC")
        print("=" * 50)
        
        # Get frames
        selected_frames = self.get_latest_frames(4)
        if not selected_frames:
            return False
        
        # Load and resize panels
        panels = []
        for i, frame_file in enumerate(selected_frames):
            panel = self.load_and_resize_panel(frame_file)
            if panel is not None:
                panels.append(panel)
                print(f"   ✅ Panel {i+1} ready")
            else:
                print(f"   ❌ Panel {i+1} failed")
                return False
        
        if len(panels) != 4:
            print(f"❌ Need 4 panels, got {len(panels)}")
            return False
        
        # Create square canvas
        canvas = np.zeros((self.square_size, self.square_size, 3), dtype=np.uint8)
        canvas.fill(255)  # White background
        
        # Place panels in 2x2 grid
        print(f"\n🔲 PLACING PANELS IN SQUARE")
        print("=" * 30)
        
        # Top-left
        canvas[0:self.panel_size, 0:self.panel_size] = panels[0]
        print("   📍 Panel 1: Top-left")
        
        # Top-right  
        canvas[0:self.panel_size, self.panel_size:self.square_size] = panels[1]
        print("   📍 Panel 2: Top-right")
        
        # Bottom-left
        canvas[self.panel_size:self.square_size, 0:self.panel_size] = panels[2]
        print("   📍 Panel 3: Bottom-left")
        
        # Bottom-right
        canvas[self.panel_size:self.square_size, self.panel_size:self.square_size] = panels[3]
        print("   📍 Panel 4: Bottom-right")
        
        # Add simple text labels (instead of complex bubbles)
        canvas_with_text = self.add_simple_labels(canvas)
        
        # Save final image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cv2.imwrite(output_path, canvas_with_text, [
            cv2.IMWRITE_PNG_COMPRESSION, 0,
        ])
        
        file_size = os.path.getsize(output_path) / (1024*1024)
        
        print(f"\n🎉 SQUARE COMIC CREATED!")
        print("=" * 30)
        print(f"✅ 4 panels stitched into perfect square")
        print(f"🔲 Size: {self.square_size}x{self.square_size}")
        print(f"💾 File: {output_path} ({file_size:.1f}MB)")
        
        return True
    
    def add_simple_labels(self, canvas):
        """Add simple text labels to panels"""
        # Convert to PIL for text drawing
        pil_image = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        # Try to get a font
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
        except:
            try:
                font = ImageFont.load_default()
            except:
                font = None
        
        # Add labels to each panel
        labels = ["Panel 1", "Panel 2", "Panel 3", "Panel 4"]
        positions = [
            (50, 50),                           # Top-left
            (self.panel_size + 50, 50),         # Top-right
            (50, self.panel_size + 50),         # Bottom-left
            (self.panel_size + 50, self.panel_size + 50)  # Bottom-right
        ]
        
        for i, (label, (x, y)) in enumerate(zip(labels, positions)):
            # Draw background for text
            if font:
                bbox = draw.textbbox((x, y), label, font=font)
                draw.rectangle([bbox[0]-5, bbox[1]-5, bbox[2]+5, bbox[3]+5], 
                             fill='white', outline='black', width=2)
                draw.text((x, y), label, fill='black', font=font)
            else:
                draw.rectangle([x-5, y-5, x+80, y+25], 
                             fill='white', outline='black', width=2)
                draw.text((x, y), label, fill='black')
            
            print(f"   💬 Added label: {label}")
        
        # Convert back to OpenCV
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

def create_stitched_square():
    """Create stitched square comic"""
    stitcher = SimpleStitcher()
    return stitcher.create_square_comic()

if __name__ == "__main__":
    create_stitched_square()