# Text-to-Video Manim Generator - Usage Guide

## 🎬 What is this?

This is a powerful AI-powered tool that converts natural language descriptions into beautiful animated videos using:
- **Google Gemini AI** for intelligent code generation
- **Manim** (Mathematical Animation Engine) for creating professional animations
- **Automatic compilation** to produce MP4 videos

## 🚀 Quick Start

### Method 1: Interactive Mode (Recommended for beginners)

```bash
cd /workspace/manim_generator
source venv/bin/activate
python main.py -i
```

This will start an interactive session where you can:
1. Enter natural language descriptions of animations
2. Choose video quality (low, medium, high, production)
3. Generate multiple videos in one session

### Method 2: Command Line Mode (For single animations)

```bash
cd /workspace/manim_generator
source venv/bin/activate
python main.py -t "Your animation description here"
```

### Method 3: Custom Quality

```bash
python main.py -t "Your description" -q h  # High quality (1080p)
```

## 🎯 Example Descriptions

Here are some example descriptions you can try:

### 🔷 Basic Shapes and Transformations
- "Create a circle transforming into a square with smooth transitions"
- "Show a triangle rotating 360 degrees with changing colors"
- "Animate a pentagon morphing into a hexagon"

### 📊 Mathematical Visualizations
- "Visualize the Pythagorean theorem with a right triangle and squares"
- "Show a sine wave transforming into a cosine wave"
- "Create an animation of the quadratic formula with a parabola"
- "Animate the concept of derivatives with a tangent line moving along a curve"

### 🎨 Text and Effects
- "Create text saying 'Hello World' with colorful fade-in effects"
- "Show the word 'MATHEMATICS' with each letter appearing one by one"
- "Animate a title sequence with glowing text effects"

### ⚗️ Physics and Science
- "Show a pendulum swinging with physics equations appearing"
- "Animate the solar system with planets orbiting the sun"
- "Create a visualization of wave interference patterns"

### 📈 Data and Graphs
- "Show a bar chart growing from zero with animated bars"
- "Create a line graph that draws itself over time"
- "Animate a pie chart with slices appearing sequentially"

## 🎥 Video Quality Options

| Quality | Resolution | FPS | Description | Render Time |
|---------|------------|-----|-------------|-------------|
| **l** (Low) | 480p | 15 | Fast rendering, good for testing | ~30 seconds |
| **m** (Medium) | 720p | 30 | Balanced quality and speed | ~1-2 minutes |
| **h** (High) | 1080p | 60 | High quality for final videos | ~3-5 minutes |
| **p** (Production) | 4K | 60 | Maximum quality, very slow | ~10+ minutes |

## 📁 Output Files

### Videos
- **Location**: `/workspace/manim_generator/videos/`
- **Format**: MP4
- **Naming**: `SceneName_quality_filename.mp4`

### Generated Code
- **Location**: `/workspace/manim_generator/generated_code/`
- **Format**: Python (.py files)
- **Purpose**: You can inspect and modify the generated Manim code

## 🔧 Advanced Usage

### Using Your Own API Key

```bash
# Set environment variable
export GEMINI_API_KEY="your_api_key_here"
python main.py -t "your description"

# Or use command line argument
python main.py --api-key "your_api_key_here" -t "your description"
```

### Batch Processing

Create a script to process multiple descriptions:

```python
from main import TextToVideoGenerator

generator = TextToVideoGenerator("your_api_key")

descriptions = [
    "Create a bouncing ball animation",
    "Show a rotating cube with lighting effects",
    "Animate mathematical functions"
]

for desc in descriptions:
    result = generator.generate_video(desc, quality="m")
    if result['success']:
        print(f"✅ Created: {result['video_path']}")
```

## 🛠️ Troubleshooting

### Common Issues

1. **"latex not found" error**
   - Solution: LaTeX is already installed in this environment

2. **"Compilation failed" error**
   - The system automatically tries to fix code errors
   - Try rephrasing your description
   - Check the generated code in `generated_code/` directory

3. **Long rendering times**
   - Use lower quality settings for testing
   - Complex animations naturally take longer

4. **Out of memory errors**
   - Use simpler descriptions
   - Lower the quality setting
   - Restart the system if needed

### Getting Better Results

1. **Be Specific**: Instead of "animate shapes", try "create a blue circle transforming into a red square"

2. **Include Details**: Mention colors, sizes, positions, and timing
   - Good: "Show a large green triangle rotating clockwise for 5 seconds"
   - Better: "Create a bright green equilateral triangle with a 2-unit side length, rotating 360 degrees clockwise over 5 seconds with a smooth animation"

3. **Mathematical Terms**: Use proper mathematical terminology
   - "parabola", "sine wave", "derivative", "integral"

4. **Animation Terms**: Use Manim-friendly language
   - "fade in", "transform", "morph", "rotate", "scale", "translate"

## 🎨 Creative Ideas

### Educational Content
- Mathematical concept explanations
- Physics simulations
- Chemistry molecular animations
- Geometry proofs

### Artistic Animations
- Abstract geometric patterns
- Color transitions and gradients
- Rhythmic movements
- Logo animations

### Data Visualizations
- Statistical charts and graphs
- Time-series data animations
- Comparative visualizations
- Interactive dashboards (static)

## 📚 Learning More

### Manim Resources
- [Manim Community Documentation](https://docs.manim.community/)
- [3Blue1Brown's Manim](https://github.com/3b1b/manim)
- [Manim Tutorial Videos](https://www.youtube.com/results?search_query=manim+tutorial)

### Understanding Generated Code
The generated Python files use standard Manim syntax:
- `Scene`: The main animation class
- `construct()`: Method containing the animation sequence
- `self.play()`: Execute animations
- `self.wait()`: Pause between animations

## 🎉 Have Fun!

This tool opens up endless possibilities for creating educational content, artistic animations, and mathematical visualizations. Experiment with different descriptions and see what amazing animations you can create!

Remember: The more detailed and specific your descriptions, the better the results will be!