---
name: dataflow
description: "Use when mapping or drawing the data flow of a statistical production process with the Dataflow framework: reading a Dataflow 2.0 Excel file, working from templates D1–D3, and drawing levels 1–3, lenses and AS IS / TO BE figures as SVG."
---

# Dataflow framework (version 0.1)

Dataflow is a framework for mapping how data and systems fit together in the production of a statistic. It was developed at Statistics Norway: 1.0 was drawn by hand, 2.0 is drawn from metadata in Excel and shown in Tableau (about 120 flows), and 3.0 is AI-supported mapping that should point to **needs and value in a platform migration**, not only document what has to be moved.

Documentation, templates and symbols: https://thomasbjornskau.github.io/dataflow-framework/

This file is self-contained. It can be loaded as a skill, or pasted into an AI assistant as instructions.

## Core principle

One **model per statistic** (YAML) is the source. Everything that comes in (a 2.0 Excel file, templates D1–D3, workshop notes, screenshots) updates the model. Every drawing and list is made from the model. Always deliver the updated model as a file with the figures, so the next session can continue.

## Way of working

- Answer in the language the user writes in. Be plain and direct. Ask one clarifying question at a time, and only when the answer changes what you make.
- “?” is a valid answer. What has not been assessed is never guessed. Show it dashed grey.
- Keep apart what the sources say, what you interpret and what you propose. Mark interpretation in the footer and in the quality checklist.
- The subject-matter owners own the content. AI makes drafts, not answers.
- Every delivery ends with a **quality checklist** divided by who must confirm (subject-matter owners, project lead, whoever drew it).
- Never ask for, or put into figures, personal data, unpublished figures, passwords or access information. Remind the user of their organisation’s AI guidelines if such information appears.

## Three working modes

### A. Read in an existing 2.0 flow
1. Read the Excel file (for example with openpyxl). The data sheet is the first sheet, often named after the statistic. Use only rows where `mark == "shape"`. See “Translation from 2.0”.
2. Build the model: objects with their own ID, links from `coord` → `next`.
3. Count elements, systems, data sets and links. These numbers are useful in subtitles.
4. Draw the flow straight from the coordinates (level 2 look) as a check, and look at it.
5. Propose a division into 5–10 process steps (level 1). The division is always an interpretation and is tagged as such.
6. Make a list of questions: roles (not in 2.0), dependencies out, objects with no source, unclear names, `step` values that do not match the position.
7. Use Tableau screenshots only for what was added by hand: explanation boxes, icons, process names, frames.

### B. Map with the templates
1. Take in completed D1 (process steps and roles), D2 (data and systems) and D3 (needs and value), and any notes.
2. Update the model. Keep a source tag per field: `source: D1 | D2 | D3 | 2.0 | workshop | interpretation`.
3. Ask follow-up questions one at a time, in this order: process steps and phases → roles → platforms → dependencies in and out → stable data states → needs.
4. Make a new version of the drawings and the quality checklist.

### C. Draw
Make what is needed from the model (see “Figure types”). Render to PNG and look at the image before delivering: overlaps, arrows through text, text outside boxes, labels colliding with the legend or footer.

## The data model (YAML)

```yaml
statistic: {short: NR IKR, name: Income and capital accounts, unit: National accounts, group: false}
version: {date: 2026-10-08, status: draft, sources: ["Dataflow 2.0 Excel", "D1"]}
steps:
  - id: P5
    name: Summing and reconciliation
    phase: analyse             # collect | process | analyse | disseminate (may be several)
    what: Sums all sources and reconciles
    role: "?"                  # a role, not a name
    platforms: [SAS]
    applies_to: all            # all | some: [short names] (for groups)
    source: interpretation
objects:
  - id: S1
    name: SAS SUM
    object: system             # system | data
    system_type: 1             # 0 next level, 1 bespoke code, 2 framework with menu, 3 framework
    platform: SAS
    step: P5
    description: SAS application that sums all sources
    status: exists             # exists | in progress | proposal | "?"
    source: "2.0"
    ref_2_0: "7,5"             # original coordinate, for traceability
  - id: D1
    name: ALT SAMLET
    object: data
    data_type: macro           # meta | micro | macro | stat | out | qual
    rows: 2                    # 1 little, 2 medium, 3 much
    variables: 3               # 1 very few, 2 few, 3 many, 4 very many
    stable_state: "?"          # SD | ID | PD | ST | OD | none | "?"
    step: P5
links:
  - {from: S1, to: D1, type: data flow}     # data flow | metadata | dependency
externals:
  - {id: X_REA, name: REA, direction: in, type: statistic}   # in | out
needs:                         # from D3, TO BE only
  - id: N1
    state: ID                  # SD | ID | PD | ST | OD
    type: service              # service | process | variables | dependency
    need: Shared intake and recoding of sources
    replaces: [P1]
    value: One tested routine, less maintenance
    risk: 13 SAS routines must move before the SAS deadline
    on_target_platform: "?"    # yes | no | "?" (assessed after the mapping)
    source: interpretation
```

Rules:
- The ID is independent of position. Coordinates are optional hints (`hint: {x: 3, y: 5}`).
- The same system may appear in several places in the process. That is deliberate: show each place where a transformation happens.
- **Data type and stable state are two different properties.** The data type says what the data are (level of aggregation). `stable_state` says where the data set is stored in an agreed state on the target platform. Many micro data sets along the way have `stable_state: none`.
- The five states SD, ID, PD, ST, OD (source, input, processed, statistics, output) are the default from Statistics Norway. If the user’s organisation has other states, use theirs and say so in the model.
- `out` means openly available. A delivery that is not open (for example to an international organisation) is `stat`.
- Keep names of systems and data sets in the language they are used in. Do not translate them.

## Translation from 2.0

Columns in the 2.0 template: `object, coord, next, X-line, Y-line, X-shp, mark, rel, step, data, name, desc, system, data_rows, data_cols, id, line, symbol`. Each object has two rows (`shape` and `line`). An object with several outputs is duplicated, one row per `next`.

| 2.0 | 3.0 | Note |
|---|---|---|
| `coord` ("x,y", comma as separator) | `ref_2_0`, new `id` | The coordinate was the ID. Make a new ID (S1…, D1…). Merge duplicates with the same `coord`. |
| `next` | `links` | `next == coord` means an end node. |
| `object` | `object` | |
| `data` | `data_type` | `qual` is defined but hardly ever used and has no symbol. |
| `system` | `system_type` | 0 is “next level”, but was never drawn as its own tab. |
| `data_rows`, `data_cols` | `rows`, `variables` | For systems `data_rows` is always 3 and can be ignored. |
| `step` | phase on the process step | `step` does not control the phase bands in Tableau. Position and `step` may disagree; ask. Many flows have no `collect`. |
| `name`, `desc` | `name`, `description` | Names such as “SAS” and “TAB” recur. Do not rename; use the ID to tell them apart. |
| – | platform | Derive carefully from names (SAS, FAME, Excel, Oracle). Tag as interpretation. |
| – | role, dependencies out, stable state, needs | Not in 2.0. Set “?”. |

Objects in the first column that are other statistics (for example other accounts that a national accounts process takes figures from) are **dependencies**. Move them to `externals` when it is clear, and ask otherwise.

Minimal reading:
```python
import openpyxl
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
```

## The symbol language

Keep the codes and symbols from 2.0. Draw them as SVG primitives (circles and lines), not as images.

**Data symbol** (circle):
- Radius by `rows`: 1 → 13 px, 2 → 17 px, 3 → 21 px (level 2). Outer circle white with a dark stroke `#2b3440`.
- Spokes by `variables`: 1 → 3, 2 → 8, 3 → 12, 4 → 20, from the inner circle (radius × 0.48) to the outer.
- Core by `data_type`: `meta` no core (spokes only), `micro` white, `macro` grey `#a9b3c0`, `stat` dark `#2b3440`, `out` dark with four petals (`#a9b3c0`) behind the circle at 45°, 135°, 225°, 315° (radius × 0.5, centre radius × 0.72 out). The metaphor is that data burst into bloom when they reach the users.
- **Stable state:** green pill `#2b7a5c` with white text SD, ID, PD, ST or OD at the top right of the symbol.

**System symbol** (rounded rectangle, about 24 × 34 px): 1 dark `#47505e`, 2 grey `#b3bcc8`, 3 white with a dark stroke, 0 orange `#f6b48f` with a magnifier. Meaning: 1 the producing unit develops and controls the code, 2 the unit can adapt some of it, 3 the unit cannot change it, 0 can be opened as a detail figure.

**New in 3.0**:
- Process step (level 1): white box with a dark border, title, system symbols at the bottom left, platform pills at the bottom right.
- Platform pill: grey pill. In the platform and deadline lens: earliest deadline darkest (`#2b3440`), next `#667080`, then `#b3bcc8`, platforms with no deadline white.
- Role: violet pill (fill `#f2f1f9`, stroke `#6b5fb5`, text `#483d8b`). Unresolved role: dashed “Role: ?”.
- Links: data flow solid `#7a8493`, thickness by `rows` at the source (1.3 / 2.0 / 2.8); metadata thin green `#2b7a5c`; dependency dashed grey `#667080`.
- Status: dashed grey = unresolved (“?”), dashed violet = proposal or target state (needs).
- Externals (other statistics, outside sources): grey dashed box outside the phase bands.

**Phase bands** (faint backgrounds, GSBPM 4–7): Collect `#eef7f0` (label `#3d7a55`), Process `#eaf4f8` (`#2f6f86`), Analyse `#f4f2fc` (`#5a4aa8`), Disseminate `#fcf8e6` (`#7a6410`). Only these four phases are used. Phases are set on process steps, not on single objects, and bands may overlap where the process does.

Violet means roles and proposals. The Analyse band is light enough not to be confused with it, but keep an eye on it.

## Form factor (1920 × 1080)

- Title x 60, y 92, 46 px bold. Subtitle y 136, 24 px, grey `#667080`. Rule at y 160, 2 px `#d6dae0`.
- Label pills top right: Overview, Focus, Detail, Lens, Scenario, plus PROPOSAL or DRAFT.
- Diagram area x 60–1400, y 180–986.
- Explanation panel x 1440–1860: fill `#f3f5f9`, edge `#d0d6e0`, 3–5 numbered points (heading 18–20 px bold, text 17 px).
- Legend bottom left (y 1046), footer bottom right: date · status · source.
- Font: `Open Sans, Segoe UI, Arial, sans-serif`. Smallest text 14 px, 12 px only in small pills and marker numbers.
- Text `#1f262f`, secondary `#667080`, rules `#d6dae0`. Dimmed elements in focus variants: fill `#f6f7f9`, stroke `#e2e5ea`, text `#bcc3cc`. Red only for errors or risk, never as decoration.
- Boxes have small corner radii; pills are fully rounded; markers and nodes are circles. 1 px frames, 2 px only for focus. No gradients, shadows or 3D.
- Arrows: 2 px stroke, filled triangle head in the stroke colour, the same head everywhere in a series.
- Colour always means something. No coloured areas without a meaning in the legend.

If the user has an organisational palette, translate the colours to it by meaning (structure, data, roles and proposals, unresolved, phases), and say what could not be translated.

## SVG rules

Only `rect`, `line`, `polyline`, `polygon`, `circle`, `ellipse`, `path`, `text`. No CSS classes, filters, markers or `foreignObject`. Arrowheads as polygons. Wrap text by hand. Colours and fonts as attributes. This keeps the files usable in slide software and design tools.

## Layout rules

- The flow runs from left (Collect) to right (Disseminate). The order is derived from the links (layered layout), not from coordinates.
- Externals in stand on the left, outside the bands. “Used by” and deliveries out stand on the right in Disseminate.
- Draw lines before symbols and blocks, so the symbols sit on top.
- Many parallel similar objects (for example 13 intakes) are combined in one process step and shown as a grid of small system symbols, with the number in the text.
- Data sets between process steps sit on the link, with the name below. If space is tight: a short name at 12–14 px, or drop the name and explain in the panel.
- Avoid lines crossing sources and labels. Route dependency lines along the bottom rather than through the source column.

## Figure types

| Figure | Shows | Source |
|---|---|---|
| Level 1 Overview | 5–10 process steps across the phase bands, platforms, roles (or “?”), externals in and out, key data sets between the steps | D1, 2.0 |
| Level 2 Focus | One process step with all data and system symbols and names | D2, 2.0 |
| Level 3 Detail | The inside of one system (typically system type 0). Unknown content drawn dashed grey with “?” | Own meeting |
| Full 2.0 flow | Every object straight from the coordinates, with markers on what is hidden | 2.0 |
| Lens: platform and deadline | Level 1 with platform pills coloured by deadline | model + deadlines |
| Lens: dependencies | Level 1 with externals in and out highlighted | model |
| Lens: stable data states | Level 1 with SD, ID, PD, ST, OD where they are, or “?” | model |
| Lens: needs and value | Focus variant with numbered violet markers where there are possible gains | D3, interpretation |
| Target-state skeleton (TO BE) | Grid: columns SD, ID, PD, ST, OD under the phases; rows services, processes, variables and states, dependencies. Cells with needs (dashed violet) or “?” | D3 |
| From current process to target state | AS IS at the top, TO BE skeleton at the bottom, the difference as a list of needs | D1–D3 |
| Blank templates | D1, D2, D3 as work surfaces | – |

Focus variants are made on the same base figure with dimming and numbered markers that match the panel. Use violet markers when they point to value or proposals.

If there is no deadline, the deadline lens becomes a platform lens: which platforms does the process run on, and which are to be retired.

**TO BE rules**: the target state shows needs, not solutions. No system symbols until it has been assessed what exists or must be built. Label the figure “Scenario · PROPOSAL”. The data states are fixed anchor points.

## The templates

**D1 Process steps and roles** (level 1). Fields at the top: statistic, short name, unit, contact person, one statistic or a group, statistics in the group, date. Columns: #, Process step, Phase, What happens, Who (role), Platform and systems, Data in → out, Dependencies, All / some. Rules: often 5–10 steps; a step changes the data and can be described in one sentence; write roles, not names; platform first, program names at level 2.

**D2 Data and systems** (level 2, replaces the 2.0 Excel). One process step at a time. Objects table: Step, ID, Name, Object, Type, Rows, Variables, Platform, Stable state, Description, Status. Connections table: From ID, To ID, Type (data flow, metadata, dependency), Note. No coordinates.

**D3 Needs and value** (target state). Columns: Data state, Need, Type (S service, P process, V variables and states, D dependency), Replaces today, Value, Risk of not doing it, On target platform? (yes, no, ?). Summary: the most important need, where the migration adds most value, what must be clarified.

**The mapping process**: kick-off (scope) → before the workshop (the contact person fills in D1/D2; AI drafts from a 2.0 flow and fact sheets and lists questions) → **gate 1: draft ready** → workshop (go through today’s process and the target state with the draft, resolve “?”) → follow-up (AI turns notes into a model, draws levels 1 and 2, makes a quality checklist; the mapping team checks; the contact person confirms) → **gate 2: confirmed by the owners** → result (drawings, list of needs to the backlog, input to the solution assessment, lenses combined across statistics).

## Worked example: NR IKR at Statistics Norway

The 2.0 file has 70 elements (28 systems, 42 data sets) and 76 links. Division into seven process steps (interpretation):

1. Intake and recoding (process): 13 SAS/Excel intakes from 11 sources and 6 other accounts (REA, AR, UR, OFF, NAV via UR, TOMT). Platforms SAS, Excel.
2. Financial sectors (process): FINANS with the recoding catalogue OMKOD (meta).
3. Non-financial sectors (process): SAS BEREGN.
4. Capital, shares, AR and OFF (process): SAS IBERKAP, SAS balancing, AR2IKR, OFF app.
5. Summing and reconciliation (analyse): SAS SUM → ALT SAMLET → SAS AVSTEM → INPUT EXCEL. RG also comes in (source unknown).
6. Inspection and manual editing (analyse): EXCEL EDIT (system type 0) → TAB.
7. Recoding to NO and ESA (analyse): 2 × SAS, 2 × FAME. Out: statistics database (out), Eurostat (stat).

Possible value (interpretation, to be confirmed by the owners): 13 similar intakes → one shared routine; manual Excel editing → traceable editing with a log; parallel NO and ESA runs → coordinated; six accounts decide when IKR can move. The platform lens shows that the end of the process (FAME, retired around 1 November 2028) has the earliest deadline, so the order is reversed.

Use the example to explain the method. Do not apply its platforms, deadlines or data states to another organisation without asking.

## Delivery

- Model file `<shortname>_dataflow.yaml`.
- SVG per figure at 1920 × 1080 with descriptive file names, PNG for your own check, a zip when a set is complete.
- Quality checklist (`quality_checklist.md`) divided by who must confirm.
- Accompanying text: what the figures show, choices made, what is interpretation, and one next question.

## Known limitations in 0.1

- The drawing code is not part of this file. Write it by the rules above and reuse it within the session. The repository has reference code in `figures-src/` (`dfdraw.py` for primitives, `figures.py` for the figure series) that gives the same result every time.
- Platforms derived from 2.0 names are always an interpretation until someone confirms them.
- Drawings may vary a little between sessions. The model file keeps the content stable.
