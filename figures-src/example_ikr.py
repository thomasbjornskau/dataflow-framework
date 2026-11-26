"""Base figure: Statistics Norway's income and capital accounts (NR IKR) at level 1 (overview).
Used by C1 (overview), C2 (platform lens), C3 (value) and B1/B4 (miniatures).
The grouping into process steps is an interpretation of the Dataflow 2.0 metadata."""
from dfdraw import *

FOOTER_IKR = "Draft · Source: Dataflow 2.0 metadata, Statistics Norway (NR IKR) · Process steps are an interpretation"

# Legacy platform -> (retirement date at Statistics Norway, order)
DEADLINE = {"FAME": ("c. 1 Nov 2028", 1), "SAS": ("2029, internal target", 2), "Oracle": ("2030", 3)}

# process steps: id -> (x, y, w, h, title lines, subtitle lines, system types, platforms)
STEPS = {
    "P1": (378, 300, 168, 548, ["Intake and", "recoding"], ["13 intakes", "in SAS/Excel"], "grid13", ["SAS", "Excel"]),
    "P2": (636, 300, 186, 118, ["Financial", "sectors"], ["FINANS"], [1], ["SAS"]),
    "P3": (636, 456, 186, 118, ["Non-financial", "sectors"], ["SAS BEREGN"], [1], ["SAS"]),
    "P4": (636, 612, 186, 140, ["Capital, shares,", "AR and OFF"], ["IBERKAP · balancing", "AR2IKR · OFF app"], [1, 1, 1, 1], ["SAS"]),
    "P5": (884, 300, 170, 140, ["Summing and", "reconciliation"], ["SAS SUM", "SAS AVSTEM"], [1, 1], ["SAS"]),
    "P6": (1080, 300, 168, 140, ["Inspection,", "manual editing"], ["EXCEL EDIT"], [0], ["Excel"]),
    "P7": (980, 560, 268, 140, ["Recoding to", "NO and ESA"], ["2 × SAS · 2 × FAME"], [1, 1, 2, 2], ["SAS", "FAME"]),
}

SOURCES = [("VOF", "micro", 2, 2), ("NO1 NO2", "micro", 2, 4), ("Balance forms", "micro", 2, 3),
           ("Tax: companies", "micro", 2, 2), ("Business reg.", "micro", 2, 3), ("Tax: persons", "micro", 2, 2),
           ("Shares", "micro", 2, 2), ("Insur./pensions", "micro", 2, 4), ("VPS", "micro", 2, 2),
           ("NO-VP", "macro", 2, 2), ("OLJE", "macro", 1, 2)]
DEPS = ["REA", "AR", "UR", "OFF", "NAV via UR", "TOMT"]


def platform_colour(p, lens):
    if lens != "deadline":
        return OUT_GREY_2, OUT_GREY, TEXT
    if p in DEADLINE:
        return {1: (INK, INK, "#ffffff"), 2: (GREY, GREY, "#ffffff"), 3: ("#b3bcc8", "#b3bcc8", TEXT)}[DEADLINE[p][1]]
    return "#ffffff", OUT_GREY, GREY


def block(f, sid, dim=False, lens=None):
    x, y, w, h, title, sub, syst, plat = STEPS[sid]
    s = DIM_S if dim else INK
    tc = DIM_T if dim else TEXT
    gc = DIM_T if dim else GREY
    f.rect(x, y, w, h, DIM_F if dim else "#ffffff", s, 2, 8)
    yy = f.lines(x + 14, y + 28, title, 16, 700, tc, lh=21)
    yy = f.lines(x + 14, yy + 2, sub, 13, 400, gc, lh=18)
    if syst == "grid13":
        for i in range(13):
            system_symbol(f, x + 30 + (i % 4) * 34, yy + 22 + (i // 4) * 46, 1, 20, 28, dim)
    else:
        for i, t in enumerate(syst):
            system_symbol(f, x + 24 + i * 28, y + h - 24, t, 18, 26, dim)
    px = x + w - 12
    for p in reversed(plat):
        fill, st, c = (DIM_F, DIM_S, DIM_T) if dim else platform_colour(p, lens)
        wp = tw(p, 12, 700) + 18
        px -= wp
        f.pill(px, y + h - 36, p, 12, fill, st, c, 700, 24, padx=9)
        px -= 6
    return x, y, w, h


def anchor(sid, side):
    x, y, w, h = STEPS[sid][:4]
    return {"l": (x, y + h / 2), "r": (x + w, y + h / 2), "t": (x + w / 2, y), "b": (x + w / 2, y + h)}[side]


def base_figure(f, focus=None, lens=None):
    """focus: set of step ids to highlight (others dimmed), plus 'DEP' and 'OUT'. lens: None | 'deadline'."""
    dim = lambda sid: focus is not None and sid not in focus
    anydim = focus is not None
    Y0, Y1 = 196, 900
    phase_band(f, "collect", 200, Y0, 166, Y1 - Y0)
    phase_band(f, "process", 366, Y0, 494, Y1 - Y0)
    phase_band(f, "analyse", 860, Y0, 404, Y1 - Y0)
    phase_band(f, "disseminate", 1264, Y0, 136, Y1 - Y0)
    for x0, w0 in [(200, 166), (366, 494), (860, 404), (1264, 136)]:
        f.pill(x0 + w0 / 2 - 34, 236, "Role: ?", 12, VIOLET_3, VIOLET_2 if anydim else VIOLET,
               DIM_T if anydim else VIOLET_TEXT, 700, 24, "4 3", 9)

    # dependencies in (grey, outside)
    d_dim = focus is not None and "DEP" not in focus
    f.rect(60, 300, 128, 548, DIM_F if d_dim else OUT_GREY_2, DIM_S if d_dim else OUT_GREY, 1.5, 8, "5 3")
    f.lines(72, 326, ["From other", "accounts"], 14, 700, DIM_T if d_dim else TEXT, lh=19)
    for i, nm in enumerate(DEPS):
        cy = 400 + i * 60
        data_symbol(f, 86, cy, "stat" if nm == "REA" else "macro", 1, 2, d_dim)
        f.text(106, cy + 5, nm, 13, 600, DIM_T if d_dim else TEXT)

    # received sources
    k_dim = focus is not None and "P1" not in focus
    f.text(283, 286, "Received sources", 13, 700, DIM_T if k_dim else GREY, "middle")
    for i in range(len(SOURCES)):
        f.line(226, 318 + i * 49, 378, 340 + i * 46, DIM_S if k_dim else FLOW, 1.4)
    for i, (nm, t, r, c) in enumerate(SOURCES):
        cy = 318 + i * 49
        data_symbol(f, 226, cy, t, min(r, 2), c, k_dim)
        f.rect(246, cy - 9, tw(nm, 12, 600) + 6, 17, PHASE["collect"][1])
        f.text(249, cy + 4, nm, 12, 600, DIM_T if k_dim else TEXT)

    def off(a, b):
        return focus is not None and not (a in focus or b in focus)

    def edge(pts, a, b, sw=2.4, dash=None):
        f.poly(pts, DIM_S if off(a, b) else FLOW, sw, dash=dash)

    def dsym(x, y, t, r, c, a, b):
        data_symbol(f, x, y, t, r, c, off(a, b))

    def label(x, y, s, a, b, anchor_="middle", size=12):
        f.text(x, y, s, size, 600, DIM_T if off(a, b) else GREY, anchor_)

    # dependencies -> P1 (dashed, along the bottom so it does not cross the sources)
    n = focus is not None and not ("DEP" in focus or "P1" in focus)
    f.poly([(124, 848), (124, 872), (420, 872), (420, 856)], DIM_S if n else GREY, 1.6, dash="6 4")
    f.poly([(415, 864), (420, 852), (425, 864)], DIM_S if n else GREY, 1.6)
    # RG: input without a known source
    nrg = focus is not None and not ("DEP" in focus or "P5" in focus)
    f.poly([(930, 282), (930, 300)], DIM_S if nrg else GREY, 1.6, dash="4 3")
    data_symbol(f, 930, 268, "stat", 1, 3, nrg)
    f.text(948, 273, "RG (source ?)", 12, 600, DIM_T if nrg else GREY)

    # P1 -> P2/P3/P4
    for sid, t, c in [("P2", "micro", 4), ("P3", "micro", 2), ("P4", "micro", 2)]:
        x2, y2 = anchor(sid, "l")
        edge([(546, y2), (x2, y2)], "P1", sid, 3.2)
        dsym(591, y2, t, 2, c, "P1", sid)
        if sid == "P4":
            for j, s in enumerate(["AKSJESTAT,", "AR, UR, OFF"]):
                label(591, y2 + 34 + j * 15, s, "P1", sid)
        else:
            label(591, y2 + 34, {"P2": "FIN", "P3": "SAMLET"}[sid], "P1", sid)
    # P2, P3, P4 -> P5
    for sid, nm, t, c, ty in [("P2", "REA", "stat", 3, 350), ("P3", "IKKE-FIN", "micro", 3, 370), ("P4", "IBERKAP", "macro", 2, 390)]:
        x1, y1 = anchor(sid, "r")
        edge([(x1, y1), (864, y1), (864, ty), (884, ty)], sid, "P5", 2.6)
        dsym(843, y1, t, 1, c, sid, "P5")
        label(826, y1 + 31, nm, sid, "P5", "start", 10)
    # P1 bypass -> P5
    edge([(470, 848), (470, 886), (876, 886), (876, 420), (884, 420)], "P1", "P5", 1.8)
    dsym(560, 886, "macro", 1, 2, "P1", "P5")
    label(578, 879, "NAV UR, TOMT, REA, AR, UR, OFF straight to summing", "P1", "P5", "start")
    # P5 -> P6 (below the blocks)
    edge([(969, 440), (969, 486), (1110, 486), (1110, 440)], "P5", "P6", 3)
    dsym(1040, 486, "macro", 2, 3, "P5", "P6")
    label(1040, 522, "INPUT EXCEL", "P5", "P6")
    # P6 -> P7
    edge([(1205, 440), (1205, 560)], "P6", "P7", 3)
    dsym(1205, 500, "stat", 2, 3, "P6", "P7")
    label(1227, 505, "TAB", "P6", "P7", "start")
    # P7 -> dissemination
    n7 = focus is not None and "P7" not in focus and "OUT" not in focus
    for yy, t, sysname in [(600, "out", "StatBank"), (670, "stat", "Eurostat")]:
        f.poly([(1248, yy), (1352, yy)], DIM_S if n7 else FLOW, 2.6)
        data_symbol(f, 1292, yy, t, 2, 3, n7)
        system_symbol(f, 1362, yy, 3, 20, 28, n7)
        f.text(1332, yy + 32, sysname, 12, 600, DIM_T if n7 else GREY, "middle")
    f.pill(1282, 760, "Used by: ?", 12, "#ffffff", DIM_S if n7 else OUT_GREY, DIM_T if n7 else GREY, 700, 24, "4 3", 9)
    f.text(1332, 812, "dependencies out", 12, 400, DIM_T if n7 else GREY, "middle")

    for sid in STEPS:
        block(f, sid, dim(sid), lens)


def legend_standard(f):
    f.legend([
        (lambda f, x, y: (data_symbol(f, x + 10, y, "micro", 1, 2), 20)[1], "Micro data"),
        (lambda f, x, y: (data_symbol(f, x + 10, y, "macro", 1, 2), 20)[1], "Macro data"),
        (lambda f, x, y: (data_symbol(f, x + 10, y, "stat", 1, 2), 20)[1], "Statistics"),
        (lambda f, x, y: (data_symbol(f, x + 12, y, "out", 1, 2), 24)[1], "Output"),
        (lambda f, x, y: (system_symbol(f, x + 7, y, 1, 14, 20), 14)[1], "Bespoke"),
        (lambda f, x, y: (system_symbol(f, x + 7, y, 2, 14, 20), 14)[1], "Framework/menu"),
        (lambda f, x, y: (system_symbol(f, x + 7, y, 3, 14, 20), 14)[1], "Framework"),
        (lambda f, x, y: (system_symbol(f, x + 7, y, 0, 14, 20), 14)[1], "Next level"),
        (lambda f, x, y: (f.line(x, y, x + 30, y, GREY, 1.6, "6 4"), 30)[1], "Dependency"),
    ])


def mini_level1(f, x, y, w, h, highlight=None, lens=None):
    """Simplified level-1 miniature. lens(sid, platforms) -> (fill, stroke). Returns block positions."""
    sx = lambda v: x + (v - 200) * w / 1200
    sy = lambda v: y + (v - 290) * h / 600
    for k, a, b in [("collect", 200, 366), ("process", 366, 860), ("analyse", 860, 1264), ("disseminate", 1264, 1400)]:
        f.rect(sx(a), y, sx(b) - sx(a), h, PHASE[k][1], "none", 0, 3)
    cen = {sid: (sx(bx + bw / 2), sy(by + bh / 2)) for sid, (bx, by, bw, bh, *_r) in STEPS.items()}
    for a, b in [("P1", "P2"), ("P1", "P3"), ("P1", "P4"), ("P2", "P5"), ("P3", "P5"), ("P4", "P5"), ("P5", "P6"), ("P6", "P7")]:
        f.line(*cen[a], *cen[b], FLOW, 1.4)
    f.line(cen["P7"][0], cen["P7"][1], sx(1390), cen["P7"][1], FLOW, 1.4)
    pos = {}
    for sid, (bx, by, bw, bh, title, sub, syst, plat) in STEPS.items():
        rx, ry, rw, rh = sx(bx), sy(by), bw * w / 1200, bh * h / 600
        col, st = ("#ffffff", INK) if not lens else lens(sid, plat)
        on = highlight and sid in highlight
        f.rect(rx, ry, rw, rh, col, VIOLET if on else st, 3 if on else 1.4, 4)
        pos[sid] = (rx, ry, rw, rh)
    return pos


def read_ikr(path):
    """Read the Dataflow 2.0 Excel file: nodes keyed by coordinate, and edges."""
    import openpyxl, warnings
    warnings.filterwarnings("ignore")
    ws = openpyxl.load_workbook(path).worksheets[0]
    nodes, edges = {}, []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[6] != "shape":
            continue
        obj, coord, nxt, step, dtype, name, desc, sysx, rows, cols = r[0], r[1], r[2], r[8], r[9], r[10], r[11], r[12], r[13], r[14]
        gx, gy = [int(v) for v in coord.split(",")]
        nodes[coord] = dict(obj=obj, gx=gx, gy=gy, step=step, dtype=dtype, name=name, desc=desc, sys=sysx, rows=rows or 1, cols=cols or 2)
        if nxt != coord:
            edges.append((coord, nxt))
    return nodes, edges
