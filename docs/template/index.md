---
title: Templates
---

# Templates

Three templates that the contact person for a statistic fills in before and after the workshop. They can be filled in here on the site, and the answers stay in your browser until you delete them. When you are done, you make a text to paste into a conversation with an AI assistant. The [dataflow skill](../7-tools.md#ai-support) turns the text into a model, drawings and a list of what must be checked.

| Template | The question | Level | Status |
|---|---|---|---|
| [D1 Process steps and roles](d1.md) | What happens, who does it, on which platform, and what is connected? | Level 1, overview | <span data-status-tmpl="D1">not started</span> |
| [D2 Data and systems](d2.md) | Which data sets and systems are in each step, and how are they connected? | Level 2, focus | <span data-status-tmpl="D2">not started</span> |
| [D3 Needs and value](d3.md) | What must be in place on the target platform, what does it replace, and what improves? | Target state | <span data-status-tmpl="D3">not started</span> |

The templates replace the Excel template from Dataflow 2.0 as the way of collecting information, but use the same codes. [Chapter 5](../5-how-to-map.md) explains where in the mapping process they are used.

## From template to drawing

1. **Fill in D1** before the workshop, as far as you can. “?” is a valid answer.
2. **Fill in D2** for the process steps that are to be drawn in detail. If the statistic has a Dataflow 2.0 drawing, it can be used instead of, or as well as, D2.
3. **Fill in D3** after the workshop, once today’s process has been gone through.
4. **Make text for the AI assistant** here on the overview. The text combines every template you have filled in and asks for a model, drawings and a quality checklist.
5. **Paste the text into your AI assistant** with the dataflow skill installed. Attach the 2.0 Excel file if there is one.
6. **Check the result.** What AI makes is a draft. The subject-matter owners confirm before anything goes further.

## Your answers

<div class="tmpl-overview" markdown="0">
<div class="tmpl-tools">
<button type="button" class="md-button md-button--primary" data-do="ai">Make combined text for the AI assistant</button>
<button type="button" class="md-button" data-do="all">Download all answers (.md)</button>
<button type="button" class="md-button" data-do="backup">Make a backup (.json)</button>
<button type="button" class="md-button" data-do="restore">Restore from a backup</button>
<button type="button" class="md-button tmpl-clear" data-do="delete">Delete all answers</button>
<input type="file" accept="application/json,.json" hidden>
<span class="tmpl-status" aria-live="polite"></span>
</div>
<div class="tmpl-ai" hidden><p class="tmpl-label">Text for the AI assistant. Copy it into a conversation.</p><textarea readonly rows="10" aria-label="Text for the AI assistant"></textarea><button type="button" class="md-button" data-do="copyai">Copy the text</button></div>
</div>

The answers are stored in the browser’s local storage on your own machine. Nothing is sent to GitHub or anywhere else. To continue on another machine, make a backup and restore it there.

!!! warning "Do not enter information that must not be shared"
    The templates describe systems, data sets and processes, not people or figures. Do not enter personal data, unpublished figures, passwords or access information. The text you make is meant for an AI tool: follow your organisation’s guidelines for using AI.
