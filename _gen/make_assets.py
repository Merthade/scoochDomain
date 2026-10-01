#!/usr/bin/env python3
"""Build every image getscooch.com serves, from the app repo's own sources.

- Icons (favicon.ico, favicon-32, apple-touch-icon, icon-512) from _gen/appicon-1024.png,
  the App Store's own render of AppIcon.icon (an Icon Composer file has no PNG to read).
- Screenshots: the App Store raws (Marketing/screenshots/raw/en, the store seed) framed in
  AlarmPlanner's web shell (side buttons that protrude), WebP at one uniform size. The raws
  already carry the Dynamic Island, so the shell does not draw one.
- og-image.png (1200x630): the store set's 'leafviolet' gradient, the name, one line, the plan.

Needs Pillow. Run from anywhere: python3 _gen/make_assets.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

GEN = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(GEN)
APP = os.path.dirname(SITE)                      # the Scooch app repo this site sits in
OUT = os.path.join(SITE, "assets")
RAW = os.path.join(APP, "Marketing", "screenshots", "raw", "en")
ICON = os.path.join(GEN, "appicon-1024.png")
FONT_BLACK = "/Library/Fonts/SF-Pro-Display-Black.otf"
FONT_BOLD = "/Library/Fonts/SF-Pro-Display-Bold.otf"

# The store set's shell (Marketing/screenshots/config.json) and 'leafviolet' gradient.
SCREEN_R_RATIO = 0.145
BEZEL_RATIO = 0.030
RIM_RATIO = 0.011
RIM_COLOR = (0x2C, 0x2C, 0x2D, 255)
LEAF_TOP = (0xA6, 0xC2, 0x5F)
LEAF_BOTTOM = (0x12, 0x16, 0x0B)
WEB_W = 640                                      # every framed shot is this wide

SHOTS = {
    "shot-plan.webp":        "plan.png",
    "shot-clash.webp":       "clash.png",
    "shot-projections.webp": "projections.png",
    "shot-furniture.webp":   "sheet_furniture.png",
    "shot-draw.webp":        "sheet_draw.png",
    "shot-plans.webp":       "plans_picker.png",
    "shot-linen.webp":       "theme_linen.png",
    "shot-amethyst.webp":    "theme_amethyst.png",
}


def shell(img):
    """AlarmPlanner's frame_web.py shell: rim, bezel, rounded screen, buttons that protrude."""
    img = img.convert("RGBA")
    sw, height = img.size
    scr_r = int(sw * SCREEN_R_RATIO)
    bez = max(6, int(sw * BEZEL_RATIO))
    rimw = max(2, int(sw * RIM_RATIO))
    bwid = max(3, rimw * 2)

    fw, fh = sw + (bez + rimw) * 2, height + (bez + rimw) * 2
    W, H = fw + bwid * 2, fh
    ox = bwid
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)

    unit = fh / 100
    for y0, y1 in [(20, 26), (30, 40), (42, 52)]:                     # action, vol up, vol down
        d.rounded_rectangle([2, int(unit * y0), ox + 2, int(unit * y1)],
                            radius=bwid // 2, fill=RIM_COLOR)
    d.rounded_rectangle([ox + fw - 2, int(unit * 33), W - 2, int(unit * 50)],   # power
                        radius=bwid // 2, fill=RIM_COLOR)

    d.rounded_rectangle([(ox, 0), (ox + fw - 1, fh - 1)], radius=scr_r + bez + rimw, fill=RIM_COLOR)
    d.rounded_rectangle([(ox + rimw, rimw), (ox + fw - rimw - 1, fh - rimw - 1)],
                        radius=scr_r + bez, fill=(8, 8, 10, 255))

    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([(0, 0), img.size], radius=scr_r, fill=255)
    img.putalpha(m)
    out.paste(img, (ox + bez + rimw, bez + rimw), img)
    return out


def save_webp(img, name, quality=82):
    path = os.path.join(OUT, name)
    img.save(path, "WEBP", quality=quality, method=6)
    print(f"{name:24s} {img.size[0]}x{img.size[1]}  {os.path.getsize(path) // 1024}KB")


def gradient(w, h):
    """The store's 'leafviolet': top colour at (0,0), bottom colour at (0.72w, h)."""
    g = Image.new("RGB", (w, h))
    px = g.load()
    vx, vy = 0.72 * w, 1.0 * h
    norm = vx * vx + vy * vy
    for y in range(h):
        for x in range(w):
            t = max(0.0, min(1.0, (x * vx + y * vy) / norm))
            px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(LEAF_TOP, LEAF_BOTTOM))
    return g


def rounded_icon(size, radius):
    icon = Image.open(ICON).convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", icon.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([(0, 0), icon.size], radius=radius, fill=255)
    icon.putalpha(mask)
    return icon


def og_image():
    W, H = 1200, 630
    img = gradient(W, H).convert("RGBA")
    d = ImageDraw.Draw(img)

    img.alpha_composite(rounded_icon(96, 22), (72, 92))
    d.text((72, 206), "Scooch", font=ImageFont.truetype(FONT_BLACK, 108), fill="white")
    sub = ImageFont.truetype(FONT_BOLD, 46)
    d.text((72, 344), "Will it fit? Find out", font=sub, fill=(255, 255, 255, 235))
    d.text((72, 398), "before you carry it.", font=sub, fill=(255, 255, 255, 235))
    d.text((72, 492), "Room & floor planner for iPhone", font=ImageFont.truetype(FONT_BOLD, 30),
           fill=(0xDC, 0xE8, 0xB8, 255))

    phone = shell(Image.open(os.path.join(RAW, "plan.png")))
    phone.thumbnail((10_000, 560), Image.LANCZOS)
    img.alpha_composite(phone, (W - phone.width - 96, (H - phone.height) // 2))

    path = os.path.join(OUT, "og-image.png")
    img.convert("RGB").save(path, "PNG", optimize=True)
    print(f"og-image.png             {W}x{H}  {os.path.getsize(path) // 1024}KB")


def icons():
    src = Image.open(ICON).convert("RGBA")
    src.resize((180, 180), Image.LANCZOS).save(os.path.join(OUT, "apple-touch-icon.png"), optimize=True)
    src.resize((512, 512), Image.LANCZOS).save(os.path.join(OUT, "icon-512.png"), optimize=True)
    src.resize((32, 32), Image.LANCZOS).save(os.path.join(OUT, "favicon-32.png"), optimize=True)
    src.save(os.path.join(SITE, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    print("icons: apple-touch-icon 180, icon-512, favicon-32, favicon.ico 16/32/48")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    icons()
    for name, raw in SHOTS.items():
        framed = shell(Image.open(os.path.join(RAW, raw)))
        height = round(WEB_W * framed.height / framed.width)
        save_webp(framed.resize((WEB_W, height), Image.LANCZOS), name)
    og_image()
