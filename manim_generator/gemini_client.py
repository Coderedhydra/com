import google.generativeai as genai
import json
import os
from typing import Dict, Any

class GeminiManimGenerator:
    def __init__(self, api_key: str):
        """Initialize the Gemini API client for Manim code generation."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def generate_manim_code(self, text_description: str) -> str:
        """
        Generate Manim code based on text description.
        
        Args:
            text_description: Description of the animation to create
            
        Returns:
            Generated Manim Python code as string
        """
        
        prompt = f"""
You are an expert Manim animator. Generate a complete, runnable Manim Python script based on the following description:

"{text_description}"

Requirements:
1. Create a complete Python script with proper imports
2. Use Manim Community Edition (manim) syntax
3. Create a scene class that inherits from Scene
4. Include proper construct() method
5. Use appropriate animations and mobjects
6. Make the animation visually appealing and smooth
7. Duration should be 10-30 seconds
8. Include text, shapes, and transitions as appropriate
9. Use colors and styling to make it engaging
10. Add proper timing with wait() calls

The script should be production-ready and executable with: manim -pql script.py SceneName

Only return the Python code, no explanations or markdown formatting.

Example structure:
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Your animation code here
        pass
```

Generate the code now:
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Error generating Manim code: {str(e)}")
    
    def refine_code(self, code: str, feedback: str) -> str:
        """
        Refine existing Manim code based on feedback.
        
        Args:
            code: Existing Manim code
            feedback: User feedback for improvements
            
        Returns:
            Refined Manim code
        """
        
        prompt = f"""
You are an expert Manim animator. Please refine the following Manim code based on the feedback provided:

CURRENT CODE:
{code}

FEEDBACK:
{feedback}

Please modify the code to address the feedback while maintaining:
1. Proper Manim syntax
2. Complete runnable script
3. Good animation practices
4. Appropriate timing and transitions

Only return the improved Python code, no explanations.
"""

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Error refining Manim code: {str(e)}")