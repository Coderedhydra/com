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
        print("🎯 High Quality Enhancer - Preserve Original Resolution")
        # Use original resolution or enhance it, don't downscale
        self.preserve_original = True
        self.min_panel_size = (1920, 1080)  # Minimum Full HD per panel
        
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
    
    def enhance_to_high_quality(self, frame_path, output_path=None):
        """High quality enhancement preserving or improving original resolution"""
        try:
            # Load original image
            img = cv2.imread(frame_path)
            if img is None:
                return False
            
            original_h, original_w = img.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Determine target size - preserve or enhance original
            if original_w >= 1920 and original_h >= 1080:
                # Original is already good quality, preserve it
                target_w, target_h = original_w, original_h
                print(f"   Preserving original high resolution")
            else:
                # Upscale to minimum Full HD
                target_w, target_h = self.min_panel_size
                print(f"   Upscaling to Full HD: {target_w}x{target_h}")
            
            # Enhance resolution if needed
            if original_w != target_w or original_h != target_h:
                enhanced = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
            else:
                enhanced = img.copy()
            
            # Minimal clean enhancement - preserve quality
            enhanced = self.minimal_clean_enhancement(enhanced)
            
            # Save with maximum quality
            if output_path is None:
                output_path = frame_path
            
            # Use zero compression for maximum quality
            cv2.imwrite(output_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # Zero compression for max quality
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
        """Advanced quality enhancement optimized for comics"""
        # Enhanced processing pipeline for better comic quality
        
        # 1. Advanced noise reduction with color preservation
        enhanced = cv2.fastNlMeansDenoisingColored(img, None, 4, 4, 7, 21)
        
        # 2. Color enhancement and saturation boost for comics
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Boost saturation for more vibrant colors (comic style)
        s = cv2.multiply(s, 1.15)  # 15% saturation boost
        s = np.clip(s, 0, 255).astype(np.uint8)
        
        enhanced = cv2.merge([h, s, v])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_HSV2BGR)
        
        # 3. Advanced contrast enhancement with LAB color space
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Enhanced CLAHE for better contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # 4. Smart sharpening with unsharp mask
        gaussian = cv2.GaussianBlur(enhanced, (0, 0), 1.0)
        unsharp_mask = cv2.addWeighted(enhanced, 1.5, gaussian, -0.5, 0)
        enhanced = cv2.addWeighted(enhanced, 0.7, unsharp_mask, 0.3, 0)
        
        # 5. Final gamma correction for better brightness
        gamma = 1.1
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        enhanced = cv2.LUT(enhanced, table)
        
        return enhanced
    
    def generate_meaningful_dialogue(self, frame_count=4):
        """Generate meaningful dialogue for comic panels"""
        # Try to get actual subtitles if available
        subtitle_dialogue = self.extract_subtitle_dialogue()
        
        if subtitle_dialogue and len(subtitle_dialogue) >= frame_count:
            # Use actual dialogue from subtitles
            return [{"text": dialogue, "x": 50 + (i * 20), "y": 50 + (i * 15)} 
                   for i, dialogue in enumerate(subtitle_dialogue[:frame_count])]
        else:
            # Generate engaging story dialogue if no subtitles
            story_dialogues = [
                "This is where our adventure begins!",
                "Something incredible is about to happen...",
                "The tension builds as we discover the truth.",
                "And here's how our story unfolds!"
            ]
            
            return [{"text": story_dialogues[i] if i < len(story_dialogues) else f"Panel {i+1} story continues...", 
                    "x": 50 + (i * 20), "y": 50 + (i * 15)} 
                   for i in range(frame_count)]
    
    def extract_subtitle_dialogue(self):
        """Extract actual dialogue from subtitle files"""
        import srt
        subtitle_file = 'test1.srt'
        
        try:
            if os.path.exists(subtitle_file):
                with open(subtitle_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                subtitles = list(srt.parse(content))
                dialogue_list = []
                
                for sub in subtitles:
                    if sub.content and sub.content != "((action-scene))":
                        # Clean up the dialogue
                        clean_text = sub.content.strip()
                        if clean_text and len(clean_text) > 3:  # Skip very short text
                            dialogue_list.append(clean_text)
                
                if dialogue_list:
                    print(f"✅ Found {len(dialogue_list)} dialogue entries from subtitles")
                    return dialogue_list
                    
        except Exception as e:
            print(f"⚠️ Could not extract subtitles: {e}")
        
        return []
    
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
    
    def create_high_quality_test_page(self):
        """Create high quality test page preserving original resolution"""
        print("\n🎯 CREATING HIGH QUALITY TEST PAGE")
        print("=" * 50)
        
        start_time = time.time()
        
        # Step 1: Analyze frames simply
        all_frames = self.analyze_original_frames()
        if not all_frames:
            return False
        
        # Step 2: Select best 4 frames
        selected_frames = self.select_best_frames_for_test(all_frames, 4)
        print(f"📋 Selected frames: {selected_frames}")
        
        # Step 3: Enhance preserving/improving original quality
        print(f"\n🔥 ENHANCING TO HIGH QUALITY (PRESERVING ORIGINAL)")
        print("=" * 50)
        
        enhanced_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if os.path.exists(frame_path):
                if self.enhance_to_high_quality(frame_path):
                    enhanced_count += 1
        
        if enhanced_count == 0:
            print("❌ No frames enhanced")
            return False
        
        # Step 4: Create test page data
        test_page = self.create_test_page_data(selected_frames)
        
        # Step 5: Save everything
        self.save_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 HIGH QUALITY TEST PAGE COMPLETED!")
        print("=" * 50)
        print(f"✅ Enhanced {enhanced_count}/4 frames preserving original quality")
        print(f"🎯 Quality: Full HD+ (1920x1080 or original resolution)")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"🌐 View at: http://localhost:5000/comic")
        
        return True
    
    def create_test_page_data(self, selected_frames):
        """Create simple test page data with meaningful dialogue"""
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "high_quality_test_page",
                "quality": "Full HD+",
                "panel_count": len(selected_frames),
                "panel_resolution": "1920x1080+",
                "creation_time": time.time(),
                "enhancement_type": "preserve_original_quality"
            }
        }
        
        # Generate meaningful dialogue for test page
        bubble_data = self.generate_meaningful_dialogue(len(selected_frames))
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "Full HD+",
                "resolution": "1920x1080+"
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
                
                if self.enhance_to_high_quality(frame_path):
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
        """Create a single comic page with meaningful dialogue"""
        page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_number": page_number,
                "quality": "2K",
                "panel_count": len(page_frames)
            }
        }
        
        # Get dialogue for this page
        page_dialogue = self.get_page_dialogue(page_number, len(page_frames))
        
        for i, frame_file in enumerate(page_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "2K"
            })
            
            # Meaningful bubble with actual dialogue
            dialogue_text = page_dialogue[i] if i < len(page_dialogue) else "((action-scene))"
            
            page["bubbles"].append({
                "dialog": dialogue_text,
                "emotion": self.detect_emotion(dialogue_text),
                "bubble_offset_x": 50 + (i * 25),  # Vary positions
                "bubble_offset_y": 50 + (i * 20),
                "tail_offset_x": 20,
                "tail_offset_y": 25,
                "tail_deg": 45
            })
        
        return page
    
    def get_page_dialogue(self, page_number, panel_count):
        """Get dialogue for a specific page"""
        all_dialogue = self.extract_subtitle_dialogue()
        
        if all_dialogue:
            # Calculate which dialogue entries to use for this page
            start_idx = (page_number - 1) * panel_count
            end_idx = start_idx + panel_count
            
            # Get dialogue for this page, pad if necessary
            page_dialogue = all_dialogue[start_idx:end_idx]
            
            # Fill remaining panels with action scenes if not enough dialogue
            while len(page_dialogue) < panel_count:
                page_dialogue.append("((action-scene))")
                
            return page_dialogue
        else:
            # Generate story-appropriate dialogue
            return self.generate_story_dialogue(page_number, panel_count)
    
    def generate_story_dialogue(self, page_number, panel_count):
        """Generate story-appropriate dialogue for a page"""
        story_beats = {
            1: ["Welcome to our story!", "Something is about to change...", "The adventure begins now!", "What lies ahead?"],
            2: ["The plot thickens...", "New challenges arise!", "Our hero must decide...", "The stakes get higher!"],
            3: ["The climax approaches!", "Everything comes together!", "The final confrontation!", "Victory or defeat?"]
        }
        
        # Use story beats based on page position
        if page_number <= 4:
            act = 1
        elif page_number <= 8:
            act = 2
        else:
            act = 3
        
        base_dialogue = story_beats.get(act, story_beats[2])
        
        # Create dialogue for this page
        page_dialogue = []
        for i in range(panel_count):
            if i < len(base_dialogue):
                page_dialogue.append(base_dialogue[i])
            else:
                page_dialogue.append("((action-scene))")
        
        return page_dialogue
    
    def detect_emotion(self, text):
        """Detect emotion from dialogue text"""
        if text == "((action-scene))":
            return "action"
        
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['!', 'amazing', 'great', 'wonderful', 'yes']):
            return "excited"
        elif any(word in text_lower for word in ['?', 'what', 'how', 'why']):
            return "confused"
        elif any(word in text_lower for word in ['no', 'stop', 'help', 'danger']):
            return "worried"
        else:
            return "normal"
    
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
    """Create high quality test page"""
    enhancer = Simple2KEnhancer()
    return enhancer.create_high_quality_test_page()

def create_full_2k_comic():
    """Create full 2K comic"""
    enhancer = Simple2KEnhancer()
    return enhancer.create_full_2k_comic()

if __name__ == "__main__":
    create_2k_test_page()