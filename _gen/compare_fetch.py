#!/usr/bin/env python3
"""Snapshot every app on the /compare/ pages from the US App Store, so each claim has a source.

    python3 _gen/compare_fetch.py            # writes _gen/compare_snapshot.json

Per app: the iTunes lookup record (version, its release date, rating, size, languages, iOS,
devices, description), the In-App Purchases list and the App Privacy categories read off the
US App Store page, and up to 100 of the most recent US reviews from the public RSS feed. The pages are built from
compare_data.py, which cites this file; re-run it, re-read what changed, and move CHECKED in
compare_data.py on the same day. The feed is flaky (empty pages): every request retries.
"""
import json
import os
import re
import time
import urllib.request

GEN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(GEN, "compare_snapshot.json")
# Listing texts and review texts are other people's words: read locally, never committed
# (this repo is public). Only facts and counts go in the snapshot above.
RAW = os.path.join(GEN, "compare_raw.json")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/18.0 Safari/605.1.15")

APPS = {
    "scooch": 6799503727,
    "magicplan": 427424432,
    "planner-5d": 606173978,
    "home-planner-ai": 1076159017,
    "home-design-3d": 463768717,
    "keyplan-3d": 983655856,
    "live-home-3d": 1066784070,
    "draft-paper": 911636555,
    "drawplan": 1451755778,
}


def get(url, tries=5, ua=UA):
    for attempt in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        except Exception as e:  # noqa: BLE001
            if attempt == tries - 1:
                raise
            print(f"  retry {attempt + 1} for {url[:70]}: {e}")
            time.sleep(3 * (attempt + 1))


def in_app_purchases(app_id):
    """[(name, price)] from the US App Store page, in the order Apple lists them."""
    page = get(f"https://apps.apple.com/us/app/id{app_id}")
    # The page can show "In-App Purchases" twice: a featured shelf (a few items, with
    # artwork and blurbs) and the Information section's full list, which follows "Yes".
    # Only the second is the list Apple publishes, so it is the one read.
    start = -1
    for m in re.finditer("In-App Purchases", page):
        after = [c.strip() for c in re.sub(r"<[^>]+>", "\n", page[m.end():m.end() + 2000]).split("\n")]
        if next((c for c in after if c), "") == "Yes":
            start = m.start()
    if start < 0:
        return []
    chunk = page[start:start + 20000]
    end = min(i for i in (chunk.find("Copyright"), chunk.find("Learn More"), len(chunk)) if i > 0)
    cells = [c.strip() for c in re.sub(r"<[^>]+>", "\n", chunk[:end]).split("\n")]
    cells = [c for c in cells if c and c not in ("In-App Purchases", "Yes")]
    pairs = []
    for name, price in zip(cells[0::2], cells[1::2]):
        if re.match(r"^\$[\d,.]+$", price):
            pairs.append((name, price))
    return pairs


PRIVACY = ("Data Used to Track You", "Data Linked to You", "Data Not Linked to You", "Data Not Collected")


def privacy_label(app_id):
    """The App Privacy card titles on the US page: which of Apple's four categories it declares."""
    page = get(f"https://apps.apple.com/us/app/id{app_id}")
    start = page.find("App Privacy")
    end = page.find("Accessibility", start)
    section = page[start:end if end > start else start + 60000]
    return [c for c in PRIVACY if c in section]


def reviews(app_id, pages=2):
    found = []
    for n in range(1, pages + 1):
        entries = []
        for attempt in range(8):
            # A full browser user agent gets an empty feed back; a bare one gets the reviews.
            raw = get(f"https://itunes.apple.com/us/rss/customerreviews/page={n}/id={app_id}"
                      f"/sortBy=mostRecent/json", ua="Mozilla/5.0")
            entries = json.loads(raw).get("feed", {}).get("entry", [])
            if isinstance(entries, dict):
                entries = [entries]
            # An empty page and a page holding only the app's own record both mean "try
            # again": the feed answers that way at random.
            if any("im:rating" in e for e in entries):
                break
            time.sleep(5 + 3 * attempt)
        for e in entries:
            if "im:rating" not in e:
                continue
            found.append({
                "rating": int(e["im:rating"]["label"]),
                "version": e.get("im:version", {}).get("label"),
                "updated": e.get("updated", {}).get("label", "")[:10],
                "title": e["title"]["label"],
                "text": e["content"]["label"],
            })
    return found


def review_summary(revs):
    """What the pages print about reviews: how many, how they split, which dates."""
    return {
        "n": len(revs),
        "low": sum(1 for r in revs if r["rating"] <= 2),
        "high": sum(1 for r in revs if r["rating"] >= 4),
        "from": min((r["updated"] for r in revs), default=None),
        "to": max((r["updated"] for r in revs), default=None),
    }


def main():
    ids = ",".join(str(i) for i in APPS.values())
    lookup = {r["trackId"]: r for r in json.loads(
        get(f"https://itunes.apple.com/lookup?country=us&id={ids}"))["results"]}
    snapshot = {"fetched": time.strftime("%Y-%m-%d"), "store": "us", "apps": {}}
    raw = {"fetched": snapshot["fetched"], "store": "us", "apps": {}}
    for key, app_id in APPS.items():
        r = lookup[app_id]
        iaps = in_app_purchases(app_id)
        time.sleep(2)
        privacy = privacy_label(app_id)
        revs = reviews(app_id)
        snapshot["apps"][key] = {
            "id": app_id,
            "name": r["trackName"],
            "seller": r["sellerName"],
            "url": f"https://apps.apple.com/us/app/id{app_id}",
            "version": r["version"],
            "version_date": r["currentVersionReleaseDate"][:10],
            "rating": round(r.get("averageUserRating", 0), 1),
            "rating_count": r.get("userRatingCount", 0),
            "price": r["formattedPrice"],
            "size_mb": round(int(r["fileSizeBytes"]) / 1e6),
            "min_ios": r["minimumOsVersion"],
            "languages": r["languageCodesISO2A"],
            "ipad": any("iPad" in d for d in r["supportedDevices"]),
            "genre": r["primaryGenreName"],
            "in_app_purchases": iaps,
            "privacy_label": privacy,
            "reviews": review_summary(revs),
        }
        raw["apps"][key] = {"description": r["description"],
                            "release_notes": r.get("releaseNotes", ""), "reviews": revs}
        print(f"{key:16} v{r['version']} {len(iaps)} IAPs, {len(revs)} reviews")
    for path, data in ((OUT, snapshot), (RAW, raw)):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=1, ensure_ascii=False)
        print("wrote", os.path.relpath(path, os.path.dirname(GEN)))


if __name__ == "__main__":
    main()
