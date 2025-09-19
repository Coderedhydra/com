"""
Simple 2K Quality Enhancer - Clean, Effective Approach
Focuses on preserving original quality with minimal processing
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import json
import time
import shutil

class Simple2KEnhancer:
    """Simple, effective 2K quality enhancement"""
    
    def __init__(self):
        print("🎯 Simple 2K Quality Enhancer - Clean & Effective")
        # 2K resolution: 2560x1440 total, 1280x720 per panel for 2x2 grid
        self.target_2k_resolution = (2560, 1440)  # Full 2K
        self.panel_2k_size = (1280, 720)  # Per panel 2K
        
    def analyze_original_frames(self, frames_dir="frames/final"):
        """Analyze original frame quality without over-processing"""
        print(f"\n📸 ANALYZING ORIGINAL FRAMES")
        print("=" * 50)
        
        if not os.path.exists(frames_dir):
            print(f"❌ Frames directory not found: {frames_dir}")
            return []
        
        frame_files = [f for f in os.listdir(frames_dir) 
                      if f.lower().endswith('.png') and f.startswith('frame')]
        frame_files.sort()
        
        if not frame_files:
            print("❌ No frame files found")
            return []
        
        print(f"📁 Found {len(frame_files)} original frames")
        
        # Simple quality analysis - keep it minimal
        frame_quality = {}
        for frame_file in frame_files:
            frame_path = os.path.join(frames_dir, frame_file)
            quality = self.simple_quality_check(frame_path)
            frame_quality[frame_file] = quality
        
        # Select best frames without over-analyzing
        sorted_frames = sorted(frame_quality.items(), key=lambda x: x[1], reverse=True)
        
        print(f"✅ Frame analysis complete")
        return [frame[0] for frame in sorted_frames]
    
    def simple_quality_check(self, frame_path):
        """Simple, fast quality check"""
        try:
            img = cv2.imread(frame_path)
            if img is None:
                return 0
            
            # Simple metrics only
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Basic sharpness
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Basic contrast
            contrast = gray.std()
            
            # Simple score
            return sharpness + contrast
            
        except:
            return 0
    
    def enhance_to_clean_2k(self, frame_path, output_path=None):
        """Clean 2K enhancement without over-processing"""
        try:
            # Load original image
            img = cv2.imread(frame_path)
            if img is None:
                return False
            
            original_h, original_w = img.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Target 2K panel size
            target_w, target_h = self.panel_2k_size
            
            # Simple, clean resize to 2K
            if original_w != target_w or original_h != target_h:
                # Use best single-step resize
                enhanced = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
            else:
                enhanced = img.copy()
            
            # Minimal enhancement - just what's necessary
            enhanced = self.minimal_clean_enhancement(enhanced)
            
            # Save with optimal quality
            if output_path is None:
                output_path = frame_path
            
            # Use optimal PNG settings
            cv2.imwrite(output_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 1,  # Light compression for balance
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            final_h, final_w = enhanced.shape[:2]
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"   Enhanced: {final_w}x{final_h} ({file_size:.1f}MB)")
            return True
            
        except Exception as e:
            print(f"❌ Enhancement failed: {e}")
            return False
    
    def minimal_clean_enhancement(self, img):
        """Minimal, clean enhancement that preserves quality"""
        # Only essential enhancements
        
        # 1. Light noise reduction (very gentle)
        enhanced = cv2.fastNlMeansDenoisingColored(img, None, 3, 3, 7, 21)
        
        # 2. Gentle contrast enhancement
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Very light CLAHE
        clahe = cv2.createCLAHE(clipLimit=1.2, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # 3. Optional: Very light sharpening if needed
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.02
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        enhanced = cv2.addWeighted(enhanced, 0.98, sharpened, 0.02, 0)
        
        return enhanced
    
    def select_best_frames_for_test(self, all_frames, count=4):
        """Select best frames for test page"""
        if len(all_frames) <= count:
            return all_frames[:count]
        
        # Simple selection - take every nth frame for diversity
        step = len(all_frames) // count
        selected = []
        
        for i in range(count):
            idx = i * step
            if idx < len(all_frames):
                selected.append(all_frames[idx])
        
        # Fill remaining with best quality
        while len(selected) < count and len(selected) < len(all_frames):
            for frame in all_frames:
                if frame not in selected:
                    selected.append(frame)
                    break
        
        return selected[:count]
    
    def create_2k_test_page(self):
        """Create simple 2K test page"""
        print("\n🎯 CREATING 2K TEST PAGE")
        print("=" * 50)
        
        start_time = time.time()
        
        # Step 1: Analyze frames simply
        all_frames = self.analyze_original_frames()
        if not all_frames:
            return False
        
        # Step 2: Select best 4 frames
        selected_frames = self.select_best_frames_for_test(all_frames, 4)
        print(f"📋 Selected frames: {selected_frames}")
        
        # Step 3: Enhance to clean 2K
        print(f"\n🔥 ENHANCING TO CLEAN 2K QUALITY")
        print("=" * 40)
        
        enhanced_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if os.path.exists(frame_path):
                if self.enhance_to_clean_2k(frame_path):
                    enhanced_count += 1
        
        if enhanced_count == 0:
            print("❌ No frames enhanced")
            return False
        
        # Step 4: Create test page data
        test_page = self.create_test_page_data(selected_frames)
        
        # Step 5: Save everything
        self.save_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 2K TEST PAGE COMPLETED!")
        print("=" * 40)
        print(f"✅ Enhanced {enhanced_count}/4 frames to clean 2K")
        print(f"🎯 Quality: 2K (1280x720 per panel)")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"🌐 View at: http://localhost:5000/comic")
        
        return True
    
    def create_test_page_data(self, selected_frames):
        """Create simple test page data"""
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "2k_test_page",
                "quality": "2K",
                "panel_count": len(selected_frames),
                "panel_resolution": "1280x720",
                "creation_time": time.time(),
                "enhancement_type": "clean_2k"
            }
        }
        
        # Simple bubble positions for 2x2 grid
        bubble_data = [
            {"text": "2K Quality Panel 1", "x": 50, "y": 50},
            {"text": "2K Quality Panel 2", "x": 50, "y": 50},
            {"text": "2K Quality Panel 3", "x": 50, "y": 50},
            {"text": "2K Quality Panel 4", "x": 50, "y": 50}
        ]
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "2K",
                "resolution": "1280x720"
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
    
    def save_test_page(self, test_page, selected_frames):
        """Save test page and copy frames"""
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
        
        print("✅ Test page saved successfully")
    
    def create_full_2k_comic(self, target_pages=12):
        """Create full comic with clean 2K quality"""
        print(f"\n📚 CREATING FULL {target_pages}-PAGE 2K COMIC")
        print("=" * 60)
        
        start_time = time.time()
        
        # Get all frames
        all_frames = self.analyze_original_frames()
        if not all_frames:
            return False
        
        # Calculate frames needed
        panels_needed = target_pages * 4  # 4 panels per page
        
        # Select frames for full comic
        if len(all_frames) >= panels_needed:
            # Take evenly distributed frames
            step = len(all_frames) // panels_needed
            selected_frames = [all_frames[i * step] for i in range(panels_needed)]
        else:
            # Use all frames and repeat if needed
            selected_frames = all_frames.copy()
            while len(selected_frames) < panels_needed:
                selected_frames.extend(all_frames)
            selected_frames = selected_frames[:panels_needed]
        
        print(f"📋 Selected {len(selected_frames)} frames for {target_pages} pages")
        
        # Enhance all selected frames
        print(f"\n🔥 ENHANCING ALL FRAMES TO 2K")
        print("=" * 40)
        
        enhanced_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            
            if os.path.exists(frame_path):
                if i % 10 == 1:  # Show progress every 10 frames
                    print(f"Processing frames {i}-{min(i+9, len(selected_frames))}...")
                
                if self.enhance_to_clean_2k(frame_path):
                    enhanced_count += 1
        
        # Create pages
        pages = []
        for page_num in range(target_pages):
            start_idx = page_num * 4
            end_idx = start_idx + 4
            page_frames = selected_frames[start_idx:end_idx]
            
            if page_frames:
                page = self.create_comic_page(page_frames, page_num + 1)
                pages.append(page)
        
        # Save full comic
        self.save_full_comic(pages, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 FULL 2K COMIC COMPLETED!")
        print("=" * 40)
        print(f"📚 Generated {len(pages)} pages")
        print(f"✅ Enhanced {enhanced_count} frames to 2K")
        print(f"🎯 Quality: Clean 2K (1280x720 per panel)")
        print(f"⏱️ Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        
        return True
    
    def create_comic_page(self, page_frames, page_number):
        """Create a single comic page"""
        page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_number": page_number,
                "quality": "2K",
                "panel_count": len(page_frames)
            }
        }
        
        for i, frame_file in enumerate(page_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "2K"
            })
            
            # Simple bubble
            page["bubbles"].append({
                "dialog": f"Page {page_number} Panel {i+1}",
                "emotion": "normal",
                "bubble_offset_x": 50,
                "bubble_offset_y": 50,
                "tail_offset_x": 20,
                "tail_offset_y": 25,
                "tail_deg": 45
            })
        
        return page
    
    def save_full_comic(self, pages, selected_frames):
        """Save full comic data"""
        # Save pages
        os.makedirs('output_template', exist_ok=True)
        with open('output_template/page.js', 'w') as f:
            f.write('var pages = ')
            json.dump(pages, f, indent=4)
        
        os.makedirs('static/comic', exist_ok=True)
        with open('static/comic/page.js', 'w') as f:
            f.write('var pages = ')
            json.dump(pages, f, indent=4)
        
        # Copy all frames
        os.makedirs('static/comic/frames/final', exist_ok=True)
        for frame in selected_frames:
            src = os.path.join('frames/final', frame)
            dst = os.path.join('static/comic/frames/final', frame)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        # Save metadata
        metadata = {
            "total_pages": len(pages),
            "total_frames": len(selected_frames),
            "quality": "2K",
            "panel_resolution": "1280x720",
            "enhancement_type": "clean_minimal",
            "generation_time": time.time()
        }
        
        with open('output_template/2k_comic_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=4)

def create_2k_test_page():
    """Create 2K test page"""
    enhancer = Simple2KEnhancer()
    return enhancer.create_2k_test_page()

def create_full_2k_comic():
    """Create full 2K comic"""
    enhancer = Simple2KEnhancer()
    return enhancer.create_full_2k_comic()

if __name__ == "__main__":
    create_2k_test_page()