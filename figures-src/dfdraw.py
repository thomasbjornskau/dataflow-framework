"""dfdraw – drawing primitives for Dataflow concept figures.

Figures are SVG at 16:9 (1920 x 1080) and can be placed straight into PowerPoint.
Only rect, line, polyline, polygon, circle and text are used, with colours as attributes,
so the files survive import into Office and design tools.

Palette: a neutral slate palette with the same logic as the original Dataflow figures:
dark ink for structure, green for data and data states, violet for roles and proposals,
grey for unresolved or outside scope, and four faint phase colours (GSBPM 4–7).
"""
import math

FONT = "Open Sans, Segoe UI, Arial, sans-serif"

# Neutral palette
INK = "#2b3440"        # structure, dark symbols
TEXT = "#1f262f"       # body text
GREY = "#667080"       # secondary text
RULE = "#d6dae0"       # lines and rules
PANEL, PANEL_EDGE = "#f3f5f9", "#d0d6e0"      # explanation panel, platforms
GREEN, GREEN_2, GREEN_3 = "#2b7a5c", "#bfdfcc", "#eef7f2"   # data and data states
VIOLET, VIOLET_2, VIOLET_3, VIOLET_TEXT = "#6b5fb5", "#c8c3e6", "#f2f1f9", "#483d8b"  # roles, proposals
OUT_GREY, OUT_GREY_2 = "#bcc3cc", "#f4f5f7"   # unresolved, outside scope
DIM_F, DIM_S, DIM_T = "#f6f7f9", "#e2e5ea", "#bcc3cc"      # dimmed (focus variants)
FLOW = "#7a8493"       # data-flow line
MACRO = "#a9b3c0"      # macro-data core and output petals

# Phase bands (GSBPM 4 Collect, 5 Process, 6 Analyse, 7 Disseminate): fill, edge, label colour
PHASE = {
    "collect":     ("Collect",     "#eef7f0", "#cfe6d6", "#3d7a55"),
    "process":     ("Process",     "#eaf4f8", "#c9e1ea", "#2f6f86"),
    "analyse":     ("Analyse",     "#f4f2fc", "#ddd7f5", "#5a4aa8"),
    "disseminate": ("Disseminate", "#fcf8e6", "#eee3b0", "#7a6410"),
}
# System types: 1 bespoke code, 2 framework with menu, 3 framework, 0 advanced (next level)
SYS = {1: ("#47505e", INK), 2: ("#b3bcc8", GREY), 3: ("#ffffff", INK), 0: ("#f6b48f", "#b8643a")}
# Stable data states (two-letter codes)
STATES = [("SD", "Source data"), ("ID", "Input data"), ("PD", "Processed data"), ("ST", "Statistics"), ("OD", "Output data")]

SPOKES = {1: 3, 2: 8, 3: 12, 4: 20}
RADIUS = {1: 13, 2: 17, 3: 21}


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def tw(s, size, weight=400):
    """Rough text width for Open Sans."""
    w = 0
    for ch in str(s):
        if ch in "il.,:;|!'Ijtf ":
            w += 0.3
        elif ch in "mwMW":
            w += 0.9
        elif ch.isupper():
            w += 0.7
        else:
            w += 0.56
    return w * size * (1.07 if weight >= 600 else 1)


def wrap(s, size, maxw, weight=400):
    out, cur = [], ""
    for word in s.split():
        t = (cur + " " + word).strip()
        if tw(t, size, weight) <= maxw:
            cur = t
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


class Fig:
    def __init__(self):
        self.el = ['<rect x="0" y="0" width="1920" height="1080" fill="#ffffff"/>']

    def add(self, s):
        self.el.append(s)

    def rect(self, x, y, w, h, fill="none", stroke="none", sw=1.5, rx=0, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def line(self, x1, y1, x2, y2, stroke=RULE, sw=1.5, dash=None, cap="round"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')

    def poly(self, pts, stroke=FLOW, sw=2, fill="none", dash=None, close=False):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        tag = "polygon" if close else "polyline"
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<{tag} points="{p}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"{d}/>')

    def circle(self, cx, cy, r, fill="none", stroke="none", sw=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=16, weight=400, fill=TEXT, anchor="start", italic=False, ls=None):
        st = ' font-style="italic"' if italic else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{st}{l}>{esc(s)}</text>')

    def lines(self, x, y, rows, size=16, weight=400, fill=TEXT, anchor="start", lh=None, italic=False):
        lh = lh or size * 1.38
        for i, r in enumerate(rows):
            self.text(x, y + i * lh, r, size, weight, fill, anchor, italic)
        return y + len(rows) * lh

    def para(self, x, y, s, size, maxw, weight=400, fill=TEXT, anchor="start", lh=None, italic=False):
        return self.lines(x, y, wrap(s, size, maxw, weight), size, weight, fill, anchor, lh, italic)

    def arrow(self, x1, y1, x2, y2, stroke=INK, sw=2, head=10, dash=None):
        a = math.atan2(y2 - y1, x2 - x1)
        bx, by = x2 - head * math.cos(a), y2 - head * math.sin(a)
        self.line(x1, y1, bx, by, stroke, sw, dash)
        p2 = (bx + head * 0.55 * math.sin(a), by - head * 0.55 * math.cos(a))
        p3 = (bx - head * 0.55 * math.sin(a), by + head * 0.55 * math.cos(a))
        self.poly([(x2, y2), p2, p3], stroke=stroke, sw=1, fill=stroke, close=True)

    def marker(self, cx, cy, n, r=15, fill=INK):
        self.circle(cx, cy, r, fill=fill, stroke="#ffffff", sw=2)
        self.text(cx, cy + 6, n, 17, 700, "#ffffff", "middle")

    def pill(self, x, y, s, size=14, fill=OUT_GREY_2, stroke=OUT_GREY, tc=TEXT, weight=600, h=28, dash=None, padx=12):
        w = tw(s, size, weight) + 2 * padx
        self.rect(x, y, w, h, fill, stroke, 1.5, h / 2, dash)
        self.text(x + w / 2, y + h / 2 + size * 0.36, s, size, weight, tc, "middle")
        return w

    def frame(self, title, subtitle, labels, footer):
        """Title, subtitle, rule, label pills top right, footer bottom right."""
        self.text(60, 92, title, 46, 700, TEXT)
        self.text(60, 136, subtitle, 24, 400, GREY)
        self.line(60, 160, 1860, 160, RULE, 2)
        x = 1860
        for lab, dark in reversed(labels):
            w = tw(lab, 16, 700) + 36
            x -= w
            if dark:
                self.rect(x, 58, w, 36, INK, "none", 0, 18)
                self.text(x + w / 2, 82, lab, 16, 700, "#ffffff", "middle")
            else:
                self.rect(x, 58, w, 36, "#ffffff", INK, 2, 18)
                self.text(x + w / 2, 82, lab, 16, 700, INK, "middle")
            x -= 10
        self.text(1860, 1062, footer, 14, 400, GREY, "end")

    def panel(self, heading, points, y0=180, h=806, box=None, mcolour=INK):
        """points: [(title, text)] – text is wrapped automatically. box: (label, text) dark box at the bottom."""
        self.rect(1440, y0, 420, h, PANEL, PANEL_EDGE, 1.5, 10)
        self.text(1464, y0 + 42, heading, 20, 700, TEXT)
        y = y0 + 86
        for i, (t, body) in enumerate(points, 1):
            self.marker(1478, y - 6, str(i), fill=mcolour)
            self.text(1506, y, t, 18, 700, TEXT)
            y = self.para(1506, y + 25, body, 17, 330, lh=24) + 22
        if box:
            lab, body = box
            rows = wrap(body, 17, 330, 600)
            bh = 46 + len(rows) * 24 + 10
            by = y0 + h - 24 - bh
            self.rect(1464, by, 372, bh, INK, "none", 0, 8)
            self.text(1482, by + 30, lab, 13, 700, GREEN_2)
            self.lines(1482, by + 56, rows, 17, 600, "#ffffff", lh=24)

    def legend(self, items, x=60, y=1046):
        for draw, lab in items:
            w = draw(self, x, y)
            self.text(x + w + 8, y + 5, lab, 15, 400, GREY)
            x += w + 8 + tw(lab, 15) + 18

    def save(self, path):
        body = "\n".join(self.el)
        open(path, "w", encoding="utf-8").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">\n{body}\n</svg>\n')


# ---------------------------------------------------------------- Dataflow symbols
def data_symbol(f, cx, cy, kind="micro", rows=2, cols=2, dim=False, state=None, R=None):
    """kind: meta, micro, macro, stat, out. rows -> size, cols -> spokes. state: stable data state code."""
    R = R or RADIUS[rows]
    s = DIM_S if dim else INK
    core = {"micro": "#ffffff", "macro": MACRO, "stat": INK, "out": INK, "meta": None}[kind]
    if dim and core not in (None, "#ffffff"):
        core = DIM_S
    if kind == "out":
        for k in range(4):
            a = math.pi / 4 + k * math.pi / 2
            f.circle(cx + R * 0.72 * math.cos(a), cy + R * 0.72 * math.sin(a), R * 0.5, DIM_S if dim else MACRO)
    big = R >= 30
    f.circle(cx, cy, R, "#ffffff", s, 3 if big else 1.6)
    ri = R * 0.48 if kind != "meta" else 0
    n = SPOKES[cols]
    for k in range(n):
        a = -math.pi / 2 + k * 2 * math.pi / n
        f.line(cx + ri * math.cos(a), cy + ri * math.sin(a), cx + R * math.cos(a), cy + R * math.sin(a), s, 2 if big else 1.1, cap="butt")
    if kind != "meta":
        f.circle(cx, cy, ri, core, s, 3 if big else 1.6)
    if state:
        state_tag(f, cx + R * 0.8, cy - R * 0.9, state)
    return R


def state_tag(f, x, y, code):
    w = 12 + 9 * len(code)
    f.rect(x - 2, y - 11, w, 20, GREEN, "#ffffff", 1.5, 10)
    f.text(x - 2 + w / 2, y + 4, code, 12, 700, "#ffffff", "middle")


def system_symbol(f, cx, cy, kind=1, w=24, h=34, dim=False):
    fill, s = SYS[kind]
    if dim:
        fill, s = DIM_F, DIM_S
    f.rect(cx - w / 2, cy - h / 2, w, h, fill, s, 1.8, 5)
    if kind == 0 and not dim:
        f.circle(cx - 2, cy - 2, 6, "none", "#8a3f1a", 2)
        f.line(cx + 2.5, cy + 2.5, cx + 7, cy + 7, "#8a3f1a", 2.5)


def phase_band(f, phase, x, y, w, h, label=True, ly=None):
    name, fill, edge, tc = PHASE[phase]
    f.rect(x, y, w, h, fill, edge, 1, 6)
    if label:
        f.text(x + w / 2, (ly or y + 22), name.upper(), 13, 700, tc, "middle", ls=1)
