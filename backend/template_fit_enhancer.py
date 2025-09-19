"""
Template Fit Enhancer - Resize and Fit All Images to Template with Quality Enhancement
Based on the approach from Coderedhydra/comic repository for proper image fitting
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import json
import time
import shutil

class TemplateFitEnhancer:
    """Enhanced image processing that properly fits images to template dimensions"""
    
    def __init__(self):
        print("🎯 Template Fit Enhancer - Resize and Fit All Images to Template")
        # Template dimensions for proper fitting
        self.template_width = 1920   # Template width
        self.template_height = 1080  # Template height
        self.panel_width = 960       # Each panel width (template_width / 2)
        self.panel_height = 540      # Each panel height (template_height / 2)
        
        # Quality enhancement settings
        self.enhance_quality = True
        self.maintain_aspect_ratio = True
        self.use_padding = True  # Add padding if needed to fit template
        
    def calculate_fit_dimensions(self, original_w, original_h, target_w, target_h):
        """Calculate dimensions to fit image into template while maintaining aspect ratio"""
        # Calculate aspect ratios
        original_aspect = original_w / original_h
        target_aspect = target_w / target_h
        
        if self.maintain_aspect_ratio:
            if original_aspect > target_aspect:
                # Image is wider, fit to width
                new_w = target_w
                new_h = int(target_w / original_aspect)
            else:
                # Image is taller, fit to height
                new_h = target_h
                new_w = int(target_h * original_aspect)
        else:
            # Stretch to fill (may distort)
            new_w = target_w
            new_h = target_h
        
        return new_w, new_h
    
    def resize_and_fit_to_template(self, image, target_w, target_h):
        """Resize and fit image to template dimensions with quality enhancement"""
        original_h, original_w = image.shape[:2]
        print(f"   Fitting {original_w}x{original_h} to template {target_w}x{target_h}")
        
        # Calculate optimal fit dimensions
        fit_w, fit_h = self.calculate_fit_dimensions(original_w, original_h, target_w, target_h)
        
        # High-quality resize
        if fit_w != original_w or fit_h != original_h:
            # Use best interpolation for resizing
            if fit_w > original_w or fit_h > original_h:
                # Upscaling - use LANCZOS4
                resized = cv2.resize(image, (fit_w, fit_h), interpolation=cv2.INTER_LANCZOS4)
            else:
                # Downscaling - use AREA for better quality
                resized = cv2.resize(image, (fit_w, fit_h), interpolation=cv2.INTER_AREA)
        else:
            resized = image.copy()
        
        # Create template-sized canvas
        if self.use_padding and (fit_w != target_w or fit_h != target_h):
            # Center the image on the template canvas
            canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
            canvas.fill(0)  # Black background
            
            # Calculate centering position
            start_y = (target_h - fit_h) // 2
            start_x = (target_w - fit_w) // 2
            
            # Place resized image on canvas
            canvas[start_y:start_y + fit_h, start_x:start_x + fit_w] = resized
            fitted_image = canvas
            
            print(f"   Fitted with padding: {fit_w}x{fit_h} centered in {target_w}x{target_h}")
        else:
            fitted_image = resized
            print(f"   Direct fit: {fit_w}x{fit_h}")
        
        return fitted_image
    
    def enhance_fitted_image(self, image):
        """Apply quality enhancement to fitted image"""
        if not self.enhance_quality:
            return image
        
        # Step 1: Noise reduction (gentle for fitted images)
        enhanced = cv2.fastNlMeansDenoisingColored(image, None, 3, 3, 7, 21)
        
        # Step 2: Contrast enhancement
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Adaptive contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Step 3: Edge enhancement for fitted images
        enhanced = cv2.edgePreservingFilter(enhanced, flags=2, sigma_s=30, sigma_r=0.3)
        
        # Step 4: PIL-based enhancements
        try:
            pil_img = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
            
            # Contrast boost
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.1)
            
            # Color enhancement
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.15)
            
            # Sharpness for fitted images
            enhancer = ImageEnhance.Sharpness(pil_img)
            pil_img = enhancer.enhance(1.05)
            
            enhanced = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except:
            pass
        
        return enhanced
    
    def process_frame_to_template(self, frame_path, output_path=None):
        """Process frame to fit template dimensions with quality enhancement"""
        try:
            # Load image
            image = cv2.imread(frame_path)
            if image is None:
                return False
            
            original_h, original_w = image.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Fit to panel dimensions (each panel in 2x2 grid)
            fitted = self.resize_and_fit_to_template(image, self.panel_width, self.panel_height)
            
            # Apply quality enhancement
            enhanced = self.enhance_fitted_image(fitted)
            
            # Save with high quality
            if output_path is None:
                output_path = frame_path
            
            cv2.imwrite(output_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # No compression for quality
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            final_h, final_w = enhanced.shape[:2]
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"   Template Fit: {final_w}x{final_h} ({file_size:.1f}MB)")
            return True
            
        except Exception as e:
            print(f"❌ Template fitting failed: {e}")
            return False
    
    def analyze_frames_for_template_fit(self, frames_dir="frames/final"):
        """Analyze frames for template fitting"""
        print(f"\n📸 ANALYZING FRAMES FOR TEMPLATE FITTING")
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
        
        print(f"📁 Found {len(frame_files)} frames for template fitting")
        print(f"🎯 Template size: {self.template_width}x{self.template_height}")
        print(f"🎯 Panel size: {self.panel_width}x{self.panel_height}")
        
        # Analyze each frame for template compatibility
        frame_info = {}
        for frame_file in frame_files:
            frame_path = os.path.join(frames_dir, frame_file)
            info = self.analyze_frame_for_template(frame_path)
            frame_info[frame_file] = info
        
        # Sort by quality score
        sorted_frames = sorted(frame_info.items(), key=lambda x: x[1]['quality_score'], reverse=True)
        
        print(f"✅ Frame analysis complete for template fitting")
        return [frame[0] for frame in sorted_frames]
    
    def analyze_frame_for_template(self, frame_path):
        """Analyze individual frame for template fitting"""
        try:
            image = cv2.imread(frame_path)
            if image is None:
                return {'quality_score': 0, 'aspect_ratio': 0, 'fit_type': 'error'}
            
            h, w = image.shape[:2]
            aspect_ratio = w / h
            target_aspect = self.panel_width / self.panel_height
            
            # Calculate quality metrics
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
            contrast = gray.std()
            
            # Aspect ratio compatibility
            aspect_diff = abs(aspect_ratio - target_aspect)
            aspect_score = max(0, 100 - aspect_diff * 50)
            
            # Resolution compatibility
            resolution_score = min(100, (w * h) / (1920 * 1080) * 100)
            
            # Combined quality score
            quality_score = (sharpness * 0.3 + contrast * 0.3 + 
                           aspect_score * 0.2 + resolution_score * 0.2)
            
            # Determine fit type
            if aspect_diff < 0.1:
                fit_type = 'perfect_fit'
            elif aspect_ratio > target_aspect:
                fit_type = 'letterbox'  # Will have horizontal padding
            else:
                fit_type = 'pillarbox'  # Will have vertical padding
            
            return {
                'quality_score': quality_score,
                'aspect_ratio': aspect_ratio,
                'fit_type': fit_type,
                'resolution': f"{w}x{h}"
            }
            
        except:
            return {'quality_score': 0, 'aspect_ratio': 0, 'fit_type': 'error'}
    
    def create_template_fit_test_page(self):
        """Create test page with template-fitted images"""
        print("\n🎯 CREATING TEMPLATE FIT TEST PAGE")
        print("=" * 60)
        
        start_time = time.time()
        
        # Step 1: Analyze frames for template fitting
        all_frames = self.analyze_frames_for_template_fit()
        if not all_frames:
            return False
        
        # Step 2: Select best 4 frames
        selected_frames = all_frames[:4]  # Take top 4 quality frames
        print(f"📋 Selected frames for template fitting: {selected_frames}")
        
        # Step 3: Process frames to fit template
        print(f"\n🔧 FITTING FRAMES TO TEMPLATE DIMENSIONS")
        print("=" * 60)
        
        processed_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if os.path.exists(frame_path):
                if self.process_frame_to_template(frame_path):
                    processed_count += 1
        
        if processed_count == 0:
            print("❌ No frames processed successfully")
            return False
        
        # Step 4: Create test page data
        test_page = self.create_template_test_page_data(selected_frames)
        
        # Step 5: Save everything
        self.save_template_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 TEMPLATE FIT TEST PAGE COMPLETED!")
        print("=" * 60)
        print(f"✅ Processed {processed_count}/4 frames to fit template")
        print(f"🎯 Template: {self.template_width}x{self.template_height}")
        print(f"🎯 Panel size: {self.panel_width}x{self.panel_height}")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"🌐 View at: http://localhost:5000/comic")
        
        return True
    
    def create_template_test_page_data(self, selected_frames):
        """Create test page data for template-fitted images"""
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "template_fit_test_page",
                "quality": "Template Fitted",
                "panel_count": len(selected_frames),
                "template_size": f"{self.template_width}x{self.template_height}",
                "panel_size": f"{self.panel_width}x{self.panel_height}",
                "creation_time": time.time(),
                "enhancement_type": "resize_and_fit_template"
            }
        }
        
        # Bubble positions optimized for fitted template
        bubble_data = [
            {"text": "Template Fit Panel 1", "x": 40, "y": 40},
            {"text": "Template Fit Panel 2", "x": 40, "y": 40},
            {"text": "Template Fit Panel 3", "x": 40, "y": 40},
            {"text": "Template Fit Panel 4", "x": 40, "y": 40}
        ]
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "Template Fitted",
                "template_fit": True
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
    
    def save_template_test_page(self, test_page, selected_frames):
        """Save template-fitted test page"""
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
        
        print("✅ Template fit test page saved successfully")
    
    def create_full_template_fit_comic(self, target_pages=12):
        """Create full comic with template-fitted images"""
        print(f"\n🎯 CREATING FULL {target_pages}-PAGE TEMPLATE FIT COMIC")
        print("=" * 70)
        
        start_time = time.time()
        
        # Get all frames
        all_frames = self.analyze_frames_for_template_fit()
        if not all_frames:
            return False
        
        # Calculate frames needed
        panels_needed = target_pages * 4
        
        # Select frames
        if len(all_frames) >= panels_needed:
            step = len(all_frames) // panels_needed
            selected_frames = [all_frames[i * step] for i in range(panels_needed)]
        else:
            selected_frames = all_frames.copy()
            while len(selected_frames) < panels_needed:
                selected_frames.extend(all_frames)
            selected_frames = selected_frames[:panels_needed]
        
        print(f"📋 Selected {len(selected_frames)} frames for template fitting")
        
        # Process all frames to fit template
        print(f"\n🔧 FITTING ALL FRAMES TO TEMPLATE")
        print("=" * 50)
        
        processed_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            
            if os.path.exists(frame_path):
                if i % 8 == 1:  # Progress every 8 frames
                    print(f"Processing template fit {i}-{min(i+7, len(selected_frames))}...")
                
                if self.process_frame_to_template(frame_path):
                    processed_count += 1
        
        # Create pages
        pages = []
        for page_num in range(target_pages):
            start_idx = page_num * 4
            end_idx = start_idx + 4
            page_frames = selected_frames[start_idx:end_idx]
            
            if page_frames:
                page = self.create_template_comic_page(page_frames, page_num + 1)
                pages.append(page)
        
        # Save full comic
        self.save_full_template_comic(pages, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 FULL TEMPLATE FIT COMIC COMPLETED!")
        print("=" * 50)
        print(f"📚 Generated {len(pages)} pages")
        print(f"✅ Processed {processed_count} frames to fit template")
        print(f"🎯 All panels: {self.panel_width}x{self.panel_height}")
        print(f"⏱️ Total time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        
        return True
    
    def create_template_comic_page(self, page_frames, page_number):
        """Create comic page with template-fitted panels"""
        page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_number": page_number,
                "quality": "Template Fitted",
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
                "quality": "Template Fitted"
            })
            
            # Bubble
            page["bubbles"].append({
                "dialog": f"Page {page_number} Panel {i+1}",
                "emotion": "normal",
                "bubble_offset_x": 40,
                "bubble_offset_y": 40,
                "tail_offset_x": 20,
                "tail_offset_y": 25,
                "tail_deg": 45
            })
        
        return page
    
    def save_full_template_comic(self, pages, selected_frames):
        """Save full template-fitted comic"""
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
            "quality": "Template Fitted",
            "template_size": f"{self.template_width}x{self.template_height}",
            "panel_size": f"{self.panel_width}x{self.panel_height}",
            "enhancement_type": "resize_and_fit_template",
            "generation_time": time.time()
        }
        
        with open('output_template/template_fit_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=4)

def create_template_fit_test_page():
    """Create template-fitted test page"""
    enhancer = TemplateFitEnhancer()
    return enhancer.create_template_fit_test_page()

def create_full_template_fit_comic():
    """Create full template-fitted comic"""
    enhancer = TemplateFitEnhancer()
    return enhancer.create_full_template_fit_comic()

if __name__ == "__main__":
    create_template_fit_test_page()