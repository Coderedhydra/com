"""
Test the image stitcher directly
"""

def test_stitcher():
    """Test the image stitcher"""
    print("🧪 Testing Image Stitcher...")
    
    from backend.image_stitcher import ImageStitcher
    
    # Create stitcher
    stitcher = ImageStitcher()
    
    # Test stitching
    success = stitcher.stitch_comic_page("test_stitched_output.png")
    
    if success:
        print("✅ Stitcher test successful!")
        print("📁 Check test_stitched_output.png")
    else:
        print("❌ Stitcher test failed")

if __name__ == "__main__":
    test_stitcher()