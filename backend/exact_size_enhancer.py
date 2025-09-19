"""
Exact Size Enhancer - 400×540 per panel for 800×1080 template
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import json
import time
import shutil

class ExactSizeEnhancer:
    """Enhance images to exact 400×540 size for perfect template fit"""
    
    def __init__(self):
        print("📐 Exact Size Enhancer - 400×540 per panel")
        # Exact template dimensions
        self.template_width = 800
        self.template_height = 1080
        self.panel_width = 400
        self.panel_height = 540
        
    def enhance_to_exact_size(self, frame_path, output_path=None):
        """Enhance frame to exactly 400×540"""
        try:
            # Load image
            img = cv2.imread(frame_path)
            if img is None:
                return False
            
            original_h, original_w = img.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Resize to exact 400×540
            enhanced = cv2.resize(img, (self.panel_width, self.panel_height), 
                                interpolation=cv2.INTER_LANCZOS4)
            
            # Apply quality enhancement
            enhanced = self.apply_quality_enhancement(enhanced)
            
            # Save with high quality
            if output_path is None:
                output_path = frame_path
            
            cv2.imwrite(output_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
            ])
            
            final_h, final_w = enhanced.shape[:2]
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"   Enhanced: {final_w}x{final_h} ({file_size:.1f}MB)")
            return True
            
        except Exception as e:
            print(f"❌ Enhancement failed: {e}")
            return False
    
    def apply_quality_enhancement(self, img):
        """Apply quality enhancement to 400×540 image"""
        # Light noise reduction
        enhanced = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)
        
        # Contrast enhancement
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=1.3, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Light sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.03
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        enhanced = cv2.addWeighted(enhanced, 0.97, sharpened, 0.03, 0)
        
        return enhanced
    
    def create_exact_size_test_page(self):
        """Create test page with exact 400×540 panels"""
        print("\n📐 CREATING EXACT SIZE TEST PAGE (400×540 per panel)")
        print("=" * 70)
        
        start_time = time.time()
        
        # Get frames
        frames_dir = "frames/final"
        if not os.path.exists(frames_dir):
            print(f"❌ Frames directory not found: {frames_dir}")
            return False
        
        frame_files = [f for f in os.listdir(frames_dir) 
                      if f.lower().endswith('.png') and f.startswith('frame')]
        frame_files.sort()
        
        if not frame_files:
            print("❌ No frame files found")
            return False
        
        # Select best 4 frames
        selected_frames = frame_files[:4]
        print(f"📋 Selected frames: {selected_frames}")
        
        # Enhance to exact size
        print(f"\n🔥 ENHANCING TO EXACT 400×540 SIZE")
        print("=" * 50)
        
        enhanced_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if os.path.exists(frame_path):
                if self.enhance_to_exact_size(frame_path):
                    enhanced_count += 1
        
        if enhanced_count == 0:
            print("❌ No frames enhanced")
            return False
        
        # Create test page data
        test_page = self.create_exact_size_page_data(selected_frames)
        
        # Save everything
        self.save_exact_size_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 EXACT SIZE TEST PAGE COMPLETED!")
        print("=" * 50)
        print(f"✅ Enhanced {enhanced_count}/4 frames to exact 400×540")
        print(f"📐 Template: 800×1080 with 4 panels of 400×540")
        print(f"🔲 Perfect fit - no gaps, exact dimensions")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"🌐 View at: http://localhost:5000/comic")
        
        return True
    
    def create_exact_size_page_data(self, selected_frames):
        """Create page data for exact size template"""
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "exact_size_test_page",
                "quality": "400×540 Exact",
                "panel_count": len(selected_frames),
                "template_size": f"{self.template_width}x{self.template_height}",
                "panel_size": f"{self.panel_width}x{self.panel_height}",
                "creation_time": time.time(),
                "enhancement_type": "exact_size_400x540"
            }
        }
        
        # Bubble positions for 400×540 panels
        bubble_data = [
            {"text": "400×540 Panel 1", "x": 50, "y": 50},
            {"text": "400×540 Panel 2", "x": 50, "y": 50},
            {"text": "400×540 Panel 3", "x": 50, "y": 50},
            {"text": "400×540 Panel 4", "x": 50, "y": 50}
        ]
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "400×540 Exact",
                "dimensions": "400x540"
            })
            
            # Bubble
            bubble = bubble_data[i] if i < len(bubble_data) else bubble_data[0]
            test_page["bubbles"].append({
                "dialog": bubble["text"],
                "emotion": "normal",
                "bubble_offset_x": bubble["x"],
                "bubble_offset_y": bubble["y"],
                "tail_offset_x": 20,
                "tail_offset_y": 25,
                "tail_deg": 45
            })
        
        return test_page
    
    def save_exact_size_test_page(self, test_page, selected_frames):
        """Save exact size test page"""
        # Save page data
        test_pages = [test_page]
        
        os.makedirs('output_template', exist_ok=True)
        with open('output_template/page.js', 'w') as f:
            f.write('var pages = ')
            json.dump(test_pages, f, indent=4)
        
        os.makedirs('static/comic', exist_ok=True)
        with open('static/comic/page.js', 'w') as f:
            f.write('var pages = ')
            json.dump(test_pages, f, indent=4)
        
        # Copy frames to static
        os.makedirs('static/comic/frames/final', exist_ok=True)
        for frame in selected_frames:
            src = os.path.join('frames/final', frame)
            dst = os.path.join('static/comic/frames/final', frame)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        print("✅ Exact size test page saved successfully")

def create_exact_size_test_page():
    """Create exact size test page"""
    enhancer = ExactSizeEnhancer()
    return enhancer.create_exact_size_test_page()

if __name__ == "__main__":
    create_exact_size_test_page()