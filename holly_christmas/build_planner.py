"""Build Holly's Christmas Budget & Gift Planner (printable PDF, US Letter)."""
import pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parent
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

CSS = """
@page{size:Letter;margin:0.55in}
:root{--red:#b3262d;--green:#2f5d46;--gold:#c9a24a;--ink:#2b2420;--cream:#fbf6ee;--line:#d9cbb7}
*{box-sizing:border-box}
body{font-family:Georgia,'Times New Roman',serif;color:var(--ink);font-size:10.5pt;margin:0}
.page{page-break-after:always;min-height:9.7in;position:relative}
.page:last-child{page-break-after:auto}
h1{font-family:'Helvetica Neue',Arial,sans-serif;color:var(--red);font-size:30pt;margin:0 0 4px}
h2{font-family:'Helvetica Neue',Arial,sans-serif;color:var(--green);font-size:20pt;margin:0 0 4px;border-bottom:3px solid var(--gold);padding-bottom:4px}
.sub{color:#7a6e64;font-style:italic;margin:0 0 12px}
table{width:100%;border-collapse:collapse;margin-top:8px}
th{background:var(--green);color:#fff;font-family:Arial,sans-serif;font-size:9pt;text-align:left;padding:6px}
td{border-bottom:1px solid var(--line);height:30px;padding:4px 6px;font-size:9.5pt}
tr:nth-child(even) td{background:#fdfaf4}
.box{display:inline-block;width:12px;height:12px;border:1.5px solid var(--ink);vertical-align:-1px;margin-right:6px}
.foot{position:absolute;bottom:0;left:0;right:0;text-align:center;font-size:8pt;color:#9a8e82}
.cover{background:var(--cream);border:3px solid var(--gold);border-radius:18px;padding:60px 40px;text-align:center;min-height:9.4in;display:flex;flex-direction:column;justify-content:center}
.cover h1{font-size:44pt;line-height:1.05}
.note{background:var(--cream);border-left:5px solid var(--red);padding:10px 14px;border-radius:6px;margin:10px 0}
.lines div{border-bottom:1px solid var(--line);height:28px}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.card{border:1.5px solid var(--line);border-radius:10px;padding:10px 12px}
.card h3{font-family:Arial,sans-serif;color:var(--red);font-size:11pt;margin:0 0 6px}
.big td{height:34px}
.cal{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin-top:8px}
.cal div{border:1px solid var(--line);height:74px;padding:3px 5px;font-family:Arial,sans-serif;font-size:8pt}
.cal .hd{height:auto;background:var(--green);color:#fff;text-align:center;font-weight:700;border:0;padding:4px}
.cal .x{background:#f5efe4;border-color:#f5efe4}
"""

FOOT = '<div class="foot">Christmas Budget &amp; Gift Planner · © Holly Bramble · @hollybrambledaysathome · personal use only</div>'

def page(inner): return f'<div class="page">{inner}{FOOT}</div>'
def rows(n, cols): return "".join("<tr>" + "".join("<td></td>" for _ in range(cols)) + "</tr>" for _ in range(n))
def table(heads, n, cls=""):
    return f'<table class="{cls}"><tr>' + "".join(f"<th>{h}</th>" for h in heads) + "</tr>" + rows(n, len(heads)) + "</table>"
def lines(n): return '<div class="lines">' + "<div></div>" * n + "</div>"

def calendar(title, first_weekday, days, notes=None):
    notes = notes or {}
    cells = "".join(f'<div class="hd">{d}</div>' for d in ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
    cells += '<div class="x"></div>' * first_weekday
    for d in range(1, days + 1):
        cells += f'<div><b>{d}</b><br>{notes.get(d, "")}</div>'
    tail = (7 - (first_weekday + days) % 7) % 7
    cells += '<div class="x"></div>' * tail
    return f"<h2>{title}</h2><div class='cal'>{cells}</div>"

pages = []

pages.append('''<div class="page"><div class="cover">
<div style="font-size:54pt">🎄</div>
<h1>Christmas Budget<br>&amp; Gift Planner</h1>
<p style="font-size:15pt;margin:18px 0 30px">Every gift, every dollar, every deadline,<br>all in one place. No January regrets.</p>
<p style="font-family:Arial,sans-serif;color:#7a6e64">by Holly Bramble · @hollybrambledaysathome</p>
<p style="margin-top:40px;font-style:italic">"It doesn't have to be perfect. It has to be ours."</p>
<p style="margin-top:30px;font-size:10pt">This planner belongs to: <span style="border-bottom:1px solid #999;display:inline-block;min-width:220px"></span></p>
</div></div>''')

pages.append(page('''<h2>How to use this planner</h2>
<p class="sub">Ten minutes now saves you a lot of stress in December.</p>
<ol style="line-height:1.8">
<li><b>Set your total budget</b> on the next page, and don't touch it after that.</li>
<li><b>List everyone</b> you're buying for on the Gift List pages, with a budget beside each name.</li>
<li><b>Brainstorm ideas</b> before you shop. Shopping without a list is where budgets break.</li>
<li><b>Track every purchase</b> on the Spending Tracker as you go. Keep the receipts.</li>
<li><b>Check the deadlines page</b> for shipping and wrapping dates, so nothing arrives on the 26th.</li>
<li><b>Plan the extras</b>: stockings, cards, hosting and food. These are the costs that sneak up on you.</li>
</ol>
<div class="note"><b>Holly's rule:</b> spend about <b>75%</b> of your budget on gifts and keep <b>25%</b> for the sneaky extras: wrapping, shipping, stocking stuffers, teacher gifts, the office swap and the extra roll of tape on the 23rd.</div>
<div class="note"><b>Tip:</b> print the Gift List and Spending Tracker pages twice if you have a big family. You'll fill them faster than you think.</div>
'''))

pages.append(page('''<h2>My Christmas Budget</h2>
<p class="sub">Decide it once. Write it down. Stick to it.</p>
<table class="big"><tr><th>Category</th><th style="width:22%">Budget</th><th style="width:22%">Spent</th><th style="width:22%">Left</th></tr>
<tr><td>🎁 Gifts</td><td></td><td></td><td></td></tr>
<tr><td>🧦 Stocking stuffers</td><td></td><td></td><td></td></tr>
<tr><td>🎀 Wrapping, tags &amp; bows</td><td></td><td></td><td></td></tr>
<tr><td>📮 Cards &amp; postage</td><td></td><td></td><td></td></tr>
<tr><td>📦 Shipping</td><td></td><td></td><td></td></tr>
<tr><td>🍪 Food &amp; baking</td><td></td><td></td><td></td></tr>
<tr><td>🥂 Hosting &amp; parties</td><td></td><td></td><td></td></tr>
<tr><td>🎄 Decorations</td><td></td><td></td><td></td></tr>
<tr><td>🍎 Teacher, coworker &amp; swap gifts</td><td></td><td></td><td></td></tr>
<tr><td>💝 Charity &amp; giving</td><td></td><td></td><td></td></tr>
<tr><td>✨ Other</td><td></td><td></td><td></td></tr>
<tr><td><b>TOTAL</b></td><td></td><td></td><td></td></tr>
</table>
<div class="grid2" style="margin-top:18px">
<div class="card"><h3>Where the money comes from</h3>''' + lines(5) + '''</div>
<div class="card"><h3>Savings goal per week until Dec 20</h3>''' + lines(5) + '''</div>
</div>'''))

for i in (1, 2):
    pages.append(page(f'''<h2>Gift List {"" if i == 1 else "(continued)"}</h2>
<p class="sub">Who's on the list, what they're getting, and whether it's done.</p>
''' + table(["Name", "Gift idea", "Budget", "Spent", "Bought", "Wrapped", "Given"], 17)))

pages.append(page('''<h2>Gift Idea Brainstorm</h2>
<p class="sub">Jot down hints all year. Write ideas here before you shop.</p>
<div class="grid2">''' + "".join(f'<div class="card"><h3>Name: ______________</h3>{lines(4)}</div>' for _ in range(8)) + "</div>"))

for i in (1, 2):
    pages.append(page(f'''<h2>Spending Tracker {"" if i == 1 else "(continued)"}</h2>
<p class="sub">Write down every purchase, including the small ones.</p>
''' + table(["Date", "Item", "For", "Store / site", "Amount", "Receipt ✓"], 20)))

pages.append(page('''<h2>Stocking Stuffers</h2>
<p class="sub">Small things add up fast. Give each stocking a budget.</p>
<div class="grid2">''' + "".join(f'<div class="card"><h3>Stocking for: __________ &nbsp; Budget: $____</h3>{lines(6)}</div>' for _ in range(6)) + "</div>"))

pages.append(page('''<h2>Online Orders &amp; Deliveries</h2>
<p class="sub">Know what's coming and when.</p>
''' + table(["Item", "Store", "Order date", "Order #", "Expected", "Arrived ✓"], 18)))

pages.append(page('''<h2>Key Dates &amp; Deadlines</h2>
<p class="sub">Shipping cutoffs change every year. Check your carriers' websites and write this year's dates here.</p>
<table class="big"><tr><th>Deadline</th><th style="width:30%">Date</th><th style="width:12%">Done</th></tr>
<tr><td>Final day to order online (standard shipping)</td><td></td><td><span class="box"></span></td></tr>
<tr><td>USPS ground / retail cutoff</td><td></td><td><span class="box"></span></td></tr>
<tr><td>USPS priority mail cutoff</td><td></td><td><span class="box"></span></td></tr>
<tr><td>UPS / FedEx ground cutoff</td><td></td><td><span class="box"></span></td></tr>
<tr><td>Mail holiday cards by</td><td></td><td><span class="box"></span></td></tr>
<tr><td>Ship gifts to out-of-town family by</td><td></td><td><span class="box"></span></td></tr>
<tr><td>Black Friday</td><td></td><td><span class="box"></span></td></tr>
<tr><td>Cyber Monday</td><td></td><td><span class="box"></span></td></tr>
<tr><td>Office / school party</td><td></td><td><span class="box"></span></td></tr>
<tr><td>Gift swap</td><td></td><td><span class="box"></span></td></tr>
<tr><td>All wrapping finished by</td><td></td><td><span class="box"></span></td></tr>
<tr><td></td><td></td><td><span class="box"></span></td></tr>
</table>'''))

pages.append(page(calendar("November 2026", 0, 30)))
pages.append(page(calendar("December 2026", 2, 31, {24: "Christmas Eve", 25: "Christmas", 31: "New Year's Eve"})))

pages.append(page('''<h2>Holiday Card List</h2>
<p class="sub">Addresses once, so next year is easy.</p>
''' + table(["Name", "Address", "Sent ✓", "Received ✓"], 18)))

pages.append(page('''<h2>Christmas Menu &amp; Hosting</h2>
<div class="grid2">
<div class="card"><h3>Christmas Eve menu</h3>''' + lines(8) + '''</div>
<div class="card"><h3>Christmas Day menu</h3>''' + lines(8) + '''</div>
<div class="card"><h3>Grocery list</h3>''' + lines(10) + '''</div>
<div class="card"><h3>Make-ahead plan</h3>''' + lines(10) + '''</div>
</div>'''))

pages.append(page('''<h2>After-Christmas Review</h2>
<p class="sub">Five minutes on December 26th makes next year easier.</p>
<table class="big"><tr><th>Question</th><th>My answer</th></tr>
<tr><td style="width:45%">Total I actually spent</td><td></td></tr>
<tr><td>Over or under budget? By how much?</td><td></td></tr>
<tr><td>Best gift I gave</td><td></td></tr>
<tr><td>What I'll start earlier next year</td><td></td></tr>
<tr><td>What I'll skip next year</td><td></td></tr>
<tr><td>Post-Christmas sales to buy for next year</td><td></td></tr>
</table>
<div class="note" style="margin-top:20px"><b>Next year's savings goal:</b> divide this year's total by 52. Saving that much each week means next December is already paid for.<br><br>$________ ÷ 52 = $________ per week</div>
<p style="text-align:center;margin-top:40px;font-style:italic">Merry Christmas from my kitchen to yours. 🎄<br>— Holly</p>'''))

html = f"<!doctype html><html><head><meta charset='utf-8'><title>Christmas Budget & Gift Planner</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
(ROOT / "christmas_budget_gift_planner.html").write_text(html)
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={ROOT / 'christmas_budget_gift_planner.pdf'}",
                f"file://{ROOT / 'christmas_budget_gift_planner.html'}"], check=True, stderr=subprocess.DEVNULL)
print("pages:", len(pages))
