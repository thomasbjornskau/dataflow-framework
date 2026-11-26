---
title: 8 Adapting the framework
---

# 8 Adapting the framework

Dataflow was built for one organisation’s production and one platform migration. Most of it travels well. Some of it is Statistics Norway’s own choice, and another organisation should make its own. This chapter separates the two.

## What to keep

These parts carry the method. Change them, and drawings from different organisations can no longer be read side by side.

- **The two main symbols and their codes.** Data circles with type, size and spokes; system rectangles with types 0–3. The codes (`micro`, `macro`, `system` and so on) are already in English and are shared by the Excel template, the model and the skill.
- **The four phases from GSBPM:** collect, process, analyse and disseminate (phases 4–7).
- **Three levels** and the rule of one figure, one question, one audience.
- **Status that is shown and never guessed,** with “?” as a valid value.
- **Needs, not solutions, in the target state.**
- **Source tags and two gates.** Nothing is final until the subject-matter owners have confirmed it.

## What to adapt

| Part | In this edition | What to consider |
|---|---|---|
| **Data states** | Five stable states: SD, ID, PD, ST, OD | Use your own platform’s states, or leave the tag out until they are agreed |
| **Platforms** | SAS, FAME, Oracle, Excel and others, from the example | Your own legacy and target platforms. The list in the templates is only a suggestion |
| **Deadlines** | Retirement dates for legacy platforms | A lens for whatever sets the order: deadlines, contract renewals, risk, or none |
| **Roles** | A short list of role names | Your own role names. Write roles, not people |
| **Phases** | GSBPM 4–7 | Add *specify needs*, *design* or *build* only if the drawings must cover development work |
| **Colours** | A neutral palette | Your own palette. Keep the four phase colours distinct and keep violet for proposals |
| **Templates** | D1–D3, in English | Translate, rename fields or add columns. See below |
| **AI support** | The dataflow skill | Use it as it is, adapt the instructions, or leave AI out and draw by hand |

### Data states { #data-states }

The five stable data states come from the data platform at Statistics Norway, where they mark the points at which data are stored in an agreed, documented state:

| Code | State | Typical content (simplified) |
|---|---|---|
| SD | Source data | Data as received, unchanged |
| ID | Input data | Data that have been recoded, checked and made ready for production |
| PD | Processed data | Edited and linked data, ready for estimation |
| ST | Statistics | Estimated statistics, not yet published |
| OD | Output data | Published and delivered statistics |

They are a useful frame because they give the target state fixed anchor points. If your organisation has other states, replace the codes in the templates, the model and the skill. If it has none yet, the data-state lens can be used to discuss where such states should be.

### Templates { #templates }

The templates are built from a specification in `figures-src/build_templates.py`. To adapt them:

1. **Change the lists of values** at the top of the script (phases, types, states, platforms, roles).
2. **Change labels and help texts** in the functions `d1()`, `d2()` and `d3()`.
3. **Keep the keys** (`D1.step.1.name` and so on) if the templates are already in use. Browsers find stored answers by key.
4. **Run the script** and build the site. The JavaScript (`docs/assets/templates.js`) does not need to change unless you add new kinds of field.

The answers are stored in the browser’s local storage under the key `dataflow-framework-templates-v1`. If you publish your own copy at a different address, it gets its own storage.

## Forking the repository

The simplest way to adopt the framework is to fork the [repository](https://github.com/thomasbjornskau/dataflow-framework) and publish your own copy with GitHub Pages:

1. **Fork** the repository, or download it and create a new one.
2. **Change `site_name`, `site_url` and `repo_url`** in `mkdocs.yml`.
3. **Settings → Pages → Source: GitHub Actions.** The workflow in `.github/workflows/pages.yml` builds and publishes the site on every push to `main`.
4. **Replace the worked example** in chapter 6 with one of your own when you have one, and remove the Statistics Norway screenshots if you do not need them.

The figures are SVG made by code in `figures-src/`. Run `python figures-src/figures.py` to rebuild them after changing the palette or the labels, and `python figures-src/expand.py` to insert new figure placeholders in the pages.

## Licence and credit { #licence-and-credit }

The text, figures and symbols are offered under [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/) (CC BY 4.0). You may copy, translate and adapt them, also commercially, as long as you give credit. The code (figure scripts, template builder and JavaScript) is under the MIT licence.

Suggested credit: *Dataflow framework, developed at Statistics Norway. Adapted by [your organisation].*

The screenshots of Statistics Norway’s Tableau drawings are included as examples and show Statistics Norway’s own processes. Replace them with your own if you publish an adapted edition.

## Experience so far

The framework is young in this form. What can be said with some confidence:

- **Drawing from metadata works.** About 120 flows were drawn in 2.0, at about 15 minutes each once the Excel template was filled in.
- **The filling in is the hard part,** not the drawing. Most of the effort goes into finding the systems and data sets and agreeing on the order.
- **Seeing the whole process is what people value.** The feedback on the first drawings was that identifying every part, end to end, was the most useful thing.

What is not yet known: how well the AI support holds up across many statistics, how much the templates reduce workshop time, and whether the needs-and-value lens leads to different decisions. If you try the framework, those are the questions where your experience would be most useful.
