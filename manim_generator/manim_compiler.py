import subprocess
import os
import tempfile
import shutil
import re
from pathlib import Path
from typing import Tuple, Optional

class ManimCompiler:
    def __init__(self, output_dir: str = "/workspace/manim_generator/videos"):
        """Initialize the Manim compiler."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def extract_scene_name(self, code: str) -> str:
        """Extract the scene class name from Manim code."""
        # Look for class definitions that inherit from Scene
        pattern = r'class\s+(\w+)\s*\(\s*Scene\s*\):'
        match = re.search(pattern, code)
        if match:
            return match.group(1)
        else:
            # Default scene name if none found
            return "GeneratedScene"
    
    def clean_code(self, code: str) -> str:
        """Clean the generated code to ensure it's properly formatted."""
        # Remove markdown code blocks if present
        code = re.sub(r'^```python\s*\n', '', code, flags=re.MULTILINE)
        code = re.sub(r'^```\s*$', '', code, flags=re.MULTILINE)
        
        # Ensure proper imports are present
        if "from manim import *" not in code and "import manim" not in code:
            code = "from manim import *\n\n" + code
            
        return code.strip()
    
    def compile_animation(self, code: str, filename: str = None) -> Tuple[bool, str, Optional[str]]:
        """
        Compile Manim code and generate video.
        
        Args:
            code: Manim Python code
            filename: Optional filename for the script
            
        Returns:
            Tuple of (success, message, video_path)
        """
        
        # Clean the code
        cleaned_code = self.clean_code(code)
        
        # Extract scene name
        scene_name = self.extract_scene_name(cleaned_code)
        
        # Generate filename if not provided
        if filename is None:
            filename = f"generated_animation_{scene_name.lower()}.py"
        
        # Create temporary file for the script
        temp_dir = tempfile.mkdtemp()
        script_path = Path(temp_dir) / filename
        
        try:
            # Write the code to temporary file
            with open(script_path, 'w') as f:
                f.write(cleaned_code)
            
            # Run manim command
            cmd = [
                "manim", 
                "-pql",  # preview, quality low for faster rendering
                str(script_path), 
                scene_name
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            
            # Execute manim
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=temp_dir,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Find the generated video file
                media_dir = Path(temp_dir) / "media" / "videos" / filename.replace('.py', '') / "480p15"
                
                # Look for the video file
                video_files = list(media_dir.glob("*.mp4"))
                
                if video_files:
                    video_file = video_files[0]
                    
                    # Copy video to output directory
                    final_video_path = self.output_dir / f"{scene_name}_{video_file.name}"
                    shutil.copy2(video_file, final_video_path)
                    
                    # Clean up temp directory
                    shutil.rmtree(temp_dir)
                    
                    return True, f"Animation compiled successfully! Video saved to: {final_video_path}", str(final_video_path)
                else:
                    return False, f"Video file not found after compilation. Output: {result.stdout}\nError: {result.stderr}", None
            else:
                return False, f"Manim compilation failed:\nOutput: {result.stdout}\nError: {result.stderr}", None
                
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out (5 minutes)", None
        except Exception as e:
            return False, f"Compilation error: {str(e)}", None
        finally:
            # Clean up temp directory if it still exists
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
    
    def compile_with_quality(self, code: str, quality: str = "l", filename: str = None) -> Tuple[bool, str, Optional[str]]:
        """
        Compile Manim code with specified quality.
        
        Args:
            code: Manim Python code
            quality: Quality setting (l=low, m=medium, h=high, p=production)
            filename: Optional filename for the script
            
        Returns:
            Tuple of (success, message, video_path)
        """
        
        # Clean the code
        cleaned_code = self.clean_code(code)
        
        # Extract scene name
        scene_name = self.extract_scene_name(cleaned_code)
        
        # Generate filename if not provided
        if filename is None:
            filename = f"generated_animation_{scene_name.lower()}.py"
        
        # Create temporary file for the script
        temp_dir = tempfile.mkdtemp()
        script_path = Path(temp_dir) / filename
        
        try:
            # Write the code to temporary file
            with open(script_path, 'w') as f:
                f.write(cleaned_code)
            
            # Run manim command with specified quality
            quality_flag = f"-pq{quality}"
            cmd = [
                "manim", 
                quality_flag,
                str(script_path), 
                scene_name
            ]
            
            print(f"Running command: {' '.join(cmd)}")
            
            # Execute manim
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=temp_dir,
                timeout=600  # 10 minute timeout for higher quality
            )
            
            if result.returncode == 0:
                # Find the generated video file - quality affects the subdirectory
                quality_dirs = {
                    'l': '480p15',
                    'm': '720p30', 
                    'h': '1080p60',
                    'p': '2160p60'
                }
                
                quality_subdir = quality_dirs.get(quality, '480p15')
                media_dir = Path(temp_dir) / "media" / "videos" / filename.replace('.py', '') / quality_subdir
                
                # Look for the video file
                video_files = list(media_dir.glob("*.mp4"))
                
                if video_files:
                    video_file = video_files[0]
                    
                    # Copy video to output directory
                    final_video_path = self.output_dir / f"{scene_name}_{quality}_{video_file.name}"
                    shutil.copy2(video_file, final_video_path)
                    
                    # Clean up temp directory
                    shutil.rmtree(temp_dir)
                    
                    return True, f"Animation compiled successfully! Video saved to: {final_video_path}", str(final_video_path)
                else:
                    return False, f"Video file not found after compilation. Output: {result.stdout}\nError: {result.stderr}", None
            else:
                return False, f"Manim compilation failed:\nOutput: {result.stdout}\nError: {result.stderr}", None
                
        except subprocess.TimeoutExpired:
            return False, "Compilation timed out", None
        except Exception as e:
            return False, f"Compilation error: {str(e)}", None
        finally:
            # Clean up temp directory if it still exists
            if os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass