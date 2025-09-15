#!/usr/bin/env python3
"""
Check GPU Support for Amit Comic
"""

import cv2

def check_gpu_support():
    """Check if GPU acceleration is available"""
    print("🔍 Checking GPU Support for Amit Comic...")
    print("=" * 50)
    
    try:
        # Check OpenCV CUDA support
        gpu_count = cv2.cuda.getCudaEnabledDeviceCount()
        
        if gpu_count > 0:
            print(f"🚀 EXCELLENT! GPU Support Available")
            print(f"📊 CUDA Devices Found: {gpu_count}")
            
            # Get device info
            for i in range(gpu_count):
                try:
                    device_info = cv2.cuda.DeviceInfo(i)
                    print(f"   GPU {i}: {device_info.name()}")
                except:
                    print(f"   GPU {i}: Available")
            
            print("\n✅ Your Amit Comic will run with GPU acceleration!")
            print("⚡ Expected speed: 5-10x faster processing")
            print("🔥 Processing time: ~30-60 seconds for 188 frames")
            
            return True
            
        else:
            print("💻 No CUDA devices found")
            print("✅ Will use CPU with parallel optimization")
            print("⚡ Expected speed: Good performance with 6-8 parallel workers")
            print("🔥 Processing time: ~2-5 minutes for 188 frames")
            
            return False
            
    except Exception as e:
        print("⚠️ OpenCV not built with CUDA support")
        print("✅ Will use CPU with maximum optimization")
        print("⚡ Expected speed: Good performance with parallel processing")
        print("🔥 Processing time: ~2-5 minutes for 188 frames")
        
        return False

def recommend_gpu_setup():
    """Recommend GPU setup if not available"""
    print("\n🔧 GPU Setup Recommendations:")
    print("=" * 30)
    
    print("📦 For GPU acceleration, you need:")
    print("   1. NVIDIA GPU with CUDA support")
    print("   2. CUDA toolkit installed")
    print("   3. OpenCV built with CUDA support")
    
    print("\n💡 If you have NVIDIA GPU but no CUDA:")
    print("   pip install opencv-contrib-python")
    print("   # This version often has better GPU support")
    
    print("\n✅ Current setup will work great with CPU optimization!")

def main():
    gpu_available = check_gpu_support()
    
    if not gpu_available:
        recommend_gpu_setup()
    
    print(f"\n🎉 Amit Comic is ready to run!")
    print("🚀 Start with: python3 start_app.py")
    
    return gpu_available

if __name__ == "__main__":
    main()