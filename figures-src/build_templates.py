"""Builds the templates D1–D3 (docs/template/d1.md … d3.md) from the specification below.

Run from the repository root:   python figures-src/build_templates.py

Every field has a fixed key (data-k). Do not change the keys once the templates are in use,
or browsers will no longer find the answers people have written.
"""
import html
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "template"

PHASE = [("", ""), ("collect", "Collect"), ("process", "Process"), ("analyse", "Analyse"), ("disseminate", "Disseminate"),
         ("several", "Several phases"), ("?", "?")]
ALL_SOME = [("", ""), ("all", "All"), ("some", "Some"), ("?", "?")]
OBJECT = [("", ""), ("data", "data"), ("system", "system")]
TYPE = [("", ""), ("meta", "meta · metadata"), ("micro", "micro · micro data"), ("macro", "macro · macro data"),
        ("stat", "stat · statistics"), ("out", "out · output"), ("qual", "qual · quality indicator"),
        ("sys0", "system 0 · next level"), ("sys1", "system 1 · bespoke code"),
        ("sys2", "system 2 · framework with menu"), ("sys3", "system 3 · framework"), ("?", "?")]
ROWS = [("", ""), ("1", "1 · little"), ("2", "2 · medium"), ("3", "3 · much"), ("?", "?")]
VARIABLES = [("", ""), ("1", "1 · very few"), ("2", "2 · few"), ("3", "3 · many"), ("4", "4 · very many"), ("?", "?")]
STATE = [("", ""), ("SD", "SD · source data"), ("ID", "ID · input data"), ("PD", "PD · processed data"),
         ("ST", "ST · statistics"), ("OD", "OD · output data"), ("none", "none"), ("?", "?")]
STATUS = [("", ""), ("exists", "exists"), ("in progress", "in progress"), ("proposal", "proposal"), ("?", "?")]
LINK = [("", ""), ("data flow", "data flow"), ("metadata", "metadata"), ("dependency", "dependency")]
NEEDTYPE = [("", ""), ("S", "S · service"), ("P", "P · process"), ("V", "V · variables and states"),
            ("D", "D · dependency"), ("?", "?")]
EXISTS = [("", ""), ("yes", "Yes"), ("no", "No"), ("?", "?")]
SCOPE = [("", ""), ("one", "One statistic"), ("group", "A group of statistics")]

DATALISTS = {
    "platforms": ["SAS", "FAME", "Oracle", "Excel", "R", "Python", "SQL database", "Survey tool", "Web portal", "Cloud platform"],
    "roles": ["statistician", "statistics owner", "methodologist", "IT / developer", "dissemination", "external supplier"],
}

E = html.escape


def select(k, l, options):
    o = "".join(f'<option value="{E(v)}">{E(t)}</option>' for v, t in options)
    return f'<select data-k="{E(k)}" data-l="{E(l)}">{o}</select>'


def text(k, l, ph="", lst=None):
    p = f' placeholder="{E(ph)}"' if ph else ""
    li = f' list="{lst}"' if lst else ""
    return f'<input type="text" data-k="{E(k)}" data-l="{E(l)}"{p}{li}>'


def area(k, l, ph="", rows=2):
    p = f' placeholder="{E(ph)}"' if ph else ""
    return f'<textarea data-k="{E(k)}" data-l="{E(l)}" rows="{rows}"{p}></textarea>'


def field(inner, lbl):
    return f'<label class="tmpl-field"><span class="tmpl-label">{E(lbl)}</span>{inner}</label>'


def part(title, inner, cls=""):
    return f'<section class="tmpl-part {cls}"><h3>{E(title)}</h3>{inner}</section>'


def table(prefix, cols, n, example=None, lst=None):
    """cols: [(key, heading, type, options/datalist, width)]. type: t text, o area, v select."""
    head = "<th>#</th>" + "".join(f"<th>{E(h)}</th>" for _, h, *_ in cols)
    rows = []
    for r in range(1, n + 1):
        cells = [f'<td class="tmpl-nr">{r}</td>']
        for key, h, typ, extra, width in cols:
            k = f"{prefix}.{r}.{key}"
            ph = example.get(key, "") if (example and r == 1) else ""
            if typ == "v":
                el = select(k, h, extra)
            elif typ == "o":
                el = f'<textarea data-k="{E(k)}" data-l="{E(h)}" rows="1"' + (f' placeholder="{E(ph)}"' if ph else "") + "></textarea>"
            else:
                el = text(k, h, ph, extra)
            cells.append(f'<td style="min-width:{width}em">{el}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")
    dl = f' data-list="{lst}"' if lst else ""
    return (f'<div class="tmpl-table"><table class="tmpl-t"{dl}><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div>')


def common():
    r1 = "".join([
        field(text("common.statistic", "Statistic", "Example: Income and capital accounts"), "Statistic"),
        field(text("common.short", "Short name", "Example: NR IKR"), "Short name"),
        field(text("common.unit", "Organisational unit", "Example: National accounts division"), "Organisational unit"),
        field(text("common.contact", "Contact person", "Role or name"), "Contact person"),
    ])
    r2 = "".join([
        field(select("common.scope", "Applies to", SCOPE), "Does the template cover one statistic or a group?"),
        field(text("common.group", "Statistics in the group", "Groups only: short names or initials"), "Statistics in the group"),
        field(text("common.date", "Date", "Example: 26 Nov 2026"), "Date"),
    ])
    return part("About the statistic (shared by all templates)",
                f'<div class="tmpl-row" style="--kol:4">{r1}</div><div class="tmpl-row" style="--kol:3">{r2}</div>', "tmpl-common")


def tools():
    return ('<div class="tmpl-tools">'
            '<button type="button" class="md-button md-button--primary" data-do="ai">Make text for the AI assistant</button>'
            '<button type="button" class="md-button" data-do="copy">Copy answers</button>'
            '<button type="button" class="md-button" data-do="download">Download (.md)</button>'
            '<button type="button" class="md-button" data-do="print">Print</button>'
            '<button type="button" class="md-button tmpl-clear" data-do="clear">Clear template</button>'
            '<span class="tmpl-status" aria-live="polite"></span></div>'
            '<div class="tmpl-ai" hidden><p class="tmpl-label">Text for the AI assistant. Copy it into a conversation, '
            'together with a Dataflow 2.0 Excel file if you have one.</p>'
            '<textarea readonly rows="8" aria-label="Text for the AI assistant"></textarea>'
            '<button type="button" class="md-button" data-do="copyai">Copy the text</button></div>')


def datalists():
    return "".join(f'<datalist id="{i}">' + "".join(f'<option value="{E(v)}">' for v in vs) + "</datalist>"
                   for i, vs in DATALISTS.items())


def template(id_, title, task, parts):
    return (f'<div class="tmpl" data-tmpl="{id_}" data-title="{E(title)}" data-task="{E(task)}">'
            f'{tools()}<form class="tmpl-form" onsubmit="return false">{datalists()}{common()}{"".join(parts)}</form></div>')


def page(id_, title, lead, how, form, prev, nxt):
    nav = []
    if prev:
        nav.append(f"[← Template {prev}]({prev.lower()}.md)")
    nav.append("[All templates](index.md)")
    if nxt:
        nav.append(f"[Template {nxt} →]({nxt.lower()}.md)")
    steps = "\n".join(f"    {i}. {p}" for i, p in enumerate(how, 1))
    return f'''---
title: "{id_} {title}"
---

# Template {id_}: {title}

{lead} The template is based on [figure {id_}](../5-how-to-map.md#figure-{id_.lower()}).

!!! info "How to fill it in"

{steps}

    Your answers are stored only in this browser. When you are done, select **Make text for the AI assistant** and paste the text into your assistant. You can also download your answers or make a backup from the [overview](index.md#your-answers).

!!! warning "Do not enter information that must not be shared"
    The templates describe systems, data sets and processes, not people or figures. Do not enter personal data, unpublished figures, passwords or access information. The text you make is meant for an AI tool: follow your organisation's guidelines for using AI.

{form}

??? note "The template as a figure (for printing or a whiteboard)"

    ![Template {id_} as a figure](../figures/{id_}.svg){{ loading=lazy }}

    [Download SVG](../figures/{id_}.svg){{ download }}

{" · ".join(nav)}
'''


def d1():
    cols = [("name", "Process step", "t", None, 11), ("phase", "Phase", "v", PHASE, 8), ("what", "What happens", "o", None, 14),
            ("role", "Who (role)", "t", "roles", 9), ("platform", "Platform and systems", "t", "platforms", 11),
            ("data", "Data in → out", "o", None, 12), ("dep", "Dependencies", "o", None, 11),
            ("scope", "All / some", "v", ALL_SOME, 6)]
    ex = {"name": "Summing and reconciliation", "what": "Sums all sources and reconciles", "role": "?",
          "platform": "SAS", "data": "FIN, IKKE-FIN → INPUT EXCEL", "dep": "In: RG (source ?)"}
    parts = [
        part("Process steps in order", '<p class="tmpl-note">A step changes the data and can be described in one sentence. '
             'Often 5–10 steps. The first row shows an example from Statistics Norway.</p>' + table("D1.step", cols, 10, ex, "_list.D1")),
        part("Dependencies for the whole process", '<div class="tmpl-row" style="--kol:2">'
             + field(area("D1.in", "Takes from others", "Example: other accounts, registers, external suppliers"), "What does the process take from other statistics, registers or external sources?")
             + field(area("D1.out", "Delivers to others", "Example: statistics database, Eurostat, other statistics"), "Who uses what comes out?")
             + "</div>"),
        part("Uncertain and open questions", field(area("D1.questions", "Uncertain and open questions", "What you do not know, or want to discuss at the workshop", 3),
                                                   "What is unclear, and who can answer?")),
    ]
    task = "D1 Process steps and roles: update the model and draft level 1 (overview) with process steps, phases, roles, platforms and dependencies."
    return page("D1", "Process steps and roles",
                "The current process at level 1: what happens, who does it, on which platform and what is connected.",
                ["**Fill in the fields about the statistic.** They are shared by all templates.",
                 "**Split the process into steps** from collection to dissemination. Write the role, not the name.",
                 "**Platform first.** Program names come in template D2.",
                 "**Write ‘?’** where you do not know. It is a valid answer."],
                template("D1", "Process steps and roles", task, parts), None, "D2")


def d2():
    cols = [("step", "Step", "t", None, 4), ("id", "ID", "t", None, 5), ("name", "Name", "t", None, 10),
            ("object", "Object", "v", OBJECT, 6), ("type", "Type", "v", TYPE, 11), ("rows", "Rows", "v", ROWS, 7),
            ("vars", "Variables", "v", VARIABLES, 8), ("platform", "Platform", "t", "platforms", 8),
            ("state", "Stable state", "v", STATE, 9), ("desc", "Description", "o", None, 14),
            ("status", "Status", "v", STATUS, 7)]
    ex = {"step": "5", "id": "S1", "name": "SAS SUM", "platform": "SAS", "desc": "Sums all sources"}
    lcols = [("from", "From ID", "t", None, 6), ("to", "To ID", "t", None, 6), ("type", "Type", "v", LINK, 8),
             ("note", "Note", "t", None, 18)]
    lex = {"from": "S1", "to": "D1", "note": "Example: the sum goes on to reconciliation"}
    fetch = ('<div class="tmpl-fetch" data-from="_list.D1"><span class="tmpl-label">The process steps from template D1</span>'
             '<p data-empty="Not filled in yet. You can still use step numbers here.">–</p></div>')
    parts = [
        part("The process steps", fetch),
        part("Objects: data and systems", '<p class="tmpl-note">One row per data set or system. '
             'The ID is free but must be unique (for example S1, S2 for systems and D1, D2 for data). '
             'The same system can appear more than once if it is used in several places.</p>' + table("D2.obj", cols, 16, ex)),
        part("Connections", '<p class="tmpl-note">What goes from where to where? Use the IDs above. No coordinates: '
             'the drawing handles placement.</p>' + table("D2.link", lcols, 16, lex)),
        part("From Dataflow 2.0", field(text("D2.v2", "Existing 2.0 drawing", "File name or link, if one exists"),
                                        "Is there a Dataflow 2.0 drawing? Attach it together with the text.")),
    ]
    task = "D2 Data and systems: build objects and connections in the model, and draw level 2 (focus) for the process steps that are filled in."
    return page("D2", "Data and systems",
                "Level 2: the data sets and systems in each process step, and the connections between them. Replaces the Dataflow 2.0 Excel template.",
                ["**Take one process step at a time,** and write the step number from D1 in the first column.",
                 "**Choose type, rows and variables** with the same codes as in Dataflow 2.0.",
                 "**Write the connections** with the IDs from the object table.",
                 "**Stable state** is where the data set is stored in an agreed state. Choose ‘?’ if you do not know."],
                template("D2", "Data and systems", task, parts), "D1", "D3")


def d3():
    cols = [("state", "Data state", "v", STATE, 9), ("need", "Need", "o", None, 14), ("type", "Type", "v", NEEDTYPE, 9),
            ("replaces", "Replaces today", "o", None, 11), ("value", "Value", "o", None, 12),
            ("risk", "Risk of not doing it", "o", None, 12), ("exists", "On target platform?", "v", EXISTS, 7)]
    ex = {"need": "Shared intake and recoding of sources", "replaces": "13 intakes in SAS/Excel (step 1)",
          "value": "One tested routine, less maintenance", "risk": "13 SAS routines must move before the deadline"}
    parts = [
        part("Needs per data state", '<p class="tmpl-note">Write what is needed, not which tool to use. '
             '‘On target platform?’ is answered later, when the solution is assessed.</p>' + table("D3.need", cols, 10, ex)),
        part("Summary", '<div class="tmpl-row" style="--kol:3">'
             + field(area("D3.main", "The most important need", "", 3), "What is the most important need?")
             + field(area("D3.value", "Most value", "", 3), "Where does the migration add most value?")
             + field(area("D3.open", "To be clarified", "", 3), "What must be clarified before a solution can be chosen?")
             + "</div>"),
    ]
    task = "D3 Needs and value: draw the target-state skeleton (TO BE) with the data states as anchor points, and the needs-and-value lens. Needs, not solutions."
    return page("D3", "Needs and value",
                "The target state: what must be in place on the target platform, what it replaces, and what improves.",
                ["**Choose the data state** for each need: source, input, processed, statistics or output data.",
                 "**Write the need,** not the solution.",
                 "**Link to today’s process:** what does the need replace?",
                 "**Value and risk:** what improves, and what happens if we only move as-is?"],
                template("D3", "Needs and value", task, parts), "D2", None)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [("d1.md", d1), ("d2.md", d2), ("d3.md", d3)]:
        (OUT / name).write_text(fn(), encoding="utf-8")
        print("wrote", OUT / name)
