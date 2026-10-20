"""Comparison pages: one dataset, rendered by build.py into /compare/ (the roundup) and
/compare/scooch-vs-<key>/ (one page per competitor). Same shape and house rules as
alarmclockplanner.com's /compare/ (AlarmPlanner website/_gen/compare_data.py, 2026-10-20).

House rules (Holocron brand.md, decision 2026-10-20):
- Every fact about another app comes from its US App Store listing, In-App Purchases list,
  privacy label or public US reviews, and the page says when it was checked (CHECKED).
  Re-check before changing a number, never from memory (compare_fetch.py re-takes the snapshot).
- Review complaints are paraphrased and attributed to "recent reviews", never quoted at length.
- Every page says who the other app suits better. We list our own cons.
- Screenshots of other apps only when we captured them ourselves; none so far.
- No "best rated": 5.0 from 2 US ratings is not comparable to 4.7 from 41,000. Tables show the
  average only; counts stay in the snapshot.
- "Not described on the listing" (a dash) where a listing is silent, never "No".
- Only features in the LIVE Scooch: 1.0.2 (37 catalogue pieces, 26 themes, PNG/PDF export, iCloud
  sync between your own devices, iPhone and iPad, 16 languages, iOS 26 or later).

Version, update date, rating and language count are NOT typed here: build.py reads them from
compare_snapshot.json, so a re-fetch updates every page.
"""

CHECKED = "20 October 2026"
CHECKED_ISO = "2026-10-20"
OUR_ONCE = 9.99   # the price every "cost for the first year" is held against

# Scooch first (ours, and the page says so); the rest in order of their US rating count, a public
# number, not our preference.
APPS = [
    dict(
        key="scooch", short="Scooch", name="Scooch", developer="Emils Ozols", store_id="6799503727",
        best_for="Checking that furniture fits a room before you buy or move it",
        summary=("A 2D room planner built around one question: will it fit? You type or drag your rooms to "
                 "their real measurements, place furniture at real sizes, and anything that overlaps another "
                 "piece or sticks out of the room is highlighted before you lift it."),
        pros=["Warns when furniture overlaps or sticks out of the room",
              "Every piece resizes to the centimetre, and you can draw your own",
              "$9.99 once: no subscription, no account",
              "iPhone and iPad, synced through your own iCloud"],
        cons=["Rooms are rectangles: no angled or curved walls",
              "37 generic pieces: no brand catalogue or decor",
              "Needs iOS 26 or later"],
        price="Free download; planning needs the one-time unlock, $9.99",
        once="Yes, $9.99", year=None,
        fit="Yes, overlaps and pieces outside the room are highlighted",
        sizes="Yes, to the centimetre, plus pieces you draw",
        three_d="No", scan="No, you measure and type",
        privacy="Yes, no data linked to you",
        vs=False,
    ),
    dict(
        key="home-design-3d", short="Home Design 3D", name="Home Design 3D", developer="Home Design 3D srl",
        store_id="463768717",
        best_for="Designing a whole house over several floors, in 3D",
        summary=("A house designer: draw floor plans in 2D and walk through them in 3D, over unlimited floors, "
                 "with thousands of items, photorealistic rendering, VR export and blueprint import. Premium "
                 "features are a subscription."),
        pros=["Multi-storey houses with adjustable walls",
              "Thousands of items with sizes you can change",
              "3D walkthrough, renders and VR export",
              "Import a blueprint and trace it"],
        cons=["Premium is a subscription",
              "Recent reviews describe one-time purchases moved to subscriptions"],
        price="Free download. Weekly premium $4.99, monthly plans $12.99 to $22.99, yearly plans $44.99 to $79.99",
        once="No, subscription only", year="$44.99 to $79.99",
        fit="Not described on the listing", sizes="Yes, per its listing",
        three_d="Yes", scan="Not described on the listing",
        privacy="No, declares data used to track you",
        vs=True,
    ),
    dict(
        key="keyplan-3d", short="Keyplan 3D", name="Keyplan 3D Lite", developer="Quasarts LLC", store_id="983655856",
        best_for="Building a home's shape and decorating it in 2D and 3D",
        summary=("A home builder and interior designer: draw walls in any shape, place furniture, windows and "
                 "doors in 2D or 3D, and paint and decorate any surface. 350+ objects are free and projects "
                 "sync through iCloud."),
        pros=["Walls in any shape, in 2D or 3D",
              "350+ free objects, paints and materials",
              "A one-time $5.99 Standard upgrade",
              "iCloud sync between iPhone and iPad"],
        cons=["Recent reviews describe purchases needed for more rooms, floors and textures",
              "Object packs are sold separately"],
        price="Free download. Standard version $5.99 once; object packs $1.99 to $2.99",
        once="Yes, $5.99", year=None,
        fit="Not described on the listing", sizes="Not described on the listing",
        three_d="Yes", scan="Not described on the listing",
        privacy="Yes, but collects data linked to you",
        vs=True,
    ),
    dict(
        key="home-planner-ai", short="Home Planner AI", name="Home Planner AI", developer="Room Planner Ltd",
        store_id="1076159017",
        best_for="3D room design with a scanner, measure tools and renders",
        summary=("A 2D and 3D design app with a built-in 3D scanner, a digital tape measure, AI design and "
                 "realistic renders. Premium unlocks the full catalogue, unlimited projects, renders, the "
                 "scanner and the measure tools."),
        pros=["Built-in 3D scanner and measure tools",
              "2D and 3D, with realistic renders",
              "AI design suggestions",
              "30 languages, the most here"],
        cons=["Scanner, measure tools and full catalogue are premium",
              "Ten different purchases make the real price hard to read"],
        price=("Free download. Purchases from $5.99 to $74.99, 6-month plans at $29.99 and $34.99, "
               "Weekly Business $17.99"),
        once="Not stated on the listing", year="Not stated on the listing",
        fit="Not described on the listing", sizes="Not described on the listing",
        three_d="Yes", scan="Yes, built-in 3D scanner",
        privacy="Yes, no data linked to you",
        vs=True,
    ),
    dict(
        key="planner-5d", short="Planner 5D", name="Planner 5D", developer="Planner5D, UAB", store_id="606173978",
        best_for="3D interior design with a large furniture catalogue",
        summary=("A 2D and 3D home design app with over 8,400 furniture and decor items with premium, "
                 "photo-like renders, AI design and 3D capture with the phone's camera. The free version has "
                 "150+ items and no furniture customization."),
        pros=["2D and 3D, with photo-like renders",
              "Over 8,400 items with premium",
              "Camera capture and AI design",
              "Apple Pencil and Vision Pro support"],
        cons=["Resizing furniture needs premium",
              "Recent reviews describe charges after free trials"],
        price=("Free with limits. Subscriptions from $7.99 a week, $19.99 a month, $29.99 to $119.99 a year; "
               "full catalogue $6.99 for 30 days or $15.99 a year"),
        once="No, subscription only", year="$29.99 to $119.99",
        fit="Not described on the listing",
        sizes="Yes, with premium (its free version has no furniture customization)",
        three_d="Yes", scan="Yes, with the camera",
        privacy="No, declares data used to track you",
        vs=True,
    ),
    dict(
        key="magicplan", short="magicplan", name="magicplan", developer="Technologies magicplan Inc.",
        store_id="427424432",
        best_for="Professionals capturing existing rooms for reports and estimates",
        summary=("A floor plan tool for remodelers, restoration and insurance claims work. You capture a room "
                 "with the phone's camera, then add photos, notes, checklists, 360° panoramas, reports and "
                 "estimates to the plan. Its listing names Xactimate and CoreLogic integrations."),
        pros=["Builds the plan from the phone's camera",
              "Photos, notes, forms and estimates on the plan",
              "Xactimate and CoreLogic integrations"],
        cons=["Priced for businesses: yearly plans from $129.99",
              "Recent reviews describe scans that miss walls or closets"],
        price=("Free download. Sketch Plan $12.99 a month or $129.99 a year, Report Plan $39.99 or $399.99, "
               "Estimate Plan $89.99 or $899.99"),
        once="No, subscription only", year="$129.99 to $899.99",
        fit="Not described on the listing", sizes="Not described on the listing",
        three_d="Not described on the listing", scan="Yes, with the camera",
        privacy="Yes, but collects data linked to you",
        vs=True,
    ),
    dict(
        key="live-home-3d", short="Live Home 3D", name="Live Home 3D", developer="Belight Software, ltd",
        store_id="1066784070",
        best_for="Detailed 3D house and interior design with realistic renders",
        summary=("A full home, interior and landscape design app: 2D plans, 3D walkthroughs, 5,000+ items and "
                 "3,000+ materials, a LiDAR room scanner, AR, renders and video. Projects move between iPhone, "
                 "iPad, Vision Pro, Mac and Windows."),
        pros=["5,000+ items and 3,000+ materials",
              "LiDAR room scan and AR",
              "Renders, flyover videos and panoramas",
              "Lifetime upgrades, and Mac and Windows versions"],
        cons=["The free version watermarks exports and keeps one project",
              "The lifetime Standard upgrade is $59.99"],
        price=("Free version with watermarked exports and one project. Standard $5.99 a month, $19.99 a year or "
               "$59.99 lifetime; Pro $14.99 a month, $39.99 a year or $129.99 lifetime"),
        once="Yes, $59.99 lifetime", year="$19.99 to $39.99",
        fit="Not described on the listing", sizes="Not described on the listing",
        three_d="Yes", scan="Yes, with LiDAR",
        privacy="Yes, no data linked to you",
        vs=True,
    ),
    dict(
        key="draft-paper", short="Draft Paper", name="Draft Paper", developer="Giles Goddard", store_id="911636555",
        best_for="Quick, precise 2D drawings and DXF export",
        summary=("A simple 2D drafting app: lines, rectangles, ellipses, text and measurements on up to 10 "
                 "layers, exported as PDF, JPEG or DXF. Made by one developer, and $9.99 once, the same as "
                 "Scooch."),
        pros=["$9.99 once, no subscription",
              "Exports PDF, JPEG and DXF",
              "Layers and Apple Pencil support",
              "Runs on iOS 15 or later"],
        cons=["No furniture: you draw every shape yourself",
              "English only"],
        price="Free download. All Features $9.99 once",
        once="Yes, $9.99", year=None,
        fit="Not described on the listing", sizes="No, you draw shapes to scale",
        three_d="No", scan="No",
        privacy="Yes, no data linked to you",
        vs=True,
    ),
    dict(
        key="drawplan", short="DrawPlan", name="DrawPlan", developer="Fleet Investments LLC", store_id="1451755778",
        best_for="To-scale 2D plans for trades and real estate, with tracing",
        summary=("A 2D floor plan app for quick sketches or to-scale drawings with automatic dimensions. You can "
                 "import an image or plan and trace it, save your own objects, and ask its AI to help draw. "
                 "Premium is a subscription."),
        pros=["Free sketching or to-scale drawing",
              "Trace over an imported plan or photo",
              "AI-assisted drawing",
              "Runs on iOS 13 or later"],
        cons=["Sync and clean exports need a subscription",
              "Recent reviews describe paying to reopen saved plans"],
        price=("Free download. $2.99 a month or $29.99 a year; Plus $4.99 or $49.99; Pro $9.99 or $99.99; "
               "AI credits $4.99 to $19.99"),
        once="No, subscription only", year="$29.99 to $99.99",
        fit="Not described on the listing", sizes="Not described on the listing",
        three_d="Not described on the listing", scan="Not described on the listing",
        privacy="Yes, no data linked to you",
        vs=True,
    ),
]

# Under the summary table. Each names whichever app the data says wins, not always us.
PICKS = [
    ("Lowest one-time price", "Keyplan 3D Lite, $5.99 for its Standard version; Scooch and Draft Paper are $9.99"),
    ("Checks that furniture fits", "Scooch"),
    ("For 3D design and renders", "Planner 5D or Live Home 3D"),
    ("For scanning a room with the camera", "magicplan, Home Planner AI, or Live Home 3D with LiDAR"),
    ("For drafting anything in 2D", "Draft Paper"),
    ("For whole houses over several floors", "Home Design 3D"),
]

# Our app in brief, for the "About Scooch" box on each head-to-head. Shipped (1.0.2) only.
ABOUT_US = [
    "Rooms drawn at their real measurements, joined into an L or a U",
    "37 pieces at real sizes, each resized to the centimetre",
    "Furniture you draw yourself, at any size",
    "Overlaps and pieces outside the room highlighted",
    "Door swings, drawers and sofa beds shown with the space they need",
    "PNG and PDF export, metric or imperial, 26 themes",
    "iPhone and iPad, synced through your own iCloud",
]

# Our screenshot on each head-to-head and on our roundup card: (file stem, alt text).
OUR_SHOT = {
    "scooch": ("shot-clash", "A 360 cm sofa flagged red in Scooch because it does not fit the room"),
    "magicplan": ("shot-plan", "A two-room flat drawn to scale in Scooch, every wall measured"),
    "planner-5d": ("shot-clash", "A 360 cm sofa flagged red in Scooch because it does not fit the room"),
    "home-planner-ai": ("shot-furniture", "The Scooch furniture list with each piece's default size"),
    "home-design-3d": ("shot-projections", "Furniture doors, drawers and a sofa bed showing the space they need in Scooch"),
    "keyplan-3d": ("shot-clash", "A 360 cm sofa flagged red in Scooch because it does not fit the room"),
    "live-home-3d": ("shot-projections", "Furniture doors, drawers and a sofa bed showing the space they need in Scooch"),
    "draft-paper": ("shot-draw", "Drawing a dining table at 140 by 90 cm in Scooch"),
    "drawplan": ("shot-plans", "Three plans in Scooch: a flat, a studio and an office"),
}

_NO_FIT = ("Its US App Store listing does not describe that, as of 20 October 2026. Scooch highlights any "
           "piece that overlaps another or sticks out of the room.")

# One page per competitor. Sections render in a fixed order (see build.py): quick answer, table,
# where they are stronger, where we are stronger, about us, what we do not do, what reviews
# mention, pricing, questions. Write the "they are stronger" part first and mean it.
VERSUS = {
"home-design-3d": dict(
    title="Home Design 3D Alternative (2026): Home Design 3D vs Scooch",
    meta=("Looking for a Home Design 3D alternative without a subscription? Scooch checks what fits at exact "
          "sizes for $9.99 once. Side by side, October 2026."),
    h1="Home Design 3D alternative: Home Design 3D vs Scooch",
    label="Scooch vs Home Design 3D",
    lede=("Home Design 3D plans whole houses in 3D. Scooch is for the room you already have, and whether the "
          "furniture you want fits in it."),
    pick_them="you are planning a house or a renovation over several floors and want to see it in 3D.",
    pick_us="you have the room already and want to know whether the furniture fits, for one price.",
    them_stronger=[
        ("Whole houses", "Several floors, adjustable wall thickness, height and angles, roofs, and a 3D walkthrough with VR export."),
        ("Thousands of items", "Far more than Scooch's 37 generic pieces, with sizes you can change, per its listing."),
        ("Blueprints", "Import an existing plan and draw over it."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room. Home Design 3D's listing does not describe this."),
        ("One price", "$9.99 once. Home Design 3D is a subscription, and recent reviews describe earlier one-time purchases moving to it."),
        ("No tracking", "Home Design 3D's App Store privacy label declares data used to track you; Scooch's declares none."),
    ],
    reviews=[
        "long-time users who bought the one-time Gold edition or content packs and lost access after the move to subscriptions",
        "most items and tools locked, and ads that interrupt projects",
        "crashes after recent updates, including projects that no longer open",
    ],
    pricing=("Home Design 3D is free to download; premium is a subscription at $4.99 a week, $12.99 to $22.99 a "
             "month or $44.99 to $79.99 a year (US). Scooch is a free download; planning needs a one-time $9.99 unlock."),
    faq=[
        ("Does Scooch do several floors or 3D?", "No. Scooch plans rooms in 2D. You can keep several plans, but not floors stacked in 3D."),
        ("Does Home Design 3D warn when furniture will not fit?", _NO_FIT),
        ("Is either a one-time purchase?", "Scooch is: $9.99 once. Home Design 3D's US purchase list shows only weekly, monthly and yearly plans."),
    ],
),
"keyplan-3d": dict(
    title="Keyplan 3D Alternative (2026): Keyplan 3D Lite vs Scooch",
    meta=("Looking for a Keyplan 3D alternative? Scooch checks what fits at exact sizes and warns when it does "
          "not. Side by side, checked October 2026."),
    h1="Keyplan 3D alternative: Keyplan 3D Lite vs Scooch",
    label="Scooch vs Keyplan 3D Lite",
    lede=("Keyplan 3D builds a home's shape and decorates it in 3D, at a low one-time price. Scooch stays in 2D "
          "and checks whether furniture at real sizes fits."),
    pick_them="you want to build a home's shape freely and decorate it in 3D, at the lowest one-time price here.",
    pick_us="you want exact furniture sizes and a warning when something does not fit.",
    them_stronger=[
        ("Any shape", "Walls go wherever you draw them; Scooch's rooms are rectangles you join into an L or a U."),
        ("3D and decoration", "Edit in 3D and paint or texture any surface."),
        ("Price", "Its Standard version is $5.99 once, less than Scooch's $9.99."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room. Keyplan's listing does not describe this."),
        ("Exact furniture sizes", "Every piece resizes to the centimetre, and you can draw your own pieces at any size."),
        ("Languages", "16 languages to Keyplan's 10."),
    ],
    reviews=[
        "the Lite version asking for purchases to add more rooms, floors or paint textures",
        "plans lost when moving to a new phone",
        "spaces that are hard to size precisely",
    ],
    pricing=("Keyplan 3D Lite is free to download; its Standard version is $5.99 once and object packs cost $1.99 "
             "to $2.99 each (US). Scooch is a free download; planning needs a one-time $9.99 unlock. Neither has a subscription."),
    faq=[
        ("Which is cheaper?", "Keyplan 3D Lite: its Standard version is $5.99 once, against Scooch's $9.99. Neither has a subscription."),
        ("Does Keyplan 3D warn when furniture will not fit?", _NO_FIT),
        ("Can Scooch draw angled walls?", "No. Scooch rooms are rectangles; you build an L or a U by joining rooms."),
    ],
),
"home-planner-ai": dict(
    title="Home Planner AI Alternative (2026): Scooch Compared",
    meta=("Looking for a Home Planner AI alternative? Scooch checks what fits at exact sizes for one price, "
          "$9.99 once. Side by side, October 2026."),
    h1="Home Planner AI alternative: Home Planner AI vs Scooch",
    label="Scooch vs Home Planner AI",
    lede=("Home Planner AI scans and designs rooms in 3D. Scooch skips the scan and the 3D, and checks whether "
          "furniture at real sizes fits the room you measured."),
    pick_them="you want to scan a room and design it in 3D with renders.",
    pick_us="you want to check what fits at exact sizes, for one clear price.",
    them_stronger=[
        ("It scans and measures", "A built-in 3D scanner and a digital tape measure. With Scooch you measure the room yourself."),
        ("3D and renders", "Layouts in 2D and 3D with realistic renders; Scooch is 2D only."),
        ("Languages", "30 languages, the most of any app compared here; Scooch has 16."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room. Home Planner AI's listing does not describe this."),
        ("Typed sizes from the start", "Rooms and furniture take the exact size you type. A recent Home Planner AI review says typing a room's size needed the subscription."),
        ("One clear price", "$9.99 once, against a purchase list of ten items and subscriptions."),
    ],
    reviews=[
        "a free version too limited to use, including typing a room's size",
        "freezing, crashes and slow loading",
        "controls that are confusing or too small to select, especially on iPad",
        "a subscription that was hard to cancel",
    ],
    pricing=("Home Planner AI is free to download; its US purchase list shows Interior Design $5.99, Floor plan "
             "creator from $6.99 to $74.99, Architecture $14.99, Design & Room maker $49.99, 6-month subscriptions "
             "at $29.99 and $34.99, and Weekly Business at $17.99, without saying which are one-time. Scooch is a "
             "free download; planning needs a one-time $9.99 unlock."),
    faq=[
        ("Can Scooch scan a room?", "No. You measure the room and type or drag its size. Home Planner AI has a built-in 3D scanner."),
        ("Does Home Planner AI warn when furniture will not fit?", _NO_FIT),
        ("How much does each cost?", "Scooch: $9.99 once. Home Planner AI lists purchases from $5.99 to $74.99 and subscriptions; see Pricing above."),
    ],
),
"planner-5d": dict(
    title="Planner 5D Alternative (2026): Planner 5D vs Scooch",
    meta=("Looking for a Planner 5D alternative? Scooch checks what fits at exact sizes, for $9.99 once with no "
          "subscription. Side by side, October 2026."),
    h1="Planner 5D alternative: Planner 5D vs Scooch",
    label="Scooch vs Planner 5D",
    lede=("Planner 5D is about seeing a room in 3D and styling it from a big catalogue. Scooch is 2D and answers "
          "one practical question: does the furniture fit?"),
    pick_them="you want to see the room in 3D, furnish it from thousands of items and render it.",
    pick_us="you need exact sizes and a clear answer on what fits, without a subscription.",
    them_stronger=[
        ("3D and renders", "Planner 5D switches between 2D and 3D and renders photo-like images. Scooch is 2D only."),
        ("A huge catalogue", "Over 8,400 furniture and decor items with premium, against Scooch's 37 generic pieces."),
        ("Camera capture and AI", "It can capture a room in 3D with the phone's camera and generate designs with AI."),
        ("More platforms and languages", "It runs across platforms and on Vision Pro, in 24 languages to Scooch's 16."),
    ],
    us_stronger=[
        ("Exact sizes without a subscription", "Every Scooch piece resizes to the centimetre with the one-time unlock. Planner 5D's listing says its free version has no furniture customization."),
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room. Planner 5D's listing does not describe this."),
        ("One price", "$9.99 once, against subscriptions from $7.99 a week."),
        ("No tracking", "Planner 5D's App Store privacy label declares data used to track you; Scooch's declares none."),
    ],
    reviews=[
        "free trials that turned into charges reviewers did not expect, and refunds that were hard to get",
        "scans, downloads and other features that each ask for another purchase",
        "an app that feels confusing, slow or prone to freezing",
        "saved projects that reverted or partly disappeared",
    ],
    pricing=("Planner 5D is free with a limited catalogue; its US purchase list shows subscriptions from $7.99 a "
             "week and $19.99 a month to $29.99, $69.99 and $119.99 a year, plus full-catalogue access at $6.99 for "
             "30 days or $15.99 a year. Scooch is a free download; planning needs a one-time $9.99 unlock."),
    faq=[
        ("Is Planner 5D free?", "It is free to download with 150+ items and no furniture customization, per its listing; the full catalogue and resizing need a subscription."),
        ("Does Scooch work in 3D?", "No. Scooch is 2D. It shows real sizes, door swings and the space drawers and sofa beds need, but not a 3D view."),
        ("Which one tells me if a sofa will fit?", "Scooch highlights furniture that overlaps or sticks out of the room. Planner 5D's listing does not describe a check like that."),
    ],
),
"magicplan": dict(
    title="magicplan Alternative (2026): magicplan vs Scooch",
    meta=("Looking for a magicplan alternative for furniture? Scooch checks what fits at exact sizes for $9.99 "
          "once. Side by side, checked October 2026."),
    h1="magicplan alternative: magicplan vs Scooch",
    label="Scooch vs magicplan",
    lede=("magicplan measures rooms with the camera and turns them into plans, photos and estimates for jobs. "
          "Scooch starts from measurements you type and answers a narrower question: does the furniture fit?"),
    pick_them="you work in remodeling, restoration or insurance claims and need plans, photos and estimates from the camera.",
    pick_us="you are at home asking whether a sofa, bed or table will fit, and want one price instead of a plan.",
    them_stronger=[
        ("It measures for you", "magicplan builds the floor plan from the phone's camera. With Scooch you measure the room and type its size."),
        ("Made for jobs", "Photos, notes, forms, 360° panoramas, reports and estimates sit on the plan, and it connects to Xactimate and CoreLogic."),
        ("A long track record", "Years on the App Store and far more ratings than Scooch, which is new."),
    ],
    us_stronger=[
        ("Furniture that knows its size", "37 pieces at real sizes, each resized to the centimetre, plus pieces you draw yourself."),
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room. magicplan's listing does not describe this."),
        ("Price", "$9.99 once, against magicplan's plans from $12.99 a month or $129.99 a year."),
        ("Languages", "Scooch is in 16 languages; magicplan's listing names 5."),
    ],
    reviews=[
        "core features, extra plans and scanning that need a subscription, with pricing some found unclear",
        "scans that miss closets, walls or doors, or struggle with open-plan rooms and sloped ceilings",
        "projects that did not save, or disappeared after an update or an account change",
        "a steep learning curve for first-time users",
    ],
    pricing=("magicplan is free to download; its plans are Sketch at $12.99 a month or $129.99 a year, Report at "
             "$39.99 or $399.99, and Estimate at $89.99 or $899.99 (US). Scooch is a free download; planning needs "
             "a one-time $9.99 unlock, with no subscription."),
    faq=[
        ("Can Scooch scan a room like magicplan?", "No. Scooch has no camera or LiDAR scan: you measure the room and type or drag its size."),
        ("Does magicplan warn when furniture will not fit?", _NO_FIT),
        ("Which is cheaper?", "Scooch: $9.99 once. magicplan's plans start at $12.99 a month or $129.99 a year."),
    ],
),
"live-home-3d": dict(
    title="Live Home 3D Alternative (2026): Live Home 3D vs Scooch",
    meta=("Looking for a simpler Live Home 3D alternative? Scooch checks what fits at exact sizes for $9.99 once. "
          "Side by side, checked October 2026."),
    h1="Live Home 3D alternative: Live Home 3D vs Scooch",
    label="Scooch vs Live Home 3D",
    lede=("Live Home 3D is a full 3D design tool, from roofs to lighting. Scooch does one part of that job, "
          "checking whether furniture fits, for less."),
    pick_them="you want detailed 3D design, renders and video, on Apple devices and Windows.",
    pick_us="you only need to know whether your furniture fits, for $9.99 once.",
    them_stronger=[
        ("Full 3D design", "Walkthroughs, renders, flyover videos, roofs, terrain and lighting."),
        ("Scanning", "A LiDAR room scanner on devices that have the sensor; with Scooch you measure."),
        ("Catalogue and platforms", "5,000+ items and 3,000+ materials, and versions for Mac and Windows."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room. Live Home 3D's listing does not describe this."),
        ("Price", "Everything in Scooch is $9.99 once; Live Home 3D's Standard upgrade is $19.99 a year or $59.99 lifetime."),
        ("Languages", "16 languages to Live Home 3D's 11."),
    ],
    reviews=[
        "the one free project locked until paying",
        "purchases or projects not carrying across devices",
        "crashes on large models and slow loading",
        "little guidance on where to start",
    ],
    pricing=("Live Home 3D has a free version that watermarks exports and keeps one project at a time. Standard is "
             "$5.99 a month, $19.99 a year or $59.99 lifetime; Pro is $14.99 a month, $39.99 a year or $129.99 "
             "lifetime (US). Scooch is a free download; planning needs a one-time $9.99 unlock."),
    faq=[
        ("Is Live Home 3D free?", "There is a free version; per its listing, exports carry a watermark and only one project can be used at a time."),
        ("Can Scooch scan with LiDAR?", "No. You measure the room and type or drag its size."),
        ("Does Live Home 3D warn when furniture will not fit?", _NO_FIT),
    ],
),
"draft-paper": dict(
    title="Draft Paper Alternative (2026): Draft Paper vs Scooch",
    meta=("Looking for a Draft Paper alternative for furniture? Scooch has furniture at real sizes and warns "
          "when it does not fit. Same $9.99 once."),
    h1="Draft Paper alternative: Draft Paper vs Scooch",
    label="Scooch vs Draft Paper",
    lede=("Draft Paper and Scooch cost the same, $9.99 once, and both draw to scale. Draft Paper draws anything; "
          "Scooch knows what a room and a sofa are."),
    pick_them="you want a general drafting tool with layers and DXF export, on an older iPhone too.",
    pick_us="you want rooms and furniture that already know their sizes, and a warning when they do not fit.",
    them_stronger=[
        ("It draws anything", "Lines, shapes, text and measurements on up to 10 layers, not only rooms and furniture."),
        ("CAD export", "It exports DXF, so the drawing opens in CAD software."),
        ("Older iPhones", "It runs on iOS 15 or later; Scooch needs iOS 26."),
    ],
    us_stronger=[
        ("Furniture, ready made", "37 pieces at real sizes, each resized to the centimetre, instead of shapes you draw."),
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room."),
        ("Languages", "16 languages; Draft Paper's listing names English only."),
    ],
    reviews=[
        "a recent update (1.19.5) that changed scrolling and undo and made drawing harder",
        "crashes that lose minutes of work, including with Apple Pencil on iPad",
        "trouble switching between metric and imperial, or importing an image",
    ],
    pricing=("Draft Paper is free to download; All Features is $9.99 once (US). Scooch is a free download; "
             "planning needs a one-time $9.99 unlock. Neither has a subscription."),
    faq=[
        ("Do they cost the same?", "Yes: both are $9.99 once in the US, with no subscription."),
        ("Does Draft Paper have furniture?", "Its listing describes drawing tools (lines, rectangles, ellipses, text, measurements), not a furniture catalogue."),
        ("Can Scooch export DXF?", "No. Scooch exports PNG and PDF."),
    ],
),
"drawplan": dict(
    title="DrawPlan Alternative (2026): DrawPlan vs Scooch",
    meta=("Looking for a DrawPlan alternative without a subscription? Scooch keeps your plans and checks what "
          "fits, for $9.99 once. October 2026."),
    h1="DrawPlan alternative: DrawPlan vs Scooch",
    label="Scooch vs DrawPlan",
    lede=("DrawPlan is a 2D drawing tool for plans at work, with tracing and AI help. Scooch is a 2D planner for "
          "furnishing your own rooms."),
    pick_them="you draw plans for work and want to trace existing drawings.",
    pick_us="you are furnishing your own home and want to know what fits, without a subscription.",
    them_stronger=[
        ("Tracing", "Import a plan or photo and draw over it."),
        ("Drawing help", "Free sketching or to-scale drawing, plus AI that helps lay out the plan."),
        ("Older iPhones", "It runs on iOS 13 or later; Scooch needs iOS 26."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch highlights a piece that overlaps another or sticks out of the room. DrawPlan's listing does not describe this."),
        ("Your plans stay yours", "After the one-time unlock every plan opens, exports as PNG or PDF and syncs through your own iCloud. DrawPlan's listing puts sync and clean exports behind a subscription."),
        ("Languages", "16 languages; DrawPlan's listing names English only."),
    ],
    reviews=[
        "having to subscribe to open a plan they had already drawn and saved",
        "saved plans that would not open or disappeared after an update",
        "no way to enter exact wall lengths or keep the plan to scale",
    ],
    pricing=("DrawPlan is free to download; its plans are $2.99 a month or $29.99 a year, Plus $4.99 or $49.99, "
             "and Pro $9.99 or $99.99, with AI credits from $4.99 to $19.99 (US). Scooch is a free download; "
             "planning needs a one-time $9.99 unlock."),
    faq=[
        ("Is DrawPlan free?", "It is a free download; per its listing, cloud sync, high-resolution exports and exports without grids or watermarks need a subscription, from $2.99 a month or $29.99 a year (US)."),
        ("Can Scooch trace a plan I already have?", "No. Scooch has no image import; you type or drag the room's measurements."),
        ("Does DrawPlan warn when furniture will not fit?", _NO_FIT),
    ],
),
}

ROUNDUP_FAQ = [
    ("Which room planner app for iPhone is best?",
     "It depends on the job. To check that furniture fits, Scooch (our app). For 3D design and renders, Planner 5D "
     "or Live Home 3D. To scan a room for work, magicplan. For whole houses over several floors, Home Design 3D."),
    ("Which room planner apps have no subscription?",
     "From this list: Scooch and Draft Paper ($9.99 once) and Keyplan 3D Lite ($5.99 once for its Standard version). "
     "Live Home 3D sells lifetime upgrades as well as subscriptions."),
    ("Which app tells me if my furniture will fit?",
     "Scooch highlights furniture that overlaps another piece or sticks out of the room. As of 20 October 2026, none "
     "of the other eight apps' US App Store listings describe a check like that."),
    ("How were these apps chosen?",
     "From the top results for room and floor planner searches on the US App Store, keeping apps that plan rooms on "
     "iPhone and have an active listing. Facts come from each listing, purchase list, privacy label and recent public "
     "reviews, checked on 20 October 2026."),
]

# Guides that link into the comparisons from their text: {key} is a head-to-head, {all} the roundup.
GUIDE_COMPARE = {
    "how-to-measure-a-room-for-furniture": ("Measuring by hand is what Scooch expects. If you would rather scan, see "
        "how it compares with {magicplan}, which measures with the camera, or {all}."),
    "standard-sofa-dimensions": ("Planning where the sofa goes in an app? See how Scooch compares with {planner-5d} "
        "and {home-design-3d}, or {all}."),
    "corner-sofa-dimensions": ("Checking a corner sofa in an app? See how Scooch compares with {planner-5d} and "
        "{live-home-3d}, or {all}."),
    "bed-sizes-and-space-around-a-bed": ("Choosing an app to plan the bedroom? See how Scooch compares with "
        "{keyplan-3d} and {home-planner-ai}, or {all}."),
    "dining-table-clearance": ("Drawing the dining room to scale? See how Scooch compares with {draft-paper} and "
        "{drawplan}, or {all}."),
}
