"""
Preview System for Amit Comic
Shows image selection and creates test page before full generation
"""

import os
import json
import shutil
from backend.class_def import Page, panel, bubble
import cv2
import numpy as np

class ComicPreviewSystem:
    """Preview system for comic generation"""
    
    def __init__(self):
        print("👁️ Comic Preview System - Test Before Full Generation")
        
    def show_selected_images(self, frames_dir="frames/final"):
        """Show which images will be selected for the comic"""
        print("\n🔍 STEP 1: Showing Selected Images...")
        print("=" * 50)
        
        if not os.path.exists(frames_dir):
            print(f"❌ Frames directory not found: {frames_dir}")
            return []
        
        # Get all frame files
        frame_files = [f for f in os.listdir(frames_dir) 
                      if f.lower().endswith('.png') and f.startswith('frame')]
        frame_files.sort()
        
        total_frames = len(frame_files)
        print(f"📸 Total frames available: {total_frames}")
        
        if total_frames == 0:
            print("❌ No frame files found")
            return []
        
        # Select frames for comic (every nth frame for variety)
        if total_frames >= 48:
            # Select every nth frame to get 48 frames
            step = total_frames // 48
            selected_frames = frame_files[::step][:48]
        else:
            # Use all frames and repeat if needed
            selected_frames = frame_files.copy()
            while len(selected_frames) < 48:
                selected_frames.extend(frame_files)
            selected_frames = selected_frames[:48]
        
        print(f"📋 Selected {len(selected_frames)} frames for comic:")
        print("   First page (4 panels):")
        for i in range(min(4, len(selected_frames))):
            frame_path = os.path.join(frames_dir, selected_frames[i])
            if os.path.exists(frame_path):
                # Get image info
                img = cv2.imread(frame_path)
                if img is not None:
                    h, w = img.shape[:2]
                    file_size = os.path.getsize(frame_path) / 1024  # KB
                    print(f"   Panel {i+1}: {selected_frames[i]} ({w}x{h}, {file_size:.1f}KB)")
                else:
                    print(f"   Panel {i+1}: {selected_frames[i]} (could not read)")
            else:
                print(f"   Panel {i+1}: {selected_frames[i]} (file not found)")
        
        if len(selected_frames) > 4:
            print(f"   ... and {len(selected_frames)-4} more frames for remaining pages")
        
        return selected_frames
    
    def enhance_test_images(self, selected_frames, frames_dir="frames/final"):
        """Enhance the first 4 images for testing"""
        print("\n🔥 STEP 2: Enhancing Test Images (4x Quality)...")
        print("=" * 50)
        
        test_frames = selected_frames[:4]
        
        for i, frame_file in enumerate(test_frames, 1):
            frame_path = os.path.join(frames_dir, frame_file)
            print(f"\n📸 Enhancing Panel {i}: {frame_file}")
            
            try:
                # Load image
                img = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                if img is None:
                    print(f"❌ Could not load {frame_file}")
                    continue
                
                h, w = img.shape[:2]
                print(f"   Original: {w}x{h}")
                
                # 4x enhancement
                enhanced = self.apply_4x_enhancement(img)
                
                # Save enhanced image
                cv2.imwrite(frame_path, enhanced, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                
                final_h, final_w = enhanced.shape[:2]
                file_size = os.path.getsize(frame_path) / (1024*1024)  # MB
                print(f"   Enhanced: {final_w}x{final_h} ({file_size:.1f}MB)")
                
            except Exception as e:
                print(f"❌ Enhancement failed for {frame_file}: {e}")
        
        print("\n✅ Test images enhanced successfully!")
        return test_frames
    
    def apply_4x_enhancement(self, img):
        """Apply 4x enhancement to image"""
        h, w = img.shape[:2]
        
        # Multi-step 4x upscaling
        # Step 1: 2x with CUBIC
        img_2x = cv2.resize(img, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
        
        # Step 2: 2x with LANCZOS4 (total 4x)
        img_4x = cv2.resize(img_2x, (w*4, h*4), interpolation=cv2.INTER_LANCZOS4)
        
        # Quality enhancement on 4x image
        # Noise reduction (lighter for 4x)
        img_4x = cv2.fastNlMeansDenoisingColored(img_4x, None, 2, 2, 5, 15)
        
        # Detail enhancement
        img_4x = cv2.bilateralFilter(img_4x, 5, 40, 40)
        
        # Color enhancement
        try:
            from PIL import Image, ImageEnhance
            pil_img = Image.fromarray(cv2.cvtColor(img_4x, cv2.COLOR_BGR2RGB))
            
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.1)
            
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.2)
            
            img_4x = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except:
            pass
        
        # Light sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.03
        sharpened = cv2.filter2D(img_4x, -1, kernel)
        img_4x = cv2.addWeighted(img_4x, 0.97, sharpened, 0.03, 0)
        
        return img_4x
    
    def create_test_page(self, test_frames):
        """Create a single test page with 4 panels"""
        print("\n📄 STEP 3: Creating Test Page (4 Panels)...")
        print("=" * 50)
        
        # Create test page data
        test_page = {
            "panels": [
                {"image": test_frames[0].replace('.png', ''), "row_span": 1, "col_span": 1},
                {"image": test_frames[1].replace('.png', ''), "row_span": 1, "col_span": 1},
                {"image": test_frames[2].replace('.png', ''), "row_span": 1, "col_span": 1},
                {"image": test_frames[3].replace('.png', ''), "row_span": 1, "col_span": 1}
            ],
            "bubbles": [
                {"dialog": "Test Panel 1", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 20, "tail_offset_y": 30, "tail_deg": 45},
                {"dialog": "Test Panel 2", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 30, "tail_offset_y": 40, "tail_deg": 60},
                {"dialog": "Test Panel 3", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 25, "tail_offset_y": 35, "tail_deg": 50},
                {"dialog": "Test Panel 4", "emotion": "normal", "bubble_offset_x": 50, "bubble_offset_y": 50, "tail_offset_x": 35, "tail_offset_y": 45, "tail_deg": 55}
            ]
        }
        
        # Save test page
        test_pages = [test_page]
        
        # Write to page.js files
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
        for frame in test_frames:
            src = os.path.join('frames/final', frame)
            dst = os.path.join('static/comic/frames/final', frame)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        print("✅ Test page created successfully!")
        print("📄 1 page with 4 panels ready for testing")
        print(f"🖼️ Using frames: {', '.join(test_frames)}")
        
        return test_page
    
    def generate_preview(self):
        """Generate preview with selected images and test page"""
        print("🎬 Amit Comic - Preview Generation")
        print("=" * 60)
        
        # Step 1: Show selected images
        selected_frames = self.show_selected_images()
        if not selected_frames:
            return False
        
        # Step 2: Enhance test images (first 4)
        test_frames = self.enhance_test_images(selected_frames)
        if not test_frames:
            return False
        
        # Step 3: Create test page
        test_page = self.create_test_page(test_frames)
        if not test_page:
            return False
        
        print("\n🎉 PREVIEW READY!")
        print("=" * 30)
        print("✅ Image selection complete")
        print("✅ 4x quality enhancement applied to test images")
        print("✅ Test page created with 4 panels")
        print("\n🌐 View your test page at: http://localhost:5000/comic")
        print("📋 If it looks good, you can generate all 12 pages")
        
        return True

def create_comic_preview():
    """Create comic preview"""
    preview_system = ComicPreviewSystem()
    return preview_system.generate_preview()

if __name__ == "__main__":
    create_comic_preview()