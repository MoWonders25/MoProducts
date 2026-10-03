"""Build Holly's printable gift tags and 25-day Christmas countdown calendar."""
import pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

def pdf(name, html):
    f = ROOT / f"{name}.html"; f.write_text(html)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={ROOT / (name + '.pdf')}", f"file://{f}"], check=True, stderr=subprocess.DEVNULL)

FOOT = "© Holly Bramble · @hollybrambledaysathome · personal use only"

# ---------------- GIFT TAGS ----------------
STYLES = {
    "classic": dict(bg="#b3262d", fg="#fff", accent="#c9a24a", line="rgba(255,255,255,.7)", icon="🎄", font="Georgia,serif",
                    words=["Merry Christmas", "Ho Ho Ho", "Season's Greetings", "Joy to You", "Merry & Bright", "Happy Holidays"]),
    "rustic":  dict(bg="#c8a77e", fg="#3b2a1a", accent="#2f5d46", line="rgba(59,42,26,.6)", icon="🌲", font="'Courier New',monospace",
                    words=["Merry Christmas", "Made with Love", "Warm Wishes", "Peace & Joy", "Cozy Christmas", "Happy Holidays"]),
    "cream":   dict(bg="#fbf6ee", fg="#2f5d46", accent="#b3262d", line="rgba(47,93,70,.55)", icon="❄️", font="'Helvetica Neue',Arial,sans-serif",
                    words=["Merry Christmas", "Let It Snow", "Joy", "Believe", "Merry & Bright", "Happy Holidays"]),
}

def tag_page(s, blank=False):
    tags = ""
    for i in range(12):
        word = "" if blank else s["words"][i % len(s["words"])]
        tags += f"""<div class='tag' style='background:{s["bg"]};color:{s["fg"]};font-family:{s["font"]}'>
          <div class='hole'></div>
          <div class='icon'>{s["icon"]}</div>
          <div class='word' style='color:{s["fg"]}'>{word}</div>
          <div class='rule' style='background:{s["accent"]}'></div>
          <div class='field'>To:<span style='border-color:{s["line"]}'></span></div>
          <div class='field'>From:<span style='border-color:{s["line"]}'></span></div>
        </div>"""
    return f"<div class='page'><div class='grid'>{tags}</div><div class='foot'>{FOOT} · Cut along the dotted lines, punch the circle, add ribbon.</div></div>"

TAG_CSS = """@page{size:Letter;margin:0.4in}*{box-sizing:border-box}body{margin:0}
.page{page-break-after:always}.page:last-child{page-break-after:auto}
.grid{display:grid;grid-template-columns:repeat(3,2.45in);grid-auto-rows:2.35in;gap:0.12in;justify-content:center}
.tag{position:relative;border:1.5px dashed #999;border-radius:14px;padding:0.32in 0.18in 0.12in;text-align:center;overflow:hidden}
.hole{position:absolute;top:0.1in;left:50%;width:0.18in;height:0.18in;margin-left:-0.09in;border-radius:50%;background:#fff;border:1px solid #bbb}
.icon{font-size:26pt;line-height:1.1}.word{font-size:15pt;font-weight:700;margin-top:2px;min-height:22pt}
.rule{height:2px;width:60%;margin:5px auto 8px}
.field{font-size:10pt;text-align:left;margin:5px 4px;display:flex;gap:6px}.field span{flex:1;border-bottom:1.2px solid}
.foot{text-align:center;font:8pt Arial,sans-serif;color:#999;margin-top:8px}
.cover{height:9.9in;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;font-family:Georgia,serif;background:#fbf6ee;border:3px solid #c9a24a;border-radius:18px}
.cover h1{font:900 38pt 'Helvetica Neue',Arial,sans-serif;color:#b3262d;margin:10px 0}"""

tag_pages = ["""<div class='page'><div class='cover'><div style='font-size:50pt'>🎁</div>
<h1>Printable Christmas<br>Gift Tags</h1><p style='font-size:14pt'>3 styles · 36 tags + 36 blank tags<br>Print, cut, punch, tie. Done.</p>
<p style='margin-top:30px;font:11pt Arial,sans-serif;color:#7a6e64'>Tip: print on cardstock (65–110 lb) for sturdy tags.<br>Use "Actual size" / 100% in your print settings.</p>
<p style='margin-top:30px;font-style:italic'>by Holly Bramble · @hollybrambledaysathome</p></div></div>"""]
for s in STYLES.values():
    tag_pages += [tag_page(s), tag_page(s, blank=True)]
pdf("christmas_gift_tags", f"<!doctype html><html><head><meta charset='utf-8'><style>{TAG_CSS}</style></head><body>{''.join(tag_pages)}</body></html>")

# ---------------- COUNTDOWN CALENDAR ----------------
ACTS = ["Write letters to Santa", "Make paper snowflakes", "Watch a Christmas movie in PJs", "Bake Christmas cookies",
        "Drive around to see the lights", "Make a paper chain", "Read a Christmas story by flashlight", "Hot cocoa bar night",
        "Donate a toy or coat", "Make homemade ornaments", "Christmas music dance party", "Build a blanket fort & read",
        "Make cards for neighbors", "Decorate gingerbread (or graham crackers)", "Family game night", "String popcorn garland",
        "Take a winter nature walk", "Do a secret kindness for someone", "Make salt dough handprints", "Christmas pajama photo",
        "Wrap a gift for someone special", "Leave a treat for the mail carrier", "Christmas craft afternoon",
        "Christmas Eve: new book & cocoa", "Merry Christmas! Read the Christmas story together"]

CD_CSS = """@page{size:Letter;margin:0.45in}*{box-sizing:border-box}body{margin:0;font-family:Georgia,serif;color:#2b2420}
.page{page-break-after:always;position:relative;height:9.9in;overflow:hidden}.page:last-child{page-break-after:auto}
h1{font:900 34pt 'Helvetica Neue',Arial,sans-serif;color:#b3262d;margin:0}h2{font:700 20pt 'Helvetica Neue',Arial,sans-serif;color:#2f5d46;margin:0 0 6px;border-bottom:3px solid #c9a24a;padding-bottom:4px}
.cards{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:8px}
.card{border:1.5px dashed #999;border-radius:12px;height:1.62in;padding:8px;text-align:center;display:flex;flex-direction:column;justify-content:center}
.card .n{font:900 28pt 'Helvetica Neue',Arial,sans-serif;color:#b3262d;line-height:1}.card:nth-child(even) .n{color:#2f5d46}
.card .t{font-size:10pt;margin-top:6px;line-height:1.25}
.track{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-top:10px}
.track div{border:2px solid #2f5d46;border-radius:50%;aspect-ratio:1;display:flex;align-items:center;justify-content:center;font:900 26pt 'Helvetica Neue',Arial,sans-serif;color:#2f5d46}
.track div:nth-child(odd){border-color:#b3262d;color:#b3262d}
.note{background:#fbf6ee;border-left:5px solid #b3262d;padding:10px 14px;border-radius:6px;margin:12px 0}
.foot{position:absolute;bottom:0;left:0;right:0;text-align:center;font:8pt Arial,sans-serif;color:#999}"""

def cards(items):
    return "<div class='cards'>" + "".join(f"<div class='card'><div class='n'>{i}</div><div class='t'>{t}</div></div>" for i, t in items) + "</div>"

blank = "<span style='display:block;border-bottom:1px solid #bbb;height:16px;margin:4px 8px'></span>" * 2
cd = [f"""<div class='page'><div style='text-align:center;margin-top:1.2in'><div style='font-size:60pt'>🎄</div>
<h1>25 Days of<br>Christmas Fun</h1><p style='font-size:15pt;margin:16px 0 30px'>A printable countdown calendar of cozy, cheap,<br>family activities, one for every day of December.</p></div>
<div class='note'><b>How to use:</b> print the activity cards on cardstock, cut them out, and tuck one into each day of an advent calendar, envelope or jar. Prefer a wall chart? Use the tracker page and color in a circle each night.</div>
<div class='note'><b>Holly's rule:</b> skip any day that doesn't fit. Swap cards around, or fill in the blank cards with your own family traditions. It doesn't have to be perfect, it has to be yours.</div>
<p style='text-align:center;margin-top:30px;font-style:italic'>by Holly Bramble · @hollybrambledaysathome</p><div class='foot'>{FOOT}</div></div>"""]
items = list(enumerate(ACTS, 1))
cd.append(f"<div class='page'><h2>Activity Cards · Days 1–12</h2>{cards(items[:12])}<div class='foot'>{FOOT} · cut along the dotted lines</div></div>")
cd.append(f"<div class='page'><h2>Activity Cards · Days 13–24</h2>{cards(items[12:24])}<div class='foot'>{FOOT} · cut along the dotted lines</div></div>")
cd.append(f"<div class='page'><h2>Day 25 + Make-Your-Own Cards</h2>{cards([items[24]] + [('★', blank)] * 11)}<div class='foot'>{FOOT}</div></div>")
cd.append(f"""<div class='page'><h2>Christmas Countdown Tracker</h2><p style='font-style:italic;color:#7a6e64'>Color in a circle each night before bed.</p>
<div class='track'>{''.join(f'<div>{i}</div>' for i in range(1, 26))}</div>
<p style='text-align:center;font:700 16pt Georgia,serif;color:#b3262d;margin-top:18px'>Merry Christmas! 🎁</p><div class='foot'>{FOOT}</div></div>""")
pdf("christmas_countdown_calendar", f"<!doctype html><html><head><meta charset='utf-8'><style>{CD_CSS}</style></head><body>{''.join(cd)}</body></html>")
print("done")
