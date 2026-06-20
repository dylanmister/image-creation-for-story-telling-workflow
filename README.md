# World Cup Story — Gemini Image Generator

Generates MS Paint-style scene illustrations for a YouTube video script using Google's Gemini Imagen API.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set your Gemini API key:
   ```
   # Windows PowerShell
   $env:GEMINI_API_KEY = "your-api-key"

   # Bash
   export GEMINI_API_KEY="your-api-key"
   ```

3. Run:
   ```
   python generate_worldcup_images.py
   ```

Images are saved as `0m01s.png`, `0m07s.png`, etc. in this folder.

## Style

All images are generated as simple MS Paint-style stick figure drawings in 16:9 format — intentionally amateur, funny, and "bad" looking.
