"""
Professional Comic Enhancer - Based on Industry Best Practices
Implements common techniques found in high-quality comic generation repositories
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageOps, ImageFilter
import json
import time
import shutil

class ProfessionalComicEnhancer:
    """Professional-grade comic enhancement using industry best practices"""
    
    def __init__(self):
        print("🎨 Professional Comic Enhancer - Industry Best Practices")
        
        # Standard comic dimensions (based on common practices)
        self.comic_page_width = 2480   # Standard print width (300 DPI)
        self.comic_page_height = 3508  # Standard print height (300 DPI)
        self.panel_width = 1240        # Panel width (page_width / 2)
        self.panel_height = 1754       # Panel height (page_height / 2)
        
        # Quality enhancement settings
        self.target_dpi = 300          # Print quality DPI
        self.enhancement_strength = 'medium'  # conservative, medium, aggressive
        self.preserve_aspect_ratio = True
        self.use_smart_cropping = True
        self.apply_comic_filters = True
        
    def analyze_frame_for_comic_suitability(self, frame_path):
        """Analyze frame suitability for comic conversion"""
        try:
            image = cv2.imread(frame_path)
            if image is None:
                return {'score': 0, 'suitability': 'poor'}
            
            h, w = image.shape[:2]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Comic-specific quality metrics
            # 1. Contrast (important for comic readability)
            contrast = gray.std()
            
            # 2. Edge definition (comic panels need clear edges)
            edges = cv2.Canny(gray, 50, 150)
            edge_strength = np.count_nonzero(edges) / edges.size
            
            # 3. Brightness distribution (avoid too dark/bright)
            brightness = gray.mean()
            brightness_score = 100 - abs(brightness - 128) / 128 * 100
            
            # 4. Detail richness (good for comic enhancement)
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 5. Color richness (for vibrant comics)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            saturation = hsv[:,:,1].mean()
            
            # 6. Face/character detection (important for comics)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            character_bonus = len(faces) * 10
            
            # Combined comic suitability score
            comic_score = (
                contrast * 0.25 +
                edge_strength * 1000 * 0.25 +
                brightness_score * 0.15 +
                laplacian_var * 0.2 +
                saturation * 0.1 +
                character_bonus * 0.05
            )
            
            # Determine suitability
            if comic_score > 80:
                suitability = 'excellent'
            elif comic_score > 60:
                suitability = 'good'
            elif comic_score > 40:
                suitability = 'fair'
            else:
                suitability = 'poor'
            
            return {
                'score': comic_score,
                'suitability': suitability,
                'contrast': contrast,
                'edge_strength': edge_strength,
                'brightness': brightness,
                'detail_level': laplacian_var,
                'color_richness': saturation,
                'character_count': len(faces)
            }
            
        except Exception as e:
            print(f"❌ Error analyzing {frame_path}: {e}")
            return {'score': 0, 'suitability': 'error'}
    
    def smart_crop_for_comic(self, image):
        """Smart cropping for comic panels (common in comic repositories)"""
        h, w = image.shape[:2]
        
        # Detect important regions using edge detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        
        # Find contours to identify important regions
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Get bounding box of all important regions
            all_contours = np.vstack(contours)
            x, y, w_box, h_box = cv2.boundingRect(all_contours)
            
            # Add padding around important region
            padding = 50
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(w, x + w_box + padding)
            y2 = min(h, y + h_box + padding)
            
            # Crop to important region
            cropped = image[y1:y2, x1:x2]
            
            print(f"   Smart crop applied: {w}x{h} → {x2-x1}x{y2-y1}")
            return cropped
        else:
            # No significant features found, return original
            return image
    
    def resize_and_fit_to_comic_template(self, image, target_w, target_h):
        """Resize and fit image to comic template (industry standard approach)"""
        original_h, original_w = image.shape[:2]
        
        # Apply smart cropping if enabled
        if self.use_smart_cropping:
            image = self.smart_crop_for_comic(image)
            crop_h, crop_w = image.shape[:2]
            print(f"   After smart crop: {crop_w}x{crop_h}")
        
        # Calculate optimal fit maintaining aspect ratio
        if self.preserve_aspect_ratio:
            # Calculate scale factors
            scale_w = target_w / image.shape[1]
            scale_h = target_h / image.shape[0]
            scale = min(scale_w, scale_h)  # Use smaller scale to fit entirely
            
            # Calculate new dimensions
            new_w = int(image.shape[1] * scale)
            new_h = int(image.shape[0] * scale)
        else:
            new_w = target_w
            new_h = target_h
        
        # High-quality resize
        if new_w > image.shape[1] or new_h > image.shape[0]:
            # Upscaling - use LANCZOS4 for best quality
            resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
            print(f"   Upscaled: {image.shape[1]}x{image.shape[0]} → {new_w}x{new_h}")
        else:
            # Downscaling - use AREA for best quality
            resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            print(f"   Downscaled: {image.shape[1]}x{image.shape[0]} → {new_w}x{new_h}")
        
        # Create template canvas with smart background
        if new_w != target_w or new_h != target_h:
            # Create canvas
            canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
            
            # Smart background color (common in comic repositories)
            bg_color = self.calculate_smart_background_color(resized)
            canvas[:] = bg_color
            
            # Center the resized image
            start_y = (target_h - new_h) // 2
            start_x = (target_w - new_w) // 2
            
            # Apply feathered edges for better integration
            if self.apply_comic_filters:
                resized = self.apply_feathered_edges(resized)
            
            # Place on canvas
            canvas[start_y:start_y + new_h, start_x:start_x + new_w] = resized
            fitted_image = canvas
            
            print(f"   Template fit: centered in {target_w}x{target_h} with smart background")
        else:
            fitted_image = resized
        
        return fitted_image
    
    def calculate_smart_background_color(self, image):
        """Calculate smart background color for comic panels"""
        # Method 1: Average of edge pixels
        h, w = image.shape[:2]
        edge_width = 10
        
        # Sample edges
        top = image[:edge_width, :].reshape(-1, 3)
        bottom = image[h-edge_width:, :].reshape(-1, 3)
        left = image[:, :edge_width].reshape(-1, 3)
        right = image[:, w-edge_width:].reshape(-1, 3)
        
        # Combine edge samples
        edge_pixels = np.vstack([top, bottom, left, right])
        
        # Calculate average with slight darkening (comic style)
        avg_color = np.mean(edge_pixels, axis=0)
        darkened_color = avg_color * 0.8  # Slightly darker for comic effect
        
        return darkened_color.astype(np.uint8)
    
    def apply_feathered_edges(self, image):
        """Apply feathered edges for better template integration"""
        h, w = image.shape[:2]
        
        # Create feather mask
        mask = np.ones((h, w), dtype=np.float32)
        feather_size = min(20, min(h, w) // 20)
        
        # Apply Gaussian blur to edges
        mask[:feather_size, :] *= np.linspace(0, 1, feather_size).reshape(-1, 1)
        mask[h-feather_size:, :] *= np.linspace(1, 0, feather_size).reshape(-1, 1)
        mask[:, :feather_size] *= np.linspace(0, 1, feather_size)
        mask[:, w-feather_size:] *= np.linspace(1, 0, feather_size)
        
        # Apply mask
        feathered = image.copy().astype(np.float32)
        for c in range(3):
            feathered[:, :, c] *= mask
        
        return feathered.astype(np.uint8)
    
    def apply_professional_comic_enhancement(self, image):
        """Apply professional comic enhancement techniques"""
        enhanced = image.copy()
        
        # Step 1: Noise reduction (preserve detail)
        enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 3, 3, 7, 21)
        
        # Step 2: Comic-style contrast enhancement
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Adaptive histogram equalization for comics
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8,8))
        l = clahe.apply(l)
        
        enhanced = cv2.merge([l, a, b])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        # Step 3: Edge enhancement (important for comics)
        enhanced = cv2.edgePreservingFilter(enhanced, flags=2, sigma_s=30, sigma_r=0.3)
        
        # Step 4: Color vibrancy for comics
        hsv = cv2.cvtColor(enhanced, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        
        # Enhance saturation for comic look
        s = cv2.add(s, 15)  # Boost saturation
        s = np.clip(s, 0, 255)
        
        enhanced = cv2.merge([h, s, v])
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_HSV2BGR)
        
        # Step 5: Professional sharpening
        if self.enhancement_strength == 'aggressive':
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.1
        elif self.enhancement_strength == 'medium':
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.05
        else:  # conservative
            kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) * 0.02
        
        sharpened = cv2.filter2D(enhanced, -1, kernel)
        enhanced = cv2.addWeighted(enhanced, 0.9, sharpened, 0.1, 0)
        
        return enhanced
    
    def process_frame_professional(self, frame_path, output_path=None):
        """Process frame using professional comic techniques"""
        try:
            # Load image
            image = cv2.imread(frame_path)
            if image is None:
                return False
            
            original_h, original_w = image.shape[:2]
            print(f"   Original: {original_w}x{original_h}")
            
            # Step 1: Resize and fit to comic template
            fitted = self.resize_and_fit_to_comic_template(
                image, self.panel_width, self.panel_height
            )
            
            # Step 2: Apply professional comic enhancement
            enhanced = self.apply_professional_comic_enhancement(fitted)
            
            # Step 3: Final quality optimization
            final = self.final_comic_optimization(enhanced)
            
            # Save with professional settings
            if output_path is None:
                output_path = frame_path
            
            # Professional PNG settings
            cv2.imwrite(output_path, final, [
                cv2.IMWRITE_PNG_COMPRESSION, 0,  # No compression
                cv2.IMWRITE_PNG_STRATEGY, cv2.IMWRITE_PNG_STRATEGY_DEFAULT
            ])
            
            final_h, final_w = final.shape[:2]
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            print(f"   Professional: {final_w}x{final_h} ({file_size:.1f}MB)")
            return True
            
        except Exception as e:
            print(f"❌ Professional enhancement failed: {e}")
            return False
    
    def final_comic_optimization(self, image):
        """Final optimization for comic display"""
        # Ensure optimal color space
        optimized = image.copy()
        
        # Color space optimization for comics
        try:
            # Convert to PIL for advanced processing
            pil_img = Image.fromarray(cv2.cvtColor(optimized, cv2.COLOR_BGR2RGB))
            
            # Comic-specific enhancements
            if self.enhancement_strength == 'aggressive':
                # High contrast for dramatic comic effect
                enhancer = ImageEnhance.Contrast(pil_img)
                pil_img = enhancer.enhance(1.2)
                
                # Vibrant colors
                enhancer = ImageEnhance.Color(pil_img)
                pil_img = enhancer.enhance(1.3)
                
                # Sharp details
                enhancer = ImageEnhance.Sharpness(pil_img)
                pil_img = enhancer.enhance(1.1)
                
            elif self.enhancement_strength == 'medium':
                # Balanced enhancement
                enhancer = ImageEnhance.Contrast(pil_img)
                pil_img = enhancer.enhance(1.1)
                
                enhancer = ImageEnhance.Color(pil_img)
                pil_img = enhancer.enhance(1.15)
                
                enhancer = ImageEnhance.Sharpness(pil_img)
                pil_img = enhancer.enhance(1.05)
                
            else:  # conservative
                # Gentle enhancement
                enhancer = ImageEnhance.Contrast(pil_img)
                pil_img = enhancer.enhance(1.05)
                
                enhancer = ImageEnhance.Color(pil_img)
                pil_img = enhancer.enhance(1.08)
            
            optimized = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
            
        except:
            pass
        
        # Final quality assurance
        optimized = np.clip(optimized, 0, 255).astype(np.uint8)
        
        return optimized
    
    def select_frames_for_comic(self, frames_dir="frames/final", count=4):
        """Select best frames for comic using professional criteria"""
        print(f"\n🎨 SELECTING FRAMES FOR PROFESSIONAL COMIC")
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
        
        print(f"📸 Analyzing {len(frame_files)} frames for comic suitability...")
        
        # Analyze all frames
        frame_analysis = {}
        for frame_file in frame_files:
            frame_path = os.path.join(frames_dir, frame_file)
            analysis = self.analyze_frame_for_comic_suitability(frame_path)
            frame_analysis[frame_file] = analysis
        
        # Sort by comic suitability score
        sorted_frames = sorted(frame_analysis.items(), 
                             key=lambda x: x[1]['score'], reverse=True)
        
        # Select diverse high-quality frames
        selected = self.select_diverse_comic_frames(sorted_frames, count)
        
        print(f"\n🏆 SELECTED FRAMES FOR COMIC:")
        for i, frame in enumerate(selected, 1):
            analysis = frame_analysis[frame]
            print(f"   Panel {i}: {frame}")
            print(f"      Score: {analysis['score']:.1f} ({analysis['suitability']})")
            print(f"      Characters: {analysis['character_count']}, Detail: {analysis['detail_level']:.1f}")
        
        return selected
    
    def select_diverse_comic_frames(self, sorted_frames, count):
        """Select diverse frames for better comic storytelling"""
        selected = []
        
        # Ensure diversity in comic panels
        min_gap = max(1, len(sorted_frames) // (count * 2))
        
        # Extract frame numbers
        frame_numbers = {}
        for frame_name, analysis in sorted_frames:
            try:
                num_str = frame_name.replace('frame', '').replace('.png', '')
                frame_numbers[frame_name] = int(num_str)
            except:
                frame_numbers[frame_name] = 0
        
        # Select with diversity
        for frame_name, analysis in sorted_frames:
            if len(selected) >= count:
                break
            
            # Check diversity
            frame_num = frame_numbers[frame_name]
            too_close = False
            
            for sel_frame in selected:
                sel_num = frame_numbers[sel_frame]
                if abs(frame_num - sel_num) < min_gap:
                    too_close = True
                    break
            
            if not too_close:
                selected.append(frame_name)
        
        # Fill remaining if needed
        if len(selected) < count:
            for frame_name, analysis in sorted_frames:
                if len(selected) >= count:
                    break
                if frame_name not in selected:
                    selected.append(frame_name)
        
        return selected[:count]
    
    def create_professional_comic_test_page(self):
        """Create professional comic test page"""
        print("\n🎨 CREATING PROFESSIONAL COMIC TEST PAGE")
        print("=" * 70)
        
        start_time = time.time()
        
        # Step 1: Select best frames for comic
        selected_frames = self.select_frames_for_comic(count=4)
        if not selected_frames:
            return False
        
        # Step 2: Process frames professionally
        print(f"\n🔥 PROFESSIONAL COMIC PROCESSING")
        print("=" * 60)
        
        processed_count = 0
        for i, frame_file in enumerate(selected_frames, 1):
            frame_path = os.path.join('frames/final', frame_file)
            print(f"\n[{i}/4] Processing: {frame_file}")
            
            if os.path.exists(frame_path):
                if self.process_frame_professional(frame_path):
                    processed_count += 1
        
        if processed_count == 0:
            print("❌ No frames processed successfully")
            return False
        
        # Step 3: Create professional test page data
        test_page = self.create_professional_test_page_data(selected_frames)
        
        # Step 4: Save everything
        self.save_professional_test_page(test_page, selected_frames)
        
        total_time = time.time() - start_time
        
        print(f"\n🎉 PROFESSIONAL COMIC TEST PAGE COMPLETED!")
        print("=" * 70)
        print(f"✅ Processed {processed_count}/4 frames professionally")
        print(f"🎨 Quality: Professional Comic ({self.panel_width}x{self.panel_height} per panel)")
        print(f"📏 Print ready: 300 DPI quality")
        print(f"⏱️ Generation time: {total_time:.1f} seconds")
        print(f"🌐 View at: http://localhost:5000/comic")
        
        return True
    
    def create_professional_test_page_data(self, selected_frames):
        """Create professional test page data"""
        test_page = {
            "panels": [],
            "bubbles": [],
            "metadata": {
                "page_type": "professional_comic_test_page",
                "quality": "Professional Comic",
                "panel_count": len(selected_frames),
                "template_size": f"{self.comic_page_width}x{self.comic_page_height}",
                "panel_size": f"{self.panel_width}x{self.panel_height}",
                "dpi": self.target_dpi,
                "creation_time": time.time(),
                "enhancement_type": "professional_comic_enhancement"
            }
        }
        
        # Professional bubble positioning
        bubble_data = [
            {"text": "Professional Panel 1", "x": 40, "y": 40},
            {"text": "Professional Panel 2", "x": 40, "y": 40},
            {"text": "Professional Panel 3", "x": 40, "y": 40},
            {"text": "Professional Panel 4", "x": 40, "y": 40}
        ]
        
        for i, frame_file in enumerate(selected_frames):
            frame_name = frame_file.replace('.png', '')
            
            # Panel
            test_page["panels"].append({
                "image": frame_name,
                "row_span": 1,
                "col_span": 1,
                "quality": "Professional Comic",
                "resolution": f"{self.panel_width}x{self.panel_height}"
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
    
    def save_professional_test_page(self, test_page, selected_frames):
        """Save professional test page"""
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
        
        print("✅ Professional comic test page saved successfully")

def create_professional_comic_test_page():
    """Create professional comic test page"""
    enhancer = ProfessionalComicEnhancer()
    return enhancer.create_professional_comic_test_page()

if __name__ == "__main__":
    create_professional_comic_test_page()