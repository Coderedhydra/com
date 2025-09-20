#!/usr/bin/env python3
"""
Text-to-Video Manim Generator
Uses Google Gemini API to convert text descriptions into Manim animations
"""

import argparse
import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from gemini_client import GeminiManimGenerator
from manim_compiler import ManimCompiler

class TextToVideoGenerator:
    def __init__(self, api_key: str):
        """Initialize the text-to-video generator."""
        self.gemini_client = GeminiManimGenerator(api_key)
        self.manim_compiler = ManimCompiler()
        
    def generate_video(self, text_description: str, quality: str = "l", save_code: bool = True) -> dict:
        """
        Generate video from text description.
        
        Args:
            text_description: Description of the animation
            quality: Video quality (l=low, m=medium, h=high, p=production)
            save_code: Whether to save the generated code
            
        Returns:
            Dictionary with results
        """
        
        print("🤖 Generating Manim code with Gemini AI...")
        print(f"📝 Description: {text_description}")
        print("-" * 50)
        
        try:
            # Generate Manim code
            generated_code = self.gemini_client.generate_manim_code(text_description)
            
            print("✅ Code generated successfully!")
            
            if save_code:
                # Save generated code
                code_filename = f"generated_code_{hash(text_description) % 10000}.py"
                code_path = Path("/workspace/manim_generator/generated_code") / code_filename
                code_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(code_path, 'w') as f:
                    f.write(generated_code)
                print(f"💾 Code saved to: {code_path}")
            
            print("\n🎬 Compiling animation...")
            print("-" * 50)
            
            # Compile the animation
            success, message, video_path = self.manim_compiler.compile_with_quality(
                generated_code, 
                quality=quality
            )
            
            result = {
                'success': success,
                'message': message,
                'video_path': video_path,
                'generated_code': generated_code,
                'description': text_description
            }
            
            if success:
                print(f"🎉 SUCCESS! {message}")
                print(f"🎥 Video available at: {video_path}")
            else:
                print(f"❌ FAILED: {message}")
                
                # Try to refine the code if compilation failed
                print("\n🔧 Attempting to fix the code...")
                try:
                    refined_code = self.gemini_client.refine_code(
                        generated_code, 
                        f"The code failed to compile with this error: {message}. Please fix the issues and return working Manim code."
                    )
                    
                    print("✅ Code refined, attempting compilation again...")
                    success, message, video_path = self.manim_compiler.compile_with_quality(
                        refined_code, 
                        quality=quality
                    )
                    
                    result.update({
                        'success': success,
                        'message': message,
                        'video_path': video_path,
                        'generated_code': refined_code,
                        'refined': True
                    })
                    
                    if success:
                        print(f"🎉 SUCCESS after refinement! {message}")
                        print(f"🎥 Video available at: {video_path}")
                        
                        if save_code:
                            # Save refined code
                            refined_code_filename = f"refined_code_{hash(text_description) % 10000}.py"
                            refined_code_path = Path("/workspace/manim_generator/generated_code") / refined_code_filename
                            
                            with open(refined_code_path, 'w') as f:
                                f.write(refined_code)
                            print(f"💾 Refined code saved to: {refined_code_path}")
                    else:
                        print(f"❌ Still failed after refinement: {message}")
                        
                except Exception as e:
                    print(f"❌ Error during code refinement: {str(e)}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error during video generation: {str(e)}"
            print(f"❌ {error_msg}")
            return {
                'success': False,
                'message': error_msg,
                'video_path': None,
                'generated_code': None,
                'description': text_description
            }

def interactive_mode(generator: TextToVideoGenerator):
    """Run in interactive mode, asking user for input."""
    
    print("🎬 Welcome to Text-to-Video Manim Generator!")
    print("=" * 50)
    print("This tool uses Google Gemini AI to convert your text descriptions")
    print("into beautiful Manim animations and compile them into videos.")
    print("=" * 50)
    
    while True:
        print("\n📝 Please describe the animation you want to create:")
        print("(Type 'quit' to exit)")
        
        text_input = input("> ").strip()
        
        if text_input.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not text_input:
            print("❌ Please provide a description!")
            continue
        
        # Ask for quality preference
        print("\n🎥 Choose video quality:")
        print("  l - Low (480p, fast)")
        print("  m - Medium (720p)")
        print("  h - High (1080p)")
        print("  p - Production (4K, slow)")
        
        quality = input("Quality [l]: ").strip().lower()
        if quality not in ['l', 'm', 'h', 'p']:
            quality = 'l'
        
        print(f"\n🚀 Generating video with {quality} quality...")
        print("=" * 50)
        
        # Generate the video
        result = generator.generate_video(text_input, quality=quality)
        
        print("\n" + "=" * 50)
        
        if result['success']:
            print("🎊 Video generation completed successfully!")
            print(f"📁 Video saved to: {result['video_path']}")
        else:
            print("😞 Video generation failed.")
            print("💡 Try rephrasing your description or check the error message above.")
        
        print("\n" + "=" * 50)

def main():
    parser = argparse.ArgumentParser(description="Text-to-Video Manim Generator using Gemini AI")
    parser.add_argument("--text", "-t", help="Text description for the animation")
    parser.add_argument("--quality", "-q", choices=['l', 'm', 'h', 'p'], default='l',
                       help="Video quality: l=low, m=medium, h=high, p=production")
    parser.add_argument("--api-key", help="Google Gemini API key (or use GEMINI_API_KEY env var)")
    parser.add_argument("--interactive", "-i", action="store_true", 
                       help="Run in interactive mode")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("GEMINI_API_KEY", "AIzaSyDUUbB-qXEgU_4uz_LMppDqrFHPm1mWXn4")
    
    if not api_key:
        print("❌ Error: No API key provided!")
        print("Please provide API key via --api-key argument or GEMINI_API_KEY environment variable")
        sys.exit(1)
    
    # Initialize generator
    generator = TextToVideoGenerator(api_key)
    
    if args.interactive or not args.text:
        # Interactive mode
        interactive_mode(generator)
    else:
        # Single generation mode
        print("🎬 Text-to-Video Manim Generator")
        print("=" * 50)
        
        result = generator.generate_video(args.text, quality=args.quality)
        
        if result['success']:
            print(f"\n🎉 Success! Video saved to: {result['video_path']}")
            sys.exit(0)
        else:
            print(f"\n❌ Failed: {result['message']}")
            sys.exit(1)

if __name__ == "__main__":
    main()