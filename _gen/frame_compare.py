#!/usr/bin/env python3
"""Frame our own captures of the other room planners for the comparison pages.

Raw device screenshots: the app repo's Marketing/competitors/<key>-<name>.png (dev iPhone, 23 Oct
2026; FINDINGS.md there says what each shows; evidence-*.png stay unpublished). The plan and fit shots
use each app's own furnished sample or template room (Emil, 2026-10-23: stacked sofas in an empty room
read as staged), with its coffee table or sofa moved onto the other, the same move as in ours. SHOTS maps each
published slot to its raw, so the raw names can stay what the test called them. Output:
assets/compare/<key>-<slot>.webp, in the same iPhone shell as our own shots, 640 px wide. A
landscape-only app's capture (Keyplan 3D) is stood upright, the phone's top to the left as it was held,
so it is the same size as the rest instead of a sliver (Emil, 2026-10-23).

MASKS hide what is not the app's to show: a "hide" box is pixelated. Boxes are fractions of the
upright image. None needed so far: no ads were seen, and the shots with the tester's own account
on screen are not published.

Run: python3 _gen/frame_compare.py   (then build.py picks them up)
"""
import os
from PIL import Image, ImageDraw

from make_assets import shell, add_camera, WEB_W

GEN = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(GEN)
RAW = os.path.join(os.path.dirname(SITE), "Marketing", "competitors")
OUT = os.path.join(SITE, "assets", "compare")

# "<key>-<slot>" -> raw file (compare_data.THEIR_SHOTS names the slots and their alt text)
SHOTS = {
    "home-design-3d-wall": "home-design-3d-login.png",
    "home-design-3d-plan": "home-design-3d-plan-v2.png",
    "home-design-3d-catalogue": "home-design-3d-catalogue.png",
    "home-design-3d-fit": "home-design-3d-overlap-v2.png",
    "planner-5d-wall": "planner-5d-wall.png",
    "planner-5d-plan": "planner-5d-plan-v2.png",
    "planner-5d-catalogue": "planner-5d-catalogue.png",
    "planner-5d-fit": "planner-5d-overlap-v2.png",
    "planner-5d-paywall": "planner-5d-paywall.png",
    "planner-5d-offer": "planner-5d-exit-offer.png",
    "magicplan-wall": "magicplan-wall.png",
    "magicplan-plan": "magicplan-editor.png",
    "magicplan-catalogue": "magicplan-catalogue.png",
    "magicplan-fit": "magicplan-overlap-v2.png",
    "keyplan-3d-plan": "keyplan-3d-room.png",
    "keyplan-3d-catalogue": "keyplan-3d-catalogue.png",
    "keyplan-3d-paywall": "keyplan-3d-paywall.png",
    "live-home-3d-wall": "live-home-3d-welcome.png",
    # v3: the sample's garden trees hidden with its own Make Invisible (seen from above they were a
    # cloud of green circles over the plan); the sofa where v2 had it.
    "live-home-3d-plan": "live-home-3d-plan-v3.png",
    "live-home-3d-fit": "live-home-3d-overlap-v3.png",
    "live-home-3d-paywall": "live-home-3d-paywall.png",
    "home-planner-ai-wall": "home-planner-ai-paywall.png",
    "home-planner-ai-plan": "home-planner-ai-plan-v2.png",
    "home-planner-ai-catalogue": "home-planner-ai-catalogue.png",
    "home-planner-ai-fit": "home-planner-ai-overlap-v2.png",
    "home-planner-ai-offer": "home-planner-ai-countdown.png",
    "draft-paper-plan": "draft-paper-plan-v2.png",
    "draft-paper-paywall": "draft-paper-paywall.png",
    # Not a capture: DrawPlan closed at every launch, so this is a plain black screen (Emil, 2026-10-23).
    "drawplan-plan": "drawplan-placeholder.png",
}

# Ours, for the slots our existing site shots do not cover: the shipped 1.0.2 (79dbbc5) on an iPhone 17 Pro
# Max simulator, the showroom fixture as fixed in 1.0.3 `2ec5aa7` (nothing in a door swing or a drawer's pull-out);
# scooch-fit is its coffee table dragged onto the sofa by hand.
OURS = {
    "scooch-wall": "scooch-first.png",
    "scooch-paywall": "scooch-paywall.png",
    "scooch-fit": "scooch-fit.png",
    "scooch-plan": "scooch-plan.png",
    "scooch-projections": "scooch-projections.png",
}

MASKS = {}


def apply_masks(img, name):
    W, H = img.size
    for kind, (x0, y0, x1, y1) in MASKS.get(name, []):
        box = (int(x0 * W), int(y0 * H), int(x1 * W), int(y1 * H))
        region = img.crop(box)
        small = region.resize((max(1, region.width // 28), max(1, region.height // 28)), Image.BILINEAR)
        img.paste(small.resize(region.size, Image.NEAREST), box)
    return img


def add_island(img):
    """Simulator screenshots leave out the Dynamic Island (the system draws it above the app), and the
    test iPhone has a notch; the store raws have the island. Same pill as the store set's config.json,
    in fractions of the screen width."""
    w = img.width
    iw, ih, top = w * 0.286, w * 0.0855, w * 0.0318
    ImageDraw.Draw(img).rounded_rectangle([(w - iw) / 2, top, (w + iw) / 2, top + ih], radius=ih / 2, fill=(0, 0, 0, 255))
    return img


def frame(src, name, camera=False):
    img = Image.open(src).convert("RGBA")
    img = apply_masks(img, name)
    if img.width > img.height:
        img = img.rotate(-90, expand=True)
    if camera:
        img = add_camera(add_island(img))
    framed = shell(img)
    size = (WEB_W, round(WEB_W * framed.height / framed.width))
    path = os.path.join(OUT, name + ".webp")
    framed.resize(size, Image.LANCZOS).save(path, "WEBP", quality=82, method=6)
    print(f"{name + '.webp':34s} {size[0]}x{size[1]}  {os.path.getsize(path) // 1024}KB")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, raw in SHOTS.items():
        # The same phone as ours, Dynamic Island included (the test iPhone has a notch, which leaves
        # the top centre of its status bar empty, and the left edge of a landscape screen). Not on the
        # black stand-in: add_camera finds no island edge on black and puts the lens in the corner.
        frame(os.path.join(RAW, raw), name, camera=not name.startswith("drawplan"))
    for name, raw in OURS.items():
        src = os.path.join(RAW, raw)
        if os.path.isfile(src):
            frame(src, name, camera=True)
