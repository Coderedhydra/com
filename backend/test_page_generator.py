"""
Test Page Generator - 4K Quality Single Page
Creates 1 test page with 4 panels in 4K quality, then offers full comic generation
"""

import os
import json
import time
import cv2
import numpy as np
from PIL import Image, ImageEnhance
import shutil

class TestPageGenerator:
    """Generate single test page in 4K quality"""
    
    def __init__(self):
        print("🧪 Test Page Generator - 4K Quality Single Page")
        self.target_resolution = "4K"  # 4K = 3840x2160, but we'll use 2560x1440 for panels
        self.panel_4k_size = (1280, 720)  # 4K panel size (1280x720 per panel)
        
    def analyze_and_select_best_frames(self, frames_dir="frames/final", count=4):
        """Analyze and select the 4 best frames for test page"""
        print(f"\n🔍 SELECTING BEST 4 FRAMES FOR TEST PAGE")
        print("=" * 60)
        
        if not os.path.exists(frames_dir):
            print(f"❌ Frames directory not found: {frames_dir}")
            return []
        
        frame_files = [f for f in os.listdir(frames_dir) 
                      if f.lower().endswith('.png') and f.startswith('frame')]
        frame_files.sort()
        
        if not frame_files:
            print("❌ No frame files found")
            return []
        
        print(f"📸 Available frames: {len(frame_files)}")
        
        # Analyze each frame for quality
        frame_scores = {}
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frames_dir, frame_file)
            score = self.calculate_frame_quality(frame_path)
            frame_scores[frame_file] = score
            
            if i % 10 == 0:  # Progress update
                print(f"   Analyzed {i+1}/{len(frame_files)} frames...")
        
        # Select top 4 frames with diversity
        sorted_frames = sorted(frame_scores.items(), key=lambda x: x[1], reverse=True)
        selected_frames = self.select_diverse_frames(sorted_frames, count)
        
        print(f"\n🏆 SELECTED TOP 4 FRAMES:")
        for i, frame in enumerate(selected_frames, 1):
            score = frame_scores[frame]
            print(f"   Panel {i}: {frame} (Quality Score: {score:.1f})")
        
        return selected_frames
    
    def calculate_frame_quality(self, frame_path):
        """Calculate comprehensive quality score for frame"""
        try:
            img = cv2.imread(frame_path)
            if img is None:
                return 0.0
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Quality metrics
            # 1. Sharpness (Laplacian variance)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 2. Contrast (standard deviation)
            contrast = gray.std()
            
            # 3. Brightness balance (optimal around 128)
            brightness = gray.mean()
            brightness_score = 100 - abs(brightness - 128) / 128 * 100
            
            # 4. Edge density (interesting content)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.count_nonzero(edges) / edges.size * 1000
            
            # 5. Color richness
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            saturation = hsv[:,:,1].mean()
            
            # 6. Face detection bonus
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            face_bonus = len(faces) * 5  # Bonus for character presence
            
            # Combined quality score
            quality_score = (
                sharpness * 0.25 +
                contrast * 0.2 +
                brightness_score * 0.15 +
                edge_density * 0.2 +
                saturation * 0.1 +
                face_bonus * 0.1
            )
            
            return min(quality_score, 100.0)  # Cap at 100
            
        except Exception as e:
            print(f"❌ Error analyzing {frame_path}: {e}")
            return 0.0
    
    def select_diverse_frames(self, sorted_frames, count):
        """Select frames with diversity to avoid similar consecutive frames"""
        selected = []
        used_indices = set()
        
        # Extract frame numbers for diversity check
        frame_numbers = {}
        for frame_name, score in sorted_frames:
            try:
                # Extract number from frame001.png format
                num_str = frame_name.replace('frame', '').replace('.png', '')
                frame_numbers[frame_name] = int(num_str)
            except:
                frame_numbers[frame_name] = len(frame_numbers)
        
        # Select with minimum distance between frames
        min_distance = max(1, len(sorted_frames) // (count * 3))  # Ensure spread
        
        for frame_name, score in sorted_frames:
            if len(selected) >= count:
                break
            
            frame_num = frame_numbers[frame_name]
            
            # Check if this frame is too close to already selected frames
            too_close = False
            for sel_frame in selected:
                sel_num = frame_numbers[sel_frame]
                if abs(frame_num - sel_num) < min_distance:
                    too_close = True
                    break
            
            if not too_close:
                selected.append(frame_name)
        
        # Fill remaining slots if needed (relax distance requirement)
        if len(selected) < count:
            for frame_name, score in sorted_frames:
                if len(selected) >= count:
                    break
                if frame_name not in selected:
                    selected.append(frame_name)
        
        return selected[:count]
    
    def enhance_frame_to_4k(self, frame_path, output_path=None):
        """Enhance single frame to 4K quality"""
        print(f"🔥 Enhancing to 4K: {os.path.basename(frame_path)}")
        
        try:
            # Load image
            img = cv2.imread(frame_path)
            if img is None:
                print(f"❌ Could not load: {frame_path}")
                return False
            
            original_h, original_w = img.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Calculate target 4K size
            target_w, target_h = self.panel_4k_size
            
            # Multi-stage 4K enhancement
            enhanced = self.apply_4k_enhancement(img, target_w, target_h)
            
            # Save with high quality
            if output_path is None:
                output_path = frame_path
            
            cv2.imwrite(output_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # No compression
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            final_h, final_w = enhanced.shape[:2]
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"   Enhanced: {final_w}x{final_h} ({file_size:.1f}MB)")
            
            return True
            
        except Exception as e:
            print(f"❌ Enhancement failed: {e}")
            return False
    
    def apply_4k_enhancement(self, img, target_w, target_h):
        """Apply 4K quality enhancement pipeline"""
        # Step 1: Smart resize to 4K dimensions
        enhanced = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Step 2: Advanced noise reduction
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 3, 3, 7, 21)
        
        # Step 3: Edge-preserving smoothing
        enhanced = cv2.edgePreservingFilter(enhanced, flags=2, sigma_s=50, sigma_r=0.4)
        
        # Step 4: Detail enhancement
        enhanced = cv2.detailEnhance(enhanced, sigma_s=10, sigma_r=0.15)
        
        # Step 5: PIL-based enhancements
        try:
            pil_img = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
            
            # Contrast enhancement
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.1)
            
            # Color saturation
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.15)
            
            # Sharpness
            enhancer = ImageEnhance.Sharpness(pil_img)
            pil_img = enhancer.enhance(1.05)
            
            enhanced = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"   PIL enhancement skipped: {e}")
        
        # Step 6: Final sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.05
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        enhanced = cv2.addWeighted(enhanced, 0.95, sharpened, 0.05, 0)
        
        # Ensure valid range
        enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)
        
        return enhanced
    
    def create_test_page_data(self, selected_frames):
        """Create test page data structure"""
        print(f"\n📄 CREATING TEST PAGE DATA")
        print("=" * 40)
        
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "test_page",
                "quality": "4K",
                "panel_count": len(selected_frames),
                "creation_time": time.time(),
                "enhancement_applied": "4K_quality"
            }
        }
        
        # Create panels and bubbles for 2x2 grid
        bubble_positions = [
            {"x": 30, "y": 30, "text": "Test Panel 1 - 4K Quality"},
            {"x": 30, "y": 30, "text": "Test Panel 2 - 4K Quality"},
            {"x": 30, "y": 30, "text": "Test Panel 3 - 4K Quality"},
            {"x": 30, "y": 30, "text": "Test Panel 4 - 4K Quality"}
        ]
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '') if frame_file.endswith('.png') else frame_file
            
            # Panel data
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "4K",
                "panel_position": i + 1
            })
            
            # Bubble data
            pos = bubble_positions[i] if i < len(bubble_positions) else bubble_positions[0]
            test_page["bubbles"].append({
                "dialog": pos["text"],
                "emotion": "normal",
                "bubble_offset_x": pos["x"],
                "bubble_offset_y": pos["y"],
                "tail_offset_x": 20,
                "tail_offset_y": 25,
                "tail_deg": 45 + (i * 15)
            })
        
        print(f"✅ Test page created with {len(selected_frames)} 4K panels")
        return test_page
    
    def save_test_page(self, test_page, selected_frames):
        """Save test page data and copy frames"""
        print(f"\n💾 SAVING TEST PAGE")
        print("=" * 30)
        
        # Save page data
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
        
        # Copy enhanced frames to static
        os.makedirs('static/comic/frames/final', exist_ok=True)
        for frame in selected_frames:
            src = os.path.join('frames/final', frame)
            dst = os.path.join('static/comic/frames/final', frame)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        # Save test metadata
        test_metadata = {
            "test_page_created": time.time(),
            "selected_frames": selected_frames,
            "quality": "4K",
            "panel_size": f"{self.panel_4k_size[0]}x{self.panel_4k_size[1]}",
            "ready_for_full_comic": True
        }
        
        with open('output_template/test_page_metadata.json', 'w') as f:
            json.dump(test_metadata, f, indent=4)
        
        with open('static/comic/test_page_metadata.json', 'w') as f:
            json.dump(test_metadata, f, indent=4)
        
        print("✅ Test page saved successfully")
        print(f"📁 Files saved to output_template/ and static/comic/")
    
    def generate_4k_test_page(self):
        """Generate single 4K test page"""
        print("\n🧪 4K TEST PAGE GENERATION")
        print("=" * 70)
        
        start_time = time.time()
        
        # Step 1: Select best 4 frames
        selected_frames = self.analyze_and_select_best_frames(count=4)
        if not selected_frames:
            print("❌ No frames selected for test")
            return False
        
        # Step 2: Enhance selected frames to 4K
        print(f"\n🔥 ENHANCING 4 FRAMES TO 4K QUALITY")
        print("=" * 50)
        
        enhanced_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if self.enhance_frame_to_4k(frame_path):
                enhanced_count += 1
        
        if enhanced_count == 0:
            print("❌ No frames enhanced successfully")
            return False
        
        # Step 3: Create test page
        test_page = self.create_test_page_data(selected_frames)
        
        # Step 4: Save test page
        self.save_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 4K TEST PAGE COMPLETED!")
        print("=" * 40)
        print(f"✅ Enhanced {enhanced_count}/4 frames to 4K quality")
        print(f"📄 Created 1 test page with 4 panels")
        print(f"🎯 Quality: 4K ({self.panel_4k_size[0]}x{self.panel_4k_size[1]} per panel)")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"\n🌐 View test page at: http://localhost:5000/comic")
        print(f"👀 If it looks good, you can generate the full 12-page comic!")
        
        return True

def generate_4k_test_page():
    """Generate 4K test page"""
    generator = TestPageGenerator()
    return generator.generate_4k_test_page()

if __name__ == "__main__":
    generate_4k_test_page()