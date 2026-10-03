"""Etsy listing images (2000x1600) for the gift tags, countdown calendar and Christmas bundle."""
import pathlib, subprocess, shutil

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
PG = ROOT / "_pages"; PG.mkdir(exist_ok=True)
for name in ("christmas_gift_tags", "christmas_countdown_calendar", "christmas_budget_gift_planner"):
    subprocess.run(["pdftoppm", "-r", "80", "-png", str(ROOT / f"{name}.pdf"), str(PG / name)], check=True)
P = lambda name, n: f"_pages/{name}-{n}.png" if name != "christmas_budget_gift_planner" else f"_pages/{name}-{n:02d}.png"
T, C, B = "christmas_gift_tags", "christmas_countdown_calendar", "christmas_budget_gift_planner"

BASE = """<!doctype html><html><head><meta charset='utf-8'><style>
*{box-sizing:border-box;margin:0}body{width:2000px;height:1600px;overflow:hidden;font-family:'Helvetica Neue',Arial,sans-serif}
.bg{width:2000px;height:1600px;position:relative;background:linear-gradient(150deg,#2f5d46 0%,#1f3f30 100%);color:#fbf6ee}
.red{background:linear-gradient(150deg,#b3262d 0%,#7f1a20 100%)}
h1{font-size:110px;line-height:1;font-weight:900}h1 span{color:#e3c47a}
.pg{position:absolute;background:#fff;box-shadow:0 30px 70px rgba(0,0,0,.4);border-radius:6px}
.tag{display:inline-block;background:#c9a24a;color:#2b2420;font-weight:800;font-size:40px;padding:14px 32px;border-radius:999px}
.sub{font-size:50px;margin-top:40px;opacity:.92;font-family:Georgia,serif;line-height:1.35}
.price{position:absolute;right:90px;bottom:80px;background:#fbf6ee;color:#b3262d;font-weight:900;font-size:80px;padding:12px 40px;border-radius:24px}
</style></head><body>BODY</body></html>"""

def left(tag, title, sub):
    return f"<div style='position:absolute;left:100px;top:210px;width:880px'><div class='tag'>{tag}</div><h1 style='margin-top:50px'>{title}</h1><p class='sub'>{sub}</p></div>"

IMAGES = {
 "tags_01_cover": "<div class='bg red'>" + left("PRINTABLE · INSTANT DOWNLOAD", "Christmas<br><span>Gift Tags</span>", "3 styles · 72 tags<br>Print, cut, punch, tie.") +
    f"<img class='pg' src='{P(T,6)}' style='left:1250px;top:300px;width:600px;transform:rotate(8deg)'>"
    f"<img class='pg' src='{P(T,4)}' style='left:1120px;top:220px;width:600px;transform:rotate(1deg)'>"
    f"<img class='pg' src='{P(T,2)}' style='left:990px;top:150px;width:600px;transform:rotate(-6deg)'></div>",
 "tags_02_styles": "<div class='bg'><h1 style='position:absolute;left:100px;top:80px;font-size:96px'>3 styles · <span>with &amp; without words</span></h1>" + "".join(
    f"<img class='pg' src='{P(T,n)}' style='left:{110 + i * 620}px;top:300px;width:560px'>" for i, n in enumerate([2, 4, 6])) +
    "<p class='sub' style='position:absolute;left:110px;top:1080px'>Classic red · Rustic kraft · Snowy cream<br>+ a blank page of each to write your own message</p></div>",
 "countdown_01_cover": "<div class='bg'>" + left("PRINTABLE · INSTANT DOWNLOAD", "25 Days of<br><span>Christmas Fun</span>", "Family countdown calendar<br>25 cozy, cheap activities") +
    f"<img class='pg' src='{P(C,5)}' style='left:1240px;top:300px;width:620px;transform:rotate(7deg)'>"
    f"<img class='pg' src='{P(C,2)}' style='left:1000px;top:170px;width:700px;transform:rotate(-4deg)'></div>",
 "countdown_02_inside": "<div class='bg red'><h1 style='position:absolute;left:100px;top:80px;font-size:96px'>What's <span>inside</span></h1>" + "".join(
    f"<img class='pg' src='{P(C,n)}' style='left:{90 + i * 370}px;top:300px;width:340px'>" for i, n in enumerate([1, 2, 3, 4, 5])) +
    "<p class='sub' style='position:absolute;left:100px;top:880px'>✓ 25 cut-out activity cards<br>✓ 11 blank cards for your own traditions<br>✓ Color-in countdown tracker</p></div>",
 "bundle_01_cover": "<div class='bg red'>" + left("BUNDLE · SAVE 35%", "Christmas<br><span>Bundle</span>", "Budget &amp; Gift Planner<br>+ Gift Tags<br>+ 25-Day Countdown") +
    f"<img class='pg' src='{P(C,2)}' style='left:1300px;top:420px;width:540px;transform:rotate(9deg)'>"
    f"<img class='pg' src='{P(T,2)}' style='left:1180px;top:300px;width:560px;transform:rotate(2deg)'>"
    f"<img class='pg' src='{P(B,1)}' style='left:1010px;top:170px;width:600px;transform:rotate(-6deg)'></div>",
}

(ROOT / "etsy_images").mkdir(exist_ok=True)
for name, body in IMAGES.items():
    html = ROOT / f"_m_{name}.html"; html.write_text(BASE.replace("BODY", body)); tmp = ROOT / f"_m_{name}.png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--window-size=2000,1800",
                    f"--screenshot={tmp}", f"file://{html}"], check=True, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-vf", "crop=2000:1600:0:0", "-q:v", "3",
                    str(ROOT / "etsy_images" / f"{name}.jpg")], check=True)
    html.unlink(); tmp.unlink(); print("built", name)
shutil.rmtree(PG)
