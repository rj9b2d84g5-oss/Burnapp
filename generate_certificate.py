from PIL import Image, ImageDraw, ImageFont
import math

W, H = 680, 980
BLUE = (90, 171, 219)
BLUE_DARK = (50, 110, 160)
GOLD = (212, 168, 0)
GOLD_LIGHT = (240, 205, 90)
CREAM = (253, 250, 240)
INK = (40, 50, 70)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# Subtle background gradient
for y in range(H):
    t = y / H
    r = int(253 - t * 8)
    g = int(250 - t * 6)
    b = int(240 - t * 4)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# Outer gold border
for i in range(6):
    d.rectangle([20 + i, 20 + i, W - 20 - i, H - 20 - i],
                outline=GOLD, width=1)
# Inner thin blue border
d.rectangle([34, 34, W - 34, H - 34], outline=BLUE, width=2)
d.rectangle([40, 40, W - 40, H - 40], outline=GOLD, width=1)

# Decorative corner ornaments
def corner(cx, cy, flip_x=1, flip_y=1):
    for r, c in [(28, GOLD), (22, GOLD_LIGHT), (14, GOLD)]:
        d.arc([cx - r, cy - r, cx + r, cy + r],
              start=180 if flip_x*flip_y > 0 else 90,
              end=270 if flip_x*flip_y > 0 else 180,
              fill=c, width=2)
    # small dots
    for k in range(3):
        d.ellipse([cx + flip_x*(8 + k*8) - 2, cy + flip_y*(8 + k*8) - 2,
                   cx + flip_x*(8 + k*8) + 2, cy + flip_y*(8 + k*8) + 2],
                  fill=GOLD)

corner(60, 60, 1, 1)
corner(W - 60, 60, -1, 1)
corner(60, H - 60, 1, -1)
corner(W - 60, H - 60, -1, -1)

# Top blue banner
d.rectangle([60, 90, W - 60, 170], fill=BLUE)
d.rectangle([60, 90, W - 60, 170], outline=GOLD, width=3)
# Banner ornaments
d.line([(80, 130), (140, 130)], fill=GOLD_LIGHT, width=2)
d.line([(W - 140, 130), (W - 80, 130)], fill=GOLD_LIGHT, width=2)
for x in [80, 140, W - 140, W - 80]:
    d.ellipse([x - 3, 127, x + 3, 133], fill=GOLD)

# Fonts
def font(size, bold=False, italic=False):
    if bold and italic:
        path = "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf"
    elif bold:
        path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
    elif italic:
        path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
    else:
        path = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
    return ImageFont.truetype(path, size)

def cx_text(y, text, fnt, fill):
    bbox = d.textbbox((0, 0), text, font=fnt)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) // 2, y), text, font=fnt, fill=fill)

# Header text
cx_text(102, "CERTIFICAT D'EXCELLENCE", font(26, bold=True), CREAM)
cx_text(140, "Record scolaire", font(18, italic=True), GOLD_LIGHT)

# Medallion
cx, cy = W // 2, 260
# Outer gold ring
for r, c, w in [(70, GOLD, 4), (62, GOLD_LIGHT, 2), (56, GOLD, 2)]:
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=w)
# Inner blue disc
d.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=BLUE)
d.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], outline=GOLD, width=2)
# Star inside
def star(cx, cy, r_out, r_in, points=5, fill=GOLD):
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=fill, outline=GOLD_LIGHT)
star(cx, cy, 32, 14, 5, GOLD)
# Ribbon tails below medallion
d.polygon([(cx - 35, cy + 55), (cx - 60, cy + 130),
           (cx - 40, cy + 115), (cx - 25, cy + 130),
           (cx - 15, cy + 70)], fill=BLUE_DARK)
d.polygon([(cx + 35, cy + 55), (cx + 60, cy + 130),
           (cx + 40, cy + 115), (cx + 25, cy + 130),
           (cx + 15, cy + 70)], fill=BLUE_DARK)
d.polygon([(cx - 35, cy + 55), (cx - 60, cy + 130),
           (cx - 50, cy + 100), (cx - 20, cy + 60)], fill=BLUE)
d.polygon([(cx + 35, cy + 55), (cx + 60, cy + 130),
           (cx + 50, cy + 100), (cx + 20, cy + 60)], fill=BLUE)

# Body
y = 430
cx_text(y, "Décerné à", font(20, italic=True), INK)
y += 50
cx_text(y, "Aaden", font(56, bold=True), BLUE_DARK)
# Underline flourish
y += 78
d.line([(W//2 - 130, y), (W//2 + 130, y)], fill=GOLD, width=2)
d.ellipse([W//2 - 4, y - 4, W//2 + 4, y + 4], fill=GOLD)

# Achievement statement
y += 30
cx_text(y, "pour avoir établi un nouveau record scolaire en", font(17), INK)
y += 30
cx_text(y, "POSITION DU TRÉPIED", font(24, bold=True), BLUE_DARK)

# Time highlight box
y += 50
box_w, box_h = 280, 80
bx0 = (W - box_w) // 2
d.rounded_rectangle([bx0, y, bx0 + box_w, y + box_h], radius=12,
                    fill=BLUE, outline=GOLD, width=3)
cx_text(y + 10, "Temps réalisé", font(13, italic=True), GOLD_LIGHT)
cx_text(y + 30, "4 minutes", font(34, bold=True), CREAM)

# School & teacher
y += box_h + 35
cx_text(y, "École du Chemin-du-Roy", font(18, bold=True), INK)
y += 28
cx_text(y, "sous la supervision de", font(14, italic=True), INK)
y += 22
cx_text(y, "Anne-Sophie", font(18, bold=True, italic=True), BLUE_DARK)

# Date row
y = H - 150
d.line([(90, y), (W - 90, y)], fill=GOLD, width=1)
# Date left
d.text((100, y + 14), "Date", font=font(12, italic=True), fill=INK)
d.text((100, y + 32), "5 mai 2026", font=font(16, bold=True), fill=BLUE_DARK)
# Signature right
sig_text = "Signature"
bbox = d.textbbox((0, 0), sig_text, font=font(12, italic=True))
d.text((W - 100 - (bbox[2] - bbox[0]), y + 14), sig_text,
       font=font(12, italic=True), fill=INK)
sig_name = "Anne-Sophie"
bbox = d.textbbox((0, 0), sig_name, font=font(16, bold=True, italic=True))
d.text((W - 100 - (bbox[2] - bbox[0]), y + 30), sig_name,
       font=font(16, bold=True, italic=True), fill=BLUE_DARK)

# Tiny seal bottom-center
sx, sy = W // 2, H - 95
d.ellipse([sx - 26, sy - 26, sx + 26, sy + 26], outline=GOLD, width=2)
d.ellipse([sx - 20, sy - 20, sx + 20, sy + 20], fill=GOLD)
star(sx, sy, 14, 6, 5, BLUE_DARK)

img.save("/home/user/Burnapp/certificat-aaden.png", "PNG", optimize=True)
print(f"Saved: {W}x{H}")
