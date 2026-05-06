from PIL import Image, ImageDraw, ImageFont
import math

W, H = 680, 980
BLUE = (90, 171, 219)
BLUE_SOFT = (220, 238, 248)
GOLD = (212, 168, 0)
GOLD_SOFT = (245, 220, 120)
WHITE = (255, 255, 255)
INK = (60, 70, 85)
INK_SOFT = (130, 140, 155)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# Outer thin gold frame
d.rectangle([18, 18, W - 18, H - 18], outline=GOLD, width=2)
d.rectangle([24, 24, W - 24, H - 24], outline=GOLD, width=1)

def font(size, bold=False, italic=False):
    if bold and italic:
        p = "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"
    elif bold:
        p = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    elif italic:
        p = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
    else:
        p = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    return ImageFont.truetype(p, size)

def serif(size, bold=False):
    if bold:
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", size)
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", size)

def cx_text(y, text, fnt, fill):
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, y), text, font=fnt, fill=fill)

# === TOP BLUE HEADER ===
header_top = 35
header_h = 145
d.rectangle([35, header_top, W - 35, header_top + header_h], fill=BLUE)

# Stars in header
def star(cx, cy, r_out, r_in, fill, points=5):
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=fill)

# Left stars
star(85, header_top + 60, 14, 6, GOLD)
star(118, header_top + 80, 9, 4, GOLD)
# Right stars
star(W - 85, header_top + 60, 14, 6, GOLD)
star(W - 118, header_top + 80, 9, 4, GOLD)

# Header text
cx_text(header_top + 30, "RECORD OFFICIEL", font(15, bold=True), WHITE)
cx_text(header_top + 55, "DE L'ÉCOLE", serif(36, bold=True), WHITE)
cx_text(header_top + 105, "ÉDUCATION PHYSIQUE ET À LA SANTÉ",
        font(11), BLUE_SOFT)

# === MEDAL BADGE ===
mx, my = W // 2, header_top + header_h + 75
# Outer ring (light blue)
d.ellipse([mx - 60, my - 60, mx + 60, my + 60], fill=BLUE_SOFT)
# Inner blue circle
d.ellipse([mx - 52, my - 52, mx + 52, my + 52], fill=BLUE)

# Medal text
cx_text(my - 28, "NOUVEAU", font(10, bold=True), BLUE_SOFT)
cx_text(my - 12, "RECORD", serif(20, bold=True), WHITE)
cx_text(my + 14, "DE L'ÉCOLE", font(10, bold=True), BLUE_SOFT)

# Two gold ribbons hanging down
ribbon_top = my + 50
# Left ribbon
d.polygon([(mx - 22, ribbon_top - 5), (mx - 8, ribbon_top - 5),
           (mx - 8, ribbon_top + 45),
           (mx - 15, ribbon_top + 35),
           (mx - 22, ribbon_top + 45)], fill=GOLD)
# Right ribbon
d.polygon([(mx + 8, ribbon_top - 5), (mx + 22, ribbon_top - 5),
           (mx + 22, ribbon_top + 45),
           (mx + 15, ribbon_top + 35),
           (mx + 8, ribbon_top + 45)], fill=GOLD)

# === BODY ===
y = my + 130
cx_text(y, "C E   R E C O R D   E S T   D É T E N U   P A R",
        font(11), INK_SOFT)

y += 30
cx_text(y, "Aaden", serif(72, bold=True), BLUE)

# Underline with gold accent
y += 88
d.line([(120, y), (W - 120, y)], fill=GOLD_SOFT, width=1)

# Achievement
y += 25
cx_text(y, "a établi le record de l'école en", font(15), INK)
y += 28
cx_text(y, "POSITION TRÉPIED", font(20, bold=True), INK)

y += 32
cx_text(y, "tenue sans interruption pendant", font(13), INK_SOFT)

# Big blue time box
y += 25
box_w, box_h = 280, 110
bx0 = (W - box_w) // 2
d.rectangle([bx0, y, bx0 + box_w, y + box_h], fill=BLUE)
# Inner gold border
d.rectangle([bx0 + 6, y + 6, bx0 + box_w - 6, y + box_h - 6],
            outline=GOLD, width=2)

# "4:00"
fnt_time = serif(64, bold=True)
bbox = d.textbbox((0, 0), "4:00", font=fnt_time)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
d.text((W // 2 - tw // 2, y + 14), "4:00", font=fnt_time, fill=WHITE)
cx_text(y + box_h - 24, "M I N U T E S", font(10, bold=True), GOLD_SOFT)

# Performance pill
y += box_h + 20
pill_w, pill_h = 280, 30
px0 = (W - pill_w) // 2
d.rounded_rectangle([px0, y, px0 + pill_w, y + pill_h],
                    radius=4, fill=BLUE_SOFT)
cx_text(y + 8, "P E R F O R M A N C E   E X C E P T I O N N E L L E",
        font(10, bold=True), BLUE)

# === FOOTER: ENSEIGNANTE / DATE ===
y += pill_h + 35
# Two columns separated by a small circle in the middle
col_y_label = y
col_y_value = y + 22

# Labels
left_label = "ENSEIGNANTE"
right_label = "DATE"
fl = font(10, bold=True)
bbox = d.textbbox((0, 0), left_label, font=fl)
d.text((130, col_y_label), left_label, font=fl, fill=INK_SOFT)
bbox = d.textbbox((0, 0), right_label, font=fl)
rw = bbox[2] - bbox[0]
d.text((W - 130 - rw, col_y_label), right_label, font=fl, fill=INK_SOFT)

# Values
fv = serif(20, bold=True)
d.text((130, col_y_value), "Anne-Sophie", font=fv, fill=INK)
bbox = d.textbbox((0, 0), "5 mai 2026", font=fv)
rw = bbox[2] - bbox[0]
d.text((W - 130 - rw, col_y_value), "5 mai 2026", font=fv, fill=INK)

# Underlines under each value
ul_y = col_y_value + 32
d.line([(130, ul_y), (W // 2 - 30, ul_y)], fill=BLUE, width=1)
d.line([(W // 2 + 30, ul_y), (W - 130, ul_y)], fill=BLUE, width=1)

# Center small circle with arrow icon
ccx, ccy = W // 2, ul_y
d.ellipse([ccx - 18, ccy - 18, ccx + 18, ccy + 18],
          fill=WHITE, outline=GOLD, width=1)
# Down arrow inside
d.line([(ccx, ccy - 7), (ccx, ccy + 6)], fill=BLUE, width=2)
d.polygon([(ccx - 5, ccy + 1), (ccx + 5, ccy + 1), (ccx, ccy + 7)],
          fill=BLUE)

# School name at bottom
y = ul_y + 30
cx_text(y, "École du Chemin-du-Roy", serif(18, bold=True), BLUE)

img.save("/home/user/Burnapp/certificat-aaden.png", "PNG", optimize=True)
print(f"Saved: {W}x{H}")
