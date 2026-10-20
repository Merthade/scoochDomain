#!/usr/bin/env python3
"""App icons for the comparison tables: each app's own App Store icon (iTunes lookup artwork),
used only to identify the app beside its name. Output: assets/compare/icons/<key>.webp, 128 px
(shown at 32 to 44 px). Same as alarmclockplanner.com's _gen/fetch_icons.py.

    python3 _gen/fetch_icons.py       re-run when an app's icon changes
"""
import io
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compare_data as C  # noqa: E402
from PIL import Image  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "compare", "icons")
os.makedirs(OUT, exist_ok=True)
ids = ",".join(a["store_id"] for a in C.APPS)
results = json.load(urllib.request.urlopen(f"https://itunes.apple.com/lookup?id={ids}&country=us"))["results"]
art = {str(r["trackId"]): r["artworkUrl512"] for r in results}
for a in C.APPS:
    url = art[a["store_id"]]
    img = Image.open(io.BytesIO(urllib.request.urlopen(url).read())).convert("RGB")
    img = img.resize((128, 128), Image.LANCZOS)
    path = os.path.join(OUT, a["key"] + ".webp")
    img.save(path, "WEBP", quality=88, method=6)
    print(f"{a['key']:16} {os.path.getsize(path) // 1024} KB")
