# How to Run the Comic Generation System

## 🚀 **Quick Start Commands**

### **Method 1: Main Application (Recommended)**
```bash
cd /workspace
python app.py
```

### **Method 2: Alternative Runners**
```bash
# Simple setup and run
python start_app.py

# Or use the simple runner
python run_simple.py

# Or basic main
python main.py
```

## 🌐 **Access the Application**

After running, open your browser and go to:
```
http://localhost:5000
```

The application will automatically open in your browser.

## 📋 **Step-by-Step Usage**

### **1. Start the Application**
```bash
cd /workspace
python app.py
```

You'll see:
```
Starting Amit Comic Flask application...
Open your browser and go to: http://localhost:5000
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[::1]:5000
```

### **2. Upload Video**
- Click "Upload Video" button
- Select your MP4 video file
- Or paste a video URL using "Enter Link" option

### **3. View Clean 2K Test Page**
- System automatically creates 1 test page with 4 panels
- Review the 2K quality (1280x720 per panel)
- Check if the layout and quality look good

### **4. Generate Full Comic (Optional)**
- If test page looks good, click "Generate 12 Pages"
- Creates complete 12-page comic with 48 panels
- All in clean 2K quality

## 🔧 **System Requirements**

### **Required Dependencies**
```bash
# Install required packages
pip install -r requirements.txt

# Or minimal requirements
pip install flask opencv-python pillow numpy srt
```

### **Optional (for advanced features)**
```bash
# For additional AI models (if needed)
pip install torch torchvision
```

## 🐛 **Troubleshooting**

### **Common Issues & Solutions:**

#### **1. Port Already in Use**
```bash
# If port 5000 is busy, use different port
python -c "
import sys
sys.path.append('/workspace')
from app import app
app.run(debug=True, host='0.0.0.0', port=5001)
"
```

#### **2. Missing Dependencies**
```bash
# Install missing packages
pip install flask opencv-python pillow numpy srt

# Or try different requirements file
pip install -r requirements_simple.txt
```

#### **3. Video Upload Issues**
- Ensure video is in MP4 format
- File size should be reasonable (< 500MB recommended)
- Check that `video/` directory exists

#### **4. Frame Generation Issues**
```bash
# Create required directories
mkdir -p frames/final
mkdir -p static/comic/frames/final
mkdir -p output_template
```

## 📁 **Directory Structure**
```
/workspace/
├── app.py                    # Main application
├── backend/
│   ├── simple_2k_enhancer.py   # Clean 2K enhancement
│   ├── keyframes/              # Frame extraction
│   └── ...
├── static/
│   └── comic/                  # Generated comic files
├── templates/
│   ├── index.html              # Upload page
│   └── comic.html              # Comic viewer
├── frames/
│   └── final/                  # Extracted frames
└── video/
    └── uploaded.mp4            # Uploaded video
```

## 🎯 **Expected Workflow**

### **1. Start Application**
```bash
python app.py
```

### **2. Upload Video**
- Browser opens automatically to `http://localhost:5000`
- Upload MP4 video file
- System processes video and extracts frames

### **3. View Test Page**
- Automatically redirects to test page
- Shows 1 page with 4 clean 2K panels
- Message: "Clean 2K Test Page Created Successfully!"

### **4. Generate Full Comic**
- Click "Generate 12 Pages" if test looks good
- Wait 2-3 minutes for full comic generation
- View complete 12-page comic

## ⚡ **Performance Tips**

### **For Better Performance:**
```bash
# Use smaller video files for testing
# Recommended: 30 seconds - 2 minutes video length

# Close other applications to free up memory
# Ensure sufficient disk space (2GB+ recommended)
```

### **For Faster Testing:**
```bash
# Test with short video clips first
# Use MP4 format for best compatibility
```

## 🔄 **Alternative Run Methods**

### **Method 1: Direct Python**
```bash
python app.py
```

### **Method 2: Using Start Script**
```bash
python start_app.py
```

### **Method 3: Simple Runner**
```bash
python run_simple.py
```

### **Method 4: Background Mode**
```bash
nohup python app.py &
```

## 📊 **Expected Output**

### **Console Output:**
```
🎬 Amit Comic - Clean 2K Test Page Generation
Starting clean 2K test page generation (1 page, 4 panels)...
🎯 Simple 2K Quality Enhancer - Clean & Effective
📸 ANALYZING ORIGINAL FRAMES
✅ Enhanced 4/4 frames to clean 2K
🎉 Clean 2K test page generation completed!
```

### **Browser Output:**
- Upload page at `http://localhost:5000`
- Test page at `http://localhost:5000/comic`
- Clean 2K quality panels in 2x2 grid

## 🎉 **Success Indicators**

✅ **Application Started**: Flask server running on port 5000  
✅ **Video Processed**: Frames extracted to `frames/final/`  
✅ **Test Page Created**: 4 panels in 2K quality  
✅ **Comic Viewable**: Accessible at `/comic` endpoint  
✅ **Full Comic Option**: "Generate 12 Pages" button available  

That's it! The system is now ready to create clean 2K quality comics from your videos.