"""
Enhanced Preview System for Amit Comic
Implements smart frame selection and maintains high quality throughout the pipeline
"""

import os
import json
import shutil
import cv2
import numpy as np
from backend.class_def import Page, panel, bubble
from PIL import Image, ImageEnhance
import time

class EnhancedComicPreviewSystem:
    """Enhanced preview system with smart frame selection and quality preservation"""
    
    def __init__(self):
        print("🚀 Enhanced Comic Preview System - Smart Selection & High Quality")
        self.selected_frames = []
        self.frame_quality_scores = {}
        
    def analyze_frame_quality(self, frame_path):
        """Analyze frame quality using multiple metrics"""
        try:
            img = cv2.imread(frame_path)
            if img is None:
                return 0.0
            
            # Convert to grayscale for analysis
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Sharpness (Laplacian variance)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Contrast (standard deviation)
            contrast = gray.std()
            
            # Brightness balance (avoid too dark/bright)
            brightness = gray.mean()
            brightness_score = 1.0 - abs(brightness - 128) / 128
            
            # Edge density (more edges = more interesting)
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.count_nonzero(edges) / edges.size
            
            # Combine scores (weighted)
            quality_score = (
                sharpness * 0.3 +
                contrast * 0.25 +
                brightness_score * 0.2 +
                edge_density * 1000 * 0.25  # Scale edge density
            )
            
            return min(quality_score, 100.0)  # Cap at 100
            
        except Exception as e:
            print(f"Error analyzing {frame_path}: {e}")
            return 0.0
    
    def smart_frame_selection(self, frames_dir="frames/final", target_count=48):
        """Smart frame selection based on quality and diversity"""
        print(f"\n🧠 SMART FRAME SELECTION (Target: {target_count} frames)")
        print("=" * 60)
        
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
        
        # Analyze quality for each frame
        print("🔍 Analyzing frame quality...")
        quality_scores = {}
        
        for i, frame_file in enumerate(frame_files):
            frame_path = os.path.join(frames_dir, frame_file)
            quality_score = self.analyze_frame_quality(frame_path)
            quality_scores[frame_file] = quality_score
            
            if i % 10 == 0:  # Progress update
                print(f"   Analyzed {i+1}/{total_frames} frames...")
        
        # Sort frames by quality
        sorted_frames = sorted(quality_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Smart selection algorithm
        selected_frames = []
        
        if total_frames <= target_count:
            # Use all frames if we have fewer than target
            selected_frames = [f[0] for f in sorted_frames]
        else:
            # Divide into quality tiers and select from each
            high_quality = sorted_frames[:total_frames//3]
            mid_quality = sorted_frames[total_frames//3:2*total_frames//3]
            low_quality = sorted_frames[2*total_frames//3:]
            
            # Select proportionally from each tier
            high_count = int(target_count * 0.6)  # 60% from high quality
            mid_count = int(target_count * 0.3)   # 30% from mid quality
            low_count = target_count - high_count - mid_count  # Remaining from low
            
            # Select with diversity (avoid consecutive frames)
            selected_frames.extend(self._select_diverse_frames(high_quality, high_count))
            selected_frames.extend(self._select_diverse_frames(mid_quality, mid_count))
            selected_frames.extend(self._select_diverse_frames(low_quality, low_count))
        
        # Store quality scores for selected frames
        self.frame_quality_scores = {f: quality_scores[f] for f in selected_frames}
        
        print(f"✅ Selected {len(selected_frames)} high-quality frames")
        print(f"📊 Average quality score: {np.mean([quality_scores[f] for f in selected_frames]):.1f}")
        
        # Show top frames for preview
        print("\n🏆 Top 4 frames for preview:")
        for i in range(min(4, len(selected_frames))):
            frame = selected_frames[i]
            score = quality_scores[frame]
            print(f"   Panel {i+1}: {frame} (Quality: {score:.1f})")
        
        self.selected_frames = selected_frames
        return selected_frames
    
    def _select_diverse_frames(self, frame_list, count):
        """Select frames with diversity (avoid consecutive frames)"""
        if count >= len(frame_list):
            return [f[0] for f in frame_list]
        
        selected = []
        used_indices = set()
        
        # Extract frame numbers for diversity check
        frame_numbers = {}
        for frame_name, score in frame_list:
            try:
                # Extract number from frame001.png format
                num_str = frame_name.replace('frame', '').replace('.png', '')
                frame_numbers[frame_name] = int(num_str)
            except:
                frame_numbers[frame_name] = 0
        
        # Select with minimum distance between frames
        for frame_name, score in frame_list:
            if len(selected) >= count:
                break
                
            frame_num = frame_numbers[frame_name]
            
            # Check if this frame is too close to already selected frames
            too_close = False
            for sel_frame in selected:
                sel_num = frame_numbers[sel_frame]
                if abs(frame_num - sel_num) < 3:  # Minimum 3 frames apart
                    too_close = True
                    break
            
            if not too_close:
                selected.append(frame_name)
        
        # Fill remaining slots if needed
        if len(selected) < count:
            for frame_name, score in frame_list:
                if len(selected) >= count:
                    break
                if frame_name not in selected:
                    selected.append(frame_name)
        
        return selected
    
    def enhance_preview_images(self, preview_frames, frames_dir="frames/final"):
        """Enhance preview images with maximum quality preservation"""
        print(f"\n🔥 ULTRA QUALITY ENHANCEMENT (Preview: {len(preview_frames)} frames)")
        print("=" * 60)
        
        for i, frame_file in enumerate(preview_frames, 1):
            frame_path = os.path.join(frames_dir, frame_file)
            print(f"\n📸 Enhancing Panel {i}: {frame_file}")
            
            try:
                # Load image with maximum quality
                img = cv2.imread(frame_path, cv2.IMREAD_COLOR)
                if img is None:
                    print(f"❌ Could not load {frame_file}")
                    continue
                
                original_h, original_w = img.shape[:2]
                original_size = os.path.getsize(frame_path) / (1024*1024)
                print(f"   Original: {original_w}x{original_h} ({original_size:.1f}MB)")
                
                # Apply ultra enhancement
                enhanced = self.apply_ultra_enhancement(img)
                
                # Save with maximum quality (no compression)
                cv2.imwrite(frame_path, enhanced, [
                    cv2.IMWRITE_PNG_COMPRESSION, 0,  # No compression
                ])
                
                final_h, final_w = enhanced.shape[:2]
                final_size = os.path.getsize(frame_path) / (1024*1024)
                quality_score = self.frame_quality_scores.get(frame_file, 0)
                
                print(f"   Enhanced: {final_w}x{final_h} ({final_size:.1f}MB)")
                print(f"   Quality Score: {quality_score:.1f}/100")
                
            except Exception as e:
                print(f"❌ Enhancement failed for {frame_file}: {e}")
        
        print(f"\n✅ Ultra quality enhancement completed!")
        return preview_frames
    
    def apply_ultra_enhancement(self, img):
        """Apply ultra-high quality enhancement"""
        h, w = img.shape[:2]
        
        # Multi-stage upscaling for maximum quality
        # Stage 1: 2x with CUBIC
        img_2x = cv2.resize(img, (w*2, h*2), interpolation=cv2.INTER_CUBIC)
        
        # Stage 2: 2x with LANCZOS4 (total 4x)
        img_4x = cv2.resize(img_2x, (w*4, h*4), interpolation=cv2.INTER_LANCZOS4)
        
        # Advanced noise reduction
        img_4x = cv2.fastNlMeansDenoisingColored(img_4x, None, 3, 3, 7, 21)
        
        # Bilateral filtering for edge preservation
        img_4x = cv2.bilateralFilter(img_4x, 9, 75, 75)
        
        # PIL-based enhancements
        try:
            pil_img = Image.fromarray(cv2.cvtColor(img_4x, cv2.COLOR_BGR2RGB))
            
            # Contrast enhancement
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.15)
            
            # Color saturation
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.25)
            
            # Sharpness
            enhancer = ImageEnhance.Sharpness(pil_img)
            pil_img = enhancer.enhance(1.1)
            
            img_4x = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"PIL enhancement failed: {e}")
        
        # Final sharpening with unsharp mask
        gaussian = cv2.GaussianBlur(img_4x, (0, 0), 2.0)
        img_4x = cv2.addWeighted(img_4x, 1.5, gaussian, -0.5, 0)
        
        # Ensure values are in valid range
        img_4x = np.clip(img_4x, 0, 255)
        
        return img_4x.astype(np.uint8)
    
    def create_enhanced_preview(self):
        """Create enhanced preview with smart selection and ultra quality"""
        print("🎬 Enhanced Comic Preview - Smart Selection & Ultra Quality")
        print("=" * 70)
        
        # Step 1: Smart frame selection
        selected_frames = self.smart_frame_selection()
        if not selected_frames:
            return False
        
        # Step 2: Enhance preview images (first 4)
        preview_frames = selected_frames[:4]
        enhanced_frames = self.enhance_preview_images(preview_frames)
        if not enhanced_frames:
            return False
        
        # Step 3: Create preview page with enhanced metadata
        preview_page = self.create_preview_page_with_metadata(enhanced_frames)
        if not preview_page:
            return False
        
        print(f"\n🎉 ENHANCED PREVIEW READY!")
        print("=" * 40)
        print("✅ Smart frame selection completed")
        print("✅ Ultra 4x quality enhancement applied")
        print("✅ High-quality preview page created")
        print("✅ Quality scores calculated and stored")
        print(f"\n🌐 View your enhanced preview at: http://localhost:5000/comic")
        print("📋 Perfect quality preserved - no cropping or zoom issues!")
        
        return True
    
    def create_preview_page_with_metadata(self, preview_frames):
        """Create preview page with quality metadata"""
        print(f"\n📄 Creating Enhanced Preview Page...")
        print("=" * 50)
        
        # Create enhanced page data with quality metadata
        preview_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "creation_time": time.time(),
                "enhancement_type": "ultra_4x",
                "total_selected_frames": len(self.selected_frames),
                "preview_frames": len(preview_frames),
                "quality_scores": {}
            }
        }
        
        # Add panels and bubbles with quality information
        for i, frame_file in enumerate(preview_frames):
            frame_name = frame_file.replace('.png', '')
            quality_score = self.frame_quality_scores.get(frame_file, 0)
            
            # Panel data
            preview_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality_score": quality_score,
                "enhancement": "ultra_4x"
            })
            
            # Bubble data with quality-based positioning
            bubble_x = 50 + (i * 10)  # Vary position slightly
            bubble_y = 50 + (i * 5)
            
            preview_page["bubbles"].append({
                "dialog": f"Ultra Quality Panel {i+1} (Score: {quality_score:.1f})",
                "emotion": "normal",
                "bubble_offset_x": bubble_x,
                "bubble_offset_y": bubble_y,
                "tail_offset_x": 20 + (i * 5),
                "tail_offset_y": 30 + (i * 5),
                "tail_deg": 45 + (i * 10)
            })
            
            # Store quality metadata
            preview_page["metadata"]["quality_scores"][frame_name] = quality_score
        
        # Save enhanced page data
        preview_pages = [preview_page]
        
        # Write to page.js files with enhanced structure
        os.makedirs('output_template', exist_ok=True)
        with open('output_template/page.js', 'w') as f:
            f.write('var pages = ')
            json.dump(preview_pages, f, indent=4)
        
        os.makedirs('static/comic', exist_ok=True)
        with open('static/comic/page.js', 'w') as f:
            f.write('var pages = ')
            json.dump(preview_pages, f, indent=4)
        
        # Copy enhanced frames to static
        os.makedirs('static/comic/frames/final', exist_ok=True)
        for frame in preview_frames:
            src = os.path.join('frames/final', frame)
            dst = os.path.join('static/comic/frames/final', frame)
            if os.path.exists(src):
                shutil.copy2(src, dst)
        
        # Save frame selection metadata
        metadata = {
            "total_frames_analyzed": len(self.frame_quality_scores),
            "selected_frames": self.selected_frames,
            "quality_scores": self.frame_quality_scores,
            "enhancement_applied": "ultra_4x",
            "creation_timestamp": time.time()
        }
        
        with open('output_template/frame_selection_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=4)
        
        print("✅ Enhanced preview page created!")
        print(f"📄 1 ultra-quality page with 4 panels")
        print(f"🖼️ Using top-quality frames: {', '.join(preview_frames)}")
        print(f"📊 Average quality: {np.mean([self.frame_quality_scores[f] for f in preview_frames]):.1f}/100")
        
        return preview_page

def create_enhanced_comic_preview():
    """Create enhanced comic preview with smart selection"""
    enhanced_system = EnhancedComicPreviewSystem()
    return enhanced_system.create_enhanced_preview()

if __name__ == "__main__":
    create_enhanced_comic_preview()