"""Build Holly's short Reels: recuts of existing voiced clips + still-image Reels."""
import pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
SEG = pathlib.Path("/tmp/claude-0/-home-user-MoProducts/15a480d9-b89d-548b-9477-e7573a5ed7ed/scratchpad/work")
SRC = ROOT / "src"; OUT = ROOT / "reels"; TMP = ROOT / "tmp"
OUT.mkdir(exist_ok=True); TMP.mkdir(exist_ok=True)
CTA = "Comment PUMPKIN for my free checklist"

# (output name, segment file, hook text, spoken text)
RECUTS = [
    ("01_ten_dollar_porch", "1_ten_dollar_porch_0", "$10 spooky porch challenge",
     "I gave myself ten dollars to make this porch look spooky. Let's see how bad this goes. Okay. Three dollars on cheesecloth, that's the ghosts."),
    ("02_free_pumpkins", "1_ten_dollar_porch_1", "Free pumpkins? Here's the trick",
     "Two on orange lights. The pumpkins were free, my neighbor grows way too many, she's practically begging people. So that's five."),
    ("03_sad_napkin_ghost", "1_ten_dollar_porch_2", "My DIY ghost looks like a sad napkin",
     "And the last five went on... wait, no, four fifty, I got change, on black paint. Is it perfect? No. One ghost looks like a sad napkin."),
    ("04_was_it_worth_it", "1_ten_dollar_porch_3", "Was my $10 porch worth it?",
     "But the neighbor kids screamed, so I'm calling it a win. It doesn't have to be perfect, it has to be ours. Follow for next week, I'm doing the mantel."),
    ("05_grandma_rule_one", "2_grandmas_rules_0", "Grandma's Halloween rule #1",
     "My grandmother had three rules for Halloween, and the second one still makes me cry. Rule one. Every costume is homemade. Mine were terrible. One year I was a pillowcase."),
    ("06_porch_light_rule", "2_grandmas_rules_1", "This Halloween rule makes me cry",
     "Rule two. Leave the porch light on late, because some kid out there has nobody to take them around, and they still deserve the good candy. She left it on till midnight."),
    ("07_stop_buying_now", "3_stop_buying_in_october_0", "Stop buying Halloween decor now",
     "If you're buying Halloween decorations right now, you're paying double. Here's when I buy. November first. The morning after. Everything's half off, sometimes more."),
    ("08_dollar_skeletons", "3_stop_buying_in_october_1", "$1 skeletons? Here's how",
     "That whole bin of skeletons back there? Like a dollar each. Okay, one was free, the cashier felt sorry for me. Right now I only buy what runs out. Lights. Candy. Cheesecloth."),
    ("09_tired_parents", "4_tired_parents_0", "Tired parents, watch this",
     "Tired parents, you don't need a Pinterest Halloween. You need two things. First, one tradition. Just one. Carving, a spooky movie, cocoa after trick-or-treating."),
    ("10_keep_it_small", "4_tired_parents_2", "Permission to keep Halloween small",
     "Store-bought costume? Fine. Cereal for dinner? Fine. They want you there, not stressed in the kitchen. Save this for the night you need it."),
]

# (output name, image, hook, list of slide texts)
STILLS = [
    ("11_porch_under_10", "hf_20261002_015254_32e066be-3f98-4a31-8223-5df2f044787f.png",
     "Expensive-looking porch for under $10",
     ["Cheesecloth ghosts · $3", "Orange string lights · $5", "Free pumpkins from neighbors", "Black spray paint · $4.50"]),
    ("12_carving_tips", "hf_20261002_015253_6c6a99dc-33b1-44dd-add2-37206bd4a66c.png",
     "3 jack-o'-lantern tips I swear by",
     ["Cut the lid at an angle", "Scrape the face wall thin", "Rub petroleum jelly on cuts"]),
    ("13_halloween_on_50", "hf_20261002_014634_05f232c3-4d91-4047-8872-4eaef999c165.png",
     "My whole Halloween costs $50",
     ["Porch · $18", "Inside decor · $10", "Costumes · $10", "Candy & party · $12"]),
]

STYLE = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,90,90,520,1
Style: Hook,DejaVu Sans,70,&H00FFFFFF,&H00FFFFFF,&H001E63D9,&H001E63D9,-1,0,0,0,100,100,0,0,3,22,0,8,70,70,220,1
Style: Cta,DejaVu Sans,60,&H00FFFFFF,&H00FFFFFF,&H00205C6F,&H00205C6F,-1,0,0,0,100,100,0,0,3,20,0,2,80,80,300,1
Style: Slide,DejaVu Sans,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,-1,0,0,0,100,100,0,0,3,26,0,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h, rem = divmod(max(t, 0), 3600); m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def chunks(text, n=4):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if len(cur) >= n or (re.search(r"[.?!,]$", w) and len(cur) >= 2):
            out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

def burn(src_args, ass, out, extra_vf=""):
    vf = (extra_vf + "," if extra_vf else "") + f"ass={ass}"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src_args, "-vf", vf,
                    "-c:v", "libx264", "-crf", "23", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], check=True)

for name, seg, hook, text in RECUTS:
    src = SEG / f"{seg}.mp4"; d = dur(src)
    ev = [f"Dialogue: 2,{ts(0)},{ts(2.5)},Hook,,0,0,0,,{hook}",
          f"Dialogue: 2,{ts(d-2.6)},{ts(d)},Cta,,0,0,0,,{CTA}"]
    start, end = 0.15, d - 0.35
    cs = chunks(text); w = [len(c) + 6 for c in cs]; t = start
    for c, wi in zip(cs, w):
        nt = t + (end - start) * wi / sum(w)
        ev.append(f"Dialogue: 0,{ts(t)},{ts(nt)},Cap,,0,0,0,,{c.upper()}"); t = nt
    ass = TMP / f"{name}.ass"; ass.write_text(STYLE + "\n".join(ev) + "\n")
    burn(["-i", str(src)], ass, OUT / f"holly_reel_{name}.mp4")
    print("built", name, round(d, 1), "s")

for name, img, hook, slides in STILLS:
    per = 2.2; d = 1.8 + per * len(slides) + 2.4
    ev = [f"Dialogue: 2,{ts(0)},{ts(d)},Hook,,0,0,0,,{hook}"]
    for i, s in enumerate(slides):
        a = 1.8 + per * i
        ev.append(f"Dialogue: 1,{ts(a)},{ts(1.8 + per * len(slides))},Slide,,0,0,{-260 + i * 150},,{{\\an5\\pos(540,{820 + i * 150})}}{s}")
    ev.append(f"Dialogue: 2,{ts(d-2.4)},{ts(d)},Cta,,0,0,0,,{CTA}")
    ass = TMP / f"{name}.ass"; ass.write_text(STYLE + "\n".join(ev) + "\n")
    frames = int(d * 30)
    zoom = (f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,scale=2160:3840,"
            f"zoompan=z='min(zoom+0.0006,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30")
    burn(["-loop", "1", "-i", str(SRC / img), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{d:.2f}", "-shortest"],
         ass, OUT / f"holly_reel_{name}.mp4", zoom)
    print("built", name, round(d, 1), "s")
