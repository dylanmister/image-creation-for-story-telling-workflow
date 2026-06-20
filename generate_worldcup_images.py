import os
import sys
import time
import re
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Installing google-genai...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "Pillow"])
    from google import genai
    from google.genai import types

from PIL import Image
import io

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: Set GEMINI_API_KEY environment variable first.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = Path(r"C:\Users\dylan\World Cup story, Gemini created images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

STYLE_PREFIX = (
    "Draw this scene in the style of an extremely simple, amateur MS Paint drawing. "
    "White background. Thick, uneven black outlines. Wobbly hand-drawn lines. "
    "Stick-figure humans with round heads and line bodies. Simple dot eyes. "
    "Very basic facial expressions. Flat colors only (green, brown, gray, red, yellow, orange, blue). "
    "No realistic shading, no 3D, no cinematic lighting, no cartoon style, no anime, no polished illustration. "
    "Objects drawn with basic shapes: squares, circles, rectangles, arrows. "
    "Handwritten-looking text only when needed, short and spelled correctly. "
    "Red arrows or red question marks when needed. Mostly white empty space. "
    "The drawing should feel amateur, funny, and intentionally bad, like a beginner drew it in MS Paint. "
    "Horizontal 16:9 wide YouTube frame format. Clear, readable, centered composition with space around characters. "
    "No glitches, no broken anatomy, no messy overlapping. Keep it simple and funny.\n\n"
)

scenes = [
    ("0m01s", "A stick figure standing with a small suitcase, looking excited. A thought bubble shows the World Cup trophy. Text on the side: 'World Cup here I come'. The stick figure has a big smile."),
    ("0m07s", "A stick figure looking at a phone/computer screen. The screen shows text 'bro the World Cup is once in a lifetime'. The stick figure has wide eyes and looks convinced."),
    ("0m15s", "A stick figure with a devil on one shoulder whispering 'terrible financial decisions'. The stick figure is smiling and nodding. A wallet is visible with money flying out."),
    ("0m18s", "A stick figure sitting at a computer clicking a 'BOOK NOW' button. A credit card is on the desk. The stick figure looks determined and happy."),
    ("0m24s", "A stick figure next to a checklist on a whiteboard. Items: 'Flight ✓', 'Ticket ✓', 'Hotel ✓'. The stick figure looks proud with hands on hips."),
    ("0m26s", "A stick figure at a desk with a laptop showing a spreadsheet with numbers. The stick figure is wearing tiny glasses and looks smug. Text: 'Budget Master'."),
    ("0m35s", "A stick figure stepping off an airplane onto American ground. A sign says 'WELCOME TO USA'. Dollar signs float everywhere in the air around the figure. The figure looks nervous."),
    ("0m42s", "A stick figure surrounded by floating dollar signs and price tags on everything - the ground, the air, a bench, a trash can. The figure has a shocked face. Text: 'Everything costs money'."),
    ("0m44s", "A stick figure standing outside an airport building, sweating. Wavy heat lines in the air. A thought bubble shows a water bottle. The figure looks desperate."),
    ("0m51s", "A stick figure at a store counter holding a water bottle. The cashier stick figure points to a price tag showing a ridiculously large number. The buyer has a shocked/confused face."),
    ("0m56s", "A stick figure holding a water bottle, blushing, with a thought bubble showing a phone number. The cashier stick figure stands behind the counter. A red question mark floats above the buyer's head."),
    ("1m03s", "A stick figure sadly handing over a big pile of money for a tiny water bottle. The figure has tears. The water bottle is tiny compared to the pile of cash."),
    ("1m08s", "A stick figure taking a tiny micro-sip from a water bottle, eyes wide, being very careful. The bottle has a golden glow around it. Text: 'liquid gold'."),
    ("1m16s", "A stick figure walking and clutching a water bottle to their chest protectively, like a precious treasure. A small health bar appears above them like in a video game, nearly empty. Text: 'Last healing potion'."),
    ("1m21s", "A stick figure looking at a phone screen showing a rideshare app. A small map is on the screen. A thought bubble shows a hotel building. The figure looks hopeful."),
    ("1m25s", "A stick figure looking at a phone. The phone screen shows '$20' with a small car icon. The figure looks slightly concerned but okay. A speech bubble: 'manageable'."),
    ("1m32s", "Same stick figure looking at phone, but now the screen shows '$30'. The figure's eyes are wider. A red arrow pointing up next to the price."),
    ("1m35s", "Same stick figure, phone now shows '$50'. The figure is sweating with huge shocked eyes. Multiple red arrows pointing up. The price has a fire emoji drawn next to it."),
    ("1m40s", "A stick figure watching a phone screen with a rising price chart line going up like a stock market graph. The figure looks panicked. Text: 'STONKS' with a red arrow going up."),
    ("1m42s", "A stick figure getting into a simple boxy car (drawn as a rectangle with circles for wheels). The figure is nervously handing money to the driver stick figure."),
    ("1m47s", "A stick figure sitting in the back of a car (shown from the side). The car is stuck in traffic (several boxy cars in a line). A meter/counter on the dashboard shows rising numbers. The figure is doing math equations floating around their head."),
    ("1m55s", "A stick figure stepping out of a car at a hotel. The car has a giant receipt trailing behind it. The figure's wallet is completely empty (shown open with moths flying out). The hotel is a simple rectangle building."),
    ("1m59s", "A stick figure lying on a simple bed in a hotel room (rectangle room). The figure looks exhausted but relieved. A speech bubble says 'finally'."),
    ("2m04s", "A split image: on the left, a computer screen showing 'Hotel: 20 min from stadium' with a checkmark. On the right, reality shows a dotted line path that goes all the way across the image with the stadium far far away. A red X over the '20 min'."),
    ("2m07s", "A stick figure imagining traveling in a fighter jet (simple triangle jet) to the stadium. Versus reality: sitting in traffic in a tiny car. Two panels side by side."),
    ("2m13s", "A stick figure getting into a car, looking determined. A big red text stamp says 'HUGE MISTAKE'. Warning signs and red arrows point at the car."),
    ("2m20s", "A stick figure pulling a simple car into a parking lot. A parking sign is visible. The figure looks unsuspecting."),
    ("2m22s", "A parking attendant stick figure at a booth pointing to a price sign with a huge number. The driver stick figure is laughing. The price has multiple zeros."),
    ("2m27s", "A stick figure standing in a parking lot looking at a receipt. A thought bubble shows the figure owning the whole parking lot with a 'SOLD' sign and a deed/certificate. A ribbon-cutting ceremony imagined."),
    ("2m32s", "A stick figure next to their parked car, sitting in a lawn chair as if they live there now. A small 'HOME SWEET HOME' sign is taped to the car. A tiny garden is drawn next to the parking spot."),
    ("2m39s", "A stick figure looking at a parked car with a calculator. Dollar signs surround the car. A thought bubble: 'I live here now'. The figure shrugs."),
    ("2m41s", "A stick figure walking through a big stadium entrance gate (simple arch shape). Inside, many tiny stick figures are visible with different colored flags. The entering figure looks amazed with wide eyes."),
    ("2m45s", "Many stick figures inside a stadium (shown as rows of seats). Tiny flags from different countries. Musical notes floating (people singing). The main figure in the center with arms up, excited. Colorful confetti or streamers."),
    ("2m53s", "A stick figure in the stadium crowd, stomach growling (wavy lines from belly). A thought bubble shows food: hot dog, fries, soda. The figure looks hungry."),
    ("2m59s", "A stick figure standing in front of a food stand labeled 'STADIUM FOOD'. The prices on the menu board are absurdly high numbers. The figure's jaw has dropped to the floor."),
    ("3m01s", "A stick figure at a food counter. Three items on the counter: a hot dog, a soda cup, and fries. The cashier stick figure shows a huge total. The buyer is looking behind them confused, pointing at themselves. Text: 'Just for me??'"),
    ("3m07s", "A hot dog drawn with a nervous sweating face on it. The hot dog knows it's expensive. The stick figure is sadly eating it. Dollar signs float around the hot dog."),
    ("3m15s", "A stick figure looking at a spreadsheet/paper that is on fire. The spreadsheet has a sad face drawn on it. Text: 'Budget: DEAD'. A small tombstone labeled 'R.I.P. Budget'."),
    ("3m19s", "A spreadsheet paper with stick legs and arms, carrying a tiny suitcase, walking away. The paper looks angry/tired. A speech bubble from it: 'I quit'. The main stick figure watches sadly."),
    ("3m25s", "A stick figure looking sad about money, but then another stick figure from a different country (with a different flag) waves hello. Musical notes and hearts appear. The mood shifts from sad to happy."),
    ("3m29s", "Multiple stick figures from different countries (each holding a tiny different-colored flag) standing together, singing. Musical notes everywhere. Arms linked. Everyone smiling."),
    ("3m33s", "A group of stick figures that just met, now best friends with arms around each other. A clock shows '90 minutes'. Hearts and musical notes. A soccer ball is nearby."),
    ("3m41s", "A stick figure happily hanging out with new friends but a tiny thought bubble shows '$18 DRINK'. The figure shrugs it off with a smile. The drink is tiny, the fun is big."),
    ("3m48s", "A stick figure in a team merchandise store surrounded by jerseys, scarves, hats, and keychains on shelves. The figure said 'I won't buy anything' but is now holding everything. A crossed-out speech bubble says 'NO souvenirs'."),
    ("3m53s", "A stick figure with arms absolutely full of merchandise: jersey, scarf, hat, keychain, and one mystery item with a question mark on it. The figure looks confused at the mystery item."),
    ("3m56s", "A cashier stick figure asking 'Want a bag?' and the buyer stick figure surrounded by a mountain of merchandise responds 'I need a financial advisor'. The register shows a huge number."),
    ("3m58s", "A stick figure walking out of a store with tons of bags. Money bills are flying away behind them. The figure's wallet is crying (drawn with a sad face). Text: 'Financial advisor needed'."),
    ("4m03s", "A stick figure looking at a phone/paper showing a bank balance that is nearly zero. The bank account graph line crashes down like a stock market crash. Disaster symbols: cracks, smoke, a tiny explosion."),
    ("4m08s", "A stick figure sitting and smiling, surrounded by happy memory bubbles: the stadium, the fans, the flags, the singing. Despite an empty wallet on the ground, the figure gives a thumbs up. Text: 'Worth it'."),
    ("4m14s", "A stick figure pointing forward confidently. A speech bubble: 'I'll budget better next time'. A second tiny thought bubble: 'probably not'. The figure is winking."),
    ("4m21s", "A stick figure with a halo and angel wings saying 'I'll follow a budget' but a devil version of the same figure behind says 'ABSOLUTELY NOT'. A budget paper is being torn in half."),
    ("4m27s", "A stick figure holding a soccer ball in one hand and an empty wallet in the other. A big sign/banner reads 'The real competition: keeping your money'. The figure shrugs with a funny smile. Dollar signs fly away."),
]

def generate_image(timestamp, description, index, total):
    prompt = STYLE_PREFIX + f"Scene description: {description}"
    filename = OUTPUT_DIR / f"{timestamp}.png"

    if filename.exists():
        print(f"  [{index}/{total}] {timestamp} — already exists, skipping.")
        return True

    print(f"  [{index}/{total}] {timestamp} — generating...")

    for attempt in range(3):
        try:
            response = client.models.generate_images(
                model="imagen-3.0-generate-002",
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="16:9",
                ),
            )

            if response.generated_images:
                img_bytes = response.generated_images[0].image.image_bytes
                img = Image.open(io.BytesIO(img_bytes))
                img.save(str(filename))
                print(f"  [{index}/{total}] {timestamp} — saved!")
                return True
            else:
                print(f"  [{index}/{total}] {timestamp} — no image returned (attempt {attempt+1})")
        except Exception as e:
            print(f"  [{index}/{total}] {timestamp} — error (attempt {attempt+1}): {e}")
            if "429" in str(e) or "quota" in str(e).lower() or "rate" in str(e).lower():
                wait = 30 * (attempt + 1)
                print(f"    Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                time.sleep(5)

    print(f"  [{index}/{total}] {timestamp} — FAILED after 3 attempts")
    return False


def main():
    total = len(scenes)
    print(f"Generating {total} images for World Cup story...")
    print(f"Output: {OUTPUT_DIR}\n")

    success = 0
    failed = 0

    for i, (timestamp, description) in enumerate(scenes, 1):
        ok = generate_image(timestamp, description, i, total)
        if ok:
            success += 1
        else:
            failed += 1
        if i < total:
            time.sleep(2)

    print(f"\nDone! {success} images saved, {failed} failed.")
    print(f"Images are in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
