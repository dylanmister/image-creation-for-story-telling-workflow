# World Cup Story — Gemini Image Generator

Generates MS Paint-style scene illustrations for a YouTube video script using Google's Gemini Imagen API.

## Project Files

| File | Description |
|------|-------------|
| `generate_worldcup_images.py` | Python script that calls Gemini Imagen API to generate all 52 images |
| `story_transcript.txt` | Full YouTube script with all timestamps (0:01 through 4:27) |
| `scene_descriptions.txt` | Detailed image description for every timestamp — what each image should look like |
| `style_guide.txt` | Complete style requirements (MS Paint, stick figures, flat colors, 16:9, etc.) |
| `requirements.txt` | Python dependencies (google-genai, Pillow) |

## How It Works

1. The script reads 52 timestamps from the World Cup story script
2. Each timestamp has a custom scene description matched to that moment in the story
3. The Gemini Imagen API generates one 16:9 image per timestamp
4. All images are saved as PNGs named by timestamp (e.g., `0m01s.png`, `1m47s.png`)
5. Built-in retry logic and rate-limit handling
6. Skips already-generated images so you can safely re-run

## Setup

1. Install Python 3.12+

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set your Gemini API key:
   ```
   # Windows PowerShell
   $env:GEMINI_API_KEY = "your-api-key"

   # Bash
   export GEMINI_API_KEY="your-api-key"
   ```

4. Run:
   ```
   python generate_worldcup_images.py
   ```

## Style

All images use a consistent MS Paint beginner drawing style:
- Stick figures with round heads and line bodies
- White background, thick wobbly black outlines
- Flat colors only (red, blue, green, yellow, orange, brown, gray)
- 16:9 horizontal YouTube frame format
- Intentionally amateur, funny, and "bad" looking

See `style_guide.txt` for full style requirements.

## Timestamps (52 total)

0:01, 0:07, 0:15, 0:18, 0:24, 0:26, 0:35, 0:42, 0:44, 0:51, 0:56, 1:03, 1:08, 1:16, 1:21, 1:25, 1:32, 1:35, 1:40, 1:42, 1:47, 1:55, 1:59, 2:04, 2:07, 2:13, 2:20, 2:22, 2:27, 2:32, 2:39, 2:41, 2:45, 2:53, 2:59, 3:01, 3:07, 3:15, 3:19, 3:25, 3:29, 3:33, 3:41, 3:48, 3:53, 3:56, 3:58, 4:03, 4:08, 4:14, 4:21, 4:27
