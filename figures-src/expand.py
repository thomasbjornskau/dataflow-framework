"""Expands [[FIG:ID]] in docs/*.md into figure blocks, with title and subtitle read from the SVG.

Run from the repository root:   python figures-src/expand.py
The placeholders are replaced in place, so the script can be run again after new placeholders are added.
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def titles(fid):
    s = (DOCS / "figures" / f"{fid}.svg").read_text(encoding="utf-8")
    t = [html.unescape(x) for x in re.findall(r"<text[^>]*>([^<]*)</text>", s) if x.strip()]
    return t[0], t[1]


def block(fid, prefix):
    title, sub = titles(fid)
    alt = f"{title}. {sub}".replace("[", "(").replace("]", ")")
    src = f"{prefix}figures/{fid}.svg"
    return (f'<figure class="fig" id="figure-{fid.lower()}" markdown="span">\n'
            f'  [![{alt}]({src}){{ loading=lazy }}]({src})\n'
            f'  <figcaption>Figure {fid}. {html.escape(title)} · <a href="{src}" download>Download SVG</a></figcaption>\n'
            f'</figure>')


for md in DOCS.rglob("*.md"):
    text = md.read_text(encoding="utf-8")
    if "[[FIG:" not in text:
        continue
    prefix = "../" * (len(md.relative_to(DOCS).parts) - 1)
    text = re.sub(r"\[\[FIG:([A-Z0-9]+)\]\]", lambda m: block(m.group(1), prefix), text)
    md.write_text(text, encoding="utf-8")
    print("expanded", md.relative_to(ROOT))
