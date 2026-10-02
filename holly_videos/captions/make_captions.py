"""Burn word-chunk captions + an opening hook onto Holly's four videos.

Timing comes from each voiceover part's real duration; words inside a part are
spread proportionally to their length (no speech recognition available here).
"""
import pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
SEG = pathlib.Path("/tmp/claude-0/-home-user-MoProducts/15a480d9-b89d-548b-9477-e7573a5ed7ed/scratchpad/work")

VIDEOS = {
    "1_ten_dollar_porch": ("$10 spooky porch. Can I do it?", [
        "I gave myself ten dollars to make this porch look spooky. Let's see how bad this goes. Okay. Three dollars on cheesecloth, that's the ghosts.",
        "Two on orange lights. The pumpkins were free, my neighbor grows way too many, she's practically begging people. So that's five.",
        "And the last five went on... wait, no, four fifty, I got change, on black paint. Is it perfect? No. One ghost looks like a sad napkin.",
        "But the neighbor kids screamed, so I'm calling it a win. It doesn't have to be perfect, it has to be ours. Follow for next week, I'm doing the mantel.",
    ]),
    "2_grandmas_rules": ("My grandma's 3 Halloween rules", [
        "My grandmother had three rules for Halloween, and the second one still makes me cry. Rule one. Every costume is homemade. Mine were terrible. One year I was a pillowcase.",
        "Rule two. Leave the porch light on late, because some kid out there has nobody to take them around, and they still deserve the good candy. She left it on till midnight.",
        "Rule three, nobody eats until everybody's home. I still follow all three. Well, mostly. Got a rule like that? Tell me in the comments.",
    ]),
    "3_stop_buying_in_october": ("You're paying double for Halloween decor", [
        "If you're buying Halloween decorations right now, you're paying double. Here's when I buy. November first. The morning after. Everything's half off, sometimes more.",
        "That whole bin of skeletons back there? Like a dollar each. Okay, one was free, the cashier felt sorry for me. Right now I only buy what runs out. Lights. Candy. Cheesecloth.",
        "Honestly, just have a plan before you walk in the store, that's when the cart fills up. My fifty-dollar Halloween guide is in my bio.",
    ]),
    "4_tired_parents": ("Tired parents: you only need 2 things", [
        "Tired parents, you don't need a Pinterest Halloween. You need two things. First, one tradition. Just one. Carving, a spooky movie, cocoa after trick-or-treating.",
        "That's what they remember. Not the decorations. Nobody remembers what was on this porch, but they remember the cocoa. Second... permission to keep it small.",
        "Store-bought costume? Fine. Cereal for dinner? Fine. They want you there, not stressed in the kitchen. Save this for the night you need it.",
    ]),
}

HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,DejaVu Sans,74,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,-1,0,0,0,100,100,0,0,1,6,2,2,90,90,520,1
Style: Hook,DejaVu Sans,72,&H00FFFFFF,&H00FFFFFF,&H001E63D9,&H001E63D9,-1,0,0,0,100,100,0,0,3,22,0,8,80,80,230,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ts(t):
    h, rem = divmod(max(t, 0), 3600); m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

def chunks(text, n=4):
    words = text.split()
    out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= n or re.search(r"[.?!,]$", w) and len(cur) >= 2:
            out.append(" ".join(cur)); cur = []
    if cur: out.append(" ".join(cur))
    return out

def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]))

for name, (hook, parts) in VIDEOS.items():
    lines, offset = [], 0.0
    lines.append(f"Dialogue: 1,{ts(0)},{ts(2.6)},Hook,,0,0,0,,{hook}")
    for i, text in enumerate(parts):
        d = dur(SEG / f"{name}_{i}.mp4")
        start, end = offset + 0.15, offset + d - 0.35
        cs = chunks(text)
        weights = [len(c) + 6 for c in cs]  # +6 ≈ pause between phrases
        total, t = sum(weights), start
        for c, w in zip(cs, weights):
            nt = t + (end - start) * w / total
            lines.append(f"Dialogue: 0,{ts(t)},{ts(nt)},Cap,,0,0,0,,{c.upper()}")
            t = nt
        offset += d
    ass = ROOT / f"{name}.ass"
    ass.write_text(HEADER + "\n".join(lines) + "\n")
    src = ROOT.parent / f"holly_{name}.mp4"
    out = ROOT / f"holly_{name}_captioned.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", f"ass={ass}",
                    "-c:v", "libx264", "-crf", "24", "-preset", "medium", "-c:a", "copy",
                    "-movflags", "+faststart", str(out)], check=True)
    print("built", out.name)
