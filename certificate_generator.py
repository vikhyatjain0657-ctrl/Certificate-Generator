# certificate_generator_centered.py
from PIL import Image, ImageDraw, ImageFont
import pandas as pd, os

# ------------- CONFIG -------------
TEMPLATE_PATH = "certificate_template.png"   # your template file
CSV_PATH = "data.csv"
OUTPUT_DIR = "certificates"
FONT_CANDIDATES = [
    "impact.ttf",
    "/usr/share/fonts/truetype/msttcorefonts/Impact.ttf",
    "/usr/share/fonts/truetype/impact.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
]

# Figma canvas & points (these are the values you measured in Figma)
FIGMA_CANVAS = (3508, 2480)
NAME_POS_FIGMA = (1754, 1300)
REG_POS_FIGMA  = (1522, 1433)
NAME_FONT_SIZE = 200
REG_FONT_SIZE  = 64

# spacing between name and reg (proportional to name font)
REG_SPACING_RATIO = 0.25  # 25% of name font size
# ----------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load template and compute scaling from Figma -> actual template
template = Image.open(TEMPLATE_PATH).convert("RGB")
W, H = template.size
fig_w, fig_h = FIGMA_CANVAS
scale_x, scale_y = W / fig_w, H / fig_h

# Scale Figma points to actual template
def scale_point(p):
    return (int(p[0] * scale_x), int(p[1] * scale_y))

NAME_POS = scale_point(NAME_POS_FIGMA)
REG_POS  = scale_point(REG_POS_FIGMA)

# Try to find an appropriate font
def find_font(candidates, size):
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except:
                pass
    return ImageFont.load_default()

# Read CSV
df = pd.read_csv(CSV_PATH)

for _, row in df.iterrows():
    name = str(row['Name']).strip()
    regno = str(row['RegNo']).strip()

    cert = template.copy()
    draw = ImageDraw.Draw(cert)

    # scale font sizes roughly to template
    base_scale = (scale_x + scale_y) / 2
    name_font_size = max(10, int(NAME_FONT_SIZE * base_scale))
    reg_font_size = max(8, int(REG_FONT_SIZE * base_scale))

    font_name = find_font(FONT_CANDIDATES, name_font_size)
    font_reg  = find_font(FONT_CANDIDATES, reg_font_size)

    # ---- place NAME centered at NAME_POS ----
    # compute bbox at (0,0) to get exact metrics
    bbox = draw.textbbox((0,0), name, font=font_name)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    # compute draw position so center is exactly NAME_POS
    draw_x = NAME_POS[0] - text_w // 2 - bbox[0]
    draw_y = NAME_POS[1] - text_h // 2 - bbox[1]
    draw.text((draw_x, draw_y), name, font=font_name, fill="black")

    # ---- place REGNO directly below name (use name metrics + spacing) ----
    spacing = int(name_font_size * REG_SPACING_RATIO)
    reg_draw_y = draw_y + text_h + spacing

    bbox_r = draw.textbbox((0,0), regno, font=font_reg)
    reg_w = bbox_r[2] - bbox_r[0]
    reg_h = bbox_r[3] - bbox_r[1]
    reg_draw_x = NAME_POS[0] - reg_w // 2 - bbox_r[0]
    draw.text((reg_draw_x, reg_draw_y), regno, font=font_reg, fill="black")

    # Save
    safe = "".join(c for c in name if c.isalnum() or c in (" ", "_")).rstrip()
    out = os.path.join(OUTPUT_DIR, f"{safe}_{regno}.png")
    cert.save(out)
    print("Saved:", out)

print("Done. Check the 'certificates' folder.")
