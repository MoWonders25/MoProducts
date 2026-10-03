"""Etsy listing images (2000x1600) for the Christmas planner."""
import pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
P = lambda n: f"pages/p-{n:02d}.png"

BASE = """<!doctype html><html><head><meta charset='utf-8'><style>
*{box-sizing:border-box;margin:0}body{width:2000px;height:1600px;overflow:hidden;font-family:'Helvetica Neue',Arial,sans-serif}
.bg{width:2000px;height:1600px;position:relative;background:linear-gradient(150deg,#2f5d46 0%,#1f3f30 100%);color:#fbf6ee}
.cream{background:#fbf6ee;color:#2b2420}
h1{font-size:118px;line-height:1;font-weight:900}h1 span{color:#c9a24a}
.cream h1 span{color:#b3262d}
.pg{position:absolute;background:#fff;box-shadow:0 30px 70px rgba(0,0,0,.4);border-radius:6px}
.tag{display:inline-block;background:#b3262d;color:#fff;font-weight:800;font-size:40px;padding:14px 32px;border-radius:999px}
.feat{font-size:46px;line-height:1.7}
</style></head><body>BODY</body></html>"""

IMAGES = {
 "01_cover": f"""<div class='bg'>
  <div style='position:absolute;left:110px;top:200px;width:880px'>
    <div class='tag'>PRINTABLE · INSTANT DOWNLOAD</div>
    <h1 style='margin-top:50px'>Christmas<br>Budget &amp;<br><span>Gift Planner</span></h1>
    <p style='font-size:50px;margin-top:40px;opacity:.9;font-family:Georgia,serif'>16 pages · US Letter · print at home</p>
  </div>
  <img class='pg' src='{P(4)}' style='left:1240px;top:260px;width:620px;transform:rotate(7deg)'>
  <img class='pg' src='{P(1)}' style='left:960px;top:170px;width:760px;transform:rotate(-3deg)'>
</div>""",
 "02_whats_inside": "<div class='bg cream'><h1 style='position:absolute;left:100px;top:70px;font-size:96px'>What's <span>inside</span></h1>" + "".join(
     f"<img class='pg' src='{P(n)}' style='left:{100 + (i % 5) * 370}px;top:{260 + (i // 5) * 660}px;width:330px'>"
     for i, n in enumerate([3, 4, 6, 7, 9, 10, 11, 12, 14, 16])) + "</div>",
 "03_features": f"""<div class='bg'>
  <img class='pg' src='{P(3)}' style='left:110px;top:150px;width:800px;transform:rotate(-3deg)'>
  <div style='position:absolute;left:1020px;top:170px;width:900px'>
    <h1 style='font-size:92px'>Every gift.<br>Every dollar.<br><span>Every deadline.</span></h1>
    <div class='feat' style='margin-top:50px'>✓ Budget by category<br>✓ Gift list with bought / wrapped / given<br>✓ Spending tracker<br>✓ Stocking stuffer planner<br>✓ Shipping deadlines page<br>✓ Nov &amp; Dec 2026 calendars<br>✓ Card list, menu &amp; review</div>
  </div>
</div>""",
}

for name, body in IMAGES.items():
    html = ROOT / f"_m_{name}.html"
    html.write_text(BASE.replace("BODY", body))
    tmp = ROOT / f"_m_{name}.png"
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--window-size=2000,1800", f"--screenshot={tmp}", f"file://{html}"], check=True, stderr=subprocess.DEVNULL)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-vf", "crop=2000:1600:0:0",
                    "-q:v", "3", str(ROOT / "etsy_images" / f"{name}.jpg")], check=True)
    html.unlink(); tmp.unlink()
    print("built", name)
