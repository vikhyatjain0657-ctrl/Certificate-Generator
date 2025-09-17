import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

TEMPLATE_PATH = "certificate_template.png"
CSV_PATH = "data.csv"
OUTPUT_DIR = "certificates"
FONT_PATH = "impact.ttf"   # exact font from Figma

# Certificate dimensions (A4, 300 DPI)
CERT_WIDTH, CERT_HEIGHT = 3508, 2480

# Positions (as percentages of canvas)
NAME_POS = (int(CERT_WIDTH * 0.5), int(CERT_HEIGHT * 0.55))
REGNO_POS = (int(CERT_WIDTH * 0.5), int(CERT_HEIGHT * 0.65))

# Font sizes (tweak as needed)
FONT_SIZE_NAME = 150
FONT_SIZE_REGNO = 100

# Create output dir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load template
template = Image.open(TEMPLATE_PATH)

# Load fonts
font_name = ImageFont.truetype(FONT_PATH, FONT_SIZE_NAME)
font_reg = ImageFont.truetype(FONT_PATH, FONT_SIZE_REGNO)

# Read CSV
df = pd.read_csv(CSV_PATH)

for _, row in df.iterrows():
    name = str(row['Name'])
    regno = str(row['RegNo'])

    cert = template.copy()
    draw = ImageDraw.Draw(cert)

    # Add centered text (anchor="mm" = middle center)
    draw.text(NAME_POS, name, font=font_name, fill="black", anchor="mm")
    draw.text(REGNO_POS, regno, font=font_reg, fill="black", anchor="mm")

    output_path = os.path.join(OUTPUT_DIR, f"{name}_{regno}.png")
    cert.save(output_path)

    print(f"✅ Certificate generated: {output_path}")
