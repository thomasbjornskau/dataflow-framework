"""The Dataflow concept figures (English edition).

Run from the repository root:   python figures-src/figures.py            (all figures)
                                python figures-src/figures.py a1 c3      (selected figures)
SVG files are written to docs/figures/. Add --png to also write PNG previews to figures-src/preview/.
"""
import os
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from dfdraw import *                       # noqa: E402,F403
from example_ikr import (base_figure, legend_standard, mini_level1, read_ikr, STEPS,  # noqa: E402
                         FOOTER_IKR)

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "figures"
PREVIEW = ROOT / "figures-src" / "preview"
IKR_XLSX = ROOT / "docs" / "files" / "templates" / "dataflow_example_nr_ikr.xlsx"
TAG = ("Dataflow", True)
PNG = "--png" in sys.argv


def save(f, name):
    OUT.mkdir(parents=True, exist_ok=True)
    f.save(OUT / f"{name}.svg")
    if PNG:
        import cairosvg
        PREVIEW.mkdir(parents=True, exist_ok=True)
        cairosvg.svg2png(url=str(OUT / f"{name}.svg"), write_to=str(PREVIEW / f"{name}.png"), output_width=1920)


def box_legend(fill, stroke, dash=None, sw=1.5):
    return lambda f, x, y: (f.rect(x, y - 10, 28, 20, fill, stroke, sw, 4, dash), 28)[1]


def tag_legend(code="SD"):
    return lambda f, x, y: (state_tag(f, x + 4, y, code), 30)[1]


# ------------------------------------------------------------ shared small drawings
def tangle(f, x, y, dim=False):
    """Schematic current process: many intakes, crossing connections, manual editing. About 400 x 170."""
    c = DIM_S if dim else FLOW
    src = [(x, y + 20 + i * 28) for i in range(6)]
    rec = [(x + 80, y + 20 + i * 28) for i in range(6)]
    mid = [(x + 175, y + 35), (x + 175, y + 90), (x + 175, y + 145)]
    tot, ed, out = (x + 270, y + 90), (x + 335, y + 90), (x + 400, y + 90)
    for i in range(6):
        f.line(*src[i], *rec[i], c, 1.5)
    for i, j in [(0, 0), (1, 0), (2, 1), (3, 0), (4, 2), (5, 1), (2, 2), (5, 2), (1, 1)]:
        f.line(*rec[i], *mid[j], c, 1.5)
    for p in mid:
        f.line(*p, *tot, c, 2)
    f.line(x + 80, y + 20, x + 80, y - 10, c, 1.2)
    f.poly([(x + 80, y - 10), (x + 300, y - 10), (x + 300, y + 90)], c, 1.2)
    f.line(*tot, *ed, c, 2.4)
    f.line(*ed, *out, c, 2.4)
    f.poly([(ed[0], ed[1] + 14), (ed[0], ed[1] + 60), (mid[2][0] + 14, ed[1] + 60), (mid[2][0] + 14, mid[2][1] + 10)], c, 1.2, dash="4 3")
    for p in src:
        data_symbol(f, *p, "micro", 1, 2, dim)
    for p in rec:
        system_symbol(f, *p, 1, 16, 22, dim)
    for p in mid:
        data_symbol(f, *p, "macro", 1, 3, dim)
    system_symbol(f, *tot, 1, 18, 26, dim)
    system_symbol(f, *ed, 0, 18, 26, dim)
    data_symbol(f, *out, "stat", 2, 3, dim)


def clean_flow(f, x, y, w, violet=True):
    """Target state: the five data states as anchors, needs in between."""
    kinds = [("SD", "micro", 2), ("ID", "micro", 3), ("PD", "micro", 3), ("ST", "stat", 3), ("OD", "out", 3)]
    step = w / 4
    for i in range(4):
        x1 = x + i * step
        f.line(x1 + 22, y, x1 + step - 22, y, FLOW, 2.4)
        bx = x1 + step / 2
        f.rect(bx - 32, y - 15, 64, 30, VIOLET_3 if violet else "#ffffff", VIOLET if violet else INK, 1.8, 6, "4 3" if violet else None)
        if violet:
            f.text(bx, y + 5, "need", 12, 700, VIOLET_TEXT, "middle")
    for i, (k, t, c) in enumerate(kinds):
        data_symbol(f, x + i * step, y, t, 2, c, state=k)


# ------------------------------------------------------------ A1
def a1():
    f = Fig()
    f.frame("From moving to improving", "Retiring legacy platforms forces a migration. What we cannot see, we take with us.",
            [("Discussion", False), TAG], "Draft · Dataflow framework · Schematic")
    X0, X1 = 140, 1380
    yr = lambda a: X0 + a * (X1 - X0) / 5
    f.text(60, 214, "DEADLINES", 13, 700, GREY, ls=1)
    f.line(X0, 250, X1, 250, RULE, 3)
    for a in range(6):
        f.line(yr(a), 244, yr(a), 256, OUT_GREY, 2)
        f.text(yr(a), 280, f"Year {a}", 14, 600, GREY, "middle")
    f.circle(yr(0.4), 250, 7, "#ffffff", INK, 2.5)
    f.text(yr(0.4), 226, "Now", 14, 700, TEXT, "middle")
    for a, name, sub in [(2.2, "Platform A", "retired"), (2.9, "Platform B", "retired"), (3.9, "Platform C", "retired")]:
        f.circle(yr(a), 250, 9, INK)
        f.text(yr(a), 226, name, 16, 700, TEXT, "middle")
        f.text(yr(a), 300, sub, 13, 400, GREY, "middle")

    def lane(y0, title, sub, violet):
        f.rect(60, y0, 1340, 300, "#ffffff", VIOLET if violet else RULE, 1.5, 10, "6 4" if violet else None)
        f.text(84, y0 + 36, title, 20, 700, VIOLET_TEXT if violet else TEXT)
        f.text(84, y0 + 62, sub, 15, 400, GREY)

    lane(330, "Move the process as it is", "Same steps on a new platform", False)
    tangle(f, 120, 430)
    f.arrow(560, 520, 660, 520, INK, 3, 14)
    f.rect(690, 360, 690, 250, PANEL, PANEL_EDGE, 2, 10)
    f.text(710, 388, "TARGET PLATFORM", 13, 700, GREY, ls=1)
    tangle(f, 820, 398)
    f.text(1035, 594, "Manual steps, duplicated work and hidden dependencies come along", 14, 600, GREY, "middle")

    lane(660, "Migrate with added value", "Map first, simplify where it pays", True)
    tangle(f, 120, 760)
    f.arrow(560, 850, 600, 850, INK, 3, 14)
    f.rect(606, 800, 150, 110, VIOLET_3, VIOLET, 2, 10)
    f.lines(681, 836, ["Mapping", "Dataflow"], 15, 700, VIOLET_TEXT, "middle", lh=20)
    f.text(681, 885, "today → target → needs", 12, 400, VIOLET_TEXT, "middle")
    f.arrow(760, 855, 800, 855, INK, 3, 14)
    f.rect(810, 690, 570, 250, PANEL, PANEL_EDGE, 2, 10)
    f.text(830, 718, "TARGET PLATFORM", 13, 700, GREY, ls=1)
    f.text(1095, 780, "SD  →  ID  →  PD  →  ST  →  OD", 13, 700, GREEN, "middle")
    clean_flow(f, 860, 830, 480)
    f.text(1095, 900, "Stable data states, fewer steps, traceable changes", 14, 600, GREY, "middle")

    f.panel("The message", [
        ("Deadlines are set", "Legacy platforms are retired on fixed dates. The dates decide when, not how."),
        ("Two ways to move", "Move the processes as they are, or use the migration to improve them."),
        ("We cannot see the whole", "Manual steps, duplicated work and dependencies are spread across tools and platforms."),
        ("Mapping shows the value", "Dataflow draws today's process and the target state in the same symbols. The difference is the needs."),
    ], box=("GOAL", "A migration that adds value, not just a move."))
    f.legend([
        (box_legend(PANEL, PANEL_EDGE), "Target platform"),
        (box_legend(VIOLET_3, VIOLET, "4 3"), "Proposal / target state"),
        (tag_legend(), "Stable data state"),
        (lambda f, x, y: (system_symbol(f, x + 7, y, 0, 14, 20), 14)[1], "Manual step"),
    ])
    save(f, "A1")


# ------------------------------------------------------------ A2
def a2():
    nodes, edges = read_ikr(IKR_XLSX)
    f = Fig()
    f.frame("What we cannot see, we take with us",
            "An income and capital account drawn straight from Dataflow 2.0 metadata: 28 systems, 42 data sets, 76 connections",
            [("Today · example", False), TAG], "Draft · Source: Dataflow 2.0 metadata, Statistics Norway (NR IKR) · Markings are interpretation")
    X = lambda gx: 100 + (gx - 1) * 79
    Y = lambda gy: 250 + (gy - 1) * 52
    phase_band(f, "process", 60, 196, X(5.5) - 60, 790)
    phase_band(f, "analyse", X(5.5), 196, X(15.5) - X(5.5), 790)
    phase_band(f, "disseminate", X(15.5), 196, 1400 - X(15.5), 790)
    for a, b in edges:
        n1, n2 = nodes[a], nodes[b]
        sw = {1: 1.3, 2: 2.0, 3: 2.8}.get(n1["rows"] if n1["obj"] == "data" else 2, 2)
        f.line(X(n1["gx"]), Y(n1["gy"]), X(n2["gx"]), Y(n2["gy"]), FLOW, sw)
    for n in nodes.values():
        x, y = X(n["gx"]), Y(n["gy"])
        if n["obj"] == "data":
            kind = n["dtype"] if n["dtype"] in ("meta", "micro", "macro", "stat", "out") else "micro"
            R = data_symbol(f, x, y, kind, min(int(n["rows"]), 2), int(n["cols"]))
        else:
            system_symbol(f, x, y, int(n["sys"]) if n["sys"] is not None else 1, 16, 24)
            R = 12
        f.text(x, y + R + 12, n["name"][:14], 9, 600, GREY, "middle")
    for nr, (x, y, w, h) in [("1", (X(2) - 26, Y(2) - 22, 52, Y(14) - Y(2) + 44)), ("2", (X(11) - 30, Y(5) - 24, 60, 48)),
                            ("3", (X(13) - 26, Y(4) - 24, X(15) - X(13) + 52, Y(5) - Y(4) + 48)),
                            ("4", (X(1) - 26, Y(9) - 22, 52, Y(14) - Y(9) + 44))]:
        f.rect(x, y, w, h, "none", VIOLET, 2.5, 10, "6 4")
        f.marker(x, y, nr, 16, VIOLET)
    f.panel("What lies hidden", [
        ("13 similar intakes", "Each source has its own SAS/Excel intake with recoding."),
        ("Manual editing", "All figures pass through a spreadsheet for inspection and manual correction."),
        ("Two parallel runs", "National and European (ESA) figures are recoded and loaded separately."),
        ("Dependencies", "Six inputs come from other national accounts."),
    ], box=("POINT", "Move the process as it is, and all of this moves with it."), mcolour=VIOLET)
    legend_standard(f)
    save(f, "A2")


# ------------------------------------------------------------ A3
def a3():
    f = Fig()
    f.frame("We do not start from scratch", "Dataflow was developed in two rounds at Statistics Norway. The third builds on both.",
            [("Overview", False), TAG], "Draft · Source: Dataflow 1.0 and 2.0 documentation, Statistics Norway")
    cards = [
        ("1.0", "Drawn by hand", "Adobe Illustrator", False,
         ["Rich picture: process names, roles, time use and iterations", "The data and system symbols were developed"],
         "DRAWBACKS", ["More than 2–3 days per drawing", "Hard to change and keep up to date"], ("A handful", "of drawings")),
        ("2.0", "Drawn from metadata", "Excel and Tableau", False,
         ["From 2–3 days to 15 minutes", "About 120 flows drawn", "AS IS can be copied to TO BE", "Shared on web, PDF and slides"],
         "MISSING", ["Roles, process steps, dependencies", "Coordinates placed by hand", "Everything through one person", "Unclear how much drawings are used"],
         ("≈ 120", "flows")),
        ("3.0", "AI-supported", "Templates and an AI skill", True,
         ["Contact persons fill in the templates", "Three levels: overview, focus, detail", "Shows needs and value, not only today"],
         "REQUIRES", ["Subject-matter owners confirm all", "AI support is tested and adjusted"], ("Complex", "statistics first")),
    ]
    W, G = 425, 32
    for i, (ver, title, tool, violet, gave, lab2, lacked, scope) in enumerate(cards):
        x = 60 + i * (W + G)
        f.rect(x, 196, W, 790, VIOLET_3 if violet else "#ffffff", VIOLET if violet else INK, 2, 12, "6 4" if violet else None)
        f.text(x + 24, 256, ver, 44, 700, VIOLET_TEXT if violet else TEXT)
        f.text(x + 110, 238, title, 20, 700, VIOLET_TEXT if violet else TEXT)
        f.text(x + 110, 262, tool, 15, 400, GREY)
        if violet:
            f.pill(x + W - 150, 212, "THIS FRAMEWORK", 11, "#ffffff", VIOLET, VIOLET_TEXT, 700, 24, None, 9)
        bx, by, bw, bh = x + 20, 290, W - 40, 250
        f.rect(bx, by, bw, bh, "#ffffff" if not violet else "#fbfbff", RULE, 1.2, 8)
        if ver == "1.0":
            for k, (fx0, fw) in zip(["collect", "process", "analyse", "disseminate"], [(0, 0.28), (0.24, 0.3), (0.5, 0.28), (0.75, 0.25)]):
                f.rect(bx + 8 + fx0 * (bw - 16), by + 10, fw * (bw - 16), bh - 20, PHASE[k][1], "none", 0, 4)
            pts = [(bx + 20, by + 150), (bx + 80, by + 120), (bx + 150, by + 160), (bx + 220, by + 110), (bx + 300, by + 140), (bx + bw - 20, by + 100)]
            f.poly(pts, OUT_GREY, 16)
            f.poly(pts, FLOW, 3)
            for j, (px, py) in enumerate(pts[1:-1]):
                system_symbol(f, px, py, [1, 2, 1, 3][j], 16, 24)
            f.text(bx + 150, by + 200, "MICRO EDITING", 11, 700, TEXT, "middle")
            f.text(bx + 260, by + 80, "MACRO EDITING", 11, 700, TEXT, "middle")
            f.pill(bx + 20, by + 24, "Respondent", 11, VIOLET_3, VIOLET, VIOLET_TEXT, 700, 20, padx=6)
            f.rect(bx + 8, by + bh - 30, bw - 16, 20, INK, "none", 0, 3)
            f.text(bx + 18, by + bh - 16, "Time use and duration per phase", 11, 600, "#ffffff")
        elif ver == "2.0":
            nodes, edges = read_ikr(IKR_XLSX)
            X = lambda gx: bx + 18 + (gx - 1) * (bw - 36) / 16
            Y = lambda gy: by + 20 + (gy - 1) * (bh - 40) / 13
            for a, b in edges:
                f.line(X(nodes[a]["gx"]), Y(nodes[a]["gy"]), X(nodes[b]["gx"]), Y(nodes[b]["gy"]), FLOW, 0.9)
            for n in nodes.values():
                if n["obj"] == "data":
                    f.circle(X(n["gx"]), Y(n["gy"]), 4.5, "#ffffff", INK, 1.2)
                else:
                    f.rect(X(n["gx"]) - 3.5, Y(n["gy"]) - 5, 7, 10, SYS.get(int(n["sys"] or 1), SYS[1])[0], INK, 1, 1.5)
            f.text(bx + bw - 10, by + bh - 10, "Example drawn from Excel", 11, 600, GREY, "end")
        else:
            for j, name in enumerate(["Overview", "Focus", "Detail"]):
                rx, ry = bx + 20 + j * 40, by + 18 + j * 70
                f.rect(rx, ry, bw - 40 - j * 80, 64, "#ffffff", VIOLET if j else INK, 1.6, 6, "4 3" if j == 2 else None)
                f.text(rx + 12, ry + 24, f"Level {j + 1} · {name}", 13, 700, TEXT)
                for q in range(4 - j):
                    if j:
                        system_symbol(f, rx + 24 + q * 34, ry + 46, 1, 12, 16)
                    else:
                        f.rect(rx + 14 + q * 50, ry + 36, 40, 18, "#ffffff", INK, 1.2, 3)
        f.text(x + 24, 580, "WHAT IT GAVE" if not violet else "WHAT IT GIVES", 13, 700, GREEN, ls=1)
        yy = 606
        for row in gave:
            yy = f.para(x + 24, yy, row, 16, W - 48, lh=22) + 2
        yy += 14
        f.text(x + 24, yy, lab2, 13, 700, "#b8643a" if not violet else VIOLET_TEXT, ls=1)
        yy += 26
        for row in lacked:
            yy = f.para(x + 24, yy, row, 16, W - 48, lh=22) + 2
        f.line(x + 24, 860, x + W - 24, 860, VIOLET_2 if violet else RULE, 1.5)
        f.text(x + 24, 890, "SCOPE", 13, 700, GREY, ls=1)
        f.text(x + 24, 940, scope[0], 34, 700, VIOLET_TEXT if violet else TEXT)
        f.text(x + 30 + tw(scope[0], 34, 700), 940, scope[1], 17, 400, GREY)
    for i in range(2):
        x = 60 + (i + 1) * (W + G) - G / 2
        f.circle(x, 590, 14, "#ffffff", INK, 2)
        f.arrow(x - 6, 590, x + 7, 590, INK, 2, 8)
    f.panel("The starting point", [
        ("The method exists", "The data and system symbols have been tested in two rounds."),
        ("Much is mapped", "Flows drawn in 2.0 can become drafts in 3.0."),
        ("The gaps are known", "Roles, process steps and dependencies. The templates ask for exactly these."),
        ("3.0 takes the best of both", "The rich picture from 1.0 and the automation from 2.0."),
    ], box=("REUSE", "Existing 2.0 flows can be read in directly, as figure A2 shows."))
    save(f, "A3")


# ------------------------------------------------------------ B1
def b1():
    f = Fig()
    f.frame("Three levels", "Overview for decisions, focus for solution work, detail only where needed",
            [("Overview · method", False), TAG], "Draft · Example: Statistics Norway, NR IKR · Level 3 is not mapped")
    PX, PW = [60, 517, 974], 426
    for i, (lv, name) in enumerate([("LEVEL 1", "Overview"), ("LEVEL 2", "Focus"), ("LEVEL 3", "Detail")]):
        f.rect(PX[i], 196, PW, 400, "#ffffff", INK if i < 2 else OUT_GREY, 2, 10, "6 4" if i == 2 else None)
        f.text(PX[i] + 20, 230, lv, 14, 700, GREY, ls=1)
        f.text(PX[i] + 20, 262, name, 26, 700, TEXT)
    f.text(PX[1] + PW - 20, 258, "Summing and reconciliation", 14, 600, GREY, "end")
    f.text(PX[2] + PW - 20, 258, "EXCEL EDIT", 14, 600, GREY, "end")
    pos = mini_level1(f, PX[0] + 20, 290, PW - 40, 280, highlight={"P5"})
    # level 2
    x0, yc = PX[1] + 30, 440
    ins = [("IKKE-FIN", "micro", 3), ("IBERKAP", "macro", 2), ("AKSJE", "macro", 2), ("REA", "stat", 3), ("RG", "stat", 3)]
    for j in range(len(ins)):
        f.line(x0 + 14, 310 + j * 52, x0 + 98, yc, FLOW, 1.4)
    for j, (nm, t, c) in enumerate(ins):
        data_symbol(f, x0 + 10, 310 + j * 52, t, 1, c)
        f.text(x0 + 30, 310 + j * 52 - 12, nm, 10, 600, GREY)
    chain = [("sys", 1, "SAS SUM"), ("data", ("macro", 3), "ALT SAMLET"), ("sys", 1, "SAS AVSTEM"), ("data", ("macro", 3), "INPUT EXCEL"), ("sys", 0, "EXCEL EDIT")]
    xs = [x0 + 100 + k * 66 for k in range(5)]
    f.line(xs[0], yc, xs[-1], yc, FLOW, 2.4)
    for k, ((kind, t, nm), xx) in enumerate(zip(chain, xs)):
        if kind == "sys":
            system_symbol(f, xx, yc, t, 20, 28)
        else:
            data_symbol(f, xx, yc, t[0], 2, t[1])
        f.text(xx, yc + (36 if kind == "sys" else 34) + (14 if k % 2 else 0), nm, 10, 600, GREY, "middle")
    f.rect(xs[-1] - 22, yc - 28, 44, 56, "none", VIOLET, 2.5, 6)
    px = x0 + 96
    for lab, fill, st, tc, dash in [("SAS", OUT_GREY_2, OUT_GREY, TEXT, None), ("Excel", OUT_GREY_2, OUT_GREY, TEXT, None),
                                    ("Role: ?", VIOLET_3, VIOLET, VIOLET_TEXT, "4 3")]:
        px += f.pill(px, 540, lab, 11, fill, st, tc, 700, 22, dash, 8) + 6
    # level 3
    x3 = PX[2] + 30
    data_symbol(f, x3 + 10, yc, "macro", 2, 3)
    f.text(x3 + 10, yc + 34, "INPUT EXCEL", 10, 600, GREY, "middle")
    for k, nm in enumerate(["Inspect figures", "Correct manually", "Save flat file"]):
        bx = x3 + 46 + k * 104
        f.rect(bx, yc - 26, 92, 52, OUT_GREY_2, OUT_GREY, 1.5, 6, "5 3")
        f.lines(bx + 46, yc - 4, wrap(nm, 12, 80, 700), 12, 700, GREY, "middle", lh=15)
        f.text(bx + 46, yc + 44, "?", 16, 700, GREY, "middle")
        if k < 2:
            f.arrow(bx + 92, yc, bx + 104, yc, GREY, 1.5, 6)
    f.line(x3 + 22, yc, x3 + 46, yc, FLOW, 1.6)
    f.line(x3 + 46 + 2 * 104 + 92, yc, x3 + 46 + 2 * 104 + 112, yc, FLOW, 1.6)
    data_symbol(f, x3 + 360, yc, "stat", 2, 3)
    f.text(x3 + 360, yc + 34, "TAB", 10, 600, GREY, "middle")
    f.lines(x3, 330, ["Description in 2.0: “Spreadsheet that supports", "inspection of figures and manual editing”"], 13, 400, GREY, italic=True, lh=18)
    f.pill(x3, 540, "Not mapped", 12, "#ffffff", OUT_GREY, GREY, 700, 24, "4 3", 10)
    rx, ry, rw, rh = pos["P5"]
    f.poly([(rx + rw, ry), (PX[1], 196)], VIOLET, 1.4, dash="4 3")
    f.poly([(rx + rw, ry + rh), (PX[1], 596)], VIOLET, 1.4, dash="4 3")
    f.poly([(xs[-1] + 22, yc - 28), (PX[2], 196)], VIOLET, 1.4, dash="4 3")
    f.poly([(xs[-1] + 22, yc + 28), (PX[2], 596)], VIOLET, 1.4, dash="4 3")
    rows = [("For whom", "Management, steering groups and project leads", "Project team, subject-matter area and platform teams", "Developers and subject experts building the solution"),
            ("Answers", "What does the process consist of, and what is urgent?", "Which data and systems are in the step?", "What happens inside one system or spreadsheet?"),
            ("Template", "D1 Process steps and roles", "D2 Data and systems", "A separate session, when needed"),
            ("Scope", "Often 5–10 process steps", "One process step, often 5–20 elements", "One system")]
    y = 630
    for lab, *cells in rows:
        f.text(60, y, lab.upper(), 12, 700, GREY, ls=1)
        for i, c in enumerate(cells):
            f.para(PX[i] + 20, y + 24, c, 15, PW - 40, lh=20)
        y += 88
        f.line(60, y - 22, 1400, y - 22, RULE, 1)
    f.panel("How to use the levels", [
        ("Start with the overview", "Level 1 fits on one slide and can be read by managers."),
        ("Open where needed", "Each process step can become its own focus figure with data and systems."),
        ("Detail only when needed", "Level 3 is for systems that hide important steps, such as EXCEL EDIT."),
        ("Same symbols", "All levels use the same symbol language, so they can be read together."),
    ], box=("FROM 2.0", "System type 0, ‘next level’, was intended for this but never drawn."))
    save(f, "B1")


# ------------------------------------------------------------ B2
def b2():
    f = Fig()
    f.frame("One symbol language", "The symbols from Dataflow 2.0 are kept. What is new covers what mapping asks for.",
            [("Overview · symbols", False), TAG], "Draft · Source: Dataflow 2.0 symbol legend · New elements are proposals")
    f.rect(60, 196, 660, 790, "#ffffff", INK, 2, 10)
    f.text(84, 232, "FROM DATAFLOW 2.0 · KEPT", 14, 700, GREY, ls=1)
    cx, cy = 190, 360
    data_symbol(f, cx, cy, "macro", 3, 3, R=78)
    for (tx, ty, ax, ay, lab, sub) in [(300, 290, cx + 20, cy - 10, "The core", "what kind of data"), (300, 360, cx + 66, cy + 20, "The spokes", "how many variables"),
                                       (300, 430, cx + 70, cy + 52, "The size", "how many rows")]:
        f.line(ax, ay, tx - 8, ty - 6, GREY, 1.2)
        f.circle(ax, ay, 3, GREY)
        f.text(tx, ty, lab, 16, 700, TEXT)
        f.text(tx + tw(lab, 16, 700) + 8, ty, sub, 15, 400, GREY)
    y = 500
    f.text(84, y, "DATA TYPE", 12, 700, GREY, ls=1)
    for i, (t, nm) in enumerate([("meta", "Metadata"), ("micro", "Micro data"), ("macro", "Macro data"), ("stat", "Statistics"), ("out", "Output")]):
        data_symbol(f, 110 + i * 122, y + 44, t, 2, 3)
        f.text(110 + i * 122, y + 84, nm, 13, 600, TEXT, "middle")
    f.text(84, y + 112, "Output ‘springs out and blossoms’: openly available statistics.", 13, 400, GREY, italic=True)
    y = 650
    f.text(84, y, "ROWS", 12, 700, GREY, ls=1)
    for i, nm in enumerate(["Few", "Medium", "Many"]):
        data_symbol(f, 110 + i * 70, y + 40, "micro", i + 1, 2)
        f.text(110 + i * 70, y + 80, nm, 12, 400, GREY, "middle")
    f.text(374, y, "VARIABLES", 12, 700, GREY, ls=1)
    for i, nm in enumerate(["Very few", "Few", "Many", "Very many"]):
        data_symbol(f, 398 + i * 74, y + 40, "micro", 2, i + 1)
        f.text(398 + i * 74, y + 80, nm, 12, 400, GREY, "middle")
    y = 780
    f.text(84, y, "SYSTEM TYPE", 12, 700, GREY, ls=1)
    for i, (t, nm, sub) in enumerate([(1, "Bespoke code", "The team develops and controls it"), (2, "Framework with menu", "The team can adjust settings"),
                                      (3, "Framework", "The team cannot change it"), (0, "Next level", "Can be opened as a detail figure")]):
        x = 84 + (i % 2) * 318
        yy = y + 34 + (i // 2) * 76
        system_symbol(f, x + 14, yy + 10, t, 24, 34)
        f.text(x + 40, yy + 6, nm, 15, 700, TEXT)
        f.text(x + 40, yy + 28, sub, 13, 400, GREY)
    # right: new
    f.rect(740, 196, 660, 790, VIOLET_3, VIOLET, 2, 10, "6 4")
    f.text(764, 232, "NEW IN 3.0", 14, 700, VIOLET_TEXT, ls=1)
    y = 276
    f.text(764, y, "STABLE DATA STATE", 12, 700, GREY, ls=1)
    for i, (k, nm) in enumerate(STATES):
        x = 790 + i * 118
        data_symbol(f, x, y + 46, "micro" if i < 3 else ("stat" if i == 3 else "out"), 2, 3, state=k)
        f.text(x, y + 88, nm, 13, 600, GREEN, "middle")
    f.para(764, y + 116, "Marks where a data set is stored in an agreed state. The data type says what the data are; the tag says where they are stable.", 13, 610, fill=GREY, lh=18)
    y = 460
    f.text(764, y, "PROCESS STEP, ROLE AND PLATFORM", 12, 700, GREY, ls=1)
    f.rect(764, y + 18, 220, 104, "#ffffff", INK, 2, 8)
    f.text(780, y + 46, "Process step", 15, 700, TEXT)
    system_symbol(f, 788, y + 92, 1, 16, 24)
    system_symbol(f, 812, y + 92, 1, 16, 24)
    f.pill(900, y + 80, "SAS", 11, OUT_GREY_2, OUT_GREY, TEXT, 700, 22, padx=8)
    f.pill(1004, y + 20, "Role", 12, VIOLET_3, VIOLET, VIOLET_TEXT, 700, 24, padx=10)
    f.text(1066, y + 37, "who does what", 13, 400, GREY)
    f.pill(1004, y + 56, "SAS", 12, OUT_GREY_2, OUT_GREY, TEXT, 700, 24, padx=10)
    f.text(1060, y + 73, "platform", 13, 400, GREY)
    f.pill(1004, y + 92, "FAME", 12, INK, INK, "#ffffff", 700, 24, padx=10)
    f.text(1072, y + 109, "platform with the nearest deadline", 13, 400, GREY)
    y = 620
    f.text(764, y, "CONNECTIONS", 12, 700, GREY, ls=1)
    for i, (sty, nm) in enumerate([("flow", "Data flow, thickness by volume"), ("meta", "Metadata, for example code lists"), ("dep", "Dependency on other statistics")]):
        yy = y + 34 + i * 34
        if sty == "flow":
            f.line(764, yy, 860, yy, FLOW, 3)
        elif sty == "meta":
            f.line(764, yy, 860, yy, GREEN, 1.6)
        else:
            f.line(764, yy, 860, yy, GREY, 1.6, "6 4")
        f.text(876, yy + 5, nm, 14, 400, TEXT)
    y = 760
    f.text(764, y, "STATUS", 12, 700, GREY, ls=1)
    f.pill(764, y + 18, "?", 13, "#ffffff", OUT_GREY, GREY, 700, 26, "4 3", 14)
    f.text(806, y + 37, "Unresolved. Never guessed.", 14, 400, TEXT)
    f.pill(1040, y + 18, "need", 12, VIOLET_3, VIOLET, VIOLET_TEXT, 700, 26, "4 3", 12)
    f.text(1108, y + 37, "Proposal or target state", 14, 400, TEXT)
    y = 850
    f.text(764, y, "PHASES (GSBPM 4–7)", 12, 700, GREY, ls=1)
    for i, k in enumerate(["collect", "process", "analyse", "disseminate"]):
        nm, fill, edge, tc = PHASE[k]
        x = 764 + i * 154
        f.rect(x, y + 18, 144, 70, fill, edge, 1, 6)
        f.text(x + 72, y + 58, nm, 14, 700, tc, "middle")
    f.panel("The choices", [
        ("Codes are kept", "Data type, rows, variables and system type are as in 2.0. Existing flows can be read in directly."),
        ("Two properties of data", "The data type says what the data are. The tag shows where they are stored as stable."),
        ("What mapping needs", "Roles, process steps, platforms and dependencies."),
        ("Neutral colours, four phases", "The phase colours link the drawing to GSBPM phases 4–7."),
    ], box=("PRINCIPLE", "Every symbol and every line type has one meaning."))
    save(f, "B2")


# ------------------------------------------------------------ B3
def b3():
    f = Fig()
    f.frame("From current process to target state", "The current process shows what is. The target state shows what is needed. The difference is the needs.",
            [("Overview · method", False), TAG], "Draft · Dataflow framework · Schematic example")
    X = {"collect": 240, "process": 530, "analyse": 820, "disseminate": 1110}
    W = 290

    def row_label(y, h, title, sub, violet=False):
        f.rect(60, y, 160, h, VIOLET_3 if violet else "#ffffff", VIOLET if violet else INK, 2, 8, "6 4" if violet else None)
        f.text(78, y + 34, title, 18, 700, VIOLET_TEXT if violet else TEXT)
        f.lines(78, y + 60, sub, 14, 400, GREY, lh=19)

    row_label(196, 340, "Today", ["AS IS", "template D1–D2"])
    for k in X:
        phase_band(f, k, X[k], 196, W - 6, 340)
    for k, role in [("collect", "Role"), ("process", "Role"), ("analyse", "Role ?"), ("disseminate", "Role")]:
        f.pill(X[k] + W / 2 - 34, 234, role, 12, VIOLET_3, VIOLET, VIOLET_TEXT, 700, 24, "4 3" if "?" in role else None, 12)
    steps = [("collect", 0, "Intake", ["Portal", "Survey"], [3, 2]),
             ("process", 0, "Checks and editing", ["SAS", "Forms"], [1, 2]),
             ("analyse", -71, "Calculation", ["SAS"], [1]),
             ("analyse", 71, "Manual adjustment", ["Excel"], [0]),
             ("disseminate", 0, "Publishing", ["Database", "Web"], [2, 3])]
    cy = 350
    pos = []
    for k, dx, *_r in steps:
        bw = 200 if dx == 0 else 108
        pos.append((X[k] + (W - 6) / 2 - bw / 2 + dx, bw))
    for ((a, b), (t, c)) in zip([(pos[i][0] + pos[i][1], pos[i + 1][0]) for i in range(4)], [("micro", 2), ("micro", 3), ("macro", 3), ("stat", 3)]):
        f.line(a, cy, b, cy, FLOW, 2.6)
        data_symbol(f, (a + b) / 2, cy, t, 1 if b - a < 60 else 2, c)
    for (k, dx, nm, plat, syst), (bx, bw) in zip(steps, pos):
        f.rect(bx, cy - 58, bw, 116, "#ffffff", INK, 2, 8)
        rows = wrap(nm, 15, bw - 24, 700)
        f.lines(bx + 12, cy - 32, rows, 15, 700, TEXT, lh=19)
        for i, t in enumerate(syst):
            system_symbol(f, bx + 22 + i * 26, cy + (12 if len(rows) > 1 else 2), t, 16, 24)
        px = bx + 10
        for p in plat:
            px += f.pill(px, cy + 28, p, 11, OUT_GREY_2, OUT_GREY, TEXT, 700, 22, padx=8) + 4
    f.pill(X["collect"] + 16, 470, "In from: other statistics, registers", 12, "#ffffff", OUT_GREY, GREY, 600, 24, "4 3", 10)
    f.pill(X["disseminate"] + 20, 470, "Out to: users, partners", 12, "#ffffff", OUT_GREY, GREY, 600, 24, "4 3", 10)
    f.rect(240, 556, 1154, 52, "#ffffff", VIOLET, 1.5, 26, "6 4")
    f.text(817, 589, "The difference becomes the list of needs  →  assessed, then logged in the backlog", 17, 700, VIOLET_TEXT, "middle")
    for x in [340, 675, 965, 1255]:
        f.arrow(x, 538, x, 552, VIOLET, 2, 9)
        f.arrow(x, 610, x, 628, VIOLET, 2, 9)
    row_label(636, 330, "Target", ["TO BE", "template D3"], violet=True)
    for k in X:
        phase_band(f, k, X[k], 636, W - 6, 330)
    anchors = [("SD", "Source data", 340, "micro", 2), ("ID", "Input data", 590, "micro", 3), ("PD", "Processed data", 760, "micro", 3),
               ("ST", "Statistics", 965, "stat", 3), ("OD", "Output data", 1255, "out", 3)]
    ya = 770
    for i in range(4):
        a, b = anchors[i][2], anchors[i + 1][2]
        f.line(a + 22, ya, b - 22, ya, FLOW, 2.4)
        m = (a + b) / 2
        f.rect(m - 34, ya - 16, 68, 32, VIOLET_3, VIOLET, 1.8, 6, "4 3")
        f.text(m, ya + 5, "need", 12, 700, VIOLET_TEXT, "middle")
    for code, nm, x, t, c in anchors:
        data_symbol(f, x, ya, t, 2, c, state=code)
        f.text(x, ya + 44, nm, 14, 700, GREEN, "middle")
    x = 250
    for r in ["Services", "Processes", "Variables and states", "Dependencies"]:
        x += f.pill(x, 870, r, 13, VIOLET_3, VIOLET, VIOLET_TEXT, 600, 26, "4 3", 11) + 10
    f.pill(x + 6, 870, "?  is a valid answer", 13, "#ffffff", OUT_GREY, GREY, 600, 26, "4 3", 11)
    f.text(250, 920, "Needs are described per data state, in four rows. No systems until the solution has been assessed.", 14, 400, GREY)
    f.panel("How it fits together", [
        ("The current process", "Process steps, roles, platforms and data, as the process runs today."),
        ("The target state", "The five data states are fixed anchor points. Between them are needs, not systems."),
        ("Same symbol language", "Data and systems are drawn the same way in both, so the difference shows."),
        ("The difference is the needs", "What must change becomes the list of needs. A later assessment decides what exists and what must be built."),
    ], box=("RULE", "The target state shows needs. Systems are drawn only after the solution has been assessed."))
    f.legend([
        (tag_legend(), "Stable data state"),
        (box_legend(VIOLET_3, VIOLET, "4 3"), "Need / proposal"),
        (box_legend("#ffffff", INK, None, 2), "Process step today"),
        (lambda f, x, y: f.pill(x, y - 11, "SAS", 11, OUT_GREY_2, OUT_GREY, TEXT, 700, 22, padx=6), "Platform"),
        (lambda f, x, y: f.pill(x, y - 11, "Role", 11, VIOLET_3, VIOLET, VIOLET_TEXT, 700, 22, padx=6), "Who does what"),
    ])
    save(f, "B3")


# ------------------------------------------------------------ B4
def b4():
    f = Fig()
    f.frame("Four lenses for decisions", "The same overview, four questions. Each lens highlights what one decision needs.",
            [("Overview · lenses", False), TAG], "Draft · Example: Statistics Norway, NR IKR (simplified) · States and value are interpretation")
    cells = [(60, 196), (740, 196), (60, 596), (740, 596)]
    CW, CH = 660, 380

    def plat_lens(sid, plat):
        if "FAME" in plat:
            return INK, INK
        if "SAS" in plat:
            return GREY, GREY
        return "#ffffff", INK

    content = [("Platform and deadline", "What must move first?", "Steps on FAME have the earliest deadline, then SAS."),
               ("Dependencies", "Who waits for whom?", "Six other accounts deliver in. Who uses IKR is unresolved."),
               ("Stable data states", "Where are data stored as stable?", "Today it is unclear where SD, ID, PD, ST and OD are. The target requires it."),
               ("Needs and value", "Where does migration pay most?", "Four places with possible gains, see figure C3.")]
    for i, ((x, y), (t, q, ex)) in enumerate(zip(cells, content)):
        f.rect(x, y, CW, CH, "#ffffff", INK, 2, 10)
        f.marker(x + 30, y + 34, str(i + 1))
        f.text(x + 56, y + 41, t, 22, 700, TEXT)
        mx, my, mw, mh = x + 24, y + 80, 400, 260
        pos = mini_level1(f, mx, my, mw, mh, lens=plat_lens if i == 0 else None)
        if i == 1:
            f.rect(mx - 8, my + 70, 30, 120, OUT_GREY_2, OUT_GREY, 1.5, 4, "4 3")
            f.poly([(mx + 22, my + 130), (pos["P1"][0], my + 130)], GREY, 2, dash="5 3")
            f.rect(mx + mw - 26, my + 190, 34, 50, "#ffffff", OUT_GREY, 1.5, 4, "4 3")
            f.text(mx + mw - 9, my + 222, "?", 18, 700, GREY, "middle")
            rx, ry, rw, rh = pos["P1"]
            f.rect(rx, ry, rw, rh, "none", VIOLET, 3, 4)
        if i == 2:
            spots = [("SD", mx + 20, my + 30), ("ID", pos["P1"][0] + pos["P1"][2] + 6, my + 30), ("PD", pos["P2"][0] + pos["P2"][2] + 4, my + 160),
                     ("ST", pos["P6"][0] + pos["P6"][2] / 2 - 10, pos["P6"][1] + pos["P6"][3] + 26), ("OD", mx + mw - 40, my + 130)]
            for k, sx_, sy_ in spots:
                state_tag(f, sx_, sy_, k)
                f.text(sx_ + 16 + 9 * len(k), sy_ + 4, "?", 15, 700, GREY)
        if i == 3:
            for n, sid in [("1", "P1"), ("2", "P6"), ("3", "P7")]:
                rx, ry, rw, rh = pos[sid]
                f.rect(rx, ry, rw, rh, "none", VIOLET, 3, 4)
                f.marker(rx, ry, n, 12, VIOLET)
            f.marker(mx + 6, my + mh - 16, "4", 12, VIOLET)
        tx = x + 446
        f.text(tx, y + 110, "QUESTION", 12, 700, GREY, ls=1)
        yy = f.para(tx, y + 136, q, 18, 190, 700, lh=24)
        f.text(tx, max(yy + 14, y + 210), "IN THE EXAMPLE", 12, 700, GREY, ls=1)
        f.para(tx, max(yy + 40, y + 236), ex, 15, 190, lh=21)
        if i == 0:
            for j, (lab, fill, tc) in enumerate([("FAME 2028", INK, "#ffffff"), ("SAS 2029", GREY, "#ffffff")]):
                f.pill(tx + j * 102, y + 330, lab, 11, fill, fill, tc, 700, 22, padx=8)
    f.panel("How to use the lenses", [
        ("Order", "Platform and deadline give the order of migration."),
        ("Coordination", "Dependencies show who must plan together."),
        ("Platform requirements", "Data states show what must be in place on the target platform."),
        ("Prioritisation", "Needs and value show where effort pays most."),
    ], box=("ACROSS", "The lenses can be laid over all statistics to give one overview."))
    save(f, "B4")


# ------------------------------------------------------------ C1–C4
def c1():
    f = Fig()
    f.frame("Income and capital accounts: overview", "Statistics Norway’s NR IKR: 70 elements and 76 connections grouped into seven process steps",
            [("Example · overview", False), TAG], FOOTER_IKR)
    base_figure(f)
    f.panel("How to read the figure", [
        ("Seven process steps", "Each step groups several programs and data sets from Dataflow 2.0. The grouping is our interpretation."),
        ("Intake dominates", "13 near-identical intakes in SAS/Excel before calculation starts."),
        ("Depends on others", "Takes figures from REA, AR, UR, OFF and other national accounts."),
        ("Roles are missing", "Who does what is not in the 2.0 template. It is filled in at the workshop."),
    ], box=("LEVEL 1", "Shows process steps, not single programs. Each step can be opened as its own focus figure."))
    legend_standard(f)
    save(f, "C1")


def c2():
    f = Fig()
    f.frame("Lens: platform and deadline", "The end of the process has the earliest deadline",
            [("Example · lens", False), TAG], "Draft · Source: Dataflow 2.0, Statistics Norway (NR IKR) · Deadlines are Statistics Norway’s")
    base_figure(f, lens="deadline")
    x, y, w, h = STEPS["P7"][:4]
    f.rect(x - 6, y - 6, w + 12, h + 12, "none", INK, 3, 12)
    f.marker(x - 6, y - 6, "1", 16)
    f.marker(STEPS["P1"][0], STEPS["P1"][1], "2", 16)
    f.marker(STEPS["P6"][0], STEPS["P6"][1], "3", 16)
    f.panel("What the lens shows", [
        ("FAME first", "Recoding to NO and ESA loads into FAME, retired around 1 November 2028."),
        ("SAS carries the rest", "Six of seven steps use SAS. The internal target is 2029."),
        ("Excel has no deadline", "But manual editing needs a solution on the new platform anyway."),
        ("The order is reversed", "The end of the process must move before the start. This needs planning."),
    ], box=("NOTE", "The deadlines are Statistics Norway’s. Yours will differ: the lens works the same way."))
    f.legend([
        (lambda f, x, y: f.pill(x, y - 11, "FAME", 11, INK, INK, "#ffffff", 700, 22, padx=8), "c. 1 Nov 2028"),
        (lambda f, x, y: f.pill(x, y - 11, "SAS", 11, GREY, GREY, "#ffffff", 700, 22, padx=8), "2029, internal target"),
        (lambda f, x, y: f.pill(x, y - 11, "Oracle", 11, "#b3bcc8", "#b3bcc8", TEXT, 700, 22, padx=8), "2030 (not in IKR)"),
        (lambda f, x, y: f.pill(x, y - 11, "Excel", 11, "#ffffff", OUT_GREY, GREY, 700, 22, padx=8), "no platform deadline"),
        (lambda f, x, y: (f.line(x, y, x + 30, y, GREY, 1.6, "6 4"), 30)[1], "Dependency"),
    ])
    save(f, "C2")


def c3():
    f = Fig()
    f.frame("Where is the value in IKR?", "Four places where the migration can give more than a straight move",
            [("Focus · possible value", False), TAG], "Draft · Source: Dataflow 2.0, Statistics Norway (NR IKR) · Possible value is interpretation")
    base_figure(f, focus={"P1", "P6", "P7", "DEP", "OUT"})
    for n, (x, y) in [("1", (378, 300)), ("2", (1080, 300)), ("3", (980, 560)), ("4", (60, 300))]:
        f.marker(x, y, n, 18, VIOLET)
    f.panel("Possible value", [
        ("One intake instead of 13", "The 13 intakes follow the same pattern. They can become one shared, tested routine."),
        ("Traceable editing", "Manual editing in Excel is hard to audit. On a new platform, changes can be logged."),
        ("One run, two deliveries", "National and ESA figures are produced in two parallel runs with SAS and FAME. They can be combined."),
        ("Others set the order", "IKR takes figures from six other accounts. They decide when IKR can move."),
    ], box=("TO BE VERIFIED", "Read from the 2.0 metadata. Subject-matter owners must confirm before further use."), mcolour=VIOLET)
    legend_standard(f)
    save(f, "C3")


def c4():
    f = Fig()
    f.frame("Target-state skeleton for IKR", "Data states as anchor points, needs between them",
            [("Scenario · PROPOSAL", False), TAG], "Draft · Illustration made without the subject-matter owners · Content from Dataflow 2.0 and figure C3")
    X0, CW = 250, 230
    for lab, a, b, k in [("Collect", 0, 1, "collect"), ("Process", 1, 3, "process"), ("Analyse", 3, 4, "analyse"), ("Disseminate", 4, 5, "disseminate")]:
        f.line(X0 + a * CW + 8, 212, X0 + b * CW - 8, 212, PHASE[k][2], 6)
        f.text(X0 + (a + b) / 2 * CW, 202, lab, 13, 700, PHASE[k][3], "middle")
    yc = 262
    f.line(X0 + CW / 2, yc, X0 + 4.5 * CW, yc, FLOW, 2.4)
    for i, ((k, nm), t) in enumerate(zip(STATES, ["micro", "micro", "micro", "stat", "out"])):
        cx = X0 + i * CW + CW / 2
        data_symbol(f, cx, yc, t, 2, 3, state=k)
        f.text(cx, yc + 42, nm, 15, 700, GREEN, "middle")
    content = {
        "Services": ["Intake of 11 sources and 6 accounts", "Shared intake and recoding (13 today)", "?", "Editing with an audit log", "Publishing to the statistics database"],
        "Processes": ["?", "Linking to national accounts codes", "Calculation by sector: financial, non-financial, capital", "Summing and reconciliation", "One run with two outputs, NO and ESA?"],
        "Variables and states": ["?", "The recoding catalogue (OMKOD)", "?", "National and ESA standards", "?"],
        "Dependencies": ["Tax, business register, VPS and others", "REA, AR, UR, OFF, NAV, TOMT on the new platform?", "OLJE, share statistics", "?", "Eurostat. Who uses IKR?"],
    }
    RY0, RH = 330, 150
    for r, nm in enumerate(content):
        y = RY0 + r * (RH + 10)
        f.rect(60, y, 172, RH, VIOLET_3, VIOLET, 2, 8)
        f.lines(76, y + 32, wrap(nm, 16, 140, 700), 16, 700, VIOLET_TEXT, lh=20)
        for c in range(5):
            x = X0 + c * CW + 4
            txt = content[nm][c]
            if txt == "?":
                f.rect(x, y, CW - 8, RH, "#ffffff", OUT_GREY, 1.5, 6, "5 3")
                f.text(x + (CW - 8) / 2, y + RH / 2 + 10, "?", 30, 700, OUT_GREY, "middle")
            else:
                f.rect(x, y, CW - 8, RH, "#ffffff", "#a7afba", 1.5, 6)
                f.rect(x + 12, y + 14, CW - 32, RH - 28, VIOLET_3, VIOLET, 1.5, 6, "4 3")
                f.lines(x + 24, y + 42, wrap(txt, 14, CW - 56, 600), 14, 600, VIOLET_TEXT, lh=19)
    f.panel("How to read the skeleton", [
        ("Needs, not solutions", "The cells say what is needed. Whether it exists on the platform is assessed later."),
        ("Taken from today", "The content is read from the 2.0 flow and the value points in figure C3."),
        ("‘?’ is deliberate", "Empty cells have not been assessed. They are filled in at the workshop."),
        ("Next step", "The subject-matter owners correct and complete it with template D3."),
    ], box=("STATUS", "Illustration. Not a proposal from the IKR subject-matter owners."), mcolour=VIOLET)
    f.legend([
        (tag_legend(), "Stable data state"),
        (box_legend(VIOLET_3, VIOLET, "4 3"), "Need (proposal)"),
        (box_legend("#ffffff", OUT_GREY, "4 3"), "Not assessed"),
    ])
    save(f, "C4")


# ------------------------------------------------------------ templates D1–D4
def table(f, x0, y0, cols, rows, hh=40, rh=56, examples=1, size=13, cell=None):
    xs = [x0]
    for _, w in cols:
        xs.append(xs[-1] + w)
    f.rect(x0, y0, xs[-1] - x0, hh, VIOLET_3, VIOLET, 1.5, 6)
    for (nm, w), x in zip(cols, xs):
        f.text(x + 9, y0 + hh / 2 + 5, nm, 13, 700, VIOLET_TEXT)
    for r, row in enumerate(rows):
        y = y0 + hh + r * rh
        ex = r < examples
        f.rect(x0, y, xs[-1] - x0, rh, OUT_GREY_2 if ex else "#ffffff", "#a7afba", 1.2, 0)
        for x in xs[1:-1]:
            f.line(x, y, x, y + rh, RULE, 1.2)
        for ci, val in enumerate(row):
            if cell and cell(f, ci, xs[ci], y, cols[ci][1], rh, ex, val):
                continue
            if val:
                rows_ = val if isinstance(val, list) else wrap(val, size, cols[ci][1] - 18)
                f.lines(xs[ci] + 9, y + 22, rows_[:3], size, 400, TEXT, lh=size + 4, italic=ex)
    return xs, y0 + hh + len(rows) * rh


def checks(f, x, y, labels, on=None, colours=None):
    for i, lab in enumerate(labels):
        bx = x + i * 30
        c = colours[i] if colours else INK
        f.rect(bx, y, 20, 20, c if on == lab else "#ffffff", c, 1.5, 3)
        f.text(bx + 10, y + 34, lab, 10, 700, c, "middle")


def fields(f, specs):
    for x, w, lab in specs:
        f.text(x, 203, lab, 13, 600, GREY)
        f.rect(x, 210, w, 38, "#ffffff", "#a7afba", 1.5, 4)


def d1():
    f = Fig()
    f.frame("Template: process steps and roles", "The current process at level 1: what happens, who does it, on which platform, and what is connected",
            [("Template · level 1", False), TAG], "Draft · Dataflow framework · Example row from Statistics Norway (NR IKR)")
    f.text(60, 203, "Applies to", 13, 600, GREY)
    for i, t in enumerate(["One statistic", "A group"]):
        f.rect(60 + i * 140, 220, 18, 18, "#ffffff", INK, 1.5, 3)
        f.text(86 + i * 140, 235, t, 15, 400, TEXT)
    fields(f, [(310, 400, "Statistic or group"), (730, 300, "Contact person"), (1050, 160, "Date"), (1230, 170, "Version")])
    cols = [("#", 34), ("Process step", 170), ("Phase", 116), ("What happens", 220), ("Who", 130),
            ("Platform and systems", 186), ("Data in → out", 190), ("Dependencies", 160), ("All / some", 134)]
    x0, y0, hh, rh = 60, 272, 48, 74
    xs = [x0]
    for _, w in cols:
        xs.append(xs[-1] + w)
    f.rect(x0, y0, xs[-1] - x0, hh, VIOLET_3, VIOLET, 1.5, 6)
    for (nm, w), x in zip(cols, xs):
        f.text(x + 10, y0 + 30, nm, 14, 700, VIOLET_TEXT)
    n = 7
    for r in range(n):
        y = y0 + hh + r * rh
        ex = r == 0
        f.rect(x0, y, xs[-1] - x0, rh, OUT_GREY_2 if ex else "#ffffff", "#a7afba", 1.2, 0)
        for x in xs[1:-1]:
            f.line(x, y, x, y + rh, RULE, 1.2)
        f.text(x0 + 17, y + 30, "E" if ex else str(r), 14, 700, GREY if ex else TEXT, "middle")
        for i, k in enumerate(["collect", "process", "analyse", "disseminate"]):
            nm, fill, edge, tc = PHASE[k]
            bx = xs[2] + 10 + i * 26
            on = ex and k == "analyse"
            f.rect(bx, y + 16, 20, 20, tc if on else fill, tc, 1.5, 3)
            f.text(bx + 10, y + 52, nm[0], 11, 700, tc, "middle")
        for i, t in enumerate(["All", "Some"]):
            bx = xs[8] + 12 + i * 60
            f.rect(bx, y + 20, 16, 16, "#ffffff", INK, 1.5, 3)
            f.text(bx + 22, y + 33, t, 12, 400, TEXT)
    y = y0 + hh
    for ci, rows in [(1, ["Summing and", "reconciliation"]), (3, ["Sums all sources", "and reconciles"]), (4, ["?"]),
                     (5, ["SAS: SAS SUM,", "SAS AVSTEM"]), (6, ["FIN, IKKE-FIN etc.", "→ INPUT EXCEL"]), (7, ["In: RG (source ?)", "Out: to editing"])]:
        f.lines(xs[ci] + 10, y + 28, rows, 13, 400, TEXT, lh=18, italic=True)
    f.text(xs[8] + 12, y + 62, "One statistic", 11, 400, GREY, italic=True)
    yb = y0 + hh + n * rh + 26
    f.text(60, yb + 19, "PLATFORMS", 13, 700, GREY, ls=1)
    x = 186
    for p in ["SAS", "FAME", "Oracle", "Excel", "R", "Python", "SQL database", "Survey tool", "Web portal"]:
        x += f.pill(x, yb, p, 13, OUT_GREY_2, OUT_GREY, TEXT, 600, 28) + 8
    for i in range(2):
        f.rect(x, yb, 80, 28, "#ffffff", OUT_GREY, 1.5, 14, "5 3")
        x += 88
    f.text(60, yb + 62, "ROLES", 13, 700, GREY, ls=1)
    x = 186
    for p in ["Statistician", "Statistics owner", "Methodologist", "IT / developer", "Dissemination", "External supplier"]:
        x += f.pill(x, yb + 44, p, 13, VIOLET_3, VIOLET, VIOLET_TEXT, 600, 28) + 8
    f.text(x + 6, yb + 63, "Suggestions. Add your own.", 13, 400, GREY, italic=True)
    f.panel("How to use the template", [
        ("Split the process into steps", "Often 5–10 steps. A step changes the data and can be described in one sentence."),
        ("Write the role, not the name", "Who does the step today? Use the role tiles or write your own."),
        ("Platform first", "The platform sets the deadline. Program names come at level 2."),
        ("Dependencies both ways", "What does the step take from others, and who uses what comes out?"),
    ], box=("RULE", "‘?’ is a valid answer. What has not been assessed is not guessed."))
    f.legend([
        (box_legend(OUT_GREY_2, "#a7afba", None, 1.2), "Example row (E)"),
        (box_legend("#ffffff", "#a7afba", None, 1.2), "Field to fill in"),
        (lambda f, x, y: (f.rect(x + 4, y - 10, 20, 20, PHASE["analyse"][3], PHASE["analyse"][3], 1.5, 3), 28)[1], "Phase: C P A D"),
    ])
    save(f, "D1")


def d2():
    f = Fig()
    f.frame("Template: data and systems", "Level 2 for one process step: one row per object, one row per connection, no coordinates",
            [("Template · level 2", False), TAG], "Draft · Replaces the Dataflow 2.0 Excel template · Example rows from Statistics Norway (NR IKR)")
    f.text(60, 203, "Process step (from D1)", 13, 600, GREY)
    f.rect(60, 210, 420, 38, "#ffffff", "#a7afba", 1.5, 4)
    f.text(74, 235, "5  Summing and reconciliation", 15, 400, TEXT, italic=True)
    f.text(500, 203, "Statistic", 13, 600, GREY)
    f.rect(500, 210, 300, 38, "#ffffff", "#a7afba", 1.5, 4)
    f.text(514, 235, "NR IKR", 15, 400, TEXT, italic=True)
    f.text(60, 290, "OBJECTS", 13, 700, GREY, ls=1)
    cols = [("ID", 56), ("Name", 140), ("Object", 84), ("Type", 92), ("Rows", 66), ("Variables", 88), ("Platform", 100),
            ("State", 156), ("Description", 330), ("Status", 228)]
    rows = [["S1", "SAS SUM", "system", "1", "–", "–", "SAS", None, "Sums all sources", "Exists"],
            ["D1", "ALT SAMLET", "data", "macro", "2", "3", "SAS", None, "Data set with all figures combined", "Exists"],
            ["S2", "SAS AVSTEM", "system", "1", "–", "–", "SAS", None, "Reconciles", "Exists"],
            ["D2", "INPUT EXCEL", "data", "macro", "2", "3", "Excel", None, "All figures reconciled, to editing", "?"],
            [None] * 10, [None] * 10]

    def cell(f, ci, x, y, w, h, ex, val):
        if ci == 7:
            for i, (k, _) in enumerate(STATES):
                bx = x + 8 + i * 29
                f.rect(bx, y + 10, 24, 18, "#ffffff", GREEN, 1.3, 9)
                f.text(bx + 12, y + 23, k, 9, 700, GREEN, "middle")
            if ex:
                f.text(x + 8, y + 46, "? (not assessed)", 11, 400, GREY, italic=True)
            return True
        return False
    xs, yend = table(f, 60, 300, cols, rows, rh=56, examples=4, cell=cell)
    f.text(60, yend + 40, "CONNECTIONS", 13, 700, GREY, ls=1)
    kc = [("From ID", 90), ("To ID", 90), ("Type", 200), ("Note", 380)]
    kr = [["IKKE-FIN", "S1", "data flow", "From step 3"], ["S1", "D1", "data flow", None], ["D1", "S2", "data flow", None],
          ["S2", "D2", "data flow", "On to step 6"], ["OMKOD", "FINANS", "metadata", "Example from step 2: code list"], [None] * 4]
    table(f, 60, yend + 50, kc, kr, rh=40, examples=5, size=12)
    bx, by = 860, yend + 50
    f.rect(bx, by, 540, 280, "#ffffff", INK, 2, 10)
    f.text(bx + 20, by + 34, "What is new since 2.0", 18, 700, TEXT)
    for i, (a, b) in enumerate([("Two rows per connection", "One row per object and connection"),
                                ("Coordinates set by hand", "Order derived from connections"),
                                ("The coordinate is the ID", "Own ID, independent of position"),
                                ("No platform or state", "Platform, state and status")]):
        yy = by + 76 + i * 50
        f.text(bx + 20, yy, a, 14, 400, GREY)
        f.arrow(bx + 228, yy - 5, bx + 252, yy - 5, INK, 1.6, 8)
        f.text(bx + 262, yy, b, 14, 700, TEXT)
    f.panel("How to use the template", [
        ("One process step at a time", "Fill it in for the steps that will be opened as focus figures."),
        ("Codes as before", "Type, rows and variables use the same codes as in 2.0."),
        ("Connections separately", "Write what goes from where to where. The drawing handles placement."),
        ("Old flows can be read in", "A 2.0 flow can be converted to this template automatically."),
    ], box=("RULE", "‘?’ is a valid answer. What has not been assessed is not guessed."))
    f.legend([
        (box_legend(OUT_GREY_2, "#a7afba", None, 1.2), "Example rows"),
        (box_legend("#ffffff", "#a7afba", None, 1.2), "Field to fill in"),
        (lambda f, x, y: (f.text(x, y + 5, "Type:", 14, 700, GREY), 40)[1], "data: meta, micro, macro, stat, out · system: 0–3"),
    ])
    save(f, "D2")


def d3():
    f = Fig()
    f.frame("Template: needs and value", "What must be in place on the target platform, what does it replace, and what improves?",
            [("Template · needs", False), TAG], "Draft · Dataflow framework · The example row is interpretation (see figure C3)")
    fields(f, [(60, 420, "Statistic or group"), (500, 300, "Contact person"), (820, 160, "Date")])
    cols = [("#", 34), ("Data state", 168), ("Need", 210), ("Type", 140), ("Replaces today", 170), ("Value", 190),
            ("Risk of not doing it", 180), ("On platform?", 148)]
    rows = [["E", None, ["Shared intake and", "recoding of sources"], None, ["13 intakes in SAS/", "Excel (step 1)"], ["One tested routine,", "less maintenance"],
             ["13 SAS routines must", "move before 2029"], None]] + [[str(i)] + [None] * 7 for i in range(1, 7)]

    def cell(f, ci, x, y, w, h, ex, val):
        if ci == 0:
            f.text(x + 17, y + 30, val, 14, 700, GREY if ex else TEXT, "middle")
            return True
        if ci == 1:
            checks(f, x + 10, y + 12, [k for k, _ in STATES], "ID" if ex else None, [GREEN] * 5)
            return True
        if ci == 3:
            checks(f, x + 10, y + 12, ["S", "P", "V", "D"], "S" if ex else None, [VIOLET] * 4)
            return True
        if ci == 7:
            checks(f, x + 10, y + 12, ["Yes", "No", "?"], "?" if ex else None)
            return True
        return False
    xs, yend = table(f, 60, 272, cols, rows, rh=78, cell=cell)
    f.text(60, yend + 30, "S = service · P = process · V = variables and states · D = dependency", 14, 400, GREY)
    f.text(60, yend + 54, "‘On platform?’ is answered when the solution is assessed. Prioritise the needs in your own backlog.", 14, 400, GREY)
    f.panel("How to use the template", [
        ("Needs, not solutions", "Write what is needed, not which tool to use."),
        ("Link to today’s process", "What does the need replace? Refer to process steps in D1."),
        ("Value and risk", "What improves, and what happens if we only move as-is?"),
        ("To assessment and backlog", "The list goes on to assessment and is logged in the backlog."),
    ], box=("RULE", "‘?’ is a valid answer. What has not been assessed is not guessed."))
    f.legend([
        (box_legend(OUT_GREY_2, "#a7afba", None, 1.2), "Example row (E)"),
        (box_legend("#ffffff", "#a7afba", None, 1.2), "Field to fill in"),
        (lambda f, x, y: (f.rect(x + 4, y - 10, 20, 20, GREEN, GREEN, 1.5, 3), 28)[1], "Data state"),
    ])
    save(f, "D3")


def d4():
    f = Fig()
    f.frame("How it works", "From template to drawing and list of needs: who does what, and where quality is assured",
            [("Process", False), TAG], "Draft · Dataflow framework · Kick-off → workshop → follow-up → result")
    phases = ["Kick-off", "Before workshop", "Workshop", "Follow-up", "Result"]
    X0, CW = 250, 230
    lanes = [("Contact person", "subject-matter area", "violet"), ("Project team", "the mapping", "ink"), ("AI support", "the dataflow skill", "panel")]
    BY0, BH = 250, 220
    sty = {"violet": (VIOLET_3, VIOLET, VIOLET_TEXT), "ink": ("#ffffff", INK, TEXT), "panel": (PANEL, "#8e9db3", TEXT)}
    for i, p in enumerate(phases):
        x = X0 + i * CW
        f.rect(x + 4, 196, CW - 8, 36, PANEL, PANEL_EDGE, 1.5, 6)
        f.text(x + CW / 2, 220, p, 15, 700, TEXT, "middle")
    for j, (nm, sub, s) in enumerate(lanes):
        y = BY0 + j * (BH + 12)
        fill, st, tc = sty[s]
        f.rect(60, y, 176, BH, fill if s != "panel" else PANEL, st if s != "panel" else PANEL_EDGE, 2, 8)
        f.text(76, y + 34, nm, 17, 700, tc)
        f.text(76, y + 58, sub, 14, 400, GREY)
        f.rect(X0, y, 5 * CW, BH, "#ffffff", RULE, 1, 8)

    def card(fi, bj, texts, s="ink", h=None):
        x = X0 + fi * CW + 12
        y = BY0 + bj * (BH + 12) + 20
        w = CW - 24
        fill, st, tc = sty[s]
        f.rect(x, y, w, h or (BH - 40), fill, st, 2, 8)
        yy = y + 30
        for k, t in enumerate(texts):
            for row in wrap(t, 15 if k == 0 else 14, w - 28, 700 if k == 0 else 400):
                f.text(x + 14, yy, row, 15 if k == 0 else 14, 700 if k == 0 else 400, tc if k == 0 else TEXT)
                yy += 20
            yy += 6

    card(0, 1, ["Agree the scope", "One statistic or a group, and who takes part"])
    card(0, 0, ["Receives the templates", "D1 process steps, D2 data and systems, D3 needs"], "violet")
    card(1, 0, ["Fills in", "D1 and D2 as far as possible. ‘?’ is fine."], "violet")
    card(1, 2, ["Drafts", "From a 2.0 flow, fact sheets and D1/D2. Lists questions."], "panel")
    card(2, 0, ["Walk through together", "Contact person and project team go through today’s process and the target with the draft. Resolve ‘?’."], "ink", h=BH * 2 - 28)
    card(3, 2, ["Processes", "Notes become a model. Draws levels 1 and 2. Makes a quality checklist."], "panel")
    card(3, 1, ["Checks", "The draft against notes and sources"])
    card(3, 0, ["Confirms or corrects", "Drawings and list of needs"], "violet")
    card(4, 1, ["Delivers", "Drawings, list of needs to the backlog, input to the solution assessment"])
    card(4, 2, ["Combines across", "The lenses for all statistics in one overview"], "panel")
    card(4, 0, ["Uses the result", "In further migration work"], "violet")
    for lab, xg in [("Gate 1 · draft ready", X0 + 2 * CW), ("Gate 2 · confirmed by owners", X0 + 4 * CW)]:
        f.line(xg, BY0 - 10, xg, BY0 + 3 * BH + 36, INK, 3, "8 5")
        w = tw(lab, 13, 700) + 28
        f.rect(xg - w / 2, BY0 + 3 * BH + 46, w, 30, INK, "none", 0, 15)
        f.text(xg, BY0 + 3 * BH + 66, lab, 13, 700, "#ffffff", "middle")
    f.panel("Division of work", [
        ("Experts own the content", "The contact person fills in, takes part and confirms."),
        ("AI drafts, it does not decide", "Everything from the AI support is marked as a draft until confirmed."),
        ("Two gates", "A draft before the workshop. Confirmation before anything moves on."),
        ("Results move on", "Needs go to assessment and the backlog. Lenses are combined across statistics."),
    ], box=("TRY IT FIRST", "Measure the time per statistic in a pilot."))
    f.legend([
        (box_legend(VIOLET_3, VIOLET), "Subject-matter area"),
        (box_legend("#ffffff", INK), "Project team"),
        (box_legend(PANEL, "#8e9db3"), "AI support"),
        (lambda f, x, y: (f.line(x, y, x + 28, y, INK, 3, "8 5"), 28)[1], "Gate"),
    ])
    save(f, "D4")


ALL = [a1, a2, a3, b1, b2, b3, b4, c1, c2, c3, c4, d1, d2, d3, d4]

if __name__ == "__main__":
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    for fn in ALL:
        if not names or fn.__name__ in names:
            fn()
            print("wrote", fn.__name__.upper())
