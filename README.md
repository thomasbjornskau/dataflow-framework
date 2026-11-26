# Dataflow framework

Dataflow is a framework for mapping and drawing the data flow in statistical production: which systems and data sets a statistic passes through, from collection to dissemination, and what a platform migration should achieve. This repository holds the English edition: eight chapters, the symbol language, fillable templates, concept figures, the Excel and Tableau templates from Dataflow 2.0, and an AI skill.

Developed at Statistics Norway. The [Norwegian edition](https://github.com/thomasbjornskau/ssb-dataflyt) describes the same method as it is used internally.

Site: https://thomasbjornskau.github.io/dataflow-framework/

> **Draft.** Version 3.0 is being tested. The worked example contains interpretations that have not been confirmed by the subject-matter owners.

## Contents

| Folder or file | What |
|---|---|
| `docs/index.md`, `docs/1-…md` – `docs/8-…md` | Home page and the eight chapters |
| `docs/template/` | The overview and the three fillable templates D1–D3 (singular, because MkDocs reserves `templates/`) |
| `docs/figures/` | Concept figures as SVG (1920 × 1080), named by figure number |
| `docs/symbols/` | All 121 symbols as SVG |
| `docs/images/` | Screenshots of Dataflow 1.0 and 2.0 drawings from Statistics Norway |
| `docs/files/templates/` | Excel template, Tableau template, the NR IKR example and the A3 grids |
| `docs/files/tableau-symbols/` | Symbols for Tableau as PNG (also in `tableau-symbols.zip`) |
| `docs/files/skills/` | The dataflow skill, as SKILL.md and zip |
| `docs/assets/` | Style (`site.css`) and the script that stores and exports template answers (`templates.js`) |
| `figures-src/` | Code for the figures, templates and symbol gallery |
| `mkdocs.yml` | Site settings and menu |
| `.github/workflows/pages.yml` | Builds the site and publishes it on GitHub Pages on every push to `main` |

## Build the site locally

```
pip install -r requirements.txt
mkdocs serve
```

Open http://127.0.0.1:8000.

## Rebuild figures and pages

```
pip install cairosvg openpyxl        # only needed for previews and the example
python figures-src/figures.py        # docs/figures/*.svg  (add --png for previews)
python figures-src/build_templates.py  # docs/template/d1.md – d3.md
python figures-src/build_gallery.py    # docs/graphic-elements.md and symbols-svg.zip
python figures-src/expand.py           # turns [[FIG:A1]] in the pages into figure blocks
```

Each template field has a fixed key (`data-k`). Do not change the keys once the templates are in use, or browsers will no longer find the answers people have written.

## Templates and privacy

The answers are stored only in the user’s browser (`localStorage`, key `dataflow-framework-templates-v1`). Nothing is sent anywhere. The pages warn users not to enter personal data, unpublished figures, passwords or access information.

## Licence

Text, figures and symbols: CC BY 4.0 (see `LICENSE-content.md`). Code: MIT (see `LICENSE`).
