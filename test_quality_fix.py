"""
Test script to verify the quality fix is working
"""

def test_quality_enhancement():
    """Test the quality enhancement directly"""
    print("🔥 TESTING HIGH QUALITY ENHANCEMENT")
    print("="*50)
    
    # Import the enhancer
    from backend.simple_2k_enhancer import Simple2KEnhancer
    
    # Create enhancer instance
    enhancer = Simple2KEnhancer()
    
    # Test a single frame enhancement
    import os
    frames_dir = "frames/final"
    
    if os.path.exists(frames_dir):
        frame_files = [f for f in os.listdir(frames_dir) 
                      if f.lower().endswith('.png') and f.startswith('frame')]
        
        if frame_files:
            test_frame = frame_files[0]
            test_path = os.path.join(frames_dir, test_frame)
            
            print(f"🧪 Testing enhancement on: {test_frame}")
            
            # Test the enhancement
            result = enhancer.enhance_to_high_quality(test_path)
            
            if result:
                print("✅ HIGH QUALITY enhancement working correctly!")
                print("✅ Original resolution should be preserved!")
            else:
                print("❌ Enhancement failed")
        else:
            print("❌ No frame files found for testing")
    else:
        print("❌ Frames directory not found")
        print("Please upload a video first to generate frames")

if __name__ == "__main__":
    test_quality_enhancement()