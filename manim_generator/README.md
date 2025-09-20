# Text-to-Video Manim Generator

A powerful tool that converts text descriptions into beautiful animated videos using Google Gemini AI and Manim (Mathematical Animation Engine).

## Features

- 🤖 **AI-Powered**: Uses Google Gemini AI to generate Manim code from text descriptions
- 🎬 **Automatic Compilation**: Compiles generated code into video files automatically
- 🔧 **Self-Healing**: Attempts to fix compilation errors automatically
- 🎥 **Multiple Quality Options**: Low, Medium, High, and Production quality settings
- 💾 **Code Preservation**: Saves generated code for inspection and reuse
- 🖥️ **Interactive Mode**: Easy-to-use interactive interface

## Installation

1. **Clone/Download** this directory to your system
2. **Install dependencies**:
   ```bash
   cd manim_generator
   python setup.py
   ```

## Usage

### Interactive Mode (Recommended)

```bash
python main.py -i
```

This will start an interactive session where you can:
- Describe animations in natural language
- Choose video quality
- Generate multiple videos in one session

### Command Line Mode

```bash
python main.py -t "Create an animation showing a circle transforming into a square"
```

### Advanced Options

```bash
# Specify quality (l=low, m=medium, h=high, p=production)
python main.py -t "your description" -q h

# Use custom API key
python main.py -t "your description" --api-key YOUR_API_KEY
```

## Quality Settings

- **Low (l)**: 480p, 15fps - Fast rendering, good for testing
- **Medium (m)**: 720p, 30fps - Balanced quality and speed
- **High (h)**: 1080p, 60fps - High quality for final videos
- **Production (p)**: 4K, 60fps - Maximum quality, slow rendering

## Example Descriptions

Here are some example text descriptions you can try:

- "Create an animation showing the Pythagorean theorem with a right triangle and squares on each side"
- "Animate a sine wave transforming into a cosine wave with labels"
- "Show a pendulum swinging with physics equations appearing"
- "Create a visualization of the quadratic formula with a parabola"
- "Animate text saying 'Hello World' with colorful effects"
- "Show a circle morphing into different shapes"

## Output

- **Videos**: Saved to `videos/` directory in MP4 format
- **Generated Code**: Saved to `generated_code/` directory for inspection
- **Logs**: Compilation output shown in terminal

## API Key

The tool uses the Google Gemini API key: `AIzaSyDUUbB-qXEgU_4uz_LMppDqrFHPm1mWXn4`

You can also set your own API key via:
- Command line: `--api-key YOUR_KEY`
- Environment variable: `export GEMINI_API_KEY=YOUR_KEY`

## Troubleshooting

### Common Issues

1. **Manim not found**: Make sure Manim is properly installed
   ```bash
   pip install manim
   ```

2. **FFmpeg missing**: Install FFmpeg for video rendering
   - Ubuntu/Debian: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from https://ffmpeg.org/

3. **Compilation errors**: The tool automatically attempts to fix errors, but you can:
   - Try rephrasing your description
   - Check the generated code in `generated_code/`
   - Use lower quality settings for faster debugging

### Getting Help

- Check the generated code in `generated_code/` directory
- Look at compilation output for specific errors
- Try simpler descriptions first to test the system

## File Structure

```
manim_generator/
├── main.py              # Main application
├── gemini_client.py     # Gemini AI integration
├── manim_compiler.py    # Manim compilation logic
├── setup.py            # Installation script
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── videos/            # Generated videos
└── generated_code/    # Generated Manim code
```

## How It Works

1. **Text Input**: You provide a natural language description
2. **AI Generation**: Gemini AI converts your description to Manim Python code
3. **Code Compilation**: The system compiles the code using Manim
4. **Video Output**: A rendered MP4 video is produced
5. **Error Handling**: If compilation fails, AI attempts to fix the code

## Examples of Generated Animations

The system can create various types of animations:
- Mathematical visualizations
- Geometric transformations
- Text animations
- Physics simulations
- Data visualizations
- Educational content

Enjoy creating amazing animations! 🎬✨