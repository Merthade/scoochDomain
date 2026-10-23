"""Comparison pages: one dataset, rendered by build.py into /compare/ (the roundup) and
/compare/scooch-vs-<key>/ (one page per competitor). Same shape and house rules as
alarmclockplanner.com's /compare/ (AlarmPlanner website/_gen/compare_data.py, 2026-10-23).

House rules (Holocron brand.md, decision 2026-10-20):
- Every fact about another app comes from its US App Store listing, In-App Purchases list,
  privacy label or public US reviews, and the page says when it was checked (CHECKED), or from
  using the app ourselves (TESTED, with the device and the date). Re-check before changing a
  number, never from memory (compare_fetch.py re-takes the snapshot).
- What we saw beats what a listing declares. First-hand notes: the app repo's
  Marketing/competitors/FINDINGS.md (Holocron projects/archive/scooch/competitor-device-test-2026-10.md).
- Review complaints are paraphrased and attributed to "recent reviews", never quoted at length.
- Every page says who the other app suits better. We list our own cons.
- Screenshots of other apps only when we captured them ourselves (THEIR_SHOTS), captioned with the
  app, its version and the capture date. No "best rated": 5.0 from 2 US ratings is not comparable
  to 4.7 from 41,000. Tables show the average only; counts stay in the snapshot.
- "Not described on the listing" (a dash) where a listing is silent, never "No".
- All prices in US dollars from the US purchase list. A plan's length comes from the app's own
  upgrade screen (ours was an EU account, so its euro amounts never reach the page), and a US price
  is used only where it clearly matches that plan.
- Only features in the LIVE Scooch: 1.0.2 (37 catalogue pieces, 26 themes, PNG/PDF export, iCloud
  sync between your own devices, iPhone and iPad, 16 languages, iOS 26 or later).

Version, update date, rating and language count are NOT typed here: build.py reads them from
compare_snapshot.json, so a re-fetch updates every page.
"""

CHECKED = "23 October 2026"
CHECKED_ISO = "2026-10-23"
TESTED_WHEN = "23 October 2026"
TESTED_ON = "an iPhone 11 Pro Max with iOS 27.0.1, on an EU App Store account"
OUR_ONCE = 9.99   # every "× ours" badge holds a price against Scooch's one-time unlock

# Scooch first (ours, and the page says so); the rest in order of their US rating count, a public
# number, not our preference.
# Short cells for the tables: once / year (prices), fit (does it warn, as seen in our test), sizes,
# three_d, scan (as each listing describes), ads and account (as seen in our test), privacy (label).
APPS = [
    dict(
        key="scooch", short="Scooch", name="Scooch", developer="Emils Ozols", store_id="6799503727",
        best_for="Checking that furniture fits a room before you buy or move it",
        summary=("A 2D room planner built around one question: will it fit? You type or drag your rooms to "
                 "their real measurements, place furniture at real sizes, and anything that overlaps another "
                 "piece or sticks out of the room is outlined in red before you lift it. It also draws the "
                 "space each wardrobe door, drawer and sofa bed needs to open."),
        pros=["Turns furniture red when it does not fit",
              "Shows door swings and drawer pull-outs",
              "Everyday pieces, or draw your own",
              "$9.99 once, no account, no ads"],
        cons=["Rectangular rooms only",
              "2D only, no 3D view",
              "Needs iOS 26 or later"],
        price="Free download; a guided first room is free, planning needs the one-time unlock, $9.99",
        once="Yes, $9.99", year=None,
        fit="Yes, overlaps and pieces outside the room turn red",
        sizes="Yes, to the centimetre, plus pieces you draw",
        three_d="No", scan="No, you measure and type",
        ads="Yes, no ads", account="Yes, no account",
        privacy="Yes, no data linked to you",
        vs=False,
    ),
    dict(
        key="home-design-3d", short="Home Design 3D", name="Home Design 3D", developer="Home Design 3D srl",
        store_id="463768717",
        best_for="Designing a whole house over several floors, in 3D",
        summary=("A house designer: draw floor plans in 2D and walk through them in 3D, over unlimited floors, "
                 "with thousands of items, photorealistic rendering, VR export and blueprint import. It is "
                 "capable and long established, and it shows its age. Premium features are a subscription."),
        pros=["Multi-storey houses with adjustable walls",
              "Thousands of items with sizes you can change",
              "3D walkthrough, renders and VR export",
              "Import a blueprint and trace it"],
        cons=["Premium is a subscription",
              "No warning when furniture overlaps",
              "Reviews describe ads in the free version"],
        price="Free download. Weekly premium $4.99, monthly plans $12.99 to $22.99, yearly plans $44.99 to $79.99",
        once="No, subscription only", year="$44.99 to $79.99",
        fit="No, a table on the sofa went unflagged in our test",
        sizes="Yes, per its listing",
        three_d="Yes", scan="Not described on the listing",
        ads="Not tested; recent reviews describe ads", account="Yes, its sign-in page can be skipped",
        privacy="No, declares data used to track you",
        vs=True,
    ),
    dict(
        key="keyplan-3d", short="Keyplan 3D", name="Keyplan 3D Lite", developer="Quasarts LLC", store_id="983655856",
        best_for="Building a home's shape and decorating it in 2D and 3D",
        summary=("A home builder and interior designer: draw walls in any shape, place furniture, windows and "
                 "doors in 2D or 3D, and paint and decorate any surface. On iPhone it runs in landscape only. "
                 "Its listing counts 350+ free objects, though recent reviews say some of them, paints included, now "
                 "need a purchase; the Standard version and object packs are one-time purchases."),
        pros=["Walls in any shape, in 2D or 3D",
              "350+ objects, paints and materials",
              "A one-time $5.99 Standard upgrade",
              "iCloud sync between iPhone and iPad"],
        cons=["Runs in landscape only on iPhone",
              "More rooms cost extra, per reviews",
              "Object packs are sold separately"],
        price="Free download. Standard version $5.99 once; object packs $1.99 to $2.99",
        once="Yes, $5.99", year=None,
        fit="Not tested; its listing does not describe it",
        sizes="Not described on the listing",
        three_d="Yes", scan="Not described on the listing",
        ads="Yes, none seen", account="Yes, no account",
        privacy="Yes, but collects data linked to you",
        vs=True,
    ),
    dict(
        key="home-planner-ai", short="Home Planner AI", name="Home Planner AI", developer="Room Planner Ltd",
        store_id="1076159017",
        best_for="3D room design with a scanner, measure tools and renders",
        summary=("A 2D and 3D design app with AI design and, with premium, a built-in 3D scanner, a digital tape "
                 "measure and realistic renders. Its first screen promises real furniture that actually fits, from 564,000+ "
                 "products; its paywall comes before the first room, and in our test it did not flag a coffee "
                 "table moved onto the sofa."),
        pros=["3D scanner and measure tools, with premium",
              "2D and 3D, with realistic renders",
              "Brand-name products at their real sizes",
              "30 languages, the most here"],
        cons=["Paywall before the first room",
              "No warning when furniture overlaps",
              "Ten purchases make the price hard to read"],
        price=("Free download. Purchases from $5.99 to $74.99, 6-month plans at $29.99 and $34.99, "
               "Weekly Business $17.99"),
        once="Not stated on the listing", year="$59.98, two 6-month plans",
        fit="No, a table on the sofa went unflagged in our test",
        sizes="Not described on the listing",
        three_d="Yes", scan="Yes, with premium, per its listing",
        ads="Yes, none seen", account="Yes, no account",
        privacy="Yes, no data linked to you",
        vs=True,
    ),
    dict(
        key="planner-5d", short="Planner 5D", name="Planner 5D", developer="Planner5D, UAB", store_id="606173978",
        best_for="3D interior design with a large furniture catalogue",
        summary=("A 2D and 3D home design app with over 8,400 furniture and decor items with premium, "
                 "photo-like renders, AI design and 3D capture with the phone's camera. It asks for an account "
                 "before the first room, then offers a free trial of a yearly plan; the free tier locks about "
                 "half the sofas."),
        pros=["2D and 3D, with photo-like renders",
              "Over 8,400 items with premium",
              "Camera capture and AI design",
              "Apple Pencil and Vision Pro support"],
        cons=["Account required before the first room",
              "Free tier locks half the sofas we saw",
              "No warning when furniture overlaps"],
        price=("Free with limits. Subscriptions from $7.99 a week, $19.99 a month, $29.99 to $119.99 a year; "
               "full catalogue $6.99 for 30 days or $15.99 a year"),
        once="No, subscription only", year="$29.99 to $119.99",
        fit="No, a table on the sofa went unflagged in our test",
        sizes="Yes, with premium (its free version has no furniture customization)",
        three_d="Yes", scan="Yes, with the camera; reviews describe an extra charge",
        ads="Yes, none seen", account="No, an account before the first room",
        privacy="No, declares data used to track you",
        vs=True,
    ),
    dict(
        key="magicplan", short="magicplan", name="magicplan", developer="Technologies magicplan Inc.",
        store_id="427424432",
        best_for="Professionals capturing existing rooms for reports and estimates",
        summary=("A floor plan tool for remodelers, restoration and insurance claims work. You capture a room "
                 "with the phone's camera, then add photos, notes, checklists, 360° panoramas, reports and "
                 "estimates to the plan. Its free Starter plan needs a sign-up and holds 2 projects; its "
                 "listing names Xactimate and CoreLogic integrations."),
        pros=["Builds the plan from the phone's camera",
              "Photos, notes, forms and estimates on the plan",
              "Every wall measured on the plan",
              "Xactimate and CoreLogic integrations"],
        cons=["Priced for business: from $129.99 a year",
              "Sign-up needed; free holds 2 projects",
              "No warning when furniture overlaps"],
        price=("Free with a sign-up, up to 2 projects. Sketch Plan $12.99 a month or $129.99 a year, Report "
               "Plan $39.99 or $399.99, Estimate Plan $89.99 or $899.99"),
        once="No, subscription only", year="$129.99 to $899.99",
        fit="No, a table on the sofa went unflagged in our test",
        sizes="Not described on the listing",
        three_d="Not described on the listing", scan="Yes, with the camera",
        ads="Yes, none seen", account="No, a free sign-up before anything is saved",
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
              "Lifetime upgrades; Mac and Windows apps"],
        cons=["Free version: one project at a time",
              "No warning when furniture overlaps",
              "Lifetime Standard costs $59.99"],
        price=("Free version with watermarked exports and one project. Standard $6.99 a month, $24.99 a year or "
               "$59.99 lifetime; Pro $14.99 a month, $49.99 a year or $129.99 lifetime"),
        once="Yes, $59.99 lifetime", year="$24.99 to $49.99",
        fit="No, the sofa over the coffee table went unflagged in our test",
        sizes="Not described on the listing",
        three_d="Yes", scan="Yes, with LiDAR",
        ads="Yes, none seen", account="Yes, no account",
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
        fit="No, it has no furniture to check",
        sizes="No, you draw shapes to scale",
        three_d="No", scan="No",
        ads="Yes, none seen", account="Yes, no account",
        privacy="Yes, no data linked to you",
        vs=True,
    ),
    dict(
        key="drawplan", short="DrawPlan", name="DrawPlan", developer="Fleet Investments LLC", store_id="1451755778",
        best_for="To-scale 2D plans for trades and real estate, with tracing",
        summary=("A 2D floor plan app for quick sketches or to-scale drawings with automatic dimensions. You can "
                 "import an image or plan and trace it, save your own objects, and ask its AI to help draw. "
                 "Premium is a subscription. In our tests on iOS 27, it closed itself at every launch."),
        pros=["Free sketching or to-scale drawing",
              "Trace over an imported plan or photo",
              "AI-assisted drawing",
              "Runs on iOS 15 or later"],
        cons=["Closed at every launch on iOS 27 in our test",
              "Sync and clean exports need a subscription",
              "Reviews describe paying to reopen saved plans"],
        price=("Free download. $2.99 a month or $29.99 a year; Plus $4.99 or $49.99; Pro $9.99 or $99.99; "
               "AI credits $4.99 to $19.99"),
        once="No, subscription only", year="$29.99 to $99.99",
        fit="Not tested; it closed at every launch",
        sizes="Not described on the listing",
        three_d="Not described on the listing", scan="Not described on the listing",
        ads="Not tested", account="Not tested",
        privacy="Yes, no data linked to you",
        vs=True,
    ),
]

# Can you plan without paying? One rule for every table and price box (brand.md 2026-10-20, rule 15):
# "free" = free, no ads, real use; "limited" = free with ads, an account, or locked parts;
# "none" = paying or a trial comes first; "untested" = we could not open it. The note is the short why.
FREE_TIER = {
    "scooch": ("none", "a guided first room; planning needs the $9.99 unlock"),
    "home-design-3d": ("limited", "with ads, most items locked and saving limited, per recent reviews"),
    "keyplan-3d": ("limited", "the Lite version: demo plans locked, and a room limit per reviews"),
    "home-planner-ai": ("limited", "after a paywall you can close; up to 45 items per category"),
    "planner-5d": ("limited", "an account first; about half the sofas locked"),
    "magicplan": ("limited", "a free sign-up; up to 2 projects"),
    "live-home-3d": ("limited", "one project; Save greyed out"),
    "draft-paper": ("limited", "pages 3 to 6 locked"),
    "drawplan": ("untested", "it closed at every launch on iOS 27"),
}
# Ours in the price box: the free tile says what the free part is, not "None".
FREE_TILE = {"scooch": ("Intro only", "a guided first room")}

# Under the summary table. Each names whichever app the data says wins, not always us.
PICKS = [
    ("Checks that furniture fits", "Scooch. In the five other apps we could test, none flagged a coffee table moved onto the sofa"),
    ("Lowest one-time price", "Keyplan 3D Lite, $5.99 for its Standard version; Scooch and Draft Paper are $9.99"),
    ("For 3D design and renders", "Planner 5D or Live Home 3D"),
    ("For scanning a room with the camera", "magicplan, Home Planner AI, or Live Home 3D with LiDAR"),
    ("For drafting anything in 2D", "Draft Paper"),
    ("For whole houses over several floors", "Home Design 3D"),
]

# Our app in brief, for the "About Scooch" box on each head-to-head. Shipped (1.0.2) only.
ABOUT_US = [
    "Rooms drawn at their real measurements, joined into an L or a U",
    "37 everyday pieces at real sizes, each resized to the centimetre",
    "A drawing tool for any other piece, at any size",
    "Overlaps and pieces outside the room outlined in red",
    "Wardrobe doors, drawers and sofa beds drawn with the space they need to open",
    "PNG and PDF export, metric or imperial, 26 themes",
    "iPhone and iPad, synced through your own iCloud",
]

# Our screenshot beside the about box on each head-to-head and on our roundup card: (file stem, alt).
OUR_SHOT = {
    "scooch": ("compare/scooch-fit", "A coffee table moved onto the sofa in Scooch: both outlined in red"),
    "draft-paper": ("shot-draw", "Drawing a dining table at 140 by 90 cm in Scooch"),
    "drawplan": ("shot-plans", "Three plans in Scooch: a flat, a studio and an office"),
}
for _key in ("magicplan", "planner-5d", "home-planner-ai", "home-design-3d", "keyplan-3d", "live-home-3d"):
    OUR_SHOT[_key] = ("compare/scooch-projections",
                      "The wardrobe's doors drawn swinging open in Scooch, clear of the desk below")

# ---- screenshots of the other apps (brand.md Decisions log 2026-10-20) ----
# Only screens we captured ourselves from the app's current version, each showing a point the page
# makes, never their App Store marketing images. Raws: the app repo's Marketing/competitors/;
# _gen/frame_compare.py frames them into assets/compare/<key>-<slot>.webp. A shot appears only once
# its file exists AND its app is in SHOTS_TAKEN; until then build.py prints it as missing.
# One capture per slot, the same slots for every app, so pages compare like with like.
SLOTS = [("wall", "Before your first room"), ("plan", "A room with furniture"),
         ("catalogue", "Choosing furniture"), ("fit", "A coffee table moved onto the sofa"),
         ("paywall", "The upgrade screen"), ("offer", "Closing the upgrade screen")]
# Where a slot shows something other than its usual screen, the row says so.
SLOT_TITLES = {"draft-paper": {"plan": "Drawing a room"}, "keyplan-3d": {"plan": "A room"},
               "drawplan": {"plan": "Opening the app"},
               "home-design-3d": {"fit": "A table moved onto the sofa"},
               "live-home-3d": {"fit": "The sofa pushed over the coffee table"},
               "home-planner-ai": {"offer": "Back on its home screen"}}
THEIR_SHOTS = {
    "home-design-3d": {
        "wall": "Home Design 3D on first launch: a page asking whether we would like to create an account, which Later skips",
        "plan": "The ground floor of Home Design 3D's furnished sample house in its 2D view",
        "catalogue": "Home Design 3D's catalogue: 584 items under Living room alone, each with its size",
        "fit": "The same floor with the lounge table moved onto the sofa: nothing flagged",
    },
    "planner-5d": {
        "wall": "Planner 5D on first launch: create an account to save all your projects, with no way past it",
        "plan": "A 4.50 by 3.40 m living room furnished by Planner 5D's Smart wizard, the size of ours. Ringed: its Ask Copilot button, floating over the top of the plan at about 40% of the screen's width",
        "catalogue": "Planner 5D's straight sofas on the free tier, about half of them behind a padlock",
        "fit": "The same room with the coffee table moved onto the sofa: nothing flagged",
        "paywall": "Planner 5D's paywall after setup: a 7-day free trial, then a yearly plan",
        "offer": "What Planner 5D showed when we closed its paywall: a one-time offer of 80% off the first year that disappears when you close it",
    },
    "magicplan": {
        "wall": "magicplan for a new user: the free Starter plan, all features for up to 2 projects, after a sign-up",
        "plan": "magicplan's furnished demo flat, every wall measured",
        "catalogue": "magicplan's objects by category",
        "fit": "The demo flat's living room with the coffee table moved onto the sofa: nothing flagged",
    },
    "keyplan-3d": {
        "plan": "A 2.22 by 1.55 m room drawn in Keyplan 3D, which runs in landscape on iPhone, so its screens stand on their side here",
        "catalogue": "Keyplan 3D's catalogue, each piece with its size in centimetres, in landscape",
        "paywall": "Keyplan 3D's shop in landscape: the Standard version once, or a starter pack with ten object packs",
    },
    "live-home-3d": {
        "wall": "Live Home 3D's first screen: a welcome, then My Projects or Create New, with no account",
        "plan": "Live Home 3D's furnished studio apartment sample in its 2D view, 7.8 by 7.6 m, its garden trees hidden",
        "fit": "The same studio with the corner sofa pushed over the coffee table and an armchair: nothing flagged",
        "paywall": "Live Home 3D's store: Standard and Pro, each monthly, yearly or for life",
    },
    "home-planner-ai": {
        "wall": "Home Planner AI's paywall, shown before the first room; its X closes it",
        "plan": "Home Planner AI's furnished 4.00 by 5.10 m living room template",
        "catalogue": "Home Planner AI's sofas on the free tier: up to 45 items in this category",
        "fit": "The same room with the coffee table moved onto the corner sofa: nothing flagged",
        "offer": "Home Planner AI after we closed its paywall: 'Price Crash! HUGE DISCOUNT' with an hour's countdown, and 9 rooms left to add",
    },
    "draft-paper": {
        "plan": "A 3 by 4.5 m living room we drew in Draft Paper: the walls, a sofa, a coffee table, an armchair and a TV unit as rectangles, with one measured line",
        "paywall": "Draft Paper's unlock: every feature for one price",
    },
    "drawplan": {
        "plan": "What DrawPlan 6.0.1 showed us on iOS 27: nothing, it closed at every launch (a stand-in, not a capture)",
    },
}
# Ours, for the side-by-side rows. (asset path, alt, caption). "offer" has no screen of ours: OUR_NONE.
OUR_SHOTS = {
    "wall": ("/assets/compare/scooch-wall.webp", "Scooch's first screen: the guided first room starts, with no account or sign-in", "Scooch"),
    "plan": ("/assets/compare/scooch-plan.webp", "Scooch's sample flat at its real measurements, each door swing and drawer pull-out drawn and clear", "Scooch"),
    "catalogue": ("/assets/shot-furniture.webp", "The Scooch furniture list with each piece's default size", "Scooch"),
    "fit": ("/assets/compare/scooch-fit.webp", "Scooch's sample flat with the coffee table moved onto the sofa: both outlined in red", "Scooch"),
    "paywall": ("/assets/compare/scooch-paywall.webp", "Scooch's unlock screen: one payment, yours for good, no subscription", "Scooch"),
}
OUR_NONE = {"offer": ("One price", "Scooch is $9.99 once. No trial to cancel, no countdown.")}

# What happened when we used each app ourselves (TESTED_ON, TESTED_WHEN). Told as what happened,
# never as a settings readout (brand.md 2026-10-20, rule 7).
TESTED = {
    "home-design-3d": [
        "It opened with Apple's tracking request, then a page asking whether we would like to create an account. Later skips it.",
        "A room in its 2D view took one drag, with the wall lengths drawn inside and out. Furniture comes from a large catalogue, 584 items under Living room alone, each with its size.",
        "In its furnished sample house we moved the lounge table onto the sofa. Nothing turned red and nothing warned us. (Earlier, in an empty room, two sofas dropped on the same spot, half through a wall, went unflagged too.)",
        "We could not see its free version. The iPhone we used is signed in with our own Apple ID, which bought Home Design 3D years ago, and every paid feature we tried was open. Its prices here come from the US purchase list.",
    ],
    "planner-5d": [
        "Before anything else it asked to send notifications and to track us, then showed its terms.",
        "Next came 'Create an account to save all your projects', with no way past it. We signed in.",
        "Three questions followed. One of the goals it offers is 'Test what furniture fits in a room'.",
        "Then its paywall: a 7-day free trial, then a yearly plan. Closing it brought up a one-time offer of 80% off the first year, gone once closed.",
        "On the free tier, about half the straight sofas in its catalogue carried a padlock.",
        "Its Smart wizard furnished a 4.50 by 3.40 m living room for us, the size of the one in our own screenshots. We moved its coffee table onto the sofa. Nothing was flagged.",
        "A large 'Ask Copilot' button floats over the top of the plan the whole time, about 40% of the screen's width.",
    ],
    "magicplan": [
        "Its first screen asks whether you already have an account. As a new user we were offered the free Starter plan, all features for up to 2 projects, after a sign-up.",
        "Without an account there is a demo that warns 'Changes will not be saved'. It opens a sample flat with every wall measured.",
        "Selected furniture offers Set Distance, to place it a set distance from a wall.",
        "In its furnished demo flat we moved the coffee table onto the sofa. Nothing was flagged. A couch inserted from its catalogue had also landed across a wall and inside a door's swing without a word.",
    ],
    "keyplan-3d": [
        "On iPhone it only runs sideways, in landscape.",
        "It opened on a tutorial, then a binder of projects with four demo plans, each behind a padlock.",
        "Its shop sells the Standard version once, with every project tool and as many rooms as you want, or a starter pack with ten object packs.",
        "Four drags drew a room with its size and area, and its catalogue gives each piece's size in centimetres. We did not get to test furniture on top of furniture in it.",
    ],
    "live-home-3d": [
        "No account and no prompts: a welcome screen, then templates and sample rooms.",
        "In the free version, Save was greyed out, and opening a second project warned that the first could no longer be edited: the free version handles one project at a time.",
        "Its store sells Standard and Pro, each monthly, yearly or for life.",
        "In its furnished studio sample we pushed the corner sofa over the coffee table and an armchair. Nothing was flagged. Earlier, a sofa dragged half through a wall went unflagged too.",
    ],
    "home-planner-ai": [
        "Its first onboarding card reads 'Real furniture that actually fits', with 564,000+ real products at true-to-life sizes.",
        "As soon as we picked a room shape, before the first room, its paywall came up: weekly, monthly or 6-month plans, each with a crossed-out price several times higher. Its X closes it.",
        "On the free tier its catalogue offers up to 45 items per category, and asks for the subscription for the full 564,000.",
        "Selected furniture shows its distance to each wall.",
        "From its own furnished 4.00 by 5.10 m living room template we moved the coffee table onto the corner sofa. Nothing was flagged.",
        "Back on its home screen after closing the paywall: 'Price Crash! HUGE DISCOUNT for all PRO subscriptions' with a one-hour countdown, and 'Add Living room (9 left)'.",
    ],
    "draft-paper": [
        "A short tutorial, then a blank sheet of grid paper. No account, no prompts and no furniture: you draw every line yourself.",
        "We drew a living room with its rectangle tool. Zoomed out, lines snap to whole metres; zoomed in, to 10 cm. Shapes that touch merge into one outline, so a sofa drawn against a wall turned into a notch in the wall.",
        "Pages 3 to 6 carry a padlock; tapping one asks you to unlock every feature, once.",
    ],
    "drawplan": [
        "In our tests on iOS 27.0.1, version 6.0.1 closed itself at every launch, so we could not use it.",
        "Its crash report points at a check iOS 27 now enforces on how apps start. If your iPhone is not on iOS 27 yet, this may not affect you.",
    ],
}
# key -> (version on the phone when captured, capture date). The caption is "<app> <version> · <date>".
SHOTS_TAKEN = {
    "home-design-3d": ("5.10", "23 Oct 2026"),
    "planner-5d": ("5.13.1", "23 Oct 2026"),
    "magicplan": ("2026.41.0", "23 Oct 2026"),
    "keyplan-3d": ("1.9.9", "23 Oct 2026"),
    "live-home-3d": ("5.1", "23 Oct 2026"),
    "home-planner-ai": ("26.50", "23 Oct 2026"),
    "draft-paper": ("1.19.6", "23 Oct 2026"),
    "drawplan": ("6.0.1", "23 Oct 2026"),
}

# One page per competitor. Sections render in a fixed order (see build.py): quick answer, table,
# where they are stronger, where we are stronger, about us, side by side, what we saw, what we do
# not do, what reviews mention, pricing, questions. Write the "they are stronger" part first and
# mean it. Fit answers come from our own test (TESTED); a listing's silence is said as silence.
VERSUS = {
"home-design-3d": dict(
    title="Home Design 3D Alternative (2026): Home Design 3D vs Scooch",
    meta=("Looking for a Home Design 3D alternative without a subscription? Scooch checks what fits at exact "
          "sizes for $9.99 once. Side by side, tested October 2026."),
    h1="Home Design 3D alternative: Home Design 3D vs Scooch",
    label="Scooch vs Home Design 3D",
    lede=("Home Design 3D plans whole houses in 3D. Scooch is for the room you already have, and whether the "
          "furniture you want fits in it."),
    maker_note=("I used Home Design 3D faithfully in the past, and paid for it. It is a capable house "
                "designer. Today it feels slow and dated for the job I kept opening it for: I did not need "
                "hundreds of couch designs, I needed to know whether one couch fits. So I made Scooch, simpler: "
                "rooms at their real size, furniture you resize to the centimetre or draw yourself at its real "
                "size, and a red outline when something does not fit."),
    pick_them="you are planning a house or a renovation over several floors and want to see it in 3D.",
    pick_us="you have the room already and want to know whether the furniture fits, for one price.",
    them_stronger=[
        ("Whole houses", "Several floors, adjustable wall thickness, height and angles, roofs, and a 3D walkthrough with VR export: the right toolbox for a house that is not built yet. In a room you already live in, the walls and the roof are given, and what is left to decide is the furniture."),
        ("Thousands of items", "Far more than Scooch's 37 everyday pieces, with sizes you can change: 584 under Living room alone in our test. Handy for styling a house. Your own sofa, or the one in the shop, is unlikely to be among them, though, so checking it means minutes of scrolling for a near match that you then resize to its real measurements anyway. And our test iPhone had bought it years ago: recent reviews say that without the subscription, most items are locked."),
        ("Blueprints", "Import an existing plan and draw over it."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch outlines in red a piece that overlaps another or sticks out of the room, so a misfit shows on the plan, not on moving day. In our test, in Home Design 3D's own furnished sample house, we moved the lounge table onto the sofa and it said nothing."),
        ("One price", "$9.99 once. Home Design 3D is a subscription, and recent reviews describe earlier one-time purchases moving to it."),
        ("No tracking", "Home Design 3D's App Store privacy label declares data used to track you, and it asked to track us on first launch; Scooch's label declares none."),
        ("Room to open it, not just to stand it", "Scooch draws each wardrobe door's swing, each drawer's pull-out and a sofa bed opened out, so you can see whether the door clears the desk and the drawer clears the bed, not only whether the piece fits."),
    ],
    we_dont=[
        ("Plan houses or floors.", "Scooch plans rooms in 2D. For a whole house over several floors in 3D, Home Design 3D is built for that."),
        ("Offer hundreds of sofas.", "37 everyday pieces you resize to the centimetre, and a drawing tool for anything else at its real size. The question is whether yours fits, not which one to pick."),
        ("Ask for a subscription, an account or your data.", "$9.99 once, 0 ads, nothing to sign up for."),
    ],
    reviews=[
        "long-time users who bought the one-time Gold edition or content packs and lost access after the move to subscriptions",
        "most items and tools locked, an ad before a project starts, and projects that will not save without the subscription",
        "crashes after recent updates, including projects that no longer open",
    ],
    pricing=("Home Design 3D is free to download; premium is a subscription at $4.99 a week, $12.99 to $22.99 a "
             "month or $44.99 to $79.99 a year (US). We could not check its free version ourselves: our test "
             "iPhone's Apple ID bought it years ago. Scooch is a free download; planning needs a one-time $9.99 unlock."),
    faq=[
        ("Does Scooch do several floors or 3D?", "No. Scooch plans rooms in 2D. You can keep several plans, but not floors stacked in 3D."),
        ("Does Home Design 3D warn when furniture will not fit?", "Not in our test (version 5.10, 23 October 2026): in its own furnished sample house, a table moved onto the sofa was not flagged. Scooch outlines both pieces in red."),
        ("Is either a one-time purchase?", "Scooch is: $9.99 once. Home Design 3D's US purchase list shows only weekly, monthly and yearly plans."),
    ],
),
"keyplan-3d": dict(
    title="Keyplan 3D Alternative (2026): Keyplan 3D Lite vs Scooch",
    meta=("Looking for a Keyplan 3D alternative? Scooch checks what fits at exact sizes and warns when it does "
          "not. Side by side, tested October 2026."),
    h1="Keyplan 3D alternative: Keyplan 3D Lite vs Scooch",
    label="Scooch vs Keyplan 3D Lite",
    lede=("Keyplan 3D builds a home's shape and decorates it in 3D, at a low one-time price. Scooch stays in 2D "
          "and checks whether furniture at real sizes fits."),
    pick_them="you want to build a home's shape freely and decorate it in 3D, at the lowest one-time price here.",
    pick_us="you want exact furniture sizes and a warning when something does not fit.",
    them_stronger=[
        ("Any shape", "Walls go wherever you draw them, handy for an odd-shaped house. Most rooms are rectangles, though, and an L or a U is two or three of them joined, which is how Scooch builds them."),
        ("3D and decoration", "Edit in 3D and paint or texture any surface, though recent reviews say the Lite version now locks the paint textures. Good for trying a colour; it does not change whether the wardrobe door clears the bed."),
        ("Price", "Its Standard version is $5.99 once, less than Scooch's $9.99. Object packs are extra, from $1.99 each, so two of them bring it to about Scooch's price."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch outlines in red a piece that overlaps another or sticks out of the room. Keyplan's listing does not describe a check like that, and we did not get to test one."),
        ("Exact furniture sizes", "Every piece resizes to the centimetre, and you can draw your own pieces at any size."),
        ("Upright, in 16 languages", "Scooch works in portrait, the way you hold a phone, in 16 languages. On iPhone, Keyplan 3D runs in landscape only, in 10."),
        ("Room to open it, not just to stand it", "Scooch draws each wardrobe door's swing, each drawer's pull-out and a sofa bed opened out, so you can see whether the door clears the desk and the drawer clears the bed, not only whether the piece fits."),
    ],
    we_dont=[
        ("Draw angled walls.", "Rooms are rectangles you join into an L or a U."),
        ("Decorate in 3D.", "No paint, textures or 3D view: Scooch is about whether things fit."),
        ("Sell packs.", "$9.99 once covers every piece, with nothing extra to buy."),
    ],
    reviews=[
        "the Lite version asking for a purchase to add more rooms or use paint textures",
        "plans lost when moving to a new phone",
        "spaces that are hard to size precisely",
    ],
    pricing=("Keyplan 3D Lite is free to download; its Standard version is $5.99 once and object packs cost $1.99 "
             "to $2.99 each (US). Scooch is a free download; planning needs a one-time $9.99 unlock. Neither has a subscription."),
    faq=[
        ("Which is cheaper?", "Keyplan 3D Lite: its Standard version is $5.99 once, against Scooch's $9.99. Neither has a subscription."),
        ("Does Keyplan 3D warn when furniture will not fit?", "Its listing does not describe a check like that, and we did not get to test one (version 1.9.9, 23 October 2026). Scooch outlines a piece in red when it overlaps another or sticks out of the room."),
        ("Can Scooch draw angled walls?", "No. Scooch rooms are rectangles; you build an L or a U by joining rooms."),
    ],
),
"home-planner-ai": dict(
    title="Home Planner AI Alternative (2026): Scooch Compared",
    meta=("Looking for a Home Planner AI alternative? Scooch checks what fits at exact sizes for one price, "
          "$9.99 once. Side by side, tested October 2026."),
    h1="Home Planner AI alternative: Home Planner AI vs Scooch",
    label="Scooch vs Home Planner AI",
    lede=("Home Planner AI scans and designs rooms in 3D, and its first screen promises real furniture that "
          "actually fits. Scooch skips the scan and the 3D and does the check itself: furniture that overlaps or "
          "sticks out of the room turns red."),
    pick_them="you want to scan a room and design it in 3D with renders and brand-name products.",
    pick_us="you want to check what fits at exact sizes, for one clear price.",
    them_stronger=[
        ("It scans and measures", "A built-in 3D scanner and a digital tape measure, premium features per its listing, so the room's size comes from the phone. The sofa still in the shop cannot be scanned: its size comes from the product page, and the fit comes down to those numbers either way. With Scooch you measure the room yourself and type them in."),
        ("3D, renders and real products", "Layouts in 2D and 3D, realistic renders with premium, and 564,000+ brand-name products at their listed size. That only helps if your sofa is one of them: recent reviews say the catalogue leans on IKEA, and a lookalike of another size says nothing about yours. On the free tier, it offers up to 45 items per category."),
        ("Languages", "30 languages, the most of any app compared here; Scooch has 16."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch outlines in red any piece that overlaps another or sticks out of the room, so a misfit shows before you buy. Home Planner AI's first screen promises 'real furniture that actually fits', but in our test, in its own furnished template room, it let us put the coffee table on the sofa without a word."),
        ("Typed sizes from the start", "Rooms and furniture take the exact size you type. Recent Home Planner AI reviews say typing a room's size needs the subscription."),
        ("One clear price, after you have tried it", "The guided first room is free, then $9.99 once. Home Planner AI shows its paywall before the first room, with weekly, monthly and 6-month plans, and its purchase list runs to ten items."),
        ("Room to open it, not just to stand it", "Scooch draws each wardrobe door's swing, each drawer's pull-out and a sofa bed opened out, so you can see whether the door clears the desk and the drawer clears the bed, not only whether the piece fits."),
    ],
    we_dont=[
        ("Scan a room.", "You measure it and type the size; a tape measure is all it takes."),
        ("Show it in 3D or render it.", "Scooch is 2D."),
        ("Sell brand furniture.", "Everyday pieces you resize to the centimetre, and a drawing tool for any piece, from its product page's measurements."),
    ],
    reviews=[
        "a free version too limited to use, including typing a room's size",
        "freezing, crashes and slow loading",
        "controls that are confusing or too small to select, especially on iPad",
        "a subscription that was hard to cancel",
    ],
    pricing=("Home Planner AI is free to download; its US purchase list shows Interior Design $5.99, Floor plan "
             "creator from $6.99 to $74.99, Architecture $14.99, 6-month subscriptions at $29.99 and $34.99, and "
             "Weekly Business at $17.99, without saying which are one-time. In the app, its paywall offered weekly, "
             "monthly and 6-month plans. Scooch is a free download; planning needs a one-time $9.99 unlock."),
    faq=[
        ("Can Scooch scan a room?", "No. You measure the room and type or drag its size. Home Planner AI has a built-in 3D scanner with premium, per its listing."),
        ("Does Home Planner AI warn when furniture will not fit?", "Not in our test (version 26.50, 23 October 2026): in its own furnished template room, a coffee table moved onto the sofa was not flagged. Scooch outlines both pieces in red."),
        ("How much does each cost?", "Scooch: $9.99 once. Home Planner AI lists purchases from $5.99 to $74.99 and 6-month subscriptions; see Pricing above."),
    ],
),
"planner-5d": dict(
    title="Planner 5D Alternative (2026): Planner 5D vs Scooch",
    meta=("Looking for a Planner 5D alternative? Scooch checks what fits at exact sizes, for $9.99 once with no "
          "subscription or account. Side by side, tested October 2026."),
    h1="Planner 5D alternative: Planner 5D vs Scooch",
    label="Scooch vs Planner 5D",
    lede=("Planner 5D is about seeing a room in 3D and styling it from a big catalogue. Scooch is 2D and answers "
          "one practical question: does the furniture fit?"),
    pick_them="you want to see the room in 3D, furnish it from thousands of items and render it.",
    pick_us="you need exact sizes and a clear answer on what fits, without an account or a subscription.",
    them_stronger=[
        ("3D and renders", "Planner 5D switches between 2D and 3D and renders photo-like images, good for seeing a style before you commit to it. Whether the sofa clears the door is a question of centimetres, though, and those show best in the plan from above."),
        ("A huge catalogue", "Over 8,400 furniture and decor items with premium, against Scooch's 37 everyday pieces. It sounds like your sofa will be in there, but the odds are it is not. You scroll for minutes for something close, and then its size still has to match yours, which its listing says the free version cannot change. On the free tier, about half the sofas we saw were locked anyway."),
        ("Camera capture and AI", "It can capture a room in 3D with the phone's camera and generate designs with AI, though recent reviews describe the scan costing extra on top of the subscription and the AI designer not always working. An AI design picks furniture for you; the question you came with, whether yours fits, stays open. Its Ask Copilot button floats over the top of the plan the whole time, about 40% of the screen's width."),
        ("More platforms and languages", "It runs across platforms and on Vision Pro, in 24 languages to Scooch's 16."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch outlines in red a piece that overlaps another or sticks out of the room. Planner 5D offered us 'Test what furniture fits in a room' as a goal during setup, then, in a living room its own wizard had furnished, let us put the coffee table on the sofa without a word."),
        ("Exact sizes without a subscription", "Every Scooch piece resizes to the centimetre with the one-time unlock. Planner 5D's listing says its free version has no furniture customization."),
        ("One price, no account", "$9.99 once, nothing to sign up for. Planner 5D asked for an account before the first room, then offered a free trial of a yearly plan, and when we closed that, a one-time discount that disappears once closed."),
        ("No tracking", "Planner 5D's App Store privacy label declares data used to track you, and it asked to track us before the first screen; Scooch's label declares none."),
        ("Room to open it, not just to stand it", "Scooch draws each wardrobe door's swing, each drawer's pull-out and a sofa bed opened out, so you can see whether the door clears the desk and the drawer clears the bed, not only whether the piece fits."),
    ],
    we_dont=[
        ("Work in 3D or render.", "Scooch is 2D: it shows real sizes, door swings and the space drawers need, not a 3D view."),
        ("Make you search a catalogue.", "Place a sofa, type the size from its product page or your tape measure, and you know whether it fits. 37 everyday pieces cover the usual furniture, and a drawing tool covers the rest."),
        ("Ask for an account.", "Nothing to sign up for; plans sync through your own iCloud."),
        ("Run trials or countdown offers.", "$9.99 once, the same for everyone."),
    ],
    reviews=[
        "free trials that turned into charges reviewers did not expect, and refunds that were hard to get",
        "scans, downloads and other features that each ask for another purchase",
        "an app that feels confusing, slow or prone to freezing",
        "saved projects that reverted or partly disappeared",
        "room and furniture sizes that are hard or impossible to set exactly",
    ],
    pricing=("Planner 5D is free with a limited catalogue and an account; its US purchase list shows subscriptions "
             "from $7.99 a week and $19.99 a month to $29.99, $69.99 and $119.99 a year, plus full-catalogue access "
             "at $6.99 for 30 days or $15.99 a year. In the app, its paywall offered a 7-day free trial of a yearly "
             "plan or a 30-day trial, and closing it brought up an offer of 80% off the first year. Scooch is a free "
             "download; planning needs a one-time $9.99 unlock."),
    faq=[
        ("Do I need a big furniture catalogue to check a fit?", "No. What decides a fit is the size of your piece, from a tape measure or the product page. A catalogue rarely has your exact sofa, so you end up resizing a near match anyway. Scooch starts from the size: 37 everyday pieces you resize to the centimetre, and a drawing tool for anything else."),
        ("Is Planner 5D free?", "It is free to download with a limited catalogue, but it asked us for an account before the first room. On the free tier about half the sofas we saw were locked, and its listing says furniture customization needs premium."),
        ("Does Scooch work in 3D?", "No. Scooch is 2D. It shows real sizes, door swings and the space drawers and sofa beds need, but not a 3D view."),
        ("Which one tells me if a sofa will fit?", "Scooch outlines furniture in red when it overlaps or sticks out of the room. In our test (Planner 5D 5.13.1, 23 October 2026), a coffee table moved onto the sofa was not flagged."),
    ],
),
"magicplan": dict(
    title="magicplan Alternative (2026): magicplan vs Scooch",
    meta=("Looking for a magicplan alternative for furniture? Scooch checks what fits at exact sizes for $9.99 "
          "once, no account. Side by side, tested October 2026."),
    h1="magicplan alternative: magicplan vs Scooch",
    label="Scooch vs magicplan",
    lede=("magicplan measures rooms with the camera and turns them into plans, photos and estimates for jobs. "
          "Scooch starts from measurements you type and answers a narrower question: does the furniture fit?"),
    pick_them="you work in remodeling, restoration or insurance claims and need plans, photos and estimates from the camera.",
    pick_us="you are at home asking whether a sofa, bed or table will fit, and want one price instead of a plan.",
    them_stronger=[
        ("It measures for you", "magicplan builds the floor plan from the phone's camera. When it works, that is quick; recent reviews describe scans that miss closets, walls or doors. For the one room you are furnishing, a tape measure takes a few minutes, and you need it for the furniture anyway. With Scooch you measure the room and type its size."),
        ("Made for jobs", "Photos, notes, forms, 360° panoramas, reports and estimates sit on the plan, and it connects to Xactimate and CoreLogic. That is what its prices pay for, from $129.99 a year. At home, with no one to bill, it is paperwork you will not use."),
        ("A long track record", "Years on the App Store and far more ratings than Scooch, which is new. Its listing speaks to remodelers, restoration and claims professionals, and that is who its features and prices are built around."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch outlines in red a piece that overlaps another or sticks out of the room. In our test, in magicplan's furnished demo flat, the coffee table moved onto the sofa without a word."),
        ("Furniture that knows its size", "37 pieces at real sizes, each resized to the centimetre, plus pieces you draw yourself."),
        ("No account, one price", "$9.99 once, nothing to sign up for. magicplan's free Starter plan needs a sign-up and holds 2 projects; its paid plans start at $12.99 a month or $129.99 a year."),
        ("Languages", "Scooch is in 16 languages; magicplan's listing names 5."),
        ("Room to open it, not just to stand it", "Scooch draws each wardrobe door's swing, each drawer's pull-out and a sofa bed opened out, so you can see whether the door clears the desk and the drawer clears the bed, not only whether the piece fits."),
    ],
    we_dont=[
        ("Scan a room.", "You measure it and type the size."),
        ("Write reports or estimates.", "Scooch is for furnishing your own rooms; magicplan is built for jobs."),
        ("Ask for an account.", "Plans stay on your devices and in your own iCloud."),
    ],
    reviews=[
        "core features, extra plans and scanning that need a subscription, with pricing some found unclear",
        "scans that miss closets, walls or doors, or struggle with open-plan rooms and sloped ceilings",
        "projects that did not save, or disappeared after an update or an account change",
        "a steep learning curve for first-time users",
    ],
    pricing=("magicplan's free Starter plan needs a sign-up and holds up to 2 projects; without one, its demo is "
             "not saved. Its paid plans are Sketch at $12.99 a month or $129.99 a year, Report at $39.99 or "
             "$399.99, and Estimate at $89.99 or $899.99 (US). Scooch is a free download; planning needs a one-time "
             "$9.99 unlock, with no subscription."),
    faq=[
        ("Can Scooch scan a room like magicplan?", "No. Scooch has no camera or LiDAR scan: you measure the room and type or drag its size."),
        ("Does magicplan warn when furniture will not fit?", "Not in our test (version 2026.41.0, 23 October 2026): in its furnished demo flat, a coffee table moved onto the sofa was not flagged. Scooch outlines both pieces in red."),
        ("Which is cheaper?", "Scooch: $9.99 once. magicplan's paid plans start at $12.99 a month or $129.99 a year; its free plan holds 2 projects."),
    ],
),
"live-home-3d": dict(
    title="Live Home 3D Alternative (2026): Live Home 3D vs Scooch",
    meta=("Looking for a simpler Live Home 3D alternative? Scooch checks what fits at exact sizes for $9.99 once. "
          "Side by side, tested October 2026."),
    h1="Live Home 3D alternative: Live Home 3D vs Scooch",
    label="Scooch vs Live Home 3D",
    lede=("Live Home 3D is a full 3D design tool, from roofs to lighting. Scooch does one part of that job, "
          "checking whether furniture fits, for less."),
    pick_them="you want detailed 3D design, renders and video, on Apple devices and Windows.",
    pick_us="you only need to know whether your furniture fits, for $9.99 once.",
    them_stronger=[
        ("Full 3D design", "Walkthroughs, renders, flyover videos, roofs, lighting and, with Pro, terrain: a full toolbox for designing a house. For checking whether one sofa fits the room you have, nearly all of it stays unused."),
        ("Scanning", "A LiDAR room scanner, on the Pro iPhones and iPads that have the sensor. On any other iPhone you measure by hand, as with Scooch, and the furniture you are buying is measured from its product page either way."),
        ("Catalogue and platforms", "5,000+ items and 3,000+ materials, thousands more models to import from Trimble 3D Warehouse and Sketchfab, and versions for Mac and Windows. That is a lot of searching for a model of your own sofa; for a fit, the width and depth on its product page are what count."),
    ],
    us_stronger=[
        ("A warning before you lift anything", "Scooch outlines in red a piece that overlaps another or sticks out of the room. In our test, in Live Home 3D's furnished studio sample, the corner sofa went over the coffee table and an armchair without a word."),
        ("Price", "Everything in Scooch is $9.99 once; Live Home 3D's Standard upgrade is $24.99 a year or $59.99 lifetime, and its free version kept Save greyed out and edits one project at a time."),
        ("Languages", "16 languages to Live Home 3D's 12."),
        ("Room to open it, not just to stand it", "Scooch draws each wardrobe door's swing, each drawer's pull-out and a sofa bed opened out, so you can see whether the door clears the desk and the drawer clears the bed, not only whether the piece fits."),
    ],
    we_dont=[
        ("Do 3D, renders or video.", "Scooch is 2D, for checking what fits."),
        ("Scan with LiDAR.", "You measure the room and type its size."),
        ("Run on a Mac or Windows.", "Scooch is for iPhone and iPad, synced through your own iCloud."),
    ],
    reviews=[
        "the one free project locked until paying",
        "purchases or projects not carrying across devices",
        "an interface some found confusing at first",
    ],
    pricing=("Live Home 3D has a free version that watermarks exports and keeps one project at a time; in our test "
             "its Save was greyed out. Standard is $6.99 a month, $24.99 a year or $59.99 lifetime; Pro is $14.99 a "
             "month, $49.99 a year or $129.99 lifetime (US). Scooch is a free download; planning needs a one-time "
             "$9.99 unlock."),
    faq=[
        ("Is Live Home 3D free?", "There is a free version; per its listing, exports carry a watermark and only one project can be used at a time, and in our test Save was greyed out."),
        ("Can Scooch scan with LiDAR?", "No. You measure the room and type or drag its size."),
        ("Does Live Home 3D warn when furniture will not fit?", "Not in our test (version 5.1, 23 October 2026): in its furnished studio sample, the sofa pushed over the coffee table was not flagged. Scooch outlines both pieces in red."),
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
        ("It draws anything", "Lines, shapes, text and measurements on up to 10 layers, not only rooms and furniture. The flip side is that it knows nothing about what you draw: every sofa and bed is a rectangle you size by hand, and when we drew a sofa against a wall, the two merged into one outline."),
        ("CAD export", "It exports DXF, so the drawing opens in CAD software."),
        ("Older iPhones", "It runs on iOS 15 or later; Scooch needs iOS 26."),
    ],
    us_stronger=[
        ("Furniture, ready made", "37 pieces at real sizes, each resized to the centimetre, instead of shapes you draw. In Draft Paper the sheet starts blank and every line is yours."),
        ("A warning before you lift anything", "Scooch outlines in red a piece that overlaps another or sticks out of the room. A drawing app has no furniture to check."),
        ("Languages", "16 languages; Draft Paper's listing names English only."),
    ],
    we_dont=[
        ("Export DXF.", "PNG and PDF only."),
        ("Draw anything.", "Rooms and furniture only, which is what lets it warn you."),
        ("Run on older iPhones.", "It needs iOS 26, which every iPhone since the iPhone 11 (2019) can run."),
    ],
    reviews=[
        "a recent update (1.19.5) that changed scrolling and undo and made drawing harder",
        "crashes that lose minutes of work",
        "trouble switching between metric and imperial, or importing an image",
    ],
    pricing=("Draft Paper is free to download, with pages 3 to 6 locked; All Features is $9.99 once (US). Scooch is "
             "a free download; planning needs a one-time $9.99 unlock. Neither has a subscription."),
    faq=[
        ("Do they cost the same?", "Yes: both are $9.99 once in the US, with no subscription."),
        ("Does Draft Paper have furniture?", "No. Its listing describes drawing tools (lines, rectangles, ellipses, text, measurements), and in our test the sheet starts blank: every shape is drawn by hand."),
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
          "furnishing your own rooms. In our tests on iOS 27, DrawPlan closed itself at every launch."),
    pick_them="you draw plans for work and want to trace existing drawings, on an iPhone it runs on.",
    pick_us="you are furnishing your own home and want to know what fits, without a subscription.",
    them_stronger=[
        ("Tracing", "Import a plan or photo and draw over it."),
        ("Drawing help", "Free sketching or to-scale drawing, plus AI that helps lay out the plan. The AI runs on credits sold separately, from $4.99 to $19.99 (US), and recent reviews describe it unable to place what it offered to."),
        ("Older iPhones and more languages", "It runs on iOS 15 or later, in 38 languages; Scooch needs iOS 26 and has 16."),
    ],
    us_stronger=[
        ("It opens", "Scooch runs on iOS 26 and iOS 27. In our tests on iOS 27.0.1, DrawPlan 6.0.1 closed itself at every launch."),
        ("A warning before you lift anything", "Scooch outlines in red a piece that overlaps another or sticks out of the room. DrawPlan's listing does not describe a check like that."),
        ("Your plans stay yours", "After the one-time unlock every plan opens, exports as PNG or PDF and syncs through your own iCloud. DrawPlan's listing puts sync and clean exports behind a subscription."),
    ],
    we_dont=[
        ("Trace a plan or photo.", "You type or drag the room's measurements."),
        ("Sketch freehand.", "Rooms and furniture snap to real sizes."),
        ("Charge monthly to sync or export.", "$9.99 once covers every plan, PNG and PDF export and iCloud sync."),
    ],
    reviews=[
        "having to subscribe to open a plan they had already drawn and saved (its 22 October update says saved plans are free to open again)",
        "saved plans that would not open or disappeared after an update",
        "no way to enter exact wall lengths or keep the plan to scale",
    ],
    pricing=("DrawPlan is free to download; its plans are $2.99 a month or $29.99 a year, Plus $4.99 or $49.99, "
             "and Pro $9.99 or $99.99, with AI credits from $4.99 to $19.99 (US). Scooch is a free download; "
             "planning needs a one-time $9.99 unlock."),
    faq=[
        ("Is DrawPlan free?", "It is a free download; per its listing, cloud sync, high-resolution exports and exports without grids or watermarks need a subscription, from $2.99 a month or $29.99 a year (US)."),
        ("Does DrawPlan work on iOS 27?", "Not in our tests on iOS 27.0.1: version 6.0.1 closed itself at every launch (23 October 2026). Its crash report points at a check iOS 27 now enforces on how apps start."),
        ("Does DrawPlan warn when furniture will not fit?", "Its listing does not describe a check like that, and we could not open it to test one. Scooch outlines a piece in red when it overlaps another or sticks out of the room."),
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
     "Scooch outlines in red any piece that overlaps another or sticks out of the room. On 23 October 2026 we took a "
     "furnished room in five of the others (Home Design 3D, Planner 5D, magicplan, Live Home 3D and Home Planner AI), "
     "moved the coffee table onto the sofa, and none of them flagged it; none of the other listings describe a check like that."),
    ("How were these apps chosen?",
     "From the top results for room and floor planner searches on the US App Store, keeping apps that plan rooms on "
     "iPhone and have an active listing. Facts come from each listing, purchase list, privacy label and recent public "
     "reviews, checked on 23 October 2026, and from using each app ourselves on an iPhone."),
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
