#!/usr/bin/env python3
"""
Fix PyTorch compatibility issues for Real-ESRGAN
"""

import subprocess
import sys

def fix_pytorch_compatibility():
    """Install compatible PyTorch versions"""
    print("🔧 Fixing PyTorch compatibility for Real-ESRGAN...")
    
    # Uninstall existing PyTorch
    print("📦 Removing existing PyTorch installations...")
    uninstall_packages = [
        "torch",
        "torchvision", 
        "torchaudio"
    ]
    
    for package in uninstall_packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "uninstall", 
                package, "-y", "--break-system-packages"
            ], check=False, capture_output=True)
            print(f"🗑️ Removed {package}")
        except:
            pass
    
    # Install compatible versions
    print("📦 Installing compatible PyTorch versions...")
    compatible_packages = [
        "torch==2.0.1",
        "torchvision==0.15.2",
        "torchaudio==2.0.2"
    ]
    
    for package in compatible_packages:
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                package, "--break-system-packages", "--no-cache-dir"
            ], check=True, capture_output=True, text=True, timeout=300)
            print(f"✅ Installed {package}")
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout installing {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e.stderr}")
    
    # Test installation
    print("🧪 Testing PyTorch installation...")
    try:
        import torch
        import torchvision
        print(f"✅ PyTorch {torch.__version__}")
        print(f"✅ torchvision {torchvision.__version__}")
        
        # Test torchvision.transforms.functional_tensor
        try:
            import torchvision.transforms.functional_tensor
            print("✅ torchvision.transforms.functional_tensor available")
        except ImportError:
            print("⚠️ torchvision.transforms.functional_tensor still not available")
            
        return True
    except ImportError as e:
        print(f"❌ PyTorch test failed: {e}")
        return False

def install_realesrgan():
    """Install Real-ESRGAN with compatible dependencies"""
    print("📦 Installing Real-ESRGAN with compatible dependencies...")
    
    packages = [
        "basicsr==1.4.2",
        "realesrgan==0.3.0"
    ]
    
    for package in packages:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                package, "--break-system-packages", "--no-deps"
            ], check=True, capture_output=True, timeout=120)
            print(f"✅ Installed {package}")
        except Exception as e:
            print(f"❌ Failed to install {package}: {e}")

def main():
    print("🔧 PyTorch Compatibility Fix for Real-ESRGAN")
    print("=" * 50)
    
    # Fix PyTorch
    if fix_pytorch_compatibility():
        print("\n✅ PyTorch compatibility fixed!")
        
        # Install Real-ESRGAN
        install_realesrgan()
        
        print("\n🎉 Setup complete!")
        print("Real-ESRGAN should now work properly.")
    else:
        print("\n⚠️ PyTorch fix failed.")
        print("Will use fallback enhancement methods.")

if __name__ == "__main__":
    main()