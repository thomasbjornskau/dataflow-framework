"""Builds docs/graphic-elements.md and docs/files/symbols-svg.zip from docs/symbols/.

Run from the repository root:   python figures-src/build_gallery.py
"""
import pathlib, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SYM = ROOT / "docs" / "symbols"

GROUPS = [
    ("Metadata", "Code lists, catalogues and other descriptions. Spokes only, no core.", "meta-"),
    ("Micro data", "Information about individual units. White core.", "micro-data-"),
    ("Macro data", "Partly aggregated data. Light grey core.", "macro-data-"),
    ("Statistics", "Fully aggregated statistics, not yet published. Dark core.", "stat-data-"),
    ("Output: simple end product", "Disseminated statistics with relatively simple content. Dark petals.", "stat-product-simple-"),
    ("Output: advanced end product", "Disseminated statistics with more complex content. Light grey petals.", "stat-product-advanced-"),
    ("Output: priority end product", "Highlighted and complex content. Red and orange petals.", "stat-product-priority-"),
    ("Output: micro data as a product", "Micro data delivered outside. Dark petals around a white core.", "micro-product-simple-"),
    ("Control data", "Control data and other data that arise along the way, in the phase colours.", "control-data-"),
    ("Systems", "The system types, and the advanced type (magnifier) for solutions that can be opened at a next level.", "system-"),
]

HEAD = """---
title: Graphic elements
---

# Graphic elements

Every symbol in Dataflow as SVG. Select a symbol to open it, or download [all the symbols in one zip file](files/symbols-svg.zip). The meaning is explained in [chapter 2](2-symbol-language.md). The symbols for the Tableau template are PNG files in [tableau-symbols.zip](files/tableau-symbols.zip).

## How the files are named

Data symbols are named `<type>-<spokes>-<size>.svg`, for example `macro-data-08-2.svg`:

| Part | Values | Meaning |
|---|---|---|
| Type | `meta`, `micro-data`, `macro-data`, `stat-data`, `stat-product-simple`, `stat-product-advanced`, `stat-product-priority`, `micro-product-simple` | Data type and type of end product |
| Spokes | `00`, `03`, `08`, `12`, `20` | Number of spokes. `03`–`20` correspond to variables 1–4 in the Excel template. `00` has no spokes |
| Size | `1`, `2`, `3` | Amount of rows: little, medium, much |

Control data are named `control-data-<phase>-<size>.svg`, and the systems `system-bespoke` (type 1), `system-framework-menu` (type 2), `system-framework` (type 3) and `system-advanced` (type 0, next level).

The names differ from those in the Norwegian edition, and from the PNG names the Tableau template uses (`data-micro-4.png`, `system--1.png`), which are kept because the Excel formulas refer to them.
"""

order = {"system-advanced": 0, "system-bespoke": 1, "system-framework-menu": 2, "system-framework": 3}
out = [HEAD]
used = set()
for title, text, prefix in GROUPS:
    files = sorted(p.name for p in SYM.glob(prefix + "*.svg"))
    if prefix == "system-":
        files.sort(key=lambda n: order.get(n[:-4], 9))
    used.update(files)
    links = "\n".join(f'<a href="symbols/{n}" title="{n[:-4]}"><img src="symbols/{n}" alt="{n[:-4]}" loading="lazy"><span>{n[:-4]}</span></a>' for n in files)
    out.append(f"## {title}\n\n{text}\n\n<div class=\"symbol-grid\">\n{links}\n</div>\n")
missing = set(p.name for p in SYM.glob("*.svg")) - used
assert not missing, missing
(ROOT / "docs" / "graphic-elements.md").write_text("\n".join(out), encoding="utf-8")
with zipfile.ZipFile(ROOT / "docs" / "files" / "symbols-svg.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(SYM.glob("*.svg")):
        z.write(p, f"dataflow-symbols/{p.name}")
print(len(used), "symbols")
