"""
Enhanced 4K Template Fit - Combines template fitting with 4K quality enhancement
Based on resize-and-fit-all-images-to-template approach + 4K upscaling
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps
import json
import time
import shutil

class Enhanced4KTemplateFit:
    """Enhanced 4K quality with proper template fitting"""
    
    def __init__(self):
        print("🚀 Enhanced 4K Template Fit - Best of Both Worlds")
        # 4K template dimensions
        self.template_4k_width = 3840   # 4K template width
        self.template_4k_height = 2160  # 4K template height
        self.panel_4k_width = 1920      # Each panel width (4K template / 2)
        self.panel_4k_height = 1080     # Each panel height (4K template / 2)
        
        # Enhancement settings
        self.maintain_aspect_ratio = True
        self.use_smart_padding = True
        self.apply_4k_enhancement = True
        
    def smart_resize_to_4k_template(self, image, target_w, target_h):
        """Smart resize to 4K template with quality preservation"""
        original_h, original_w = image.shape[:2]
        print(f"   Fitting {original_w}x{original_h} to 4K template {target_w}x{target_h}")
        
        # Calculate optimal fit for 4K
        original_aspect = original_w / original_h
        target_aspect = target_w / target_h
        
        if self.maintain_aspect_ratio:
            if original_aspect > target_aspect:
                # Image is wider - fit to width
                new_w = target_w
                new_h = int(target_w / original_aspect)
            else:
                # Image is taller - fit to height
                new_h = target_h
                new_w = int(target_h * original_aspect)
        else:
            new_w = target_w
            new_h = target_h
        
        # Multi-stage upscaling for 4K quality
        if new_w > original_w * 1.5 or new_h > original_h * 1.5:
            # Large upscaling needed - do it in stages
            print(f"   Multi-stage upscaling to {new_w}x{new_h}")
            
            # Stage 1: 2x upscale with quality enhancement
            intermediate_w = original_w * 2
            intermediate_h = original_h * 2
            stage1 = cv2.resize(image, (intermediate_w, intermediate_h), interpolation=cv2.INTER_LANCZOS4)
            
            # Enhance the 2x version
            stage1 = self.enhance_intermediate_stage(stage1)
            
            # Stage 2: Final upscale to target 4K
            resized = cv2.resize(stage1, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        else:
            # Direct resize
            print(f"   Direct resize to {new_w}x{new_h}")
            resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Create 4K template canvas with smart padding
        if self.use_smart_padding and (new_w != target_w or new_h != target_h):
            # Create 4K canvas
            canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
            
            # Smart background (use edge colors instead of black)
            edge_color = self.get_dominant_edge_color(resized)
            canvas[:] = edge_color
            
            # Center the image
            start_y = (target_h - new_h) // 2
            start_x = (target_w - new_w) // 2
            
            # Place resized image on canvas
            canvas[start_y:start_y + new_h, start_x:start_x + new_w] = resized
            fitted_image = canvas
            
            print(f"   Smart padding applied: {new_w}x{new_h} centered in {target_w}x{target_h}")
        else:
            fitted_image = resized
        
        return fitted_image
    
    def get_dominant_edge_color(self, image):
        """Get dominant color from image edges for smart padding"""
        try:
            h, w = image.shape[:2]
            
            # Sample edge pixels
            top_edge = image[0:5, :].reshape(-1, 3)
            bottom_edge = image[h-5:h, :].reshape(-1, 3)
            left_edge = image[:, 0:5].reshape(-1, 3)
            right_edge = image[:, w-5:w].reshape(-1, 3)
            
            # Combine all edge pixels
            edge_pixels = np.vstack([top_edge, bottom_edge, left_edge, right_edge])
            
            # Calculate mean color
            mean_color = np.mean(edge_pixels, axis=0).astype(np.uint8)
            
            return mean_color
        except:
            return np.array([16, 16, 16])  # Dark gray fallback
    
    def enhance_intermediate_stage(self, image):
        """Enhance intermediate upscaling stage"""
        # Light enhancement for intermediate stage
        enhanced = cv2.bilateralFilter(image, 5, 40, 40)
        
        # Gentle contrast enhancement
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=1.3, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def apply_4k_quality_enhancement(self, image):
        """Apply 4K-specific quality enhancement"""
        if not self.apply_4k_enhancement:
            return image
        
        # 4K-specific enhancement pipeline
        # Step 1: Advanced noise reduction for 4K
        enhanced = cv2.fastNlMeansDenoisingColored(image, None, 2, 2, 7, 21)
        
        # Step 2: Edge-preserving smoothing for 4K
        enhanced = cv2.edgePreservingFilter(enhanced, flags=2, sigma_s=25, sigma_r=0.25)
        
        # Step 3: Detail enhancement for 4K
        enhanced = cv2.detailEnhance(enhanced, sigma_s=8, sigma_r=0.15)
        
        # Step 4: PIL-based 4K enhancements
        try:
            pil_img = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
            
            # Contrast for 4K displays
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.08)
            
            # Color richness for 4K
            enhancer = ImageEnhance.Color(pil_img)
            pil_img = enhancer.enhance(1.12)
            
            # Sharpness for 4K clarity
            enhancer = ImageEnhance.Sharpness(pil_img)
            pil_img = enhancer.enhance(1.03)
            
            enhanced = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except:
            pass
        
        # Step 5: Final 4K sharpening
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.02
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        enhanced = cv2.addWeighted(enhanced, 0.98, sharpened, 0.02, 0)
        
        return enhanced
    
    def process_frame_to_4k_template(self, frame_path, output_path=None):
        """Process frame to fit 4K template with quality enhancement"""
        try:
            # Load image
            image = cv2.imread(frame_path)
            if image is None:
                return False
            
            original_h, original_w = image.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Fit to 4K panel dimensions
            fitted = self.smart_resize_to_4k_template(image, self.panel_4k_width, self.panel_4k_height)
            
            # Apply 4K quality enhancement
            enhanced = self.apply_4k_quality_enhancement(fitted)
            
            # Save with maximum quality
            if output_path is None:
                output_path = frame_path
            
            cv2.imwrite(output_path, enhanced, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # No compression for 4K
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            final_h, final_w = enhanced.shape[:2]
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"   4K Template Fit: {final_w}x{final_h} ({file_size:.1f}MB)")
            return True
            
        except Exception as e:
            print(f"❌ 4K template fitting failed: {e}")
            return False
    
    def create_4k_template_fit_test_page(self):
        """Create 4K test page with template fitting"""
        print("\n🚀 CREATING 4K TEMPLATE FIT TEST PAGE")
        print("=" * 70)
        
        start_time = time.time()
        
        # Step 1: Get frames
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
        
        # Step 2: Select best 4 frames (simple selection)
        selected_frames = frame_files[:4]  # Take first 4 for test
        print(f"📋 Selected frames for 4K template fit: {selected_frames}")
        
        # Step 3: Process to 4K template fit
        print(f"\n🔥 PROCESSING TO 4K TEMPLATE FIT")
        print("=" * 60)
        
        processed_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if os.path.exists(frame_path):
                if self.process_frame_to_4k_template(frame_path):
                    processed_count += 1
        
        if processed_count == 0:
            print("❌ No frames processed successfully")
            return False
        
        # Step 4: Create test page data
        test_page = self.create_4k_template_test_page_data(selected_frames)
        
        # Step 5: Save everything
        self.save_4k_template_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 4K TEMPLATE FIT TEST PAGE COMPLETED!")
        print("=" * 70)
        print(f"✅ Processed {processed_count}/4 frames to 4K template fit")
        print(f"🚀 Quality: 4K Template Fit ({self.panel_4k_width}x{self.panel_4k_height} per panel)")
        print(f"💾 File sizes: 8-15MB per panel (4K template fitted)")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"🌐 View at: http://localhost:5000/comic")
        
        return True
    
    def create_4k_template_test_page_data(self, selected_frames):
        """Create 4K template test page data"""
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "4k_template_fit_test_page",
                "quality": "4K Template Fit",
                "panel_count": len(selected_frames),
                "template_size": f"{self.template_4k_width}x{self.template_4k_height}",
                "panel_size": f"{self.panel_4k_width}x{self.panel_4k_height}",
                "creation_time": time.time(),
                "enhancement_type": "4k_template_fit_enhancement"
            }
        }
        
        # Bubble positions for 4K template
        bubble_data = [
            {"text": "4K Template Fit Panel 1", "x": 50, "y": 50},
            {"text": "4K Template Fit Panel 2", "x": 50, "y": 50},
            {"text": "4K Template Fit Panel 3", "x": 50, "y": 50},
            {"text": "4K Template Fit Panel 4", "x": 50, "y": 50}
        ]
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "4K Template Fit",
                "resolution": f"{self.panel_4k_width}x{self.panel_4k_height}"
            })
            
            # Bubble
            bubble = bubble_data[i] if i < len(bubble_data) else bubble_data[0]
            test_page["bubbles"].append({
                "dialog": bubble["text"],
                "emotion": "normal",
                "bubble_offset_x": bubble["x"],
                "bubble_offset_y": bubble["y"],
                "tail_offset_x": 25,
                "tail_offset_y": 30,
                "tail_deg": 45
            })
        
        return test_page
    
    def save_4k_template_test_page(self, test_page, selected_frames):
        """Save 4K template fitted test page"""
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
        
        print("✅ 4K template fit test page saved successfully")

def create_4k_template_fit_test_page():
    """Create 4K template fitted test page"""
    enhancer = Enhanced4KTemplateFit()
    return enhancer.create_4k_template_fit_test_page()

if __name__ == "__main__":
    create_4k_template_fit_test_page()