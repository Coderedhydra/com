"""
Comic Ratio Enhancer - Perfect comic book proportions for 2x2 grid
Uses standard comic book aspect ratios for optimal visual experience
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import json
import time
import shutil

class ComicRatioEnhancer:
    """Enhance images using perfect comic book ratios"""
    
    def __init__(self):
        print("📚 Comic Ratio Enhancer - Perfect Comic Book Proportions")
        
        # Standard comic book ratios (based on industry standards)
        # Most comics use 2:3 ratio (width:height) for panels
        self.comic_panel_ratio = 2/3  # Classic comic panel ratio
        
        # Perfect square page dimensions for 2x2 grid
        self.page_width = 1000
        self.page_height = 1000   # Perfect square page (1000:1000)
        
        # Each panel dimensions (perfect squares)
        self.panel_width = 500   # page_width / 2
        self.panel_height = 500  # page_height / 2 (perfect square panels)
        
        print(f"📐 Comic page: {self.page_width}×{self.page_height}")
        print(f"📐 Each panel: {self.panel_width}×{self.panel_height}")
        print(f"📐 Panel ratio: {self.panel_width/self.panel_height:.3f} (1:1 perfect squares)")
        
    def enhance_to_comic_ratio(self, frame_path, output_path=None):
        """Enhance frame to perfect square ratio (500×500)"""
        try:
            # Load image
            img = cv2.imread(frame_path)
            if img is None:
                return False
            
            original_h, original_w = img.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Resize to perfect square panels (400×400)
            enhanced = cv2.resize(img, (self.panel_width, self.panel_height), 
                                interpolation=cv2.INTER_LANCZOS4)
            
            # Apply comic-specific enhancement
            enhanced = self.apply_comic_enhancement(enhanced)
            
            # Save with high quality
            if output_path is None:
                output_path = frame_path
            
            cv2.imwrite(output_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,
            ])
            
            final_h, final_w = enhanced.shape[:2]
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"   Comic Ratio: {final_w}x{final_h} ({file_size:.1f}MB)")
            return True
            
        except Exception as e:
            print(f"❌ Enhancement failed: {e}")
            return False
    
    def apply_comic_enhancement(self, img):
        """Apply comic-specific enhancement for optimal readability"""
        # Step 1: Gentle noise reduction (preserve comic detail)
        enhanced = cv2.fastNlMeansDenoisingColored(img, None, 2, 2, 7, 21)
        
        # Step 2: Comic-optimized contrast
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Adaptive contrast for comic readability
        clahe = cv2.createCLAHE(clipLimit=1.4, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Step 3: Edge enhancement for comic clarity
        enhanced = cv2.edgePreservingFilter(enhanced, flags=2, sigma_s=25, sigma_r=0.3)
        
        # Step 4: Comic color enhancement
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Boost saturation for comic vibrancy
        s = cv2.add(s, 10)
        s = np.clip(s, 0, 255)
        
        enhanced = cv2.merge([h, s, v])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_HSV2BGR)
        
        # Step 5: Light comic sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.04
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        enhanced = cv2.addWeighted(enhanced, 0.96, sharpened, 0.04, 0)
        
        return enhanced
    
    def create_comic_ratio_test_page(self):
        """Create test page with perfect comic ratios"""
        print("\n🔲 CREATING PERFECT SQUARE TEST PAGE (500×500)")
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
        
        # Select best 4 frames for comic
        selected_frames = self.select_best_comic_frames(frame_files, 4)
        print(f"📋 Selected frames for comic ratio: {selected_frames}")
        
        # Enhance to perfect squares
        print(f"\n🔲 ENHANCING TO PERFECT SQUARES (500×500)")
        print("=" * 60)
        
        enhanced_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if os.path.exists(frame_path):
                if self.enhance_to_comic_ratio(frame_path):
                    enhanced_count += 1
        
        if enhanced_count == 0:
            print("❌ No frames enhanced")
            return False
        
        # Create comic ratio page data
        test_page = self.create_comic_ratio_page_data(selected_frames)
        
        # Save everything
        self.save_comic_ratio_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 COMIC RATIO TEST PAGE COMPLETED!")
        print("=" * 60)
        print(f"✅ Enhanced {enhanced_count}/4 frames to comic ratio")
        print(f"📚 Template: {self.page_width}×{self.page_height} (perfect comic page)")
        print(f"📐 Each panel: {self.panel_width}×{self.panel_height} (2:3 comic ratio)")
        print(f"🔲 Zero gaps - perfect comic book layout")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"🌐 View at: http://localhost:5000/comic")
        
        return True
    
    def select_best_comic_frames(self, frame_files, count):
        """Select best frames for comic book layout"""
        # For comic books, we want diverse, high-quality frames
        if len(frame_files) <= count:
            return frame_files[:count]
        
        # Select frames with good distribution
        step = len(frame_files) // count
        selected = []
        
        for i in range(count):
            idx = i * step
            if idx < len(frame_files):
                selected.append(frame_files[idx])
        
        return selected[:count]
    
    def create_comic_ratio_page_data(self, selected_frames):
        """Create page data for comic ratio template"""
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "comic_ratio_test_page",
                "quality": "Comic Ratio",
                "panel_count": len(selected_frames),
                "template_size": f"{self.page_width}x{self.page_height}",
                "panel_size": f"{self.panel_width}x{self.panel_height}",
                "panel_ratio": "2:3 (comic standard)",
                "creation_time": time.time(),
                "enhancement_type": "comic_ratio_enhancement"
            }
        }
        
        # Comic-style bubble positions
        bubble_data = [
            {"text": "Comic Panel 1", "x": 60, "y": 80},
            {"text": "Comic Panel 2", "x": 60, "y": 80},
            {"text": "Comic Panel 3", "x": 60, "y": 80},
            {"text": "Comic Panel 4", "x": 60, "y": 80}
        ]
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "Comic Ratio",
                "dimensions": f"{self.panel_width}x{self.panel_height}",
                "ratio": "2:3"
            })
            
            # Comic-style bubble
            bubble = bubble_data[i] if i < len(bubble_data) else bubble_data[0]
            test_page["bubbles"].append({
                "dialog": bubble["text"],
                "emotion": "normal",
                "bubble_offset_x": bubble["x"],
                "bubble_offset_y": bubble["y"],
                "tail_offset_x": 25,
                "tail_offset_y": 35,
                "tail_deg": 45
            })
        
        return test_page
    
    def save_comic_ratio_test_page(self, test_page, selected_frames):
        """Save comic ratio test page"""
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
        
        print("✅ Comic ratio test page saved successfully")

def create_comic_ratio_test_page():
    """Create comic ratio test page"""
    enhancer = ComicRatioEnhancer()
    return enhancer.create_comic_ratio_test_page()

if __name__ == "__main__":
    create_comic_ratio_test_page()