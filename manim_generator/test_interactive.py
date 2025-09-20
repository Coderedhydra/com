#!/usr/bin/env python3
"""
Test script to demonstrate the interactive functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from main import TextToVideoGenerator

def test_interactive():
    """Test the generator with a few examples"""
    
    api_key = "AIzaSyDUUbB-qXEgU_4uz_LMppDqrFHPm1mWXn4"
    generator = TextToVideoGenerator(api_key)
    
    test_cases = [
        "Show a simple bouncing ball animation",
        "Create a mathematical visualization of the Pythagorean theorem",
        "Animate text saying 'Hello Manim!' with cool effects"
    ]
    
    print("🎬 Testing Text-to-Video Manim Generator")
    print("=" * 50)
    
    for i, description in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {description}")
        print("-" * 30)
        
        result = generator.generate_video(description, quality="l")
        
        if result['success']:
            print(f"✅ Test {i} passed! Video: {result['video_path']}")
        else:
            print(f"❌ Test {i} failed: {result['message']}")
    
    print("\n🎉 Testing complete!")

if __name__ == "__main__":
    test_interactive()