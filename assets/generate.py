"""Generates the arcade-style SVGs for the GitHub profile README.

Everything is drawn with a hand-made 5x7 pixel font and pixel sprites, so the text looks
like a game on every device (SVGs shown as images on GitHub cannot load web fonts).
Run from the repo root: python3 assets/generate.py assets
"""
import sys, os

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

# Palette
BG0, BG1, BG2 = "#0D0221", "#1B0B3B", "#2E0F5C"
CYAN, PINK, YELLOW, GREEN, PURPLE, WHITE = "#00E5FF", "#FF2BD6", "#FFD93D", "#39FF14", "#7B2FF7", "#F5F5FF"

FONT = {
"A":[".###.","#...#","#...#","#####","#...#","#...#","#...#"],
"B":["####.","#...#","#...#","####.","#...#","#...#","####."],
"C":[".###.","#...#","#....","#....","#....","#...#",".###."],
"D":["####.","#...#","#...#","#...#","#...#","#...#","####."],
"E":["#####","#....","#....","####.","#....","#....","#####"],
"F":["#####","#....","#....","####.","#....","#....","#...."],
"G":[".###.","#...#","#....","#.###","#...#","#...#",".####"],
"H":["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
"I":[".###.","..#..","..#..","..#..","..#..","..#..",".###."],
"J":["..###","...#.","...#.","...#.","#..#.","#..#.",".##.."],
"K":["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
"L":["#....","#....","#....","#....","#....","#....","#####"],
"M":["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],
"N":["#...#","#...#","##..#","#.#.#","#..##","#...#","#...#"],
"O":[".###.","#...#","#...#","#...#","#...#","#...#",".###."],
"P":["####.","#...#","#...#","####.","#....","#....","#...."],
"Q":[".###.","#...#","#...#","#...#","#.#.#","#..#.",".##.#"],
"R":["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
"S":[".####","#....","#....",".###.","....#","....#","####."],
"T":["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
"U":["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
"V":["#...#","#...#","#...#","#...#","#...#",".#.#.","..#.."],
"W":["#...#","#...#","#...#","#.#.#","#.#.#","#.#.#",".#.#."],
"X":["#...#","#...#",".#.#.","..#..",".#.#.","#...#","#...#"],
"Y":["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
"Z":["#####","....#","...#.","..#..",".#...","#....","#####"],
"0":[".###.","#...#","#..##","#.#.#","##..#","#...#",".###."],
"1":["..#..",".##..","..#..","..#..","..#..","..#..",".###."],
"2":[".###.","#...#","....#","...#.","..#..",".#...","#####"],
"3":["####.","....#","....#",".###.","....#","....#","####."],
"4":["...#.","..##.",".#.#.","#..#.","#####","...#.","...#."],
"5":["#####","#....","####.","....#","....#","#...#",".###."],
"6":[".###.","#....","#....","####.","#...#","#...#",".###."],
"7":["#####","....#","...#.","..#..",".#...",".#...",".#..."],
"8":[".###.","#...#","#...#",".###.","#...#","#...#",".###."],
"9":[".###.","#...#","#...#",".####","....#","....#",".###."],
" ":["....."]*7,
"-":[".....",".....",".....",".###.",".....",".....","....."],
".":[".....",".....",".....",".....",".....",".....","..#.."],
",":[".....",".....",".....",".....",".....","..#..",".#..."],
":":[".....","..#..",".....",".....",".....","..#..","....."],
"!":["..#..","..#..","..#..","..#..","..#..",".....","..#.."],
"?":[".###.","#...#","....#","...#.","..#..",".....","..#.."],
"/":["....#","...#.","...#.","..#..",".#...",".#...","#...."],
"+":[".....","..#..","..#..","#####","..#..","..#..","....."],
">":["#....",".#...","..#..","...#.","..#..",".#...","#...."],
"<":["....#","...#.","..#..",".#...","..#..","...#.","....#"],
"&":[".##..","#..#.","#.#..",".#...","#.#.#","#..#.",".##.#"],
"*":[".....","..#..",".###.","#####",".###.","..#..","....."],  # diamond
"(":["...#.","..#..",".#...",".#...",".#...","..#..","...#."],
")":[".#...","..#..","...#.","...#.","...#.","..#..",".#..."],
"'":["..#..","..#..",".....",".....",".....",".....","....."],
"=":[".....",".....","#####",".....","#####",".....","....."],
"%":["##...","##..#","...#.","..#..",".#...","#..##","...##"],
}

def text_w(s, k):
    return len(s) * 6 * k - k

def pixtext(s, x, y, k, fill, extra=""):
    """Text as one <path>: each lit pixel is a k x k square."""
    d = []
    for i, ch in enumerate(s.upper()):
        g = FONT[ch]
        ox = x + i * 6 * k
        for r, row in enumerate(g):
            c = 0
            while c < 5:
                if row[c] == "#":
                    run = 1
                    while c + run < 5 and row[c + run] == "#":
                        run += 1
                    d.append(f"M{ox + c * k} {y + r * k}h{run * k}v{k}h{-run * k}z")
                    c += run
                else:
                    c += 1
    return f'<path d="{"".join(d)}" fill="{fill}" {extra}/>'

def pixtext_c(s, cx, y, k, fill, extra=""):
    return pixtext(s, cx - text_w(s, k) / 2, y, k, fill, extra)

# Original pixel sprite: a developer in a cyan hoodie. Two running frames.
SPRITE_TOP = [
    "..hhhh..",
    ".hhhhhh.",
    ".hssssh.",
    ".sesses.",
    "..ssss..",
    ".cccccc.",
    "sccwwccs",
    "sccccccs",
    ".bbbbbb.",
]
FRAME_A = [".bb..bb.", "kk....kk"]
FRAME_B = ["..bbbb..", "..kkkk.."]
SPRITE_COLORS = {"h": "#3B2416", "s": "#F2C29B", "e": "#111111", "c": CYAN, "w": WHITE,
                 "b": "#3A3F8F", "k": PINK}

def sprite(rows, x, y, k):
    out = []
    by_color = {}
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch != ".":
                by_color.setdefault(SPRITE_COLORS[ch], []).append(
                    f"M{x + c * k} {y + r * k}h{k}v{k}h{-k}z")
    for col, d in by_color.items():
        out.append(f'<path d="{"".join(d)}" fill="{col}"/>')
    return "".join(out)

HEART = [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."]
COIN = [".###.", "#####", "##.##", "##.##", "##.##", "#####", ".###."]

def icon(rows, x, y, k, fill, hole=None):
    d = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                d.append(f"M{x + c * k} {y + r * k}h{k}v{k}h{-k}z")
    return f'<path d="{"".join(d)}" fill="{fill}"/>'

def svg(w, h, body, style="", title=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'shape-rendering="crispEdges" role="img" aria-label="{title}">'
            f"<title>{title}</title>"
            f"<style>{style}"
            "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
            f"</style>{body}</svg>")

def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print(name, len(content) // 1024, "KB")

# Deterministic "random" for star placement
def rng(seed):
    x = seed
    while True:
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        yield x

# ───────────────────────── HEADER: arcade title screen ─────────────────────────
def header():
    W, H = 1200, 420
    HOR = 310  # horizon
    b = []
    style = """
.tw{animation:tw 2.4s steps(2) infinite}
@keyframes tw{0%{opacity:1}50%{opacity:.2}}
.blink{animation:bl 1.1s steps(1) infinite}
@keyframes bl{50%{opacity:0}}
.run{animation:run 11s linear infinite}
@keyframes run{from{transform:translateX(-90px)}to{transform:translateX(1260px)}}
.fa{animation:fa .32s steps(1) infinite}.fb{animation:fb .32s steps(1) infinite}
@keyframes fa{50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}
.bob{animation:bob 1.2s steps(2) infinite}
@keyframes bob{50%{transform:translateY(-8px)}}
.spin{animation:spin .9s steps(4) infinite;transform-box:fill-box;transform-origin:center}
@keyframes spin{0%{transform:scaleX(1)}25%{transform:scaleX(.6)}50%{transform:scaleX(.15)}75%{transform:scaleX(.6)}}
.gl{animation:gl 4s steps(1) infinite}
@keyframes gl{0%,86%,100%{transform:translate(0,0)}88%{transform:translate(-7px,2px)}90%{transform:translate(6px,-2px)}92%{transform:translate(-3px,0)}}
.gl2{animation:gl2 4s steps(1) infinite}
@keyframes gl2{0%,86%,100%{transform:translate(8px,8px)}88%{transform:translate(16px,8px)}90%{transform:translate(0,8px)}92%{transform:translate(8px,8px)}}
.scan{animation:scan 6s linear infinite}
@keyframes scan{from{transform:translateY(-40px)}to{transform:translateY(440px)}}
"""
    b.append(f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{BG0}"/><stop offset=".6" stop-color="{BG1}"/>'
             f'<stop offset="1" stop-color="{BG2}"/></linearGradient>'
             f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{YELLOW}"/><stop offset=".55" stop-color="#FF7A3D"/>'
             f'<stop offset="1" stop-color="{PINK}"/></linearGradient>'
             f'<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="#240046"/><stop offset="1" stop-color="{BG0}"/></linearGradient>'
             f'<clipPath id="fl"><rect x="0" y="{HOR}" width="{W}" height="{H - HOR}"/></clipPath>'
             f'<clipPath id="sunc"><circle cx="600" cy="{HOR}" r="110"/></clipPath>'
             f'</defs>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
    # stars
    g = rng(7)
    for i in range(70):
        x, y = next(g) % W, next(g) % (HOR - 20)
        s = 2 if next(g) % 4 else 4
        col = [WHITE, CYAN, PINK, YELLOW][next(g) % 4] if s == 4 else WHITE
        delay = (next(g) % 24) / 10
        cls = ' class="tw"' if i % 2 == 0 else ""
        b.append(f'<rect{cls} x="{x}" y="{y}" width="{s}" height="{s}" fill="{col}" '
                 f'style="animation-delay:-{delay}s" opacity=".9"/>')
    # sun with stripes
    stripes = "".join(
        f'<rect x="480" y="{HOR - 60 + i * 14}" width="240" height="{2 + i * 1.5:.0f}" fill="{BG1}"/>'
        for i in range(5))
    b.append(f'<g clip-path="url(#sunc)"><rect x="480" y="{HOR - 112}" width="240" height="112" fill="url(#sun)"/>{stripes}</g>')
    # mountains
    b.append(f'<polygon points="0,{HOR} 90,{HOR-70} 170,{HOR-30} 260,{HOR-95} 360,{HOR-25} 430,{HOR-55} 500,{HOR} " fill="#3C096C"/>')
    b.append(f'<polygon points="700,{HOR} 780,{HOR-50} 860,{HOR-20} 960,{HOR-100} 1060,{HOR-40} 1130,{HOR-80} 1200,{HOR-35} 1200,{HOR}" fill="#3C096C"/>')
    b.append(f'<polygon points="0,{HOR} 60,{HOR-30} 140,{HOR-8} 230,{HOR-45} 330,{HOR} " fill="#5A189A"/>')
    b.append(f'<polygon points="820,{HOR} 920,{HOR-38} 1010,{HOR-12} 1110,{HOR-50} 1200,{HOR-20} 1200,{HOR}" fill="#5A189A"/>')
    # floor grid
    b.append(f'<rect x="0" y="{HOR}" width="{W}" height="{H - HOR}" fill="url(#floor)"/>')
    grid = [f'<g clip-path="url(#fl)" stroke="{PINK}" stroke-width="2" opacity=".75" shape-rendering="auto">']
    for k in range(-14, 15):
        grid.append(f'<line x1="{600 + k * 28}" y1="{HOR}" x2="{600 + k * 230}" y2="{H}"/>')
    for i in range(7):
        grid.append(f'<line x1="0" x2="{W}" y1="{HOR}" y2="{HOR}">'
                    f'<animate attributeName="y1" values="{HOR};{H + 10}" dur="3.5s" begin="-{i * 0.5}s" '
                    f'repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 1"/>'
                    f'<animate attributeName="y2" values="{HOR};{H + 10}" dur="3.5s" begin="-{i * 0.5}s" '
                    f'repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 1"/></line>')
    grid.append("</g>")
    b.append("".join(grid))
    b.append(f'<rect x="0" y="{HOR - 1}" width="{W}" height="3" fill="{CYAN}"/>')
    # coins along the horizon
    for i, cx in enumerate([180, 330, 870, 1020]):
        b.append(f'<g class="bob" style="animation-delay:-{i * 0.3}s"><g class="spin">'
                 f'{icon(COIN, cx, HOR - 70, 4, YELLOW)}</g></g>')
    # runner
    k = 5
    top = HOR - 11 * k
    body = sprite(SPRITE_TOP, 0, top, k)
    fa = sprite(SPRITE_TOP[:0] + [""] * 9 + FRAME_A, 0, top, k)
    fb = sprite([""] * 9 + FRAME_B, 0, top, k)
    b.append(f'<g class="run">{body}<g class="fa">{fa}</g><g class="fb">{fb}</g></g>')
    # HUD
    b.append(pixtext("1UP", 40, 24, 3, PINK))
    b.append(pixtext("002027", 40, 52, 3, WHITE))
    b.append(pixtext_c("HI-SCORE", 600, 24, 3, PINK))
    b.append(pixtext_c("999999", 600, 52, 3, WHITE))
    b.append(pixtext("LEVEL", W - 40 - text_w("LEVEL", 3), 24, 3, PINK))
    b.append(pixtext("IT-03", W - 40 - text_w("IT-03", 3), 52, 3, WHITE))
    # title with glitchy neon shadow
    title, tk = "MUBASHIR FAYYAZ", 8
    tx = (W - text_w(title, tk)) / 2
    b.append(f'<g class="gl2">{pixtext(title, tx, 100, tk, "#B5179E")}</g>')
    b.append(f'<g class="gl">{pixtext(title, tx, 100, tk, CYAN)}</g>')
    b.append(pixtext_c("* FULL-STACK DEV * CYBER & DEVOPS ENGINEER *", 600, 176, 3, YELLOW))
    # press start
    ps = "PRESS START"
    b.append(f'<rect x="{600 - text_w(ps, 4) / 2 - 16}" y="{HOR + 46}" width="{text_w(ps, 4) + 32}" height="52" fill="{BG0}" opacity=".85"/>')
    b.append(f'<g class="blink">{pixtext_c("> " + ps, 600, HOR + 58, 4, WHITE)}</g>')
    # CRT scanline + vignette
    b.append(f'<rect class="scan" x="0" y="0" width="{W}" height="26" fill="{WHITE}" opacity=".05"/>')
    lines = "".join(f'<rect x="0" y="{y}" width="{W}" height="1" fill="#000" opacity=".18"/>' for y in range(0, H, 4))
    b.append(lines)
    write("header.svg", svg(W, H, "".join(b), style, "Mubashir Fayyaz: arcade title screen"))

# ───────────────────────── STAGE section headers ─────────────────────────
def stage(num, name, color, fname):
    W, H = 900, 76
    style = """
.blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
.dash{animation:dash 1.2s linear infinite}@keyframes dash{to{stroke-dashoffset:-32}}
.hop{animation:hop .8s steps(2) infinite}@keyframes hop{50%{transform:translateX(6px)}}
"""
    b = []
    b.append(f'<rect x="0" y="6" width="{W}" height="58" fill="{BG0}"/>')
    b.append(f'<rect x="0" y="6" width="8" height="58" fill="{color}"/>')
    # arrow
    arrow = ["#...", "##..", "###.", "####", "###.", "##..", "#..."]
    b.append(f'<g class="hop">{icon(arrow, 28, 17, 5, color)}</g>')
    lbl = f"STAGE {num:02d}"
    b.append(pixtext(lbl, 66, 21, 4, YELLOW))
    x2 = 66 + text_w(lbl, 4) + 24
    b.append(pixtext(name, x2, 21, 4, color))
    end = x2 + text_w(name, 4) + 10
    b.append(f'<rect class="blink" x="{end}" y="21" width="16" height="28" fill="{WHITE}"/>')
    b.append(f'<line class="dash" x1="0" y1="71" x2="{W}" y2="71" stroke="{color}" stroke-width="4" stroke-dasharray="16 16"/>')
    write(fname, svg(W, H, "".join(b), style, f"Stage {num}: {name.title()}"))

# ───────────────────────── CHARACTER SHEET ─────────────────────────
def character():
    W, H = 900, 542
    style = """
.bob{animation:bob 1.4s steps(2) infinite}@keyframes bob{50%{transform:translateY(-8px)}}
.blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
.beat{animation:beat 1.2s steps(2) infinite;transform-box:fill-box;transform-origin:center}
@keyframes beat{50%{transform:scale(1.15)}}
.glow{animation:glow 1.6s steps(2) infinite}@keyframes glow{50%{opacity:.55}}
"""
    b = []
    b.append(f'<rect width="{W}" height="{H}" fill="{BG0}"/>')
    # pixel frame
    b.append(f'<rect x="6" y="6" width="{W - 12}" height="{H - 12}" fill="none" stroke="{CYAN}" stroke-width="6"/>')
    b.append(f'<rect x="16" y="16" width="{W - 32}" height="{H - 32}" fill="none" stroke="{PURPLE}" stroke-width="2"/>')
    for (x, y) in [(0, 0), (W - 12, 0), (0, H - 12), (W - 12, H - 12)]:
        b.append(f'<rect x="{x}" y="{y}" width="12" height="12" fill="{PINK}"/>')
    # title bar
    b.append(f'<rect x="16" y="16" width="{W - 32}" height="44" fill="{BG2}"/>')
    b.append(pixtext("CHARACTER SHEET", 34, 27, 3, YELLOW))
    b.append(f'<g class="blink">{pixtext("P1 READY", W - 34 - text_w("P1 READY", 3), 27, 3, GREEN)}</g>')
    # portrait
    b.append(f'<rect x="40" y="84" width="230" height="230" fill="{BG1}" stroke="{PURPLE}" stroke-width="4"/>')
    for gx in range(44, 270, 22):
        b.append(f'<rect x="{gx}" y="88" width="1" height="222" fill="{PURPLE}" opacity=".35"/>')
    k = 16
    sx, sy = 155 - 4 * k, 300 - 11 * k
    b.append(f'<rect x="{155 - 60}" y="296" width="120" height="8" fill="#000" opacity=".4"/>')
    b.append(f'<g class="bob">{sprite(SPRITE_TOP + FRAME_B, sx, sy, k)}</g>')
    b.append(pixtext_c("MUBASHIR", 155, 334, 4, WHITE))
    b.append(pixtext_c("LV 03  IT STUDENT", 155, 372, 2, CYAN))
    # HP hearts
    for i in range(5):
        b.append(f'<g class="beat" style="animation-delay:-{i * .15}s">{icon(HEART, 66 + i * 38, 398, 4, PINK)}</g>')
    # info rows
    rows = [("CLASS", "FULL-STACK DEVELOPER"), ("SUBCLASS", "CYBER & DEVOPS ENGINEER"), ("GUILD", "UNIVERSITY OF LAHORE"),
            ("MAIN QUEST", "AGROBID PAKISTAN"), ("NEXT LEVEL", "GRADUATION SEP 2027"),
            ("STATUS", "OPEN TO INTERNSHIPS")]
    y = 88
    for lbl, val in rows:
        b.append(pixtext(lbl, 304, y, 2, PINK))
        b.append(pixtext(". " * ((12 - len(lbl)) // 2 + 1), 304 + text_w(lbl, 2) + 8, y, 2, PURPLE))
        b.append(pixtext(val, 470, y, 2, WHITE if lbl != "STATUS" else GREEN))
        y += 28
    b.append(f'<rect x="304" y="{y + 2}" width="566" height="2" fill="{PURPLE}"/>')
    b.append(pixtext("ATTRIBUTES", 304, y + 18, 3, YELLOW))
    stats = [("FRONTEND", 82, CYAN), ("BACKEND", 74, GREEN), ("DATABASES", 70, YELLOW),
             ("CLOUD/DEVOPS", 64, "#FF7A3D"), ("CYBERSEC", 62, "#FF4D6D"), ("AI / ML", 60, PINK), ("LINUX", 68, "#B388FF")]
    y += 52
    bx, bw = 470, 330
    for i, (lbl, v, col) in enumerate(stats):
        b.append(pixtext(lbl, 304, y + 3, 2, WHITE))
        b.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="20" fill="{BG1}" stroke="{PURPLE}" stroke-width="2"/>')
        segs = "".join(f'<rect x="{bx + 4 + s * 13}" y="{y + 4}" width="10" height="12" fill="{col}"/>'
                       for s in range(int((bw - 8) * v / 100 / 13)))
        b.append(f'<clipPath id="c{i}"><rect x="{bx}" y="{y}" width="0" height="20">'
                 f'<animate attributeName="width" from="0" to="{bw}" dur="1.6s" begin="{0.3 + i * 0.25}s" fill="freeze"/>'
                 f'</rect></clipPath><g clip-path="url(#c{i})">{segs}</g>')
        b.append(f'<g class="glow" style="animation-delay:-{i * .2}s">{pixtext(str(v), bx + bw + 14, y + 3, 2, col)}</g>')
        y += 30
    lines = "".join(f'<rect x="0" y="{yy}" width="{W}" height="1" fill="#000" opacity=".15"/>' for yy in range(0, H, 4))
    b.append(lines)
    write("character.svg", svg(W, H, "".join(b), style, "Character sheet: Mubashir, full-stack developer"))

# ───────────────────────── FOOTER: continue? countdown ─────────────────────────
def footer():
    W, H = 1200, 300
    keys = []
    for i in range(10):
        a, bb = i * 10, (i + 1) * 10
        kf = f"@keyframes d{i}{{0%{{opacity:0}}{a}%{{opacity:1}}{bb}%{{opacity:0}}100%{{opacity:0}}}}"
        if i == 0:
            kf = f"@keyframes d0{{0%{{opacity:1}}10%{{opacity:0}}100%{{opacity:0}}}}"
        keys.append(kf + f".d{i}{{animation:d{i} 10s steps(1) infinite}}")
    style = "".join(keys) + """
.blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
.beat{animation:beat 1s steps(2) infinite;transform-box:fill-box;transform-origin:center}
@keyframes beat{50%{transform:scale(1.15)}}
.tw{animation:tw 2.4s steps(2) infinite}@keyframes tw{50%{opacity:.2}}
"""
    b = []
    b.append(f'<defs><linearGradient id="fb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG2}"/>'
             f'<stop offset="1" stop-color="{BG0}"/></linearGradient></defs>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#fb)"/>')
    g = rng(99)
    for i in range(40):
        x, y = next(g) % W, next(g) % H
        b.append(f'<rect class="tw" x="{x}" y="{y}" width="3" height="3" fill="{WHITE}" style="animation-delay:-{(next(g) % 24) / 10}s"/>')
    b.append(pixtext_c("THANKS FOR PLAYING!", 600, 40, 6, CYAN))
    b.append(pixtext_c("CONTINUE?", 560, 130, 5, YELLOW))
    cx = 560 + text_w("CONTINUE?", 5) / 2 + 40
    for i in range(10):
        b.append(f'<g class="d{i}" opacity="0">{pixtext(str(9 - i), cx, 130, 5, WHITE)}</g>')
    for i in range(3):
        b.append(f'<g class="beat" style="animation-delay:-{i * .2}s">{icon(HEART, 520 + i * 54, 190, 5, PINK)}</g>')
    b.append(f'<g class="blink">{pixtext_c("INSERT COIN TO COLLABORATE", 600, 248, 3, GREEN)}</g>')
    lines = "".join(f'<rect x="0" y="{yy}" width="{W}" height="1" fill="#000" opacity=".18"/>' for yy in range(0, H, 4))
    b.append(lines)
    write("footer.svg", svg(W, H, "".join(b), style, "Thanks for playing! Continue?"))

# ───────────────────────── PLAY button (links to the game) ─────────────────────────
def play_button():
    W, H = 640, 96
    style = """
.blink{animation:bl 1s steps(1) infinite}@keyframes bl{50%{opacity:0}}
.pulse{animation:pu 1.2s steps(2) infinite}@keyframes pu{50%{stroke:#FF2BD6}}
.hop{animation:hop .6s steps(2) infinite}@keyframes hop{50%{transform:translateX(6px)}}
"""
    b = []
    b.append(f'<rect x="8" y="8" width="{W - 16}" height="{H - 16}" fill="#000"/>')
    b.append(f'<rect x="0" y="0" width="{W - 16}" height="{H - 16}" fill="{BG2}"/>')
    b.append(f'<rect class="pulse" x="3" y="3" width="{W - 22}" height="{H - 22}" fill="none" stroke="{CYAN}" stroke-width="6"/>')
    arrow = ["#....", "##...", "###..", "####.", "#####", "####.", "###..", "##...", "#...."]
    b.append(f'<g class="hop">{icon(arrow, 34, 17, 5, YELLOW)}</g>')
    b.append(pixtext("PLAY DEPLOY RUN", 82, 23, 5, WHITE))
    b.append(f'<rect class="blink" x="{82 + text_w("PLAY DEPLOY RUN", 5) + 12}" y="23" width="20" height="35" fill="{PINK}"/>')
    write("play-button.svg", svg(W, H, "".join(b), style, "Play Deploy Run"))

play_button()

header()
character()
footer()
stage(1, "PLAYER PROFILE", CYAN, "stage-1.svg")
stage(2, "INVENTORY", GREEN, "stage-2.svg")
stage(3, "QUEST LOG", YELLOW, "stage-3.svg")
stage(4, "ACHIEVEMENTS", PINK, "stage-4.svg")
stage(5, "BOSS LEVEL", "#FF7A3D", "stage-5.svg")
stage(6, "MULTIPLAYER", "#B388FF", "stage-6.svg")
