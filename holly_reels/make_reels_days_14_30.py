"""Build Holly's Reels for days 14-30 (Oct 17 - Nov 2). Free: uses existing clips, photos and product pages."""
import pathlib, subprocess, shutil

HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / "make_reels.py").read_text()
exec(src.split("for name, seg, hook, text in RECUTS:")[0])  # helpers, STYLE, RECUTS, paths

REPO = HERE.parent
OUT = HERE / "reels_days_14_30"; OUT.mkdir(exist_ok=True)
TMP = HERE / "tmp"; TMP.mkdir(exist_ok=True)
TEXT = {seg: text for _, seg, _, text in RECUTS}
PUMPKIN = "Comment PUMPKIN for my free checklist"
PORCH, CARVE, PORTRAIT, CRAFT = (SRC / "hf_20261002_015254_32e066be-3f98-4a31-8223-5df2f044787f.png",
                                 SRC / "hf_20261002_015253_6c6a99dc-33b1-44dd-add2-37206bd4a66c.png",
                                 SRC / "hf_20261002_005210_5aa827e3-6eb8-47e6-9544-cbdfa72df2e4.png",
                                 SRC / "hf_20261002_014634_05f232c3-4d91-4047-8872-4eaef999c165.png")
XMAS = REPO / "holly_christmas/holly_images/holly_christmas_planner.png"

def pages(pdf, nums):
    d = TMP / pdf.stem; d.mkdir(exist_ok=True)
    subprocess.run(["pdftoppm", "-r", "110", "-png", str(pdf), str(d / "p")], check=True)
    files = sorted(d.glob("p-*.png"))
    return [files[n - 1] for n in nums]

def repost(name, seg, hook, cta=PUMPKIN):
    s = SEG / f"{seg}.mp4"; d = dur(s); text = TEXT[seg]
    ev = [f"Dialogue: 2,{ts(0)},{ts(2.5)},Hook,,0,0,0,,{hook}", f"Dialogue: 2,{ts(d-2.6)},{ts(d)},Cta,,0,0,0,,{cta}"]
    cs = chunks(text); w = [len(c) + 6 for c in cs]; t, end = 0.15, d - 0.35
    for c, wi in zip(cs, w):
        nt = t + (end - 0.15) * wi / sum(w); ev.append(f"Dialogue: 0,{ts(t)},{ts(nt)},Cap,,0,0,0,,{c.upper()}"); t = nt
    ass = TMP / f"{name}.ass"; ass.write_text(STYLE + "\n".join(ev) + "\n")
    burn(["-i", str(s)], ass, OUT / f"holly_reel_{name}.mp4")

def still(name, img, hook, slides, cta=PUMPKIN):
    per = 2.2; d = 1.8 + per * len(slides) + 2.4
    ev = [f"Dialogue: 2,{ts(0)},{ts(d)},Hook,,0,0,0,,{hook}"]
    for i, s in enumerate(slides):
        ev.append(f"Dialogue: 1,{ts(1.8 + per * i)},{ts(1.8 + per * len(slides))},Slide,,0,0,0,,{{\\an5\\pos(540,{800 + i * 140})}}{s}")
    ev.append(f"Dialogue: 2,{ts(d-2.4)},{ts(d)},Cta,,0,0,0,,{cta}")
    ass = TMP / f"{name}.ass"; ass.write_text(STYLE + "\n".join(ev) + "\n")
    frames = int(d * 30)
    zoom = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=2160:3840,"
            f"zoompan=z='min(zoom+0.0006,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30")
    burn(["-loop", "1", "-i", str(img), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{d:.2f}", "-shortest"],
         ass, OUT / f"holly_reel_{name}.mp4", zoom)

def product(name, pdf, nums, hook, labels, cta, bg="0xfbf6ee", per=2.6):
    clips = []
    for i, p in enumerate(pages(pdf, nums)):
        c = TMP / f"{name}_{i}.mp4"; frames = int(per * 30)
        vf = (f"scale=900:-1,pad=1080:1920:(ow-iw)/2:(oh-ih)/2+80:color={bg},scale=2160:3840,"
              f"zoompan=z='min(zoom+0.0008,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(p), "-t", f"{per}", "-vf", vf,
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", str(c)], check=True)
        clips.append(c)
    lst = TMP / f"{name}.txt"; lst.write_text("".join(f"file '{c}'\n" for c in clips))
    joined = TMP / f"{name}_joined.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)], check=True)
    d = per * len(clips)
    ev = [f"Dialogue: 2,{ts(0)},{ts(d)},Hook,,0,0,0,,{hook}"]
    for i, l in enumerate(labels):
        ev.append(f"Dialogue: 1,{ts(per * i + 0.3)},{ts(min(per * (i + 1), d - 2.3))},Slide,,0,0,0,,{{\\an5\\pos(540,1700)}}{l}")
    ev.append(f"Dialogue: 2,{ts(d-2.2)},{ts(d)},Cta,,0,0,0,,{cta}")
    ass = TMP / f"{name}.ass"; ass.write_text(STYLE + "\n".join(ev) + "\n")
    burn(["-i", str(joined), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-shortest"], ass, OUT / f"holly_reel_{name}.mp4")

GUIDE = REPO / "holly_products/halloween_on_50.pdf"
CHECK = REPO / "holly_products/free_halloween_checklist.pdf"
PLANNER = REPO / "holly_christmas/christmas_budget_gift_planner.pdf"

repost("day14_oct17_still_not_decorated", "1_ten_dollar_porch_0", "Still not decorated? Watch this")
still("day15_oct18_two_weeks_out", PORCH, "2 weeks to Halloween. Do these 4 things",
      ["1. Hang the lights first", "2. Make ghosts tonight", "3. Plan one costume", "4. Buy candy last"])
product("day16_oct19_halloween_plan", GUIDE, [1, 2, 3, 4, 5], "My whole Halloween plan, $50 total",
        ["The guide", "The $50 budget", "Porch DIYs", "Costumes for $0-3", "Week-by-week timeline"], "Full plan in my shop, link in bio")
still("day17_oct20_cheap_costumes", CARVE, "Costumes for $0-3 each",
      ["Black cat · $2", "Scarecrow · $3", "Ghost · $0", "Witch · $3", "Skeleton · $3"])
repost("day18_oct21_porch_light_rule", "2_grandmas_rules_1", "Grandma's rule that still makes me cry")
still("day19_oct22_three_mistakes", PORTRAIT, "3 Halloween mistakes that cost you money",
      ["Buying decor in October", "Buying candy too early", "Shopping without a list"])
repost("day20_oct23_write_this_date", "3_stop_buying_in_october_1", "Write this date down: Nov 1")
still("day21_oct24_paper_bats", CRAFT, "Weekend craft: $1 paper bats",
      ["Trace one bat", "Cut 20 from black paper", "Fold the wings", "Tape them up the wall"])
repost("day22_oct25_one_week_left", "4_tired_parents_0", "One week left, tired parents")
still("day23_oct26_halloween_night", PORCH, "Halloween night timeline",
      ["3pm · cider on", "Dusk · test the lights", "6pm · porch light ON", "Save the good candy for last"])
product("day24_oct27_free_checklist", CHECK, [1], "The free checklist everyone's asking for",
        ["Fridge-ready, 4 weeks to Nov 1"], PUMPKIN, per=9)
repost("day25_oct28_favorite_ghost", "1_ten_dollar_porch_2", "Still my favorite ghost")
still("day26_oct29_cocoa_bar", PORTRAIT, "Cocoa bar for $5",
      ["Cocoa mix", "Mini marshmallows", "Crushed candy canes", "Whipped cream"])
repost("day27_oct30_homemade_costume", "2_grandmas_rules_0", "Homemade costume? Even if it's terrible")
still("day28_oct31_happy_halloween", PORCH, "Happy Halloween from my porch",
      ["It doesn't have to be perfect.", "It has to be ours."], "Leave the porch light on tonight")
product("day29_nov01_christmas_planner", PLANNER, [1, 3, 4, 11], "54 days to Christmas. Start your list today",
        ["The planner", "Budget by category", "Gift list", "Shipping deadlines"], "Planner in my shop, link in bio")
still("day30_nov02_budget_rule", XMAS, "The 75/25 Christmas budget rule",
      ["75% for gifts", "25% for sneaky extras", "Wrapping · shipping", "Stockings · gift swaps"], "Comment GIFT for my free gift list")
shutil.rmtree(TMP)
print("built", len(list(OUT.glob("*.mp4"))), "reels")
