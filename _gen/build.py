#!/usr/bin/env python3
"""Generate every page of getscooch.com: home, the sofa fit calculator, guides, guides hub,
support, privacy, terms, 404, sitemap, robots, CNAME.

getchoru.com's build.py is the template (itself AlarmPlanner's alarmclockplanner.com): same
page shapes, same campaign-link rules, same analytics. Scooch adds a tool page, size tables,
and the cm/inch helpers below, so no conversion is ever typed by hand.

Every claim about the app was checked against 1.0.1 (build 6, e0d9f06) on 2026-10-01:
37 catalogue pieces, 26 themes, metric or imperial, PNG/PDF export, iCloud backup, the
one-piece corner sofa, iPhone only, iOS 26.0+. Change a feature, change the copy.
The room numbers in the guides are common rules of thumb, worded as such.
Run: python3 _gen/build.py
"""
import html
import json
import os
import re

GEN = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(GEN)
DOMAIN = "https://getscooch.com"
APP_ID = "6799503727"
STORE_CANONICAL = f"https://apps.apple.com/app/id{APP_ID}"
TODAY = "2026-10-01"
MIN_IOS = "26"              # IPHONEOS_DEPLOYMENT_TARGET 26.0 in 1.0.1

# ---- App Analytics campaign attribution (AlarmPlanner's rules, same provider) ----------
# /app/apple-store/id<id>?pt=&ct=&mt=8, BOTH tokens required (a ct without the pt reported
# nothing for AlarmPlanner until 2026-08-08). Coarse ct buckets: App Analytics shows a
# campaign only after 5 first-time downloads. Per-page clicks are in PostHog instead.
PROVIDER_TOKEN = "2187944"
CT_HOME = "Website_Home"      # home, support, legal, 404
CT_GUIDE = "Website_Guide"    # every /guides/ page
CT_TOOL = "Website_Tool"      # the sofa fit calculator
CT_COMPARE = "Website_Compare"  # /compare/ and every one-vs-one page

import sys  # noqa: E402
sys.path.insert(0, GEN)
import compare_data as C  # noqa: E402

VS_URL = lambda key: f"/compare/scooch-vs-{key}/"  # noqa: E731


def store_url(campaign):
    assert 0 < len(campaign) <= 30 and campaign == campaign.strip(), f"bad ct: {campaign!r}"
    return (f"https://apps.apple.com/app/apple-store/id{APP_ID}"
            f"?pt={PROVIDER_TOKEN}&amp;ct={campaign}&amp;mt=8")


# ---- Units: every inch, foot and metre on the site comes from here ----------------------
def _half_up(x):
    # round() is banker's rounding: 75 in = 190.5 cm would print as 190, not 191
    return int(x + 0.5)


def _in(c):
    return _half_up(c / 2.54)


def cm(a, b=None):
    """'190 to 230 cm (75 to 91 in)' or '60 cm (24 in)'."""
    if b is None:
        return f"{a} cm ({_in(a)} in)"
    return f"{a} to {b} cm ({_in(a)} to {_in(b)} in)"


def cm_short(a, b=None):
    """Table cells: '190 to 230 cm<br>75 to 91 in'."""
    if b is None:
        return f"{a} cm<br><span class='sub'>{_in(a)} in</span>"
    return f"{a} to {b} cm<br><span class='sub'>{_in(a)} to {_in(b)} in</span>"


def inch_bed(w, l):
    """A US mattress, defined in inches."""
    return f"{w} × {l} in", f"{_half_up(w * 2.54)} × {_half_up(l * 2.54)} cm"


def cm_bed(w, l):
    """A UK or European mattress, defined in centimetres."""
    return f"{w} × {l} cm", f"{_half_up(w / 2.54)} × {_half_up(l / 2.54)} in"


def m_ft(c):
    return f"{c / 100:.1f} m ({c / 30.48:.1f} ft)"


# person_profiles 'identified_only' and nothing ever identifies: anonymous events, no
# profiles. persistence 'memory': no cookie and nothing in storage. No autocapture, no
# session recording: page views, the data-ph taps, and the calculator's outcome only.
# The shared PostHog project turns on dead clicks, web vitals and surveys remotely, and the
# privacy page names none of them, so the site switches each off here (2026-10-01).
ANALYTICS = """<link rel="preconnect" href="https://eu.i.posthog.com">
<script>
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing startSessionRecording stopSessionRecording isSessionRecordingStarted".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
    if (!/^(localhost|127\\.0\\.0\\.1|\\[::1\\])$/.test(location.hostname) && location.hostname !== '') {
        posthog.init('phc_ztIjBWZp495eGWUZSUprsXSLzyElBWMcf2xc65kKfE5', {
            api_host: 'https://eu.i.posthog.com',
            person_profiles: 'identified_only',
            persistence: 'memory',
            autocapture: false,
            disable_session_recording: true,
            capture_dead_clicks: false,
            capture_performance: false,
            enable_heatmaps: false,
            disable_surveys: true
        });
        posthog.register({ app_name: 'scooch_web' });
    }
</script>"""

PAGE_JS = """<script>
    // posthog.capture exists only after posthog.init, which is skipped on localhost: guard it,
    // so a preview click still works and no tracking call can stop the page responding.
    document.addEventListener('click', function (e) {
        var el = e.target.closest('[data-ph]');
        if (!el) return;
        try {
            if (window.posthog && typeof posthog.capture === 'function') {
                posthog.capture(el.getAttribute('data-ph'), { page: location.pathname });
            }
        } catch (err) {}
    });
</script>"""

HEADER_TPL = """<header class="site-header">
  <nav class="nav" aria-label="Main">
    <a class="nav-logo" href="/">
      <img src="/assets/apple-touch-icon.png" alt="" width="34" height="34">
      Scooch
    </a>
    <div class="nav-links">
      <a href="/#features">Features</a>
      <a href="/sofa-fit-calculator/">Sofa fit calculator</a>
      <a href="/guides/">Guides</a>
      <a href="/compare/">Compare</a>
      <a href="/#faq">FAQ</a>
      <a class="nav-cta" href="{store}" data-ph="appstore_click">Download</a>
    </div>
  </nav>
</header>"""

FOOTER_TPL = """<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <img src="/assets/apple-touch-icon.png" alt="" width="30" height="30">
          Scooch
        </div>
        <p class="footer-note">Room and floor planner for iPhone. Will it fit?<br>Requires iOS {min_ios} or later.</p>
      </div>
      <div class="footer-links">
        <a href="/sofa-fit-calculator/">Sofa fit calculator</a>
        <a href="/guides/">Guides</a>
        <a href="/compare/">Compare</a>
        <a href="{store}" data-ph="appstore_click">App Store</a>
        <a href="/support/">Support</a>
        <a href="/privacy/">Privacy</a>
        <a href="/terms/">Terms</a>
        <a href="https://ozols.dev" rel="author">Made by Emils Ozols</a>
      </div>
    </div>
    <p class="footer-note">© Emils Ozols. Apple, iPhone, and the App Store badge are trademarks of Apple Inc.</p>
  </div>
</footer>"""


def header(campaign=CT_HOME):
    return HEADER_TPL.format(store=store_url(campaign))


def footer(campaign=CT_HOME):
    return FOOTER_TPL.format(store=store_url(campaign), min_ios=MIN_IOS)


def head(title, desc, canonical, og_type="article", ogtitle=None, ogdesc=None):
    ogtitle = html.escape(ogtitle or title)
    ogdesc = html.escape(ogdesc or desc)
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="apple-itunes-app" content="app-id={APP_ID}">
<meta name="theme-color" content="#12160b">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/styles.css">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Scooch">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{ogdesc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@ozolsdev">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{ogdesc}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-image.png">
{ANALYTICS}"""


def ld(data):
    return f'<script type="application/ld+json">\n{json.dumps(data, indent=2, ensure_ascii=False)}\n</script>'


def badge(campaign, label="Download Scooch on the App Store"):
    return f"""<a class="badge-link" href="{store_url(campaign)}" data-ph="appstore_click" aria-label="{label}">
          <img src="/assets/appstore-badge.svg" alt="Download on the App Store" width="180" height="60">
        </a>"""


def figure(src, alt, caption):
    return f"""<figure>
  <img class="screen" src="/assets/{src}" alt="{html.escape(alt)}" loading="lazy" width="640" height="1284">
  <figcaption>{caption}</figcaption>
</figure>"""


def table(head_cells, rows):
    th = "".join(f"<th>{h}</th>" for h in head_cells)
    trs = "\n".join("      <tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"""<div class="table-wrap">
  <table>
    <thead><tr>{th}</tr></thead>
    <tbody>
{trs}
    </tbody>
  </table>
</div>"""


_VERSIONS = {}


def _v(rel):
    """Content hash of a site file, so a changed stylesheet or a recaptured screenshot under the same name
    is fetched again (AlarmPlanner, 2026-10-23: new badges showed unstyled from a cached styles.css)."""
    if rel not in _VERSIONS:
        import hashlib
        with open(os.path.join(SITE, rel), "rb") as f:
            _VERSIONS[rel] = hashlib.sha1(f.read()).hexdigest()[:8]
    return _VERSIONS[rel]


def _busted(text):
    text = text.replace('href="/styles.css"', f'href="/styles.css?v={_v("styles.css")}"')
    return re.sub(r'src="/(assets/[^"?]+\.(?:webp|png|jpg|svg))"',
                  lambda m: f'src="/{m.group(1)}?v={_v(m.group(1))}"' if os.path.isfile(os.path.join(SITE, m.group(1)))
                  else m.group(0), text)


def write(rel, text):
    if rel.endswith(".html"):
        text = _busted(text)
    path = os.path.join(SITE, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("wrote", rel)


def plain(s):
    """Visible text of a snippet, for structured data."""
    return html.unescape(re.sub(r"<[^>]+>", "", " ".join(s.split())))


def page(title, desc, canonical, body, campaign=CT_HOME, extra_head="", og_type="article",
         ogtitle=None, ogdesc=None, scripts=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, desc, canonical, og_type=og_type, ogtitle=ogtitle, ogdesc=ogdesc)}
{extra_head}
</head>
<body>

{header(campaign)}

<main>
{body}
</main>

{footer(campaign)}
{PAGE_JS}
{scripts}
</body>
</html>
"""


def cta_html(h, ptext, campaign):
    # The ENTIRE box is one anchor (no nested links: the badge is a decorative span)
    return f"""<a class="article-cta" href="{store_url(campaign)}" data-ph="appstore_click" aria-label="Download Scooch on the App Store">
    <h2>{h}</h2>
    <p>{ptext}</p>
    <div class="cta-row">
      <span class="badge-link">
        <img src="/assets/appstore-badge.svg" alt="Download on the App Store" width="180" height="60">
      </span>
    </div>
  </a>"""


def faq_details(items):
    out = []
    for q, a, href in items:
        if href is None:
            link = ""
        elif href.startswith("#"):
            link = f' <a href="{href}">Get the app</a>'
        else:
            link = f' <a href="{href}">Read more</a>'
        out.append(f"""      <details>
        <summary>{q}</summary>
        <p>{" ".join(a.split())}{link}</p>
      </details>""")
    return "\n".join(out)


def faq_ld(items):
    return ld({
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": plain(q),
                        "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
                       for q, a, _ in items],
    })


def breadcrumb_ld(trail):
    return ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                            for i, (n, u) in enumerate(trail)],
    })


CALC = "/sofa-fit-calculator/"

# =========================================================================================
# GUIDES
# =========================================================================================
TV_ROWS = [(s, f"{m_ft(s * 2.54)} to {m_ft(s * 2.54 * 1.5)}") for s in (43, 50, 55, 65, 75)]

PAGES = [
# ---------------------------------------------------------------- sofa sizes
dict(
slug="standard-sofa-dimensions",
title="Standard Sofa Dimensions in cm and Inches, by Seat Count",
meta="Typical sofa sizes by number of seats, in cm and inches: width, depth, height and seat height, plus how much room a sofa bed needs when it is open.",
h1="Standard Sofa Dimensions, in cm and Inches",
lede="There is no official sofa size, but most sofas land in the same ranges. Here they are, with the numbers worth checking before you order one.",
card="Typical widths, depths and heights by number of seats, and how far a sofa bed opens.",
quick=f"""<strong>Quick answer:</strong> A typical 3-seater sofa is {cm(190, 230)} wide, {cm(85, 100)} deep and {cm(75, 90)} tall. A 2-seater is about {cm(140, 175)} wide. Use these to shortlist, then go by the listing: two sofas with the same number of seats can differ by 40 cm.""",
body=f"""
<h2>Sofa sizes by number of seats</h2>
<p>Width is measured arm to arm, depth from the back to the front of the arm or seat, and height from the floor to the top of the back.</p>
{table(["Type", "Width", "Depth", "Height"], [
    ["Armchair", cm_short(75, 100), cm_short(80, 95), cm_short(75, 95)],
    ["2-seater", cm_short(140, 175), cm_short(85, 95), cm_short(75, 90)],
    ["3-seater", cm_short(190, 230), cm_short(85, 100), cm_short(75, 90)],
    ["4-seater", cm_short(230, 260), cm_short(90, 105), cm_short(75, 90)],
    ['<a href="/guides/corner-sofa-dimensions/">Corner sofa</a>', cm_short(220, 300) + '<br><span class="sub">long side</span>', cm_short(85, 100) + '<br><span class="sub">each side</span>', cm_short(75, 90)],
])}
<p>These are typical ranges, not rules. A deep lounge sofa can pass 110 cm, and a compact apartment sofa can sit under 85 cm.</p>

<h2>The other numbers on the listing</h2>
<ul>
  <li><strong>Seat height:</strong> usually {cm(40, 48)} from the floor. Lower feels loungier and is harder to get up from.</li>
  <li><strong>Seat depth:</strong> usually {cm(50, 60)} from the front edge to the back cushion. Deeper suits sitting with your feet up; shorter suits shorter legs.</li>
  <li><strong>Arm height:</strong> usually {cm(55, 70)}. It matters if a side table or a window sill sits next to it.</li>
  <li><strong>Sofa bed, open:</strong> most reach about {cm(200, 220)} from the back of the sofa to the foot of the mattress. Leave room to walk past the foot as well.</li>
  <li><strong>Diagonal depth:</strong> the number that decides whether it gets through your door. <a href="{CALC}">The sofa fit calculator</a> shows how to measure it.</li>
</ul>

<h2>How much room to leave around a sofa</h2>
<p>The sofa is only half the footprint. Common rules of thumb:</p>
<ul>
  <li>{cm(35, 45)} between the sofa and the coffee table.</li>
  <li>{cm(75, 90)} for a walkway people use every day, and at least {cm(60)} for a short squeeze.</li>
  <li>A few centimetres between the back and the wall, more if a radiator is behind it.</li>
</ul>
<p>There is more on this in <a href="/guides/space-between-sofa-coffee-table-and-tv/">how much space to leave between a sofa, coffee table and TV</a>.</p>

<h2>Try it at its real size first</h2>
<p>A sofa that looks fine in the shop can swallow a living room. In <a href="/">Scooch</a>, draw the room at its real measurements, add a sofa, and type the width, depth and height from the listing. The drawing keeps up: a wider sofa gets more cushions. If it overlaps something or pokes out of the room, it turns red.</p>
{figure("shot-clash.webp", "Scooch with a 3-seat sofa typed in at 360 cm wide, flagged red because it does not fit the room", "Type the size from the listing. Red means it does not fit.")}
""",
related=["corner-sofa-dimensions", "space-between-sofa-coffee-table-and-tv", "how-to-measure-a-room-for-furniture"],
cta_h="Will the sofa fit the room?",
cta_p="Draw the room, type the sofa's size from the listing, and see it before it is delivered.",
),
# ---------------------------------------------------------------- corner sofas
dict(
slug="corner-sofa-dimensions",
title="Corner Sofa Dimensions: Sizes, Depths and How to Measure",
meta="Typical corner sofa sizes in cm and inches, what left-hand and right-hand mean, and how to measure your corner before you order one.",
h1="Corner Sofa Dimensions and How to Measure for One",
lede="A corner sofa has two lengths, two depths, and a left or right side that you and the shop might name differently. Here is what to measure before you order.",
card="Typical sizes, left-hand versus right-hand, and how to measure the corner.",
quick=f"""<strong>Quick answer:</strong> Most corner sofas are about {cm(220, 300)} along the long side and {cm(150, 220)} along the short side, with each side {cm(85, 100)} deep. Measure both walls from the corner, take off room to walk past the open end, and check which side the shop calls left.""",
body=f"""
<h2>Typical corner sofa sizes</h2>
{table(["Size", "Long side", "Short side", "Depth of each side"], [
    ["Compact", cm_short(200, 230), cm_short(150, 170), cm_short(85, 95)],
    ["Standard", cm_short(240, 270), cm_short(170, 200), cm_short(85, 100)],
    ["Large", cm_short(280, 320), cm_short(200, 250), cm_short(90, 105)],
])}
<p>Treat these as a starting point. Corner sofas vary more than straight ones, and the two sides of the same sofa are not always the same depth.</p>

<h2>Corner sofa or chaise?</h2>
<p>A <strong>corner sofa</strong> has a seat in the corner and a backrest along both sides, so people sit along both arms of the L. A <strong>chaise sofa</strong> has one long seat at one end for your legs, usually {cm(140, 170)} from the back, with no backrest along it. The footprint can be similar. How you use it is not.</p>

<h2>Left-hand or right-hand?</h2>
<p>Most shops name the side as you stand in front of the sofa and look at it: on a left-hand corner sofa, the short side is on your left. Some shops name it as you sit on it, which flips it. Check the drawing in the listing before you order, not the name.</p>

<h2>How to measure your corner</h2>
<ol>
  <li>Measure each wall from the corner to the first thing in the way: a door's swing, a radiator, a window you need to reach.</li>
  <li>Take off room to walk past the open end: at least {cm(60)}, and {cm(75, 90)} if it is a main path.</li>
  <li>Decide how deep each side can be. A deep sofa on both sides eats a lot of floor where the two meet.</li>
  <li>Measure the way in. Many corner sofas arrive in two or more pieces, so check the largest piece against your doors with the <a href="{CALC}">sofa fit calculator</a>.</li>
</ol>

<h2>Plan it at its real size</h2>
<p><a href="/">Scooch</a> has a corner sofa as one L-shaped piece. Stretch it to the long and short side you measured, and type the depth of each side on its own. Mirror it to swap left and right. Turn on the sofa bed and the drawing shows where the mattress pulls out, up to the corner.</p>
""",
related=["standard-sofa-dimensions", "space-between-sofa-coffee-table-and-tv", "how-to-measure-a-room-for-furniture"],
cta_h="Draw the corner before you order the sofa",
cta_p="Type both lengths and both depths, and see whether the L leaves room to walk.",
),
# ---------------------------------------------------------------- beds
dict(
slug="bed-sizes-and-space-around-a-bed",
title="Bed Sizes in cm and Inches, and How Much Space Around a Bed",
meta="US, UK and European mattress sizes in cm and inches, plus how much room to leave around a bed to walk, make it, and open the wardrobe.",
h1="Bed Sizes and How Much Space You Need Around a Bed",
lede="A queen in New York, a king in London and a 160 in Berlin are three different beds. Here are the sizes, and the room you need around them.",
card="US, UK and European mattress sizes, and the room to leave on each side.",
quick=f"""<strong>Quick answer:</strong> Leave at least {cm(60)} beside each side of the bed you use and at the foot, and {cm(75, 90)} if you can. In front of a wardrobe or a chest of drawers, leave room for the doors or drawers to open and for you to stand: around {cm(90)}.""",
body=f"""
<h2>US mattress sizes</h2>
{table(["Name", "Inches", "Centimetres"], [
    ["Twin", *inch_bed(38, 75)],
    ["Twin XL", *inch_bed(38, 80)],
    ["Full (double)", *inch_bed(54, 75)],
    ["Queen", *inch_bed(60, 80)],
    ["King", *inch_bed(76, 80)],
    ["California king", *inch_bed(72, 84)],
])}

<h2>UK mattress sizes</h2>
{table(["Name", "Centimetres", "Inches"], [
    ["Single", *cm_bed(90, 190)],
    ["Small double", *cm_bed(120, 190)],
    ["Double", *cm_bed(135, 190)],
    ["King", *cm_bed(150, 200)],
    ["Super king", *cm_bed(180, 200)],
])}

<h2>European mattress sizes</h2>
<p>Most of continental Europe names a bed by its width in centimetres, almost always 200 cm long.</p>
{table(["Size", "Centimetres", "Inches"], [
    ["90", *cm_bed(90, 200)],
    ["140", *cm_bed(140, 200)],
    ["160", *cm_bed(160, 200)],
    ["180", *cm_bed(180, 200)],
])}
<div class="note-box">These are mattress sizes. The frame adds to them: a few centimetres for a simple frame, 10 cm or more on each side for a padded or chunky one. Measure the frame you are buying, not the mattress.</div>

<h2>How much space around the bed</h2>
<ul>
  <li><strong>The sides you get in from:</strong> {cm(60)} at least, {cm(75, 90)} to move comfortably.</li>
  <li><strong>The foot:</strong> {cm(60)} to walk past. More if a wardrobe or a dresser faces it.</li>
  <li><strong>Against a wall:</strong> pushing one side to the wall saves a walkway in a small room, but whoever sleeps there climbs over, and making the bed gets harder.</li>
  <li><strong>Nightstands:</strong> most are {cm(40, 60)} wide. Two of them add up fast next to a wide bed.</li>
  <li><strong>Wardrobes and drawers:</strong> leave space for doors and drawers to open fully, plus room to stand in front of them.</li>
</ul>

<h2>Check it in the room</h2>
<p>A bed is the biggest thing in most bedrooms, so it decides everything else. In <a href="/">Scooch</a>, draw the bedroom, add a bed at the size you are buying, and the nightstands and wardrobe around it. Wardrobe doors and drawers can show the space they need to open, so you can see whether they hit the bed.</p>
{figure("shot-projections.webp", "Scooch showing furniture doors, drawers and a sofa bed with the space they need when open", "Doors, drawers and sofa beds can show the space they need.")}
""",
related=["how-to-measure-a-room-for-furniture", "standard-sofa-dimensions", "dining-table-clearance"],
cta_h="Will the bed and the wardrobe both fit?",
cta_p="Draw the bedroom at its real size and see the gaps before anything heavy moves.",
),
# ---------------------------------------------------------------- living room spacing
dict(
slug="space-between-sofa-coffee-table-and-tv",
title="How Much Space Between a Sofa, Coffee Table and TV?",
meta="How far a coffee table should be from the sofa, how far to sit from the TV, and how wide to keep the walkways in a living room, in cm and inches.",
h1="How Much Space Between a Sofa, Coffee Table and TV",
lede="Close enough to reach your mug, far enough not to bang your shins. These distances work in most living rooms.",
card="Sofa to coffee table, sofa to TV, and how wide to keep the walkways.",
quick=f"""<strong>Quick answer:</strong> Put the coffee table {cm(35, 45)} from the sofa. Keep the walkways people use every day {cm(75, 90)} wide. For a 4K TV, a common rule of thumb is to sit 1 to 1.5 times the screen size away: a 55-inch TV works from about {m_ft(55 * 2.54)} to {m_ft(55 * 2.54 * 1.5)}.""",
body=f"""
<h2>Sofa to coffee table</h2>
<p>{cm(35, 45)} between the sofa's front edge and the table is the usual range: you can reach it without leaning, and there is room for your legs. Under 30 cm and you are stepping over it. Over 50 cm and it starts to feel like a different piece of furniture.</p>
<p>For the size of the table itself, a common guide is about two-thirds of the sofa's length, at or a little under the height of the seat.</p>

<h2>Sofa to TV</h2>
<p>For a 4K TV, a common rule of thumb is a viewing distance of 1 to 1.5 times the screen size. Closer than that, the screen fills more of your view. Further, it is still fine, just smaller. Lower-resolution screens are usually watched from a little further back.</p>
{table(["Screen size", "Distance from the sofa"], [[f"{s} in", d] for s, d in TV_ROWS])}
<p>Height matters as much as distance: mount or stand it so the middle of the screen is roughly at eye level when you are sitting down.</p>

<h2>Walkways</h2>
<ul>
  <li><strong>Main paths</strong>, like from the door to the sofa or through to the kitchen: {cm(75, 90)}.</li>
  <li><strong>Short squeezes</strong>, like between an armchair and a side table: at least {cm(60)}.</li>
  <li><strong>Doors:</strong> keep the whole swing of the door clear, not just the doorway.</li>
</ul>

<h2>See the gaps before you move anything</h2>
<p>The easy way to get these right is to try them at real size first. In <a href="/">Scooch</a>, draw the living room, add the sofa, coffee table and TV stand at the sizes you have or want, and slide them around until the layout works. Doors show their swing, so you can see if one clips the sofa.</p>
{figure("shot-plan.webp", "A two-room flat drawn in Scooch, with a living room holding a sofa, coffee table, rug and dining table, every wall measured", "A living room drawn to scale, every wall measured.")}
""",
related=["standard-sofa-dimensions", "dining-table-clearance", "how-to-measure-a-room-for-furniture"],
cta_h="Try the layout before you lift anything",
cta_p="Drag the sofa, the table and the TV around at real size. Your back will thank you.",
),
# ---------------------------------------------------------------- dining
dict(
slug="dining-table-clearance",
title="How Much Space Around a Dining Table? (cm and Inches)",
meta="How much room to leave around a dining table for chairs and walkways, how many seats fit a table, and how big a table a room can take.",
h1="How Much Space Do You Need Around a Dining Table?",
lede="A table that fits the room on paper can still leave nobody able to pull out a chair. Plan for the chairs, not just the table.",
card="Room for the chairs, room to walk behind them, and how many seats fit.",
quick=f"""<strong>Quick answer:</strong> Leave {cm(75, 90)} between the table's edge and a wall or other furniture, so a chair can be pulled out and sat on. Where people need to walk behind someone sitting down, leave {cm(90, 120)}. Allow about {cm(60)} of table edge per person.""",
body=f"""
<h2>The numbers</h2>
<ul>
  <li><strong>Behind a chair:</strong> {cm(75, 90)} from the table's edge to the wall, enough to pull the chair out and sit.</li>
  <li><strong>Walking behind someone seated:</strong> {cm(90, 120)}.</li>
  <li><strong>Per person:</strong> about {cm(60)} of table edge, a little more with armchairs.</li>
  <li><strong>Table depth:</strong> {cm(80, 100)} leaves room for plates on both sides and dishes in the middle.</li>
</ul>

<h2>How many seats fit a table</h2>
{table(["Seats", "Rectangular", "Round (diameter)"], [
    ["4", "120 × 80 cm<br><span class='sub'>47 × 31 in</span>", cm_short(90, 110)],
    ["6", "160 to 180 × 90 cm<br><span class='sub'>63 to 71 × 35 in</span>", cm_short(120, 140)],
    ["8", "200 to 240 × 90 to 100 cm<br><span class='sub'>79 to 94 × 35 to 39 in</span>", cm_short(150, 170)],
])}

<h2>How big a table your room can take</h2>
<p>Take the room's length and width, and subtract the clearance on every side where people will sit. With 80 cm all round, a room of 320 × 280 cm takes a table of up to 160 × 120 cm. If one long side goes against a wall as a bench, you get that side's clearance back.</p>
<p>Check what else is in the way too: a radiator, a door that swings in, a sideboard you need to open.</p>

<h2>Lay the table before you buy it</h2>
<p>In <a href="/">Scooch</a>, a dining table is drawn with its places set: stretch it longer and it sets more plates. Chairs tuck under it, just like in real life, so a pushed-in chair does not count as a clash, but one that sticks into a doorway does.</p>
{figure("shot-draw.webp", "Scooch drawing a dining table at 140 by 90 cm, 75 cm tall", "Type the table's size, or draw your own.")}
""",
related=["space-between-sofa-coffee-table-and-tv", "how-to-measure-a-room-for-furniture", "bed-sizes-and-space-around-a-bed"],
cta_h="Will everyone get a chair?",
cta_p="Draw the dining area and see the table, the chairs and the walkway at real size.",
),
# ---------------------------------------------------------------- measuring
dict(
slug="how-to-measure-a-room-for-furniture",
title="How to Measure a Room for Furniture (and Draw a Floor Plan)",
meta="How to measure a room for furniture placement: walls, doors, windows, radiators and ceiling height, what people forget, and how to turn it into a plan.",
h1="How to Measure a Room for Furniture",
lede="Ten minutes with a tape measure can save a sofa going back to the shop. Here is what to measure, in what order, and what people forget.",
card="Walls, doors, windows, radiators, and the things people forget to measure.",
quick="""<strong>Quick answer:</strong> Measure every wall at floor level, then mark where each door, window and radiator starts and ends, measured from a corner. Note which way each door swings, the ceiling height, and anything fixed, like sockets and pipes. Then draw it to scale, on paper or in an app like <a href="/">Scooch</a>, before you buy anything.""",
body=f"""
<h2>What you need</h2>
<ul>
  <li>A tape measure, ideally {cm(500)} or longer.</li>
  <li>A laser measure if you have one. It makes long walls a one-person job.</li>
  <li>Paper and a pencil, for a rough sketch to write the numbers on.</li>
</ul>

<h2>Step by step</h2>
<ol>
  <li><strong>Sketch the room</strong> roughly, from above. It does not need to be neat. It is somewhere to write numbers.</li>
  <li><strong>Measure every wall at floor level</strong>, where the furniture will stand. Skirting boards take a little off each wall.</li>
  <li><strong>Mark the doors and windows:</strong> how wide each one is, and how far it starts from the nearest corner. Add the window sill's height if something will go under it.</li>
  <li><strong>Note the door swings:</strong> which way each door opens, and how far into the room it reaches.</li>
  <li><strong>Add the fixed things:</strong> radiators (and how far they stick out), sockets, switches, pipes, columns, a chimney breast.</li>
  <li><strong>Measure the ceiling height</strong>, and any slope or beam that lowers it.</li>
  <li><strong>Check the corners:</strong> measure both diagonals. If they match, the corners are square. If not, the room is a little out, which is normal in older buildings. Plan with the shorter numbers.</li>
</ol>

<h2>What people forget</h2>
<ul>
  <li><strong>The way in.</strong> The furniture has to get through the front door, up the stairs and round the corner first. The <a href="{CALC}">sofa fit calculator</a> checks a doorway and a turn.</li>
  <li><strong>Things that open:</strong> wardrobe doors, drawers, an oven, a sofa bed. They need their space in front of them.</li>
  <li><strong>Radiators:</strong> a sofa pushed up against one can stick out further than you planned.</li>
  <li><strong>Walkways:</strong> {cm(75, 90)} for the paths you use every day.</li>
</ul>

<h2>Turn the numbers into a plan</h2>
<p>A sketch with numbers on it is a list. A plan drawn to scale shows you where things go. In <a href="/">Scooch</a>, type each wall's length and it stays exact, slide doors and windows along the walls, and join rooms into an L or a U for the whole flat. Every wall shows its measurement, in metric or imperial.</p>
{figure("shot-plan.webp", "A flat drawn to scale in Scooch, with a bedroom and a living room, every wall showing its length", "Every wall keeps its measurement.")}
""",
related=["standard-sofa-dimensions", "bed-sizes-and-space-around-a-bed", "space-between-sofa-coffee-table-and-tv"],
cta_h="Your measurements, drawn to scale",
cta_p="Type the walls, add doors and windows, and start placing furniture.",
),
]

BY_SLUG = {p["slug"]: p for p in PAGES}


def related_html(slugs):
    items = "\n".join(f'      <li><a href="/guides/{s}/">{BY_SLUG[s]["h1"]}</a></li>' for s in slugs)
    return f"""<div class="related">
    <h2>Related</h2>
    <ul>
      <li><a href="{CALC}">Will my sofa fit through the door? The sofa fit calculator</a></li>
{items}
    </ul>
    <p><a href="/guides/">All guides</a></p>
  </div>"""


def article_ld(p, canonical):
    return ld({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": p["h1"],
        "description": p["meta"],
        "image": f"{DOMAIN}/assets/og-image.png",
        "datePublished": TODAY,
        "dateModified": TODAY,
        "author": {"@type": "Person", "name": "Emils Ozols", "url": "https://ozols.dev"},
        "publisher": {"@type": "Organization", "name": "Scooch",
                      "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/icon-512.png"}},
        "mainEntityOfPage": canonical,
    }) + "\n" + breadcrumb_ld([("Home", f"{DOMAIN}/"), ("Guides", f"{DOMAIN}/guides/"),
                               (p["h1"], canonical)])


def guide_compare(slug):
    """A guide's line into the comparisons (compare_data.GUIDE_COMPARE), or nothing."""
    text = C.GUIDE_COMPARE.get(slug)
    if not text:
        return ""
    names = {a["key"]: a["name"] for a in C.APPS}
    links = {k: f'<a href="{VS_URL(k)}">{html.escape(n)}</a>' for k, n in names.items()}
    links["all"] = f'<a href="/compare/">all {len(C.APPS)} room planner apps compared</a>'
    for k, link in links.items():
        text = text.replace("{" + k + "}", link)
    return f'\n<p class="compare-link">{text}</p>'


for p in PAGES:
    canonical = f"{DOMAIN}/guides/{p['slug']}/"
    body = f"""<article class="article">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/guides/">Guides</a> › {p['h1']}</nav>
  <h1>{p['h1']}</h1>
  <p class="lede">{p['lede']}</p>
  <div class="quick-answer"><p>{p['quick']}</p></div>
{p['body']}{guide_compare(p['slug'])}
{cta_html(p['cta_h'], p['cta_p'], CT_GUIDE)}
{related_html(p['related'])}
</article>"""
    write(f"guides/{p['slug']}/index.html",
          page(p["title"], p["meta"], canonical, body, CT_GUIDE, article_ld(p, canonical)))

# =========================================================================================
# THE SOFA FIT CALCULATOR
# =========================================================================================
# Side view, back on the left: depth 90, height 85, arm 65 cm at 2.6 px/cm. The straight
# edge runs from the top of the back to the front of the arm; the diagonal depth is the
# perpendicular from the bottom back corner to it, about 77 cm here (foot at 123.6, 48.7).
DIAGRAM = """<figure class="diagram">
  <svg viewBox="0 0 560 330" role="img" aria-labelledby="dd-title">
    <title id="dd-title">Side view of a sofa: depth along the floor, height up the back, and the diagonal depth measured from the bottom back corner to a straight edge laid from the top of the back to the front of the arm</title>
    <g fill="none" stroke="#3b4527" stroke-width="2"><line x1="40" y1="260" x2="520" y2="260"/></g>
    <polygon points="80,245 80,39 130,39 130,91 314,91 314,245" fill="#c77deb" fill-opacity="0.28" stroke="#c77deb" stroke-width="2.5"/>
    <rect x="88" y="245" width="12" height="15" fill="#c77deb" fill-opacity="0.6"/>
    <rect x="294" y="245" width="12" height="15" fill="#c77deb" fill-opacity="0.6"/>
    <line x1="66" y1="35.9" x2="340" y2="96.8" stroke="#eef2e2" stroke-width="2.5" stroke-dasharray="7 5"/>
    <line x1="80" y1="245" x2="123.6" y2="48.7" stroke="#a6c25f" stroke-width="3.5"/>
    <circle cx="80" cy="245" r="4.5" fill="#a6c25f"/>
    <circle cx="123.6" cy="48.7" r="4.5" fill="#a6c25f"/>
    <g stroke="#aab392" stroke-width="1.5">
      <line x1="80" y1="290" x2="314" y2="290"/><line x1="80" y1="282" x2="80" y2="298"/><line x1="314" y1="282" x2="314" y2="298"/>
      <line x1="44" y1="39" x2="44" y2="260"/><line x1="36" y1="39" x2="52" y2="39"/><line x1="36" y1="260" x2="52" y2="260"/>
    </g>
    <g font-family="-apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif" font-size="15" fill="#aab392">
      <text x="197" y="314" text-anchor="middle">Depth</text>
      <text x="30" y="150" text-anchor="middle" transform="rotate(-90 30 150)">Height</text>
      <text x="350" y="92" fill="#eef2e2">straight edge</text>
      <text x="112" y="175" fill="#cfe09a" font-weight="700" transform="rotate(-77.5 112 175)" text-anchor="middle">Diagonal depth</text>
    </g>
  </svg>
  <figcaption>Diagonal depth: from the bottom back corner, at a right angle, up to a straight edge laid from the top of the back to the front of the arm.</figcaption>
</figure>"""


def field(fid, name, hint=""):
    hint_html = f" {hint}" if hint else ""
    return f"""        <label for="{fid}"><span class="name">{name}</span>
          <span class="fit-field"><input id="{fid}" type="number" inputmode="decimal" min="0" step="any"><span class="unit-label">cm</span></span>{hint_html}
        </label>"""


CALC_FAQ = [
    ("What is diagonal depth on a sofa?",
     """The distance from the bottom back corner of the sofa to a straight edge laid from the top of
     the back to the front of the arm. It is the narrowest the sofa gets when you tip it back, so if
     it is smaller than the doorway, the sofa can be tipped through even when its depth and height
     are not.""", None),
    ("How much room should I leave in the doorway?",
     """At least 2.5 cm (1 in). Moving blankets, the door handle and an unsteady grip all take a little
     of it. The calculator marks anything closer than that as only just fitting.""", None),
    ("Does taking the door off help?",
     """Usually, yes. An open door still sits in the opening and narrows it by about its own
     thickness. With the door off its hinges, measure again from frame to frame, minus the door
     stops.""", None),
    ("What about stairs?",
     """Stairs add two things to check: the headroom where the stairs turn, and the width of the
     landing. Measure the narrowest point of the whole route. A tight turn on a landing is where
     standing the sofa on its end often helps.""", None),
    ("It gets through the door. Will it fit the room?",
     """That is the other half of the job. Draw the room at its real size and place the sofa at the
     size from the listing, with room to walk round it. Scooch does exactly that on iPhone.""",
     "/guides/standard-sofa-dimensions/"),
]

calc_canonical = f"{DOMAIN}{CALC}"
calc_body = f"""<article class="article">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> › Sofa fit calculator</nav>
  <h1>Will my sofa fit through the door?</h1>
  <p class="lede">Type in the sofa and the doorway. The calculator tells you whether it goes straight through, needs tipping back, or will not make it, and whether it gets round a turn on the way. It all runs in your browser: nothing you type is sent anywhere.</p>

  <form class="fit-tool" id="fit-form" novalidate>
    <div class="unit-toggle" role="radiogroup" aria-label="Units">
      <label><input type="radio" name="unit" value="cm" checked><span>cm</span></label>
      <label><input type="radio" name="unit" value="in"><span>inches</span></label>
    </div>
    <fieldset>
      <legend>Your sofa</legend>
      <div class="fit-grid">
{field("sofa-w", "Width", "arm to arm")}
{field("sofa-d", "Depth", "back to front")}
{field("sofa-h", "Height", "floor to top of back")}
{field("sofa-dd", "Diagonal depth", "optional, see below")}
{field("legs", "Legs that come off", "optional, their height")}
      </div>
    </fieldset>
    <fieldset>
      <legend>The doorway</legend>
      <div class="fit-grid">
{field("door-w", "Width", "the open gap")}
{field("door-h", "Height", "optional, 200 cm if empty")}
      </div>
    </fieldset>
    <fieldset>
      <legend>A turn on the way <span class="opt">(optional)</span></legend>
      <div class="fit-grid">
{field("hall-a", "Hallway width", "before the turn")}
{field("hall-b", "Width after the turn", "the door's, if empty")}
{field("ceiling", "Ceiling height", "for standing it on end")}
      </div>
    </fieldset>
    <button class="fit-submit" type="submit">Check the fit</button>
    <div id="fit-result" aria-live="polite"></div>
  </form>

  <h2>How to measure the sofa</h2>
  <ul>
    <li><strong>Width:</strong> arm to arm, at the widest point.</li>
    <li><strong>Depth:</strong> from the back to the front of the arm or the seat, whichever sticks out further.</li>
    <li><strong>Height:</strong> from the floor to the top of the back. If the legs unscrew, measure them too: the calculator takes them off the height.</li>
    <li><strong>Diagonal depth:</strong> lay a straight edge, like a broom handle, from the top of the back to the front of the arm. Then measure from the bottom back corner of the sofa up to the straight edge, at a right angle. Shop listings often give it too.</li>
  </ul>
  {DIAGRAM}

  <h2>How to measure the doorway</h2>
  <ul>
    <li><strong>Width:</strong> open the door all the way and measure the narrowest gap. That is usually from the door stop on one side to the face of the open door on the other, not the frame.</li>
    <li><strong>Height:</strong> from the floor to the underside of the frame.</li>
    <li><strong>A turn on the way:</strong> if the sofa has to turn from a hallway into the door, measure the hallway's narrowest width. The calculator assumes it turns straight into the doorway unless you give the width after the turn.</li>
  </ul>

  <h2>What the answer means</h2>
  <ul>
    <li><strong>Straight through:</strong> the gap is wider than the sofa's depth, carried upright, or its height, carried on its back.</li>
    <li><strong>Tipped back:</strong> neither fits, but the diagonal depth does. Tip the sofa back and swing it through the opening.</li>
    <li><strong>The turn:</strong> the calculator works out the longest box that can be carried level round a right-angle turn. Standing a sofa on its end can beat that, if the ceiling is high enough. Movers also tilt and twist, which this flat-floor maths does not count, so a near miss is worth a second look.</li>
  </ul>

  <h2>If it does not fit</h2>
  <ul>
    <li>Take the legs off. Many screw off by hand.</li>
    <li>Take the door off its hinges and measure again.</li>
    <li>Ask the shop whether the back or the arms come off, or whether it comes in sections. Many corner sofas arrive in two or more pieces.</li>
    <li>Measure the whole route, not just one door: the front door, the stairs, the landings, the turn into the room. The tightest point decides.</li>
  </ul>

  <h2>Then make sure it fits the room</h2>
  <p>Getting it through the door is half the job. The other half is whether it fits the room with space to walk round it. In <a href="/">Scooch</a>, draw the room at its real measurements, add the sofa at the size from the listing, and anything that clashes turns red, before anything heavy moves. There are typical sizes in the <a href="/guides/standard-sofa-dimensions/">sofa dimensions guide</a>.</p>

{cta_html("Fits the door. Does it fit the room?", "Draw the room, drop in the sofa at its real size, and see what fits.", CT_TOOL)}

  <h2>Common questions</h2>
  <div class="faq-list">
{faq_details(CALC_FAQ)}
  </div>
</article>"""
calc_ld = ld({
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Sofa fit calculator",
    "url": calc_canonical,
    "applicationCategory": "UtilitiesApplication",
    "operatingSystem": "Any",
    "browserRequirements": "Requires JavaScript",
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    "description": "Checks whether a sofa fits through a doorway, straight, on its back or tipped back by its diagonal depth, and whether it gets round a turn in a hallway.",
}) + "\n" + faq_ld(CALC_FAQ) + "\n" + breadcrumb_ld([("Home", f"{DOMAIN}/"), ("Sofa fit calculator", calc_canonical)])
write("sofa-fit-calculator/index.html",
      page("Will My Sofa Fit Through the Door? Sofa Fit Calculator",
           "Type your sofa's width, depth, height and diagonal depth, and the doorway. See if it goes through, needs tipping back, or gets round the turn.",
           calc_canonical, calc_body, CT_TOOL, calc_ld,
           scripts='<script src="/assets/fit.js" defer></script>'))

# =========================================================================================
# GUIDES HUB
# =========================================================================================
CLUSTERS = [
    ("Will it fit?",
     """Most furniture regrets start with one number nobody checked. These cover the sizes worth
     knowing before you order, and the route the piece has to take to get in.""",
     ["standard-sofa-dimensions", "corner-sofa-dimensions"]),
    ("Space around furniture",
     """A room can hold a piece of furniture and still not work with it in. The gaps are what make it
     livable: room to walk, to sit down, to open a door.""",
     ["space-between-sofa-coffee-table-and-tv", "bed-sizes-and-space-around-a-bed", "dining-table-clearance"]),
    ("Measuring and planning",
     """Everything else starts here: the walls, the doors, and the things that stick out.""",
     ["how-to-measure-a-room-for-furniture"]),
]
_clustered = [s for _, _, slugs in CLUSTERS for s in slugs]
assert sorted(_clustered) == sorted(BY_SLUG), (
    f"hub out of sync: missing {sorted(set(BY_SLUG) - set(_clustered))}, "
    f"unknown {sorted(set(_clustered) - set(BY_SLUG))}")

HUB_FAQ = [
    ("How big is a standard 3-seater sofa?",
     f"""Usually {cm(190, 230)} wide, {cm(85, 100)} deep and {cm(75, 90)} tall. Check the listing:
     sofas with the same number of seats vary a lot.""",
     "/guides/standard-sofa-dimensions/"),
    ("How do I know if a sofa will fit through my door?",
     """Compare the doorway's open width with the sofa's depth and height. If both are bigger, compare
     the diagonal depth: if that is smaller than the doorway, the sofa can be tipped through.""",
     CALC),
    ("How much space should be between a sofa and a coffee table?",
     f"""{cm(35, 45)}: close enough to reach, far enough for your legs.""",
     "/guides/space-between-sofa-coffee-table-and-tv/"),
    ("How much space do you need around a bed?",
     f"""At least {cm(60)} on the sides you use and at the foot, and {cm(75, 90)} if you can.""",
     "/guides/bed-sizes-and-space-around-a-bed/"),
    ("How much space do you need around a dining table?",
     f"""{cm(75, 90)} from the table's edge to a wall, so a chair can be pulled out. {cm(90, 120)} where
     people walk behind someone seated.""",
     "/guides/dining-table-clearance/"),
]


def cards(slugs):
    return "\n".join(f"""      <a class="guide-card" href="/guides/{s}/">
        <h3>{BY_SLUG[s]['h1']}</h3>
        <p>{BY_SLUG[s]['card']}</p>
        <span class="more">Read the guide</span>
      </a>""" for s in slugs)


TOOL_CARD = f"""      <a class="guide-card tool" href="{CALC}">
        <h3>Will my sofa fit through the door?</h3>
        <p>The sofa fit calculator: the doorway, tipping it back, and the turn in the hallway.</p>
        <span class="more">Check the fit</span>
      </a>"""

clusters_html = "\n".join(f"""  <div class="container guide-cluster">
    <h2>{h}</h2>
    <p class="cluster-intro">{" ".join(intro.split())}</p>
    <div class="guide-grid">
{TOOL_CARD + chr(10) if i == 0 else ""}{cards(slugs)}
    </div>
  </div>""" for i, (h, intro, slugs) in enumerate(CLUSTERS))

hub_body = f"""<article class="article">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> › Guides</nav>
  <h1>Room Planning Guides</h1>
  <p class="lede">Furniture sizes, the space to leave around them, and how to measure a room, in centimetres and inches.</p>
  <p>Almost every "it does not fit" comes down to a number nobody wrote down: the doorway, the depth of the sofa, the room a chair needs to pull out. These guides collect the numbers worth knowing, as common rules of thumb rather than laws, and say how to check them in your own room.</p>
  <p>Each one ends with how to try it in <a href="/">Scooch</a>, the iPhone app I make for exactly this. Where a tape measure and a pencil are enough, the guide says so.</p>
</article>
<section style="padding-top: 0;">
{clusters_html}
</section>
<section>
  <div class="container">
    <h2>Common questions</h2>
    <div class="faq-list">
{faq_details(HUB_FAQ)}
    </div>
  </div>
</section>"""
hub_desc = "Furniture sizes in cm and inches, the space to leave around a sofa, bed or dining table, how to measure a room, and a sofa fit calculator."
hub_head_ld = ld({
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "Room Planning Guides",
    "description": hub_desc,
    "url": f"{DOMAIN}/guides/",
}) + "\n" + faq_ld(HUB_FAQ)
write("guides/index.html",
      page("Room Planning Guides: Furniture Sizes, Clearances, Measuring",
           hub_desc, f"{DOMAIN}/guides/", hub_body, CT_GUIDE, hub_head_ld))

# =========================================================================================
# HOME
# =========================================================================================
ICONS = {
    "ruler": '<path d="M3 17L17 3l4 4L7 21z"/><path d="M7 13l2 2M10 10l2 2M13 7l2 2"/>',
    "door": '<path d="M4 21h16"/><path d="M6 21V4h8v17"/><path d="M14 4c3.5 1 5.5 4.5 5.5 9"/><circle cx="11.5" cy="12.5" r="0.9" fill="currentColor" stroke="none"/>',
    "sofa": '<path d="M4 11V8a2 2 0 012-2h12a2 2 0 012 2v3"/><path d="M2 12a2 2 0 014 0v2h12v-2a2 2 0 014 0v5H2z"/><path d="M5 17v2M19 17v2"/>',
    "clash": '<rect x="3" y="7" width="11" height="9" rx="1.5"/><rect x="10" y="4" width="11" height="9" rx="1.5"/><path d="M10 7h4v6h-4z" fill="currentColor" stroke="none" opacity="0.6"/>',
    "swing": '<path d="M4 20V6"/><path d="M4 6h10"/><path d="M14 6c0 7.7-4.3 14-10 14" stroke-dasharray="2.5 2.5"/>',
    "pencil": '<path d="M16 3l5 5L9 20H4v-5z"/><path d="M13 6l5 5"/>',
    "plans": '<rect x="3" y="4" width="8" height="7" rx="1.2"/><rect x="13" y="4" width="8" height="7" rx="1.2"/><rect x="3" y="13" width="8" height="7" rx="1.2"/><path d="M17 14v6M14 17h6"/>',
    "corner": '<path d="M3 6h18v6H9v8H3z"/><path d="M3 12h6"/>',
}
FEATURES = [
    ("ruler", "Rooms at their real size", "Type a wall's length and it stays exact. Every wall shows its measurement, in metric or imperial."),
    ("door", "Doors and windows on the walls", "Doors, windows and arches slide along a wall, with real swing arcs."),
    ("sofa", "Furniture that keeps up", "37 pieces at real sizes. Stretch a dining table and it sets more plates. Widen a sofa and it gets more cushions."),
    ("clash", "Clashes in red", "A piece that overlaps another or sticks out of the room turns red. Chairs tucked under a table are fine."),
    ("swing", "Room to open", "Doors, drawers and sofa beds can show the space they need to open."),
    ("corner", "Corner sofas", "One L-shaped piece with its own depth on each side, and a sofa bed that pulls out to the corner."),
    ("pencil", "Draw your own", "Missing a piece? Draw it, type its size, and it behaves like any other."),
    ("plans", "As many plans as you need", "Your flat, the summer place, the office move. Export any plan as a PNG or a PDF."),
]
SHOTS = [
    ("shot-plan.webp", "A two-room flat drawn to scale, every wall measured", "Your rooms at their real size"),
    ("shot-clash.webp", "A 360 cm sofa flagged red because it does not fit the room", "Red means it does not fit"),
    ("shot-projections.webp", "Furniture doors, drawers and a sofa bed showing the space they need", "Room to open"),
    ("shot-furniture.webp", "The furniture list with each piece's default size", "Real sizes to start from"),
    ("shot-draw.webp", "Drawing a dining table at 140 by 90 cm", "Draw your own furniture"),
    ("shot-plans.webp", "Three plans: a flat, a studio and an office", "Every place you plan"),
    ("shot-linen.webp", "The same flat in the light Linen theme", "26 themes"),
    ("shot-amethyst.webp", "The same flat in the Amethyst theme", "Dark or light"),
]
HOME_FAQ = [
    ("Is Scooch free?",
     """Scooch is free to download, and your first room is on the house: draw it and see what fits.
     Keeping going is a one-time unlock, not a subscription. The price is shown in the app before you
     buy. If you had Scooch before version 1.0.1, everything stays unlocked for you.""",
     "/terms/"),
    ("Can I type exact sizes from a shop listing?",
     """Yes. Tap any piece of furniture or any room and type the numbers. Typed sizes stay exact, and
     the drawing redraws to match: more cushions on a wider sofa, more plates on a longer table.""",
     None),
    ("Does it work in inches?",
     """Yes. Switch between metric and imperial in Settings, and every measurement follows.""",
     None),
    ("Can it tell me if a sofa fits through my door?",
     """The app plans the room. For the doorway, use the free sofa fit calculator on this site: it
     checks the opening, tipping the sofa back, and a turn in the hallway.""",
     CALC),
    ("Is there a corner sofa?",
     """Yes, as one L-shaped piece. Type the depth of each side on its own, mirror it to swap the side,
     and turn on the sofa bed to see where it pulls out.""",
     "/guides/corner-sofa-dimensions/"),
    ("Where are my plans stored?",
     """On your iPhone. If iCloud is available, Scooch also keeps a backup in your own iCloud, so a new
     phone can pick up where you left off. There is no account, and nothing is sent to me.""",
     "/privacy/"),
    ("Can I share or print a plan?",
     """Yes. Export any plan as a PNG image or a PDF page and share it like any other file.""",
     None),
    ("Does Scooch have ads, or need an account?",
     """No ads and no account.""",
     "#download"),
    ("Is there an Android version?",
     """Not at the moment: Scooch is made for iPhone.""",
     None),
]


def feature_cards():
    return "\n".join(f"""      <div class="feature-card">
        <div class="ico"><svg viewBox="0 0 24 24" aria-hidden="true">{ICONS[i]}</svg></div>
        <h3>{h}</h3>
        <p>{p}</p>
      </div>""" for i, h, p in FEATURES)


def marquee_set(hidden):
    figs = "\n".join(f"""          <figure>
            <img class="screen" src="/assets/{src}" alt="{'' if hidden else html.escape(alt)}" loading="lazy" width="640" height="1284">
            <figcaption>{cap}</figcaption>
          </figure>""" for src, alt, cap in SHOTS)
    aria = ' aria-hidden="true"' if hidden else ""
    return f"""        <div class="shots-set"{aria}>
{figs}
        </div>"""


HOME_TITLE = "Scooch: Room and Floor Planner for iPhone. Will It Fit?"
HOME_DESC = ("Draw your rooms at their real measurements, place furniture at real sizes, and see what "
             "fits before you move anything heavy. A floor plan app for iPhone.")
HOME_OG = "Draw the room, drop in the furniture at real size, and see what fits before anything heavy moves."
STORE = store_url(CT_HOME)

home_body = f"""
<!-- ============ HERO ============ -->
<section class="hero" id="download">
  <div class="container hero-grid">
    <div>
      <span class="eyebrow">Room and floor planner for iPhone</span>
      <h1>Will it fit? Find out <span class="accent">before you carry it</span></h1>
      <p class="hero-sub">The tape measure says 214 cm. The room disagrees. Moving day is a bad time to find out who is right. Scooch draws your rooms at their real measurements and your furniture at real sizes, so you see what fits and what collides before anything heavy moves.</p>
      <div class="cta-row">
        {badge(CT_HOME)}
        <a class="btn-secondary" href="{CALC}">Sofa fit calculator</a>
      </div>
      <div class="trust-row">
        <span>Typed sizes stay exact</span>
        <span>Metric or imperial</span>
        <span>No account, no ads</span>
        <span>One-time unlock, no subscription</span>
      </div>
    </div>
    <div class="hero-art">
      <img class="screen" src="/assets/shot-plan.webp" alt="Scooch on iPhone: a two-room flat drawn to scale, with furniture placed and every wall measured" width="640" height="1284" fetchpriority="high">
    </div>
  </div>
</section>

<!-- ============ FEATURES ============ -->
<section id="features">
  <div class="container">
    <div class="section-head">
      <h2>A measuring tape that draws</h2>
      <p>Not photorealistic renders. Clean shapes at real sizes, and an honest answer.</p>
    </div>
    <div class="feature-grid">
{feature_cards()}
    </div>
    <p class="extras"><strong>Also in the box:</strong> 26 themes, a native Liquid Glass design for iOS 26, plans that join rooms into an L or a U, and an automatic backup to your own iCloud.</p>
  </div>
</section>

<!-- ============ SCREENSHOTS ============ -->
<section id="screenshots">
  <div class="container">
    <div class="section-head">
      <h2>See it in action</h2>
      <p>Real screens, straight from the app.</p>
    </div>
  </div>
  <div class="shots-marquee">
      <div class="shots-track">
{marquee_set(False)}
{marquee_set(True)}
      </div>
    </div>
</section>

<!-- ============ HOW IT WORKS ============ -->
<section id="how-it-works">
  <div class="container">
    <div class="section-head">
      <h2>How it works</h2>
      <p>From "will it fit?" to an answer, in three steps.</p>
    </div>
    <div class="steps">
      <div class="step">
        <div class="num">1</div>
        <h3>Draw the room</h3>
        <p>Type the walls in, then slide the doors and windows to where they really are. <a href="/guides/how-to-measure-a-room-for-furniture/">How to measure a room</a>.</p>
      </div>
      <div class="step">
        <div class="num">2</div>
        <h3>Add the furniture</h3>
        <p>Pick from the list and type the sizes from the shop listing, or draw your own piece.</p>
      </div>
      <div class="step">
        <div class="num">3</div>
        <h3>See what fits</h3>
        <p>Anything that clashes turns red. A couch that will not fit is a lot easier to move on screen.</p>
      </div>
    </div>
  </div>
</section>

<!-- ============ TOOLS AND GUIDES ============ -->
<section id="guides">
  <div class="container">
    <div class="section-head">
      <h2>Free tools and guides</h2>
      <p>The numbers worth knowing before anything is delivered.</p>
    </div>
    <div class="guide-grid">
{TOOL_CARD}
{cards([p["slug"] for p in PAGES])}
    </div>
  </div>
</section>

<!-- ============ FAQ ============ -->
<section id="faq">
  <div class="container">
    <div class="section-head">
      <h2>Frequently asked questions</h2>
    </div>
    <div class="faq-list">
{faq_details(HOME_FAQ)}
    </div>
  </div>
</section>

<!-- ============ CTA ============ -->
<section>
  <div class="container">
    <a class="cta-band" href="{STORE}" data-ph="appstore_click" aria-label="Download Scooch on the App Store">
      <h2>Measure once, move nothing</h2>
      <p>Draw your first room free, then unlock everything with one payment. No subscription.</p>
      <div class="cta-row">
        <span class="badge-link">
          <img src="/assets/appstore-badge.svg" alt="Download on the App Store" width="180" height="60">
        </span>
      </div>
    </a>
  </div>
</section>
"""
home_ld = ld({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Scooch",
    "operatingSystem": f"iOS {MIN_IOS} or later",
    "applicationCategory": "DesignApplication",
    "description": "Room and floor planner for iPhone. Draw rooms at their real measurements, place furniture at real sizes, and see what fits and what collides before you move anything.",
    "url": f"{DOMAIN}/",
    "downloadUrl": STORE_CANONICAL,
    "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
    "author": {"@type": "Person", "name": "Emils Ozols", "url": "https://ozols.dev"},
    "image": f"{DOMAIN}/assets/icon-512.png",
}) + "\n" + faq_ld(HOME_FAQ)
write("index.html", page(HOME_TITLE, HOME_DESC, f"{DOMAIN}/", home_body, CT_HOME, home_ld,
                         og_type="website", ogdesc=HOME_OG))

# =========================================================================================
# SUPPORT / PRIVACY / TERMS (ported from ozols.dev/scooch/, which stays live: the 1.0.1
# paywall and the App Store listing link there. Move those links in a later version.)
# =========================================================================================
LEGAL = [
dict(
slug="support",
title="Support | Scooch",
meta="Support for Scooch, the room and floor planner for iPhone: contact, the one-time unlock, exact sizes, backups and sharing a plan.",
h1="Support",
sub="Questions, problems or ideas? Every email lands in a real inbox, and I read everything.",
body="""
<div class="quick-answer"><p><strong>Email:</strong> <a href="mailto:emils@ozols.dev?subject=Scooch%20support">emils@ozols.dev</a>. I usually reply within a couple of days. Scooch is made by one person, so a short description of what you expected and what happened instead helps a lot. You can also use the feedback form inside the app.</p></div>

<h2>Frequently asked</h2>

<h3>Is Scooch free?</h3>
<p>Scooch is free to download. You can draw your first room and check the fit; keeping going is a one-time unlock, not a subscription. If you had Scooch before version 1.0.1, everything stays unlocked for you.</p>

<h3>I bought it on another phone</h3>
<p>Sign in with the same Apple Account and tap Restore on the unlock screen. The purchase comes back at no cost.</p>

<h3>How do I get exact sizes?</h3>
<p>Tap any piece of furniture or room and type the numbers. Typed dimensions stay exact. You can switch between metric and imperial in Settings.</p>

<h3>Where are my plans stored?</h3>
<p>On your device. If iCloud is available, Scooch also keeps a backup in your own iCloud storage so a new phone can pick up where you left off. Nothing is sent to me or anyone else.</p>

<h3>Can I share a plan?</h3>
<p>Yes. Export any plan as a PNG image or a PDF page from Settings and share it like any file.</p>

<h3>Something is flagged red. Why?</h3>
<p>Red means two things overlap in a way that would not work in real life, or a piece does not fit inside the room. Chairs tucked under tables are fine and stay unflagged.</p>

<h2>Guides</h2>
<p>For furniture sizes, the space to leave around them and how to measure a room, see the <a href="/guides/">guides</a>. To check a doorway, use the <a href="/sofa-fit-calculator/">sofa fit calculator</a>.</p>
""",
),
dict(
slug="privacy",
title="Privacy Policy | Scooch",
meta="Privacy policy for Scooch, the iPhone floor plan app. No account, no ads, anonymous opt-out usage analytics: your plans stay on your device.",
h1="Privacy Policy",
sub="Last updated: 1 October 2026",
body="""
<h2>Data storage</h2>
<p>Scooch stores your plans, custom furniture and settings on your device. There is no account and no login, and I run no server that holds your plans. Your data stays on your device, apart from the optional iCloud backup and the anonymous analytics described below. Buying the unlock goes through Apple, as described under Purchases.</p>

<h2>iCloud backup</h2>
<p>So your plans survive a reinstall or a move to a new iPhone, Scooch can back them up to your own private iCloud. Backup is on by default when you are signed in to iCloud, and you can turn it off at any time in Settings. The backup is held by Apple under your Apple Account and covered by Apple's privacy terms. It is not sent to me and I cannot see it. This is a restore point, not live cross-device sync.</p>

<h2>Anonymous usage analytics</h2>
<p>Scooch uses <strong>PostHog</strong> (hosted in the EU) to collect anonymous usage statistics, so I can see which features get used and where people get stuck.</p>
<p>What is collected:</p>
<ul>
  <li>Counts of interactions: rooms added, furniture placed, plans exported, backups made</li>
  <li>Which onboarding steps were viewed, and the fit check's final gap number</li>
  <li>App-level context: how many plans, rooms and pieces exist, the active theme, metric or imperial</li>
  <li>Taps on the drawing: whether a tap landed on a piece, a room or empty floor, never your drawing itself</li>
  <li>The unlock screen: whether it was shown, and whether you bought, restored or cancelled, with the price and currency shown to you</li>
  <li>When the app was first installed (the date only)</li>
  <li>If you came from an Apple Search Ads ad: the campaign, ad group and keyword numbers and the country Apple reports for that ad, through Apple's AdServices framework, which uses no advertising identifier</li>
  <li>An approximate location, country and city, that PostHog estimates from your connection when data arrives. Your IP address itself is discarded and not stored.</li>
  <li>Generic device context (device model, iOS version, language, app version, debug vs release build) and a random ID for this install, so events from one install can be counted together</li>
  <li>If you submit the improvement survey, the text you typed</li>
</ul>
<p>What is <strong>not</strong> collected:</p>
<ul>
  <li>Your name, email, or any personal identifiers</li>
  <li>The contents of your plans: your rooms, labels and layouts stay on your device</li>
  <li>Your precise location, contacts, or advertising identifier (IDFA)</li>
  <li>Anything linked back to you as an individual</li>
</ul>
<p>Analytics can be turned off at any time in Settings, Help out, "Share anonymous usage". The app respects it immediately.</p>

<h2>This website</h2>
<p>getscooch.com counts page views, taps on its App Store links, and whether the sofa fit calculator's answer was yes or no, with PostHog, hosted in the EU, so I can see which pages are useful. The calculator runs in your browser: the measurements you type are never sent anywhere. The site sets no cookies, stores nothing on your device, and does not build a profile of you.</p>

<h2>Purchases</h2>
<p>Scooch is free to download, and keeping going after your first room takes a one-time unlock. Apple processes that payment through the App Store. I never see your card, your Apple Account or your name; Scooch only learns from Apple whether the unlock is owned, and records the purchase in the anonymous analytics above. Refunds and billing are Apple's, see the <a href="/terms/">terms of use</a>.</p>

<h2>Third-party sharing</h2>
<p>I do not sell, share, or transfer your personal data to third parties. The services involved are PostHog, for the anonymous analytics described above, stored on EU servers and never linked to you as an individual, and Apple, which handles purchases, iCloud backup and the Apple Search Ads attribution under its own privacy terms.</p>

<h2>Your rights</h2>
<ul>
  <li><strong>Access &amp; export</strong>: your plans are visible in the app at all times and exportable as PNG or PDF. No separate copy is held elsewhere.</li>
  <li><strong>Deletion</strong>: uninstalling the app removes all plan data from that device. If iCloud backup was on, remove the saved copy by managing Scooch's storage under iCloud in iOS Settings.</li>
  <li><strong>Opt out of analytics</strong>: the Settings toggle above.</li>
</ul>
<p>If you are an EU/EEA resident, the GDPR grants you additional rights regarding any data processed. Contact me using the email below to exercise them.</p>

<h2>Children's privacy</h2>
<p>Scooch does not knowingly collect personal information from children under 13. The app requires no account and no personal information to function.</p>

<h2>Support email</h2>
<p>If you email <a href="mailto:emils@ozols.dev">emils@ozols.dev</a>, I use your message and address only to reply. No mailing lists, no sharing.</p>

<h2>Changes</h2>
<p>If a future version of Scooch changes any of the above, this page and the App Store privacy label will be updated before that version ships.</p>
""",
),
dict(
slug="terms",
title="Terms of Use | Scooch",
meta="Terms of use for Scooch, the iPhone floor plan app: the one-time unlock, refunds, measurements, and your plans.",
h1="Terms of Use",
sub="Last updated: 28 September 2026",
body="""
<p>These terms cover your use of Scooch, the iPhone floor plan app made by Emils Ozols ("I", "me"). By downloading or using Scooch you agree to them. If you do not agree, please do not use the app.</p>

<h2>Using Scooch</h2>
<p>You may use Scooch on Apple devices you own or control. Apple's <a href="https://www.apple.com/legal/internet-services/itunes/dev/stdeula/">Standard End User License Agreement</a> also applies. You may not copy, resell, reverse-engineer or redistribute the app.</p>

<h2>The unlock</h2>
<p>Scooch is free to download. You can draw your first room and see how your furniture fits; keeping going takes a one-time unlock. It is a single payment, not a subscription: nothing renews and there is nothing to cancel.</p>
<p>The price is shown in the app before you buy and varies by country or region. Apple processes the payment through the App Store, tied to your Apple Account. On a new phone, tap Restore on the unlock screen to bring your purchase back.</p>
<p>If you installed Scooch before the unlock existed (version 1.0), you keep the whole app without paying. There is nothing to do on your side.</p>

<h2>Refunds</h2>
<p>Apple handles every payment, so I cannot issue refunds myself. You can ask Apple for one at <a href="https://reportaproblem.apple.com/">reportaproblem.apple.com</a>, under Apple's refund policy.</p>

<h2>Your plans</h2>
<p>What you draw in Scooch is yours. It lives on your device and, if backup is on, in your own iCloud, as the <a href="/privacy/">privacy policy</a> describes.</p>

<h2>Measurements</h2>
<p>Scooch is a planning aid. A plan is only as accurate as the numbers you enter, and a drawing cannot see skirting boards, radiators or a wall that is not quite square. Measure the real thing before you buy, move or build anything. The same goes for the sofa fit calculator and the guides on this site: they are rules of thumb and flat-floor maths, not a promise that something fits.</p>

<h2>Acceptable use</h2>
<p>Use Scooch lawfully. Do not try to disrupt it, or to reach the systems it relies on without permission.</p>

<h2>No warranty</h2>
<p>Scooch is provided "as is" and "as available", without warranties of any kind, express or implied. Backups depend on your device, iOS and iCloud, which are outside my control, so export anything you cannot afford to lose.</p>

<h2>Limitation of liability</h2>
<p>To the extent the law allows, I am not liable for indirect, incidental or consequential damages from using Scooch or being unable to use it, including furniture bought or work done on the strength of a plan. Where liability cannot be excluded, it is limited to what you paid for Scooch in the twelve months before the claim.</p>

<h2>Changes</h2>
<p>I may change or remove features, and update these terms. If the terms change in a meaningful way, the date at the top changes too. Using Scooch after a change means you accept the updated terms.</p>

<h2>Governing law</h2>
<p>These terms are governed by the laws of Latvia and the European Union. Nothing here limits the consumer rights you have under the law of the country you live in.</p>

<h2>Contact</h2>
<p>Questions about these terms: <a href="mailto:emils@ozols.dev?subject=Scooch%20terms">emils@ozols.dev</a>. For help with the app, see <a href="/support/">support</a>.</p>
""",
),
]

for lp in LEGAL:
    body = f"""<article class="article">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> › {lp['h1']}</nav>
  <h1>{lp['h1']}</h1>
  <p class="lede">{lp['sub']}</p>
{lp['body']}
</article>"""
    write(f"{lp['slug']}/index.html", page(lp["title"], lp["meta"], f"{DOMAIN}/{lp['slug']}/", body))

# =========================================================================================
# /COMPARE/: the roundup and one page per competitor
# =========================================================================================
# Data, house rules and the head-to-head texts: compare_data.py; store facts:
# compare_snapshot.json (compare_fetch.py). Same shape as alarmclockplanner.com's /compare/
# (AlarmPlanner website/_gen/gen_guides.py, 2026-10-20): apps as columns, check / cross / dash
# marks, Apple-style footnotes, no rating or review markup for any app, only our screenshots.

with open(os.path.join(GEN, "compare_snapshot.json"), encoding="utf-8") as f:
    SNAP = json.load(f)["apps"]

_MON = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
for _a in C.APPS:
    _s = SNAP[_a["key"]]
    _a.update(version=_s["version"], updated_iso=_s["version_date"], rating=f"{_s['rating']:.1f}",
              languages=len(_s["languages"]), store=_s["url"], reviews_n=_s["reviews"]["n"])
US = C.APPS[0]
COMPARE_URLS = [f"{DOMAIN}/compare/"] + [f"{DOMAIN}{VS_URL(a['key'])}" for a in C.APPS if a["vs"]]

FN = {"about": "*", "price": "**", "listing": "***", "test": "†"}


def fn(key):
    return f'<sup class="fn"><a href="#fn-{key}" aria-label="Note {FN[key]}">{FN[key]}</a></sup>'


def footnotes(about_extra=""):
    notes = [
        ("about", "We make Scooch, so weigh our view accordingly. Facts about the other apps come from their US "
                  "App Store listings, purchase lists, privacy labels and public US reviews, checked on "
                  f"{C.CHECKED}, and from using each app ourselves.{about_extra}"),
        ("price", "US App Store prices. The US list does not name plan lengths, so a plan's length comes from the "
                  "app's own upgrade screen, and a US price is used only where it clearly matches that plan. "
                  "“Cost for one year if subscribed” is the cheapest listed plan that covers 12 months. A mark on "
                  "“Pay once” only says whether a one-time unlock exists; “6× ours” compares a price with "
                  "Scooch's $9.99 once."),
        ("listing", "As each listing describes it. A dash means the listing does not say, not that the app cannot do it."),
        ("test", f"What we saw using each app ourselves, on {C.TESTED_WHEN}, on {C.TESTED_ON}; screens from "
                 "that account show euro prices, the prices on this page are the US ones. Offers can differ by "
                 "country and change over time. On “Plan without paying”, a tick means free with no ads, amber "
                 "means free with ads, an account or locked parts, a cross means a payment or a trial comes first, "
                 "and a dash that we could not open the app. “Warns when furniture does not fit” is what happened "
                 "when we took a furnished room from each app's own samples or templates and moved the coffee table "
                 "onto the sofa."),
    ]
    return ('<div class="footnotes">\n' + "\n".join(
        f'    <p id="fn-{k}"><span class="fn-mark">{FN[k]}</span> {html.escape(t)}</p>' for k, t in notes)
        + "\n  </div>")


_YES = re.compile(r"^Yes\b[\s,.:;]*")
_NO = re.compile(r"^No\b(?!t)[\s,.:;]*")
_CHECK = ('<svg viewBox="0 0 16 16" width="17" height="17" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.8" '
          'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
_CROSS = ('<svg viewBox="0 0 16 16" width="17" height="17" aria-hidden="true"><path d="M4.2 4.2l7.6 7.6M11.8 4.2l-7.6 7.6" '
          'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>')
_DASH = ('<svg viewBox="0 0 16 16" width="17" height="17" aria-hidden="true"><path d="M4.5 8h7" fill="none" '
         'stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>')
_WARN = ('<svg viewBox="0 0 16 16" width="17" height="17" aria-hidden="true"><path d="M8 3.6v5.6" fill="none" '
         'stroke="currentColor" stroke-width="2.3" stroke-linecap="round"/><circle cx="8" cy="12.4" r="1.35" '
         'fill="currentColor"/></svg>')


def mark_cell(text):
    """"Yes..." gets a check, "No..." a cross, "Not stated/listed/described/tested" a dash. The word
    stays in the page for screen readers and search engines."""
    def note(rest):
        rest = rest.strip()
        return f' <span class="mark-note">{html.escape(rest[0].upper() + rest[1:])}</span>' if rest else ""
    if m := _YES.match(text):
        return f'<span class="mark yes">{_CHECK}<span class="sr-only">Yes</span></span>{note(text[m.end():])}'
    if m := _NO.match(text):
        return f'<span class="mark no">{_CROSS}<span class="sr-only">No</span></span>{note(text[m.end():])}'
    if text.startswith(("Not stated", "Not listed", "Not described", "Not tested")):
        return f'<span class="mark unknown">{_DASH}</span> <span class="mark-note">{html.escape(text)}</span>'
    return html.escape(text)


def _quarter(iso):
    y, m, _ = iso.split("-")
    return int(y), (int(m) - 1) // 3 + 1


def update_cell(a):
    """Last update as a quarter: this quarter gets a check, two or more quarters back is red."""
    y, q = _quarter(a["updated_iso"])
    cy, cq = _quarter(C.CHECKED_ISO)
    behind = (cy - y) * 4 + (cq - q)
    label = f"Q{q} {y}"
    if behind <= 0:
        return f'<span class="mark yes">{_CHECK}</span> {label}'
    if behind >= 2:
        return f'<span class="stale">{label}</span>'
    return label


# Can you plan without paying? One set of marks for every table and price box (compare_data.FREE_TIER).
_TIER_MARK = {"free": ("yes", _CHECK, "Yes"), "limited": ("warn", _WARN, "Limited"), "none": ("no", _CROSS, "No"),
              "untested": ("unknown", _DASH, "Not tested")}


def tier_mark(tier):
    cls, svg, word = _TIER_MARK[tier]
    return f'<span class="mark {cls}">{svg}<span class="sr-only">{word}</span></span>'


def free_cell(a):
    tier, note = C.FREE_TIER[a["key"]]
    return f'{tier_mark(tier)} <span class="mark-note">{html.escape(note[0].upper() + note[1:])}</span>'


def _cheapest(text):
    """"$44.99 to $79.99" -> 44.99; no price -> None."""
    found = [float(x) for x in re.findall(r"\$(\d+(?:\.\d+)?)", text or "")]
    return min(found) if found else None


def times_badge(a, text):
    """How many times Scooch's $9.99 once a price is; nothing for ours or for no price. Marks say whether
    an option exists; how a price compares is this badge (brand.md 2026-10-20, rule 15)."""
    amount = _cheapest(text)
    if a is US or amount is None:
        return ""
    x = amount / C.OUR_ONCE
    label = f"{x:.0f}×" if x >= 10 else f"{x:.1f}".rstrip("0").rstrip(".") + "×"
    return (f' <span class="times{" more" if x > 1.05 else ""}" title="Compared with Scooch\'s '
            f'${C.OUR_ONCE:.2f} one-time unlock">{label} ours</span>')


def once_cell(a):
    """Pay once: a check when a one-time unlock exists (whatever it costs), a cross when it does not."""
    text = a["once"]
    if m := _YES.match(text):
        return mark_cell(text) + times_badge(a, text[m.end():])
    return mark_cell(text)


def year_cell(a):
    """Cheapest 12 months as a price, no mark; the badge says how it compares with ours."""
    if a["year"] is None:
        return '<span class="mark-note">No subscription</span>'
    if _cheapest(a["year"]) is None:
        return mark_cell(a["year"])
    return f'<span class="mark-note">{html.escape(a["year"])}</span>{times_badge(a, a["year"])}'


def rating_cell(a):
    """US average: a check at 4.5 and above, a cross below. No counts (Emil, 2026-10-20)."""
    return mark_cell(("Yes, " if float(a["rating"]) >= 4.5 else "No, ") + f"{a['rating']}★")


def lang_cell(a):
    return mark_cell("Yes, 10 or more" if a["languages"] >= 10 else "No, fewer than 10")


def download_cell(a):
    """Ours is the tracked campaign link, theirs a plain nofollow store link."""
    if a is US:
        return (f'<a class="table-get" href="{store_url(CT_COMPARE)}" data-ph="appstore_click" '
                f'aria-label="Download Scooch on the App Store">Download</a>')
    return (f'<a class="table-store" href="{a["store"]}" rel="nofollow noopener" target="_blank" '
            f'aria-label="{html.escape(a["name"])} on the App Store">App Store</a>')


def other_link(a):
    if a is US:
        return f'<a href="{store_url(CT_COMPARE)}" data-ph="appstore_click">View on the App Store</a>'
    return (f'<a href="{a["store"]}" rel="nofollow noopener" target="_blank" '
            f'aria-label="View {html.escape(a["name"])} on the App Store">View on the App Store</a>')


def app_icon(a, size=36):
    """The app's own App Store icon (fetch_icons.py), only to identify it; the name follows."""
    return (f'<img class="app-icon" src="/assets/compare/icons/{a["key"]}.webp" alt="" width="{size}" '
            f'height="{size}" loading="lazy">')


def li(items):
    return "\n".join(f"        <li>{html.escape(x)}</li>" for x in items)


def _img(path, alt):
    from PIL import Image
    w, h = Image.open(os.path.join(SITE, path.lstrip("/"))).size
    return f'<img class="screen" src="{path}" alt="{html.escape(alt)}" loading="lazy" width="{w}" height="{h}">'


def our_shot(key):
    """Ours beside the about box and on our roundup card (compare_data.OUR_SHOT)."""
    f, alt = C.OUR_SHOT[key]
    return f'<figure>\n  {_img(f"/assets/{f}.webp", alt)}\n  <figcaption>Scooch {US["version"]}</figcaption>\n</figure>'


MISSING_SHOTS = set()


def their_shot(app, slot):
    """Our own capture of the other app for one slot (compare_data.THEIR_SHOTS), or nothing."""
    spots = C.THEIR_SHOTS.get(app["key"], {})
    if slot not in spots:
        return ""
    path = f"assets/compare/{app['key']}-{slot}.webp"
    if not os.path.isfile(os.path.join(SITE, path)) or app["key"] not in C.SHOTS_TAKEN:
        MISSING_SHOTS.add(path)
        return ""
    version, taken = C.SHOTS_TAKEN[app["key"]]
    return (f'<figure>\n  {_img("/" + path, spots[slot])}\n'
            f'  <figcaption>{html.escape(app["name"])} {version} · {taken}</figcaption>\n</figure>')


def our_slot_shot(slot):
    path, alt, name = C.OUR_SHOTS[slot]
    return f'<figure>\n  {_img(path, alt)}\n  <figcaption>{name} {US["version"]}</figcaption>\n</figure>'


def side_by_side(a):
    """Row per slot the other app has: their screen, ours next to it, or a card where we have no such screen."""
    spots = C.THEIR_SHOTS.get(a["key"], {})
    rows = []
    for slot, title in C.SLOTS:
        theirs = their_shot(a, slot)
        if not theirs:
            continue
        title = C.SLOT_TITLES.get(a["key"], {}).get(slot, title)
        if slot in C.OUR_SHOTS:
            ours = our_slot_shot(slot)
        else:
            head, text = C.OUR_NONE[slot]
            ours = (f'<div class="sbs-none"><span class="mark yes">{_CHECK}</span><strong>{html.escape(head)}</strong>'
                    f'<span>{html.escape(text)}</span></div>')
        rows.append(f'  <div class="sbs-row">\n    <h3>{html.escape(title)}</h3>\n    <p>{html.escape(spots[slot])}.</p>\n'
                    f'    <div class="sbs-pair">\n    {theirs}\n    {ours}\n    </div>\n  </div>')
    if not rows:
        return ""
    return (f'<h2 class="app-title">{app_icon(a, 32)}<span>{html.escape(a["short"])} and Scooch, side by side</span></h2>\n'
            f'  <p>Screens we captured ourselves, {html.escape(a["short"])} on the left, Scooch on the right. Ours ran on '
            f'an EU App Store account, so prices on screen are in euros.{fn("test")}</p>\n' + "\n".join(rows))


def tested(a):
    if a["key"] not in C.TESTED:
        return ""
    return (f'<h2 class="app-title">{app_icon(a, 32)}<span>What we saw using {html.escape(a["short"])}</span></h2>\n'
            f'  <p>On {C.TESTED_WHEN}, on {C.TESTED_ON}.{fn("test")}</p>\n  <ul>\n{li(C.TESTED[a["key"]])}\n  </ul>')


def we_dont(v):
    """What we leave out, for this page's reader: (lead, why) pairs; our generic cons where a page has none."""
    if "we_dont" not in v:
        return li(US["cons"])
    return "\n".join(f"        <li><strong>{html.escape(h)}</strong> {html.escape(t)}</li>" for h, t in v["we_dont"])


def maker_note(v):
    if not v.get("maker_note"):
        return ""
    return (f'  <div class="maker-note"><p>{html.escape(v["maker_note"])}</p>'
            f'<p class="maker-by">Emils, who makes Scooch</p></div>')


def faq_html(faq):
    items = "\n".join(f"  <h3>{html.escape(q)}</h3>\n  <p>{html.escape(a)}</p>" for q, a in faq)
    return f"<h2>Questions</h2>\n{items}"


def compare_jsonld(headline, desc, canonical, crumbs, faq=None, itemlist=None):
    blocks = [{
        "@context": "https://schema.org", "@type": "Article", "headline": headline, "description": desc,
        "image": f"{DOMAIN}/assets/og-image.png", "datePublished": C.CHECKED_ISO, "dateModified": C.CHECKED_ISO,
        "author": {"@type": "Person", "name": "Emils Ozols", "url": "https://ozols.dev"},
        "publisher": {"@type": "Organization", "name": "Scooch",
                      "logo": {"@type": "ImageObject", "url": f"{DOMAIN}/assets/icon-512.png"}},
        "mainEntityOfPage": canonical,
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                            for i, (n, u) in enumerate(crumbs)],
    }]
    if faq:
        blocks.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    if itemlist:
        # Names and store links only: no rating markup for third-party apps (self-serving review markup).
        blocks.append({"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": a["name"], "url": a["store"]}
            for i, a in enumerate(itemlist)]})
    return "\n".join(ld(b) for b in blocks)


def price_card(a):
    """The card's price box: the free version, a year, and a one-time unlock, each with the same marks and
    "× ours" badges as the tables; the full plan list below as fine print."""
    tier, tier_note = C.FREE_TIER[a["key"]]
    if a["key"] in C.FREE_TILE:
        free_value, free_unit = C.FREE_TILE[a["key"]]
    else:
        free_value, free_unit = ("Free" if tier in ("free", "limited") else "Not tested" if tier == "untested" else "None"), tier_note
    tiles = [("Free version", free_value, free_unit, tier if tier != "untested" else "", tier_mark(tier), "")]
    if a["year"] and _cheapest(a["year"]) is not None:
        value, _, extra = a["year"].partition(", ")
        tiles.append(("Per year", value, f"if subscribed, {extra}" if extra else "if subscribed",
                      "", "", times_badge(a, a["year"])))
    if m := _YES.match(a["once"]):
        once = a["once"][m.end():]
        amount = re.search(r"\$\d+(?:\.\d+)?", once)
        tiles.append((f'Pay once{fn("price") if a is US else ""}', amount.group(0) if amount else once,
                      "lifetime" if "lifetime" in once else "no subscription", "", tier_mark("free"),
                      times_badge(a, once)))
    elif _NO.match(a["once"]):
        tiles.append(("Pay once", "Not offered", "subscription only", "none", tier_mark("none"), ""))
    if len(tiles) == 1:
        # Neither a yearly nor a one-time price is stated: show the listed range rather than hide it.
        amounts = re.findall(r"\$\d+(?:\.\d+)?", a["price"])
        if amounts:
            lo = min(amounts, key=lambda x: float(x[1:]))
            hi = max(amounts, key=lambda x: float(x[1:]))
            tiles.append(("Paid plans", f"{lo} to {hi}", "lengths not listed", "", "", ""))
    tile_html = "".join(
        f'<div class="price-tile{" " + cls if cls else ""}"><span class="price-label">{mark}{label}</span>'
        f'<span class="price-amount">{html.escape(value)}{badge}</span><span class="price-unit">{html.escape(unit)}</span></div>'
        for label, value, unit, cls, mark, badge in tiles)
    note = re.sub(r"^Free( download| with limits| version[^.]*| with a sign-up[^.]*)?[.;] ?", "", a["price"])
    note = note[0].upper() + note[1:] if note else ""
    return (f'<div class="price-card{" ours" if a is US else ""}"><div class="price-tiles">{tile_html}</div>'
            + (f'<p class="price-note">{html.escape(note)}{fn("price")}</p>' if a is not US and note else "")
            + "</div>")


def _ours(a):
    return ' class="ours"' if a is US else ""


FLIP_ROWS = [
    ("Best for", lambda a: html.escape(a["best_for"])),
    ("US rating (average)", rating_cell),
    (f'Plan without paying{fn("test")}', free_cell),
    (f'Pay once, no subscription{fn("price")}', once_cell),
    (f'Cost for one year if subscribed{fn("price")}', year_cell),
    (f'Warns when furniture does not fit{fn("test")}', lambda a: mark_cell(a["fit"])),
    (f'Furniture at sizes you type{fn("listing")}', lambda a: mark_cell(a["sizes"])),
    (f'3D view{fn("listing")}', lambda a: mark_cell(a["three_d"])),
    (f'Scans the room with the camera{fn("listing")}', lambda a: mark_cell(a["scan"])),
    (f'No account needed{fn("test")}', lambda a: mark_cell(a["account"])),
    (f'No ads{fn("test")}', lambda a: mark_cell(a["ads"])),
    ("No tracking (App Store privacy label)", lambda a: mark_cell(a["privacy"])),
    ("Languages", lang_cell),
    ("Last update", update_cell),
    ("Get it", download_cell),
]
VERSIONS = ", ".join(f'{a["name"]} {a["version"]}' for a in C.APPS)

# ---- the roundup ----
ROUNDUP_TITLE = f"Best Room Planner Apps for iPhone (2026): {len(C.APPS)} Compared"
ROUNDUP_META = ("Nine iPhone room planner apps, tested side by side: US prices, free versions, whether each warns "
                "when furniture does not fit, pros and cons. October 2026.")
heads = "".join(
    f'<th scope="col"{_ours(a)}><a class="app-head" href="#{a["key"]}">{app_icon(a)}<span>{i + 1}. '
    f'{html.escape(a["name"])}</span></a></th>' for i, a in enumerate(C.APPS))
rows = "\n".join(f'      <tr><th scope="row">{label}</th>' + "".join(f"<td{_ours(a)}>{cell(a)}</td>" for a in C.APPS)
                 + "</tr>" for label, cell in FLIP_ROWS)
picks = "\n".join(f"    <li><strong>{html.escape(k)}:</strong> {html.escape(v)}</li>" for k, v in C.PICKS)
cards = []
for i, a in enumerate(C.APPS):
    vs = f' · <a href="{VS_URL(a["key"])}">Full comparison</a>' if a["vs"] else ""
    pic = our_shot("scooch") if a is US else their_shot(a, "plan")  # a plan in the app, never a wall or paywall
    cards.append(f"""<section class="app-card" id="{a['key']}">
  <h2 class="app-title">{app_icon(a, 44)}<span>{i + 1}. {html.escape(a['name'])}</span></h2>
  <p class="app-meta">By {html.escape(a['developer'])} · Best for: {html.escape(a['best_for'])} · {a['rating']}★ average US rating</p>
  <p>{html.escape(a['summary'])}</p>
  <div class="app-card-body{' with-shot' if pic else ''}">
  {pic}
  <div class="card-side">
  <div class="pros-cons">
    <div><h3>Pros</h3><ul>
{li(a['pros'])}
    </ul></div>
    <div><h3>Cons</h3><ul>
{li(a['cons'])}
    </ul></div>
  </div>
  {price_card(a)}
  <p class="checked">{other_link(a)}{vs}</p>
  </div>
  </div>
</section>""")

roundup_body = f"""<article class="article compare">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> › Compare</nav>
  <h1>{ROUNDUP_TITLE}</h1>
  <p class="lede">There is no single best room planner, because people want different things from one. Some want to see a room in 3D, some need to scan it for work, some just need to know whether the sofa fits. Here are {len(C.APPS)} iPhone room planners, what each does best, and where each falls short. One question runs through all of them, and we tested it in each app we could open: when a piece does not fit, does the app tell you?{fn("about")}</p>
  <div class="table-wrap">
    <table class="compare-table flip">
      <thead><tr><th scope="col"><span class="sr-only">Feature</span></th>{heads}</tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </div>
  <p class="table-note">Scroll sideways for all {len(C.APPS)} apps.</p>
  <h2>Quick picks</h2>
  <ul class="picks">
{picks}
  </ul>
{"".join(cards)}
{faq_html(C.ROUNDUP_FAQ)}
{cta_html("Check what fits before you buy", "Rooms at their real size, furniture at real sizes, and a red outline when something does not fit. $9.99 once.", CT_COMPARE)}
  <div class="related">
    <h2>One-to-one comparisons</h2>
    <ul>
{chr(10).join(f'      <li><a href="{VS_URL(a["key"])}">{html.escape(C.VERSUS[a["key"]]["label"])}</a></li>' for a in C.APPS if a["vs"])}
    </ul>
    <p><a href="/guides/">Room planning guides</a></p>
  </div>
  {footnotes(" Scooch is listed first because it is ours; the rest are in order of their number of US ratings. Versions compared: " + VERSIONS + ".")}
</article>"""
canonical = f"{DOMAIN}/compare/"
write("compare/index.html",
      page(ROUNDUP_TITLE, ROUNDUP_META, canonical, roundup_body, CT_COMPARE,
           compare_jsonld(ROUNDUP_TITLE, ROUNDUP_META, canonical, [("Home", f"{DOMAIN}/"), ("Compare", canonical)],
                          faq=C.ROUNDUP_FAQ, itemlist=C.APPS)))

# ---- one page per competitor ----
VS_ROWS = [(label, cell) for label, cell in FLIP_ROWS if not label.startswith("Best for")]


def blocks(items):
    return "\n".join(f"  <h3>{html.escape(h)}</h3>\n  <p>{html.escape(p_)}</p>" for h, p_ in items)


for a in C.APPS:
    if not a["vs"]:
        continue
    v = C.VERSUS[a["key"]]
    them = a["short"]
    canonical = f"{DOMAIN}{VS_URL(a['key'])}"
    trs = "\n".join(
        f'      <tr><th scope="row">{label}</th><td>{cell(a)}</td><td>{cell(US)}</td></tr>'
        for label, cell in [("Best for", lambda x: html.escape(x["best_for"]))] + VS_ROWS)
    reviews = ""
    if v["reviews"]:
        reviews = (f'<h2 class="app-title">{app_icon(a, 32)}<span>What recent reviews of {html.escape(them)} mention</span></h2>\n'
                   f"  <p>From the {a['reviews_n']} most recent US App Store reviews of {html.escape(them)}, read on {C.CHECKED}. "
                   "These are individual experiences, not tests we ran, but these themes came up more than once:</p>\n"
                   f"  <ul>\n{li(v['reviews'])}\n  </ul>")
    others = "\n".join(f'      <li><a href="{VS_URL(b["key"])}">{html.escape(C.VERSUS[b["key"]]["label"])}</a></li>'
                       for b in C.APPS if b["vs"] and b is not a)
    body = f"""<article class="article compare">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/compare/">Compare</a> › {html.escape(v['label'])}</nav>
  <h1>{html.escape(v['h1'])}</h1>
  <p class="lede">{html.escape(v['lede'])}{fn("about")}</p>
{maker_note(v)}
  <div class="quick-answer"><p><strong>Pick {html.escape(them)}</strong> if {html.escape(v['pick_them'])}<br><strong>Pick Scooch</strong> if {html.escape(v['pick_us'])}</p></div>
  <div class="table-wrap">
    <table class="compare-table vs">
      <thead><tr><th></th><th><span class="app-head row">{app_icon(a, 32)}<span>{html.escape(a['name'])}</span></span></th><th><span class="app-head row">{app_icon(US, 32)}<span>Scooch</span></span></th></tr></thead>
      <tbody>
{trs}
      </tbody>
    </table>
  </div>
  <h2 class="app-title">{app_icon(a, 32)}<span>Where {html.escape(them)} is stronger</span></h2>
{blocks(v['them_stronger'])}
  <h2 class="app-title">{app_icon(US, 32)}<span>Where Scooch is stronger</span></h2>
{blocks(v['us_stronger'])}
  <div class="app-card-body with-shot about-us">
  {our_shot(a['key'])}
  <div class="card-side"><div class="about-box">
    <h3>About Scooch</h3>
    <p>A 2D room planner for checking that furniture fits, before anything heavy moves.</p>
    <ul>
{li(C.ABOUT_US)}
    </ul>
    <p><a href="/#features">See all features</a></p>
  </div></div>
  </div>
  {side_by_side(a)}
  {tested(a)}
  <h2 class="app-title">{app_icon(US, 32)}<span>What Scooch does not do</span></h2>
  <ul>
{we_dont(v)}
  </ul>
  {reviews}
  <h2>Pricing</h2>
  <p>{html.escape(v['pricing'])}</p>
{faq_html(v['faq'])}
{cta_html("Try Scooch", "Rooms at their real size, furniture at real sizes, and a red outline when something does not fit. $9.99 once.", CT_COMPARE)}
  <div class="related">
    <h2>Other comparisons</h2>
    <ul>
{others}
    </ul>
    <p><a href="/compare/">All {len(C.APPS)} room planner apps compared</a></p>
  </div>
  {footnotes(f" Versions compared: {a['name']} {a['version']}, Scooch {US['version']}.")}
</article>"""
    write(VS_URL(a["key"]).strip("/") + "/index.html",
          page(v["title"], v["meta"], canonical, body, CT_COMPARE,
               compare_jsonld(v["h1"], v["meta"], canonical,
                              [("Home", f"{DOMAIN}/"), ("Compare", f"{DOMAIN}/compare/"), (v["label"], canonical)],
                              faq=v["faq"])))
if MISSING_SHOTS:
    print(f"competitor screenshots not taken yet ({len(MISSING_SHOTS)}): " + ", ".join(sorted(MISSING_SHOTS)))


# =========================================================================================
# 404, SITEMAP, ROBOTS, CNAME
# =========================================================================================
e404_body = """<article class="article" style="text-align:center; padding-top: 70px; padding-bottom: 90px;">
  <h1>404: this page did not fit</h1>
  <p class="lede">It does not exist, or it moved.</p>
  <div class="cta-row" style="justify-content: center;"><a class="btn-secondary" href="/">Back to the homepage</a><a class="btn-secondary" href="/guides/">Browse the guides</a></div>
</article>"""
write("404.html", page("Page Not Found | Scooch",
                       "That page does not exist. Head back to the Scooch homepage or browse the room planning guides.",
                       f"{DOMAIN}/404.html", e404_body))

urls = ([f"{DOMAIN}/", f"{DOMAIN}{CALC}", f"{DOMAIN}/guides/"]
        + [f"{DOMAIN}/guides/{p['slug']}/" for p in PAGES]
        + [f"{DOMAIN}/{lp['slug']}/" for lp in LEGAL])
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
sitemap += [f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls]
sitemap += [f"  <url><loc>{u}</loc><lastmod>{C.CHECKED_ISO}</lastmod></url>" for u in COMPARE_URLS]
sitemap.append("</urlset>")
write("sitemap.xml", "\n".join(sitemap) + "\n")
write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
write("CNAME", "getscooch.com\n")
print(f"{len(urls) + len(COMPARE_URLS)} urls in the sitemap")

# ---------- WebP fallback (2026-10-30) ----------
# Some company networks refuse image/webp: every WebP gets a PNG twin and every <img> an onerror
# that swaps it in. Runs last, over generated and hand-written pages alike (_gen/webp_fallback.py).
import webp_fallback  # noqa: E402
webp_fallback.run()
