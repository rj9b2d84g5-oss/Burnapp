from PIL import Image, ImageDraw, ImageFont
import math

W, H = 680, 980
BLUE = (90, 171, 219)
BLUE_DEEP = (70, 150, 200)
BLUE_SOFT = (220, 238, 248)
GOLD = (212, 168, 0)
GOLD_BRIGHT = (240, 195, 30)
GOLD_SOFT = (245, 220, 120)
WHITE = (255, 255, 255)
INK = (50, 60, 75)
INK_SOFT = (140, 150, 165)

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# Outer thin gold frame
d.rectangle([18, 18, W - 18, H - 18], outline=GOLD, width=2)
d.rectangle([24, 24, W - 24, H - 24], outline=GOLD, width=1)

def font(size, bold=False, italic=False, black=False):
    base = "/usr/share/fonts/truetype/liberation/LiberationSans"
    if black or (bold and italic):
        suffix = "-Bold.ttf" if not italic else "-BoldItalic.ttf"
    elif bold:
        suffix = "-Bold.ttf"
    elif italic:
        suffix = "-Italic.ttf"
    else:
        suffix = "-Regular.ttf"
    return ImageFont.truetype(base + suffix, size)

def serif(size, bold=False):
    p = "/usr/share/fonts/truetype/liberation/LiberationSerif"
    p += "-Bold.ttf" if bold else "-Regular.ttf"
    return ImageFont.truetype(p, size)

def cx_text(y, text, fnt, fill):
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, y), text, font=fnt, fill=fill)

def star(cx, cy, r_out, r_in, fill, points=5, rotate=0):
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + rotate + i * math.pi / points
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=fill)

# === TOP BLUE HEADER ===
header_top = 35
header_h = 155
d.rectangle([35, header_top, W - 35, header_top + header_h], fill=BLUE)

# Decorative stars
star(85, header_top + 60, 18, 8, GOLD_BRIGHT)
star(125, header_top + 95, 11, 5, GOLD_BRIGHT)
star(W - 85, header_top + 60, 18, 8, GOLD_BRIGHT)
star(W - 125, header_top + 95, 11, 5, GOLD_BRIGHT)

cx_text(header_top + 28, "RECORD OFFICIEL", font(15, bold=True), WHITE)
cx_text(header_top + 55, "DE L'ÉCOLE", serif(46, bold=True), WHITE)
cx_text(header_top + 130, "ÉDUCATION PHYSIQUE ET À LA SANTÉ",
        font(12, bold=True), BLUE_SOFT)

# === MEDAL BADGE ===
mx, my = W // 2, header_top + header_h + 70
# Light outer ring
d.ellipse([mx - 70, my - 70, mx + 70, my + 70], fill=BLUE_SOFT)
# Inner blue circle
d.ellipse([mx - 60, my - 60, mx + 60, my + 60], fill=BLUE)

cx_text(my - 32, "NOUVEAU", font(11, bold=True), BLUE_SOFT)
cx_text(my - 14, "RECORD", serif(24, bold=True), WHITE)
cx_text(my + 16, "DE L'ÉCOLE", font(11, bold=True), BLUE_SOFT)

# Two gold ribbons - V-shape, forked at the bottom
rb_top = my + 55
# Left ribbon
d.polygon([(mx - 28, rb_top - 8),
           (mx - 8, rb_top - 8),
           (mx - 8, rb_top + 50),
           (mx - 18, rb_top + 38),
           (mx - 28, rb_top + 50)],
          fill=GOLD_BRIGHT)
# Left ribbon shadow
d.polygon([(mx - 28, rb_top - 8),
           (mx - 22, rb_top - 8),
           (mx - 22, rb_top + 44),
           (mx - 28, rb_top + 50)],
          fill=GOLD)
# Right ribbon
d.polygon([(mx + 8, rb_top - 8),
           (mx + 28, rb_top - 8),
           (mx + 28, rb_top + 50),
           (mx + 18, rb_top + 38),
           (mx + 8, rb_top + 50)],
          fill=GOLD_BRIGHT)
d.polygon([(mx + 22, rb_top - 8),
           (mx + 28, rb_top - 8),
           (mx + 28, rb_top + 50),
           (mx + 22, rb_top + 44)],
          fill=GOLD)

# === BODY ===
y = my + 130
cx_text(y, "C E   R E C O R D   E S T   D É T E N U   P A R",
        font(11, bold=True), INK_SOFT)

# Aaden - HUGE, bold sans
y += 25
cx_text(y, "Aaden", font(96, bold=True), BLUE)

# Subtle gold underline
y += 115
d.line([(140, y), (W - 140, y)], fill=GOLD_SOFT, width=1)

# Achievement
y += 22
cx_text(y, "a établi le record de l'école en", font(15), INK)
y += 30
cx_text(y, "POSITION TRÉPIED", font(22, bold=True), INK)

y += 36
cx_text(y, "tenue sans interruption pendant", font(13), INK_SOFT)

# Big blue time box
y += 18
box_w, box_h = 320, 130
bx0 = (W - box_w) // 2
d.rectangle([bx0, y, bx0 + box_w, y + box_h], fill=BLUE)
d.rectangle([bx0 + 7, y + 7, bx0 + box_w - 7, y + box_h - 7],
            outline=GOLD_BRIGHT, width=2)

# 4:00
fnt_time = serif(78, bold=True)
bbox = d.textbbox((0, 0), "4:00", font=fnt_time)
tw = bbox[2] - bbox[0]
d.text((W // 2 - tw // 2, y + 18), "4:00", font=fnt_time, fill=WHITE)
cx_text(y + box_h - 28, "M I N U T E S",
        font(11, bold=True), GOLD_BRIGHT)

# Performance pill
y += box_h + 18
pill_w, pill_h = 320, 32
px0 = (W - pill_w) // 2
d.rounded_rectangle([px0, y, px0 + pill_w, y + pill_h],
                    radius=4, fill=BLUE_SOFT)
cx_text(y + 9, "P E R F O R M A N C E   E X C E P T I O N N E L L E",
        font(11, bold=True), BLUE_DEEP)

# === FOOTER: ENSEIGNANTE / DATE ===
y += pill_h + 30
fl = font(11, bold=True)
fv = serif(20, bold=True)

# Labels
d.text((130, y), "ENSEIGNANTE", font=fl, fill=INK_SOFT)
bbox = d.textbbox((0, 0), "DATE", font=fl)
d.text((W - 130 - (bbox[2] - bbox[0]), y), "DATE",
       font=fl, fill=INK_SOFT)

# Values
y += 20
d.text((130, y), "Anne-Sophie", font=fv, fill=INK)
bbox = d.textbbox((0, 0), "5 mai 2026", font=fv)
d.text((W - 130 - (bbox[2] - bbox[0]), y), "5 mai 2026",
       font=fv, fill=INK)

# Underlines
ul_y = y + 32
d.line([(130, ul_y), (W // 2 - 28, ul_y)], fill=BLUE, width=1)
d.line([(W // 2 + 28, ul_y), (W - 130, ul_y)], fill=BLUE, width=1)

# Center circle + down-arrow
ccx, ccy = W // 2, ul_y
d.ellipse([ccx - 20, ccy - 20, ccx + 20, ccy + 20],
          fill=WHITE, outline=GOLD, width=1)
d.line([(ccx, ccy - 8), (ccx, ccy + 6)], fill=BLUE, width=2)
d.polygon([(ccx - 6, ccy + 1), (ccx + 6, ccy + 1), (ccx, ccy + 8)],
          fill=BLUE)

img.save("/home/user/Burnapp/certificat-aaden.png", "PNG", optimize=True)
print(f"Saved: {W}x{H}")
