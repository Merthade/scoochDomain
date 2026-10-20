"""The /compare/ pages' content: one dict per app, rendered into the combined page and the
one-vs-one pages by build.py.

Rules (Holocron brand.md, decision 2026-10-20): every claim about another app comes from its
US App Store listing (description, In-App Purchases list) or its public US reviews, as
fetched on CHECKED by compare_fetch.py (facts and counts in compare_snapshot.json; listing and
review texts in compare_raw.json, local only: this repo is public); reviews are paraphrased, never
quoted at length; each page says who the other app suits better; Scooch's own limits are
listed; only Scooch's screenshots are shown; no superlative the data does not support; only
features in the live Scooch (1.0.2, checked against the shipped code: 37 catalogue pieces,
26 themes, PNG/PDF export, iCloud sync between your own devices, iPhone and iPad, 16
languages, iOS 26.0 or later).

Version, update date, rating, size, languages and minimum iOS are NOT typed here: build.py
reads them from the snapshot, so a re-fetch updates every page. Move CHECKED whenever the
snapshot is re-taken and the text below has been re-read against it.
"""

CHECKED = "2026-10-20"
CHECKED_TEXT = "20 October 2026"
OURS = "scooch"

# Row order of the one-vs-one "at a glance" table, and the combined table's capability columns.
FIT = "Warns when furniture overlaps or sticks out of the room"
SIZES = "Furniture at sizes you type"
HOW = "How you make the plan"
THREE_D = "3D view"

APPS = {
    "scooch": {
        "name": "Scooch",
        "developer": "Emils Ozols",
        "best_for": "Checking that furniture fits a room before you buy or move it",
        "how": "Type or drag the room's measurements, in 2D",
        "sizes": "Yes: 37 pieces, any size to the centimetre, plus pieces you draw",
        "fit": "Yes: overlaps and pieces outside the room are highlighted",
        "three_d": "No",
        "price": "Free download; $9.99 once to unlock planning",
        "price_detail": [
            "Free download. After the short intro, planning needs the one-time unlock: $9.99 (US).",
            "No subscription, no account. The unlock works on your iPhone and iPad with the same Apple Account.",
        ],
        "summary": ("A 2D planner built around one question: will it fit? You type or drag your "
                    "rooms to their real measurements, drop in furniture at real sizes, and "
                    "anything that overlaps or sticks out of the room is highlighted before you "
                    "lift it."),
        "pros": [
            "Flags furniture that overlaps another piece or sticks out of the room",
            "Every piece resizes to the centimetre or inch you type, and you can draw your own",
            "One-time $9.99, no subscription and no account",
            "11 MB download; iPhone and iPad, synced through your own iCloud",
            "26 colour themes and 16 languages",
        ],
        "cons": [
            "No 3D view, no renders, no camera or LiDAR scan: you measure and type",
            "Rooms are rectangles; L and U shapes are rooms joined together, no angled walls",
            "37 generic pieces: no brand catalogue, materials or decor",
            "Needs iOS 26 and an iPhone or iPad: no Mac, Android or web",
            "Planning needs the $9.99 unlock; only 2 US ratings so far",
        ],
    },

    "magicplan": {
        "name": "magicplan",
        "developer": "Technologies magicplan Inc.",
        "best_for": "Professionals capturing existing rooms for reports and estimates",
        "how": "Capture with the phone's camera, then edit",
        "sizes": "Objects and equipment on the plan (sizing not described in the listing)",
        "fit": "Not mentioned in its listing",
        "three_d": "Not mentioned in its listing",
        "price": "Free download; plans from $12.99/month or $129.99/year",
        "price_detail": [
            "Sketch Plan $12.99 a month or $129.99 a year, Report Plan $39.99 a month or $399.99 a year, "
            "Estimate Plan $89.99 a month or $899.99 a year (its US In-App Purchases list).",
        ],
        "summary": ("A floor plan tool for remodelers, restoration and insurance claims "
                    "professionals: you capture a room with the phone's camera and add photos, "
                    "notes, checklists, 360° panoramas, reports and estimates. Its listing names "
                    "Xactimate and CoreLogic integrations."),
        "pros": [
            "Builds the floor plan from the phone's camera, no extra hardware",
            "Photos, notes, forms, 360° panoramas, reports and estimates on the same plan",
            "Integrates with Xactimate and CoreLogic, per its listing",
            "4.7 stars from over 41,000 US ratings",
        ],
        "cons": [
            "Priced for businesses: the cheapest yearly plan is $129.99",
            "Its listing does not describe furniture fit checks",
            "5 languages; a 347 MB download",
        ],
        "theirs_stronger": [
            "It measures the room for you with the camera; Scooch needs you to measure and type.",
            "It is a working tool for jobs: photos, notes, forms, panoramas, reports and estimates sit on the plan.",
            "It connects to Xactimate and CoreLogic, which claims and restoration work relies on.",
            "Far more ratings: 4.7 stars from over 41,000 in the US.",
        ],
        "ours_stronger": [
            "It is built for furniture: 37 pieces at real sizes, resized to the centimetre, and your own drawn pieces.",
            "It highlights furniture that overlaps or sticks out of the room; magicplan's listing does not describe this.",
            "$9.99 once instead of a plan from $12.99 a month.",
            "16 languages and an 11 MB download, against 5 languages and 347 MB.",
        ],
        "verdict_theirs": "you work in remodeling, restoration or insurance claims and need plans, photos and estimates from the camera",
        "verdict_ours": "you are at home asking whether a sofa, bed or table will fit, and want a one-time price",
        "review_themes": [
            'Paying is the most common complaint: reviewers say scanning, more than one plan and even deleting a project need a subscription, and several found the pricing unclear before they started.',
            'Several say scans missed closets, walls or doors, or struggled with open-plan rooms and sloped ceilings.',
            'Several say a project did not save, or vanished after an update or an account change.',
            'Several call it hard to get started with.',
        ],
        "review_praise": 'The positive reviews praise the scanning and how quickly a usable plan comes together, including for trades work.',
    },

    "planner-5d": {
        "name": "Planner 5D",
        "developer": "Planner5D, UAB",
        "best_for": "3D interior design with a large furniture catalogue",
        "how": "Draw in 2D and switch to 3D; camera capture; AI design",
        "sizes": "Premium only: its listing says the free version has no furniture customization",
        "fit": "Not mentioned in its listing",
        "three_d": "Yes",
        "price": "Free with limits; subscriptions from $7.99/week",
        "price_detail": [
            "Its US In-App Purchases list shows subscriptions from $7.99 a week and $19.99 a month to "
            "$29.99, $69.99 and $119.99 a year, plus full-catalogue access at $6.99 for 30 days or $15.99 a year.",
            "Its own listing text quotes $9.99 a month or $59.99 a year, and notes prices vary by region.",
        ],
        "summary": ("A 2D and 3D home design app with a catalogue of over 8,400 items, photo-like "
                    "'Snapshot' renders, AI design generation and 3D capture with the phone's "
                    "camera. The free version has 150+ items and no furniture customization; the "
                    "rest is a subscription."),
        "pros": [
            "2D and 3D, with photo-like renders",
            "Over 8,400 furniture and decor items with premium",
            "Works across platforms and offline, per its listing; Apple Pencil and Vision Pro support",
            "24 languages",
        ],
        "cons": [
            "Changing furniture sizes needs premium",
            "Subscription pricing, many tiers",
            "A 980 MB download; its listing does not describe fit checks",
        ],
        "theirs_stronger": [
            "It shows your room in 3D and renders photo-like images; Scooch is 2D only.",
            "Its catalogue is far larger: over 8,400 items with premium, against Scooch's 37 generic pieces.",
            "It runs on more platforms and supports Apple Pencil and Vision Pro, per its listing.",
            "24 languages against Scooch's 16, and far more ratings (over 42,000 in the US).",
        ],
        "ours_stronger": [
            "Every piece resizes to the centimetre with the $9.99 unlock; Planner 5D's free version has no furniture customization.",
            "It highlights furniture that overlaps or sticks out of the room; Planner 5D's listing does not describe this.",
            "One payment of $9.99 instead of a subscription.",
            "An 11 MB download against 980 MB.",
        ],
        "verdict_theirs": "you want to see the room in 3D, style it from a big catalogue and render it",
        "verdict_ours": "you need exact sizes and a clear answer on what fits, without a subscription",
        "review_themes": [
            'Billing is the most common complaint by far: many say a free trial turned into a charge they did not expect, and that refunds were hard to get.',
            'Several say scans, downloads and other features each ask for another purchase.',
            'Several call it confusing, slow or prone to freezing.',
            'A few say saved projects reverted or partly disappeared.',
        ],
        "review_praise": 'The positive reviews praise it for interior design and the room scan.',
    },

    "home-planner-ai": {
        "name": "Home Planner AI",
        "developer": "Room Planner Ltd",
        "best_for": "3D room design with a scanner, measure tools and renders",
        "how": "Draw in 2D or 3D, or scan the room with the built-in 3D scanner",
        "sizes": "Not described in its listing",
        "fit": "Not mentioned in its listing",
        "three_d": "Yes",
        "price": "Free download; purchases from $5.99, subscriptions from $17.99/week",
        "price_detail": [
            "Its US In-App Purchases list shows Interior Design $5.99, Floor plan creator from $6.99 to "
            "$74.99, Architecture $14.99, Design & Room maker $49.99, 6-month subscriptions at $29.99 and "
            "$34.99, and a Weekly Business plan at $17.99.",
        ],
        "summary": ("A 2D and 3D design app with a built-in 3D scanner, a digital tape measure, AI "
                    "design and realistic renders. Premium unlocks the full catalogue, unlimited "
                    "projects, renders and the scanner and measure tools."),
        "pros": [
            "Built-in 3D scanner and measure tools",
            "2D and 3D, with realistic renders",
            "30 languages, the most in this comparison",
            "4.6 stars from over 46,000 US ratings",
        ],
        "cons": [
            "Scanner, measure tools, full catalogue and unlimited projects are premium",
            "Ten different purchases on its US list, which makes the real price hard to read",
            "A 1.4 GB download; its listing does not describe fit checks",
        ],
        "theirs_stronger": [
            "It can scan the room and measure it for you; with Scooch you measure and type.",
            "It shows the room in 3D with realistic renders; Scooch is 2D only.",
            "30 languages against Scooch's 16, and over 46,000 US ratings.",
        ],
        "ours_stronger": [
            "It highlights furniture that overlaps or sticks out of the room; Home Planner AI's listing does not describe this.",
            "One price, $9.99 once, against a list of ten purchases and subscriptions.",
            "An 11 MB download against about 1.4 GB.",
        ],
        "verdict_theirs": "you want to scan the room and design it in 3D with renders",
        "verdict_ours": "you want to check what fits at exact sizes, for one clear price",
        "review_themes": [
            "The free version is the most common complaint: several say it is too limited to use, including one reviewer who could not type a room's size without subscribing.",
            'Several mention freezing, crashes and slow loading.',
            'A few find it confusing or say the buttons are too small to select things, especially on iPad.',
        ],
        "review_praise": 'Over half of these reviews give five stars, mostly saying how much fun it is to design rooms.',
    },

    "home-design-3d": {
        "name": "Home Design 3D",
        "developer": "Home Design 3D srl",
        "best_for": "Designing a whole house over several floors, in 3D",
        "how": "Draw in 2D, view in 3D; import a blueprint and trace it",
        "sizes": "Yes, per its listing (customize furniture size)",
        "fit": "Not mentioned in its listing",
        "three_d": "Yes",
        "price": "Subscriptions from $4.99/week",
        "price_detail": [
            "Its US In-App Purchases list shows Weekly premium $4.99, monthly plans $12.99 to $22.99, and "
            "yearly plans from $44.99 to $79.99.",
        ],
        "summary": ("A house designer: draw floor plans in 2D and walk through them in 3D, over "
                    "unlimited floors, with thousands of items, photorealistic rendering, VR "
                    "export and blueprint import for tracing. Premium features are a subscription."),
        "pros": [
            "Multi-storey houses, walls with adjustable thickness, height and angles",
            "Thousands of items, with furniture sizes you can change",
            "3D walkthrough, photorealistic rendering, VR export",
            "The most ratings in this comparison: over 104,000 in the US",
        ],
        "cons": [
            "Premium is a subscription",
            "A 987 MB download",
            "Its listing does not describe fit checks",
        ],
        "theirs_stronger": [
            "It designs whole houses: several floors, angled walls, a 3D walkthrough and VR export.",
            "Thousands of items against Scooch's 37 generic pieces.",
            "You can import a blueprint and draw over it.",
            "18 languages against 16, and over 104,000 US ratings.",
        ],
        "ours_stronger": [
            "It highlights furniture that overlaps or sticks out of the room; Home Design 3D's listing does not describe this.",
            "$9.99 once instead of a subscription from $4.99 a week.",
            "An 11 MB download against 987 MB.",
        ],
        "verdict_theirs": "you are planning a house or a renovation over several floors and want to see it in 3D",
        "verdict_ours": "you have the room already and want to know whether the furniture fits",
        "review_themes": [
            'The move to subscriptions is the most common complaint: many long-time users who bought the one-time Gold edition or content packs say they lost access after updates and are now asked to subscribe.',
            'Several say most items and tools are locked, and that ads interrupt projects.',
            'Several mention crashes after recent updates, including projects that no longer open.',
        ],
        "review_praise": 'The positive reviews praise it as an enjoyable way to design houses.',
    },

    "keyplan-3d": {
        "name": "Keyplan 3D Lite",
        "developer": "Quasarts LLC",
        "best_for": "Building a home's shape and decorating it in 2D and 3D",
        "how": "Draw walls like pencil lines, any shape; edit in 2D or 3D",
        "sizes": "Not described in its listing",
        "fit": "Not mentioned in its listing",
        "three_d": "Yes",
        "price": "Free download; Standard version $5.99 once",
        "price_detail": [
            "Its US In-App Purchases list shows the Standard version at $5.99 and object packs from $1.99 "
            "to $2.99 (a $23.90 Starter Pack is also featured on the page).",
        ],
        "summary": ("A home builder and interior designer: draw walls in any shape, then place "
                    "furniture, windows and doors in 2D or 3D, and paint and decorate any surface. "
                    "350+ objects are free and the projects sync through iCloud."),
        "pros": [
            "Walls in any shape, edited in 2D or 3D",
            "350+ free objects, plus paints and materials",
            "A one-time Standard upgrade at $5.99, lower than Scooch's $9.99",
            "iCloud sync between iPhone and iPad",
        ],
        "cons": [
            "Extra objects come as paid packs",
            "Its listing does not describe fit checks",
            "A 663 MB download; last updated in August 2026",
        ],
        "theirs_stronger": [
            "Walls can take any shape; Scooch's rooms are rectangles you join.",
            "It shows the plan in 3D and lets you paint and decorate surfaces.",
            "Its one-time Standard upgrade is $5.99, cheaper than Scooch's $9.99.",
            "Over 52,000 US ratings.",
        ],
        "ours_stronger": [
            "It highlights furniture that overlaps or sticks out of the room; Keyplan's listing does not describe this.",
            "Every piece resizes to the centimetre you type, and you can draw your own pieces.",
            "16 languages against 10, and an 11 MB download against 663 MB.",
        ],
        "verdict_theirs": "you want to build a home's shape freely and decorate it in 3D, at a low one-time price",
        "verdict_ours": "you want exact furniture sizes and a warning when something does not fit",
        "review_themes": [
            'The limits of the Lite version are the most common complaint: several say more rooms, floors or paint textures need a purchase.',
            'A few mention plans lost when moving to a new phone, or that sizing spaces precisely is hard.',
        ],
        "review_praise": 'Most of these reviews are positive, calling it easy to use and worth the money.',
    },

    "live-home-3d": {
        "name": "Live Home 3D",
        "developer": "Belight Software, ltd",
        "best_for": "Detailed 3D house and interior design with realistic renders",
        "how": "Draw 2D plans, walk through in 3D; LiDAR room scan; AR",
        "sizes": "Not described in its listing",
        "fit": "Not mentioned in its listing",
        "three_d": "Yes",
        "price": "Free version with limits; Standard from $5.99/month or $59.99 once",
        "price_detail": [
            "Standard Features: $5.99 a month, $19.99 a year or $59.99 lifetime. Pro Features: $14.99 a "
            "month, $39.99 a year or $129.99 lifetime. Content packs at $5.99 (its US In-App Purchases list).",
            "Per its listing, the free version watermarks exports and allows one project at a time.",
        ],
        "summary": ("A full home, interior and landscape design app: 2D plans, 3D walkthroughs, "
                    "5,000+ items and 3,000+ materials, a LiDAR room scanner, AR, realistic "
                    "renders and video. Projects move between iOS, iPadOS, visionOS, macOS and "
                    "Windows."),
        "pros": [
            "5,000+ items and 3,000+ materials, plus imports from 3D Warehouse and Sketchfab",
            "LiDAR room scanning and AR, per its listing",
            "Renders, flyover videos and 360° panoramas",
            "Lifetime purchase options, and Mac and Windows versions",
        ],
        "cons": [
            "Free version watermarks exports and keeps one project at a time",
            "Its listing does not describe fit checks",
            "A 554 MB download",
        ],
        "theirs_stronger": [
            "It is a full 3D design tool: walkthroughs, renders, video, roofs, terrain and lighting.",
            "It can scan a room with LiDAR (on devices that have it); Scooch needs you to measure.",
            "5,000+ items and 3,000+ materials, and it runs on Mac and Windows too.",
            "Over 19,000 US ratings.",
        ],
        "ours_stronger": [
            "It highlights furniture that overlaps or sticks out of the room; Live Home 3D's listing does not describe this.",
            "Everything in Scooch is $9.99 once; Live Home 3D's lifetime Standard upgrade is $59.99.",
            "16 languages against 11, and an 11 MB download against 554 MB.",
        ],
        "verdict_theirs": "you want detailed 3D design, renders and video, on Apple devices and Windows",
        "verdict_ours": "you only need to know whether your furniture fits, for $9.99",
        "review_themes": [
            'A few say they were locked out of their one free project until they paid.',
            'A few mention purchases or projects not carrying across devices, crashes on large models and slow loading.',
            'A few say it does not explain where to start.',
        ],
        "review_praise": 'Most of these reviews are positive, praising the results and calling it quick to learn.',
    },

    "draft-paper": {
        "name": "Draft Paper",
        "developer": "Giles Goddard",
        "best_for": "Quick, precise 2D drawings and DXF export",
        "how": "Draw lines, rectangles and text on layers",
        "sizes": "No furniture catalogue: you draw shapes to scale",
        "fit": "Not mentioned in its listing",
        "three_d": "No",
        "price": "Free download; All Features $9.99 once",
        "price_detail": [
            "All Features: $9.99, one time (its US In-App Purchases list).",
        ],
        "summary": ("A simple 2D drafting app: lines, rectangles, ellipses, text and measurements on "
                    "up to 10 layers, exported as PDF, JPEG or DXF. It is made by one developer "
                    "and costs $9.99 once, the same as Scooch."),
        "pros": [
            "Same one-time $9.99, no subscription",
            "A 2 MB download, the smallest here, and runs on iOS 15",
            "Exports PDF, JPEG and DXF for CAD software",
            "Layers, Apple Pencil support, unlimited undo",
        ],
        "cons": [
            "No furniture: rooms and pieces are shapes you draw",
            "Its listing does not describe fit checks",
            "English only",
        ],
        "theirs_stronger": [
            "It draws anything, not only rooms and furniture, on up to 10 layers.",
            "It exports DXF, so the drawing opens in CAD software.",
            "It runs on iOS 15 or later; Scooch needs iOS 26.",
            "A 2 MB download, and over 15,000 US ratings.",
        ],
        "ours_stronger": [
            "Furniture is ready made: 37 pieces at real sizes, resized to the centimetre, instead of shapes you draw.",
            "It highlights furniture that overlaps or sticks out of the room.",
            "16 languages against English only.",
        ],
        "verdict_theirs": "you want a general drafting tool with layers and DXF export",
        "verdict_ours": "you want rooms and furniture that already know their sizes and warn you when they do not fit",
        "review_themes": [
            'Several long-time users say a recent update (1.19.5) changed scrolling and undo and made drawing harder.',
            'Several mention crashes, some losing minutes of work, including with Apple Pencil on iPad.',
            'Several could not switch between metric and imperial, or import an image.',
        ],
        "review_praise": 'The positive reviews call it simple, flexible and good enough for daily work.',
    },

    "drawplan": {
        "name": "DrawPlan",
        "developer": "Fleet Investments LLC",
        "best_for": "To-scale 2D plans for trades and real estate, with tracing",
        "how": "Sketch freely or draw to scale; trace imported plans; AI help",
        "sizes": "Furniture objects and your own saved objects (sizing not described)",
        "fit": "Not mentioned in its listing",
        "three_d": "Not mentioned in its listing",
        "price": "Subscriptions from $2.99/month",
        "price_detail": [
            "DrawPlan $2.99 a month or $29.99 a year, Plus $4.99 a month or $49.99 a year, Pro $9.99 a month "
            "or $99.99 a year, AI Credits $4.99 to $19.99 (its US In-App Purchases list).",
            "Per its listing, premium is needed for cloud sync, high-resolution exports and exports without grids or watermarks.",
        ],
        "summary": ("A 2D floor plan app for quick sketches or to-scale drawings with automatic "
                    "dimensions. You can import an image or plan and trace it, save your own "
                    "objects, and ask its AI to help draw. Premium is a subscription."),
        "pros": [
            "Sketch freely or draw to scale with automatic dimensions",
            "Import a plan or photo and trace over it",
            "AI-assisted drawing and custom objects",
            "Runs on iOS 13 or later",
        ],
        "cons": [
            "Subscription for sync, high-resolution exports and clean exports",
            "3.5 stars from about 5,300 US ratings",
            "English only; its listing does not describe fit checks",
        ],
        "theirs_stronger": [
            "You can import a plan or photo and trace it.",
            "AI can help draw the plan, and it supports free sketching as well as to-scale drawing.",
            "It runs on iOS 13 or later; Scooch needs iOS 26.",
        ],
        "ours_stronger": [
            "It highlights furniture that overlaps or sticks out of the room; DrawPlan's listing does not describe this.",
            "$9.99 once, with PNG and PDF export and iCloud sync included, instead of a subscription.",
            "16 languages against English only.",
        ],
        "verdict_theirs": "you draw plans for work and want to trace existing drawings",
        "verdict_ours": "you are furnishing your own home and want to know what fits",
        "review_themes": [
            'Paying to reopen your own plan is the most common complaint by far: many reviewers drew and saved a plan, then found they had to subscribe to open it again.',
            'Several say saved plans would not open or disappeared after an update.',
            'Several say they could not enter exact wall lengths or keep the plan to scale.',
        ],
        "review_praise": 'The positive reviews call it straightforward for a quick plan.',
    },
}

# Combined-page order: Scooch first (disclosed), then by US rating count, so the order
# follows a public number rather than our preference.
ORDER = ["scooch", "home-design-3d", "keyplan-3d", "home-planner-ai", "planner-5d",
         "magicplan", "live-home-3d", "draft-paper", "drawplan"]
