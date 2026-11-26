/* Templates D1–D3: saving in the browser, export, print and text for an AI assistant.
   Everything is kept in localStorage under one key. Nothing is sent anywhere. */
(function () {
  "use strict";
  var LS = "dataflow-framework-templates-v1";
  var ORDER = ["D1", "D2", "D3"];
  var COMMON = [
    ["common.statistic", "Statistic"], ["common.short", "Short name"], ["common.unit", "Organisational unit"],
    ["common.contact", "Contact person"], ["common.scope", "Applies to"], ["common.group", "Statistics in the group"],
    ["common.date", "Date"]
  ];

  function load() {
    try { return JSON.parse(window.localStorage.getItem(LS)) || {}; } catch (e) { return {}; }
  }
  function store(d) {
    try { window.localStorage.setItem(LS, JSON.stringify(d)); return true; } catch (e) { return false; }
  }
  function all(root, sel) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function clean(s) { return String(s == null ? "" : s).replace(/\|/g, "/").replace(/\s*\n\s*/g, " ").trim(); }

  function value(el) { return el.type === "checkbox" ? el.checked : el.value; }
  function shown(el) {
    if (el.tagName === "SELECT") {
      var o = el.options[el.selectedIndex];
      return o && o.value ? o.textContent : "";
    }
    return el.value;
  }

  function fill(tmpl, d) {
    all(tmpl, "[data-k]").forEach(function (el) {
      if (!/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) return;
      var v = d[el.dataset.k];
      if (v === undefined) return;
      if (el.type === "checkbox") el.checked = !!v; else el.value = v;
    });
    all(tmpl, ".tmpl-fetch").forEach(function (h) {
      var p = h.querySelector("p");
      var v = d[h.dataset.from];
      p.textContent = v ? v : p.dataset.empty;
      p.classList.toggle("tmpl-empty", !v);
    });
  }

  /* Tables become markdown tables with only the rows that are filled in */
  function tableMd(tab) {
    var head = all(tab, "thead th").map(function (th) { return th.textContent; });
    var rows = [];
    all(tab, "tbody tr").forEach(function (tr) {
      var cells = all(tr, "td").map(function (td) {
        var el = td.querySelector("[data-k]");
        return el ? clean(shown(el)) : clean(td.textContent);
      });
      if (cells.slice(1).some(function (c) { return c; })) rows.push(cells);
    });
    if (!rows.length) return "–";
    var out = ["| " + head.join(" | ") + " |", "|" + head.map(function () { return "---"; }).join("|") + "|"];
    rows.forEach(function (r) { out.push("| " + r.map(function (c) { return c || " "; }).join(" | ") + " |"); });
    return out.join("\n");
  }

  function commonMd(d) {
    var lines = [];
    COMMON.forEach(function (f) { if (d[f[0]]) lines.push("- **" + f[1] + ":** " + d[f[0]]); });
    return lines.join("\n");
  }

  function toMarkdown(tmpl, d) {
    var lines = ["# Template " + tmpl.dataset.tmpl + ": " + tmpl.dataset.title, ""];
    var c = commonMd(d);
    if (c) lines.push(c, "");
    all(tmpl, ".tmpl-part").forEach(function (part) {
      if (part.classList.contains("tmpl-common")) return;
      lines.push("## " + part.querySelector("h3").textContent, "");
      all(part, "table.tmpl-t, .tmpl-field > [data-k], .tmpl-fetch").forEach(function (el) {
        if (el.tagName === "TABLE") { lines.push(tableMd(el), ""); return; }
        if (el.classList.contains("tmpl-fetch")) {
          lines.push("- **" + el.querySelector(".tmpl-label").textContent + ":** " + (d[el.dataset.from] || "–"));
          return;
        }
        var t = clean(shown(el));
        lines.push("- **" + el.dataset.l + ":** " + (t || "–"));
      });
      lines.push("");
    });
    return lines.join("\n").replace(/\n{3,}/g, "\n\n").trim() + "\n";
  }

  function aiText(ids, d) {
    var name = d["common.statistic"] || "the statistic";
    var tasks = ids.map(function (id) { return d["_task." + id]; }).filter(Boolean);
    var parts = ids.map(function (id) { return d["_md." + id]; }).filter(Boolean);
    var out = [
      "Use the Dataflow framework (the dataflow skill if it is installed), working mode B: map with the templates.",
      "",
      "Below are completed templates for " + name + ". “?” means something has not been assessed. Do not guess it.",
      "",
      "Task:"
    ];
    tasks.forEach(function (t) { out.push("- " + t); });
    out.push("- Deliver the model file (YAML) and a quality checklist grouped by who must confirm each point.");
    out.push("- Ask follow-up questions one at a time before drawing anything that rests on assumptions.");
    out.push("- Answer in the language of this text.");
    out.push("", "---", "");
    return out.join("\n") + parts.join("\n---\n\n");
  }

  function save(tmpl, status) {
    var d = load();
    all(tmpl, "[data-k]").forEach(function (el) {
      if (!/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) return;
      d[el.dataset.k] = value(el);
    });
    /* Lists that other templates can fetch */
    all(tmpl, "[data-list]").forEach(function (tab) {
      var names = [];
      all(tab, "tbody tr").forEach(function (tr, i) {
        var el = tr.querySelector("[data-k]");
        if (el && el.value.trim()) names.push((i + 1) + " " + el.value.trim());
      });
      d[tab.dataset.list] = names.join(" · ");
    });
    d["_md." + tmpl.dataset.tmpl] = toMarkdown(tmpl, d);
    d["_task." + tmpl.dataset.tmpl] = tmpl.dataset.task;
    d["_t." + tmpl.dataset.tmpl] = new Date().toISOString();
    var ok = store(d);
    if (status) {
      var t = new Date();
      status.textContent = ok
        ? "Saved in this browser at " + String(t.getHours()).padStart(2, "0") + ":" + String(t.getMinutes()).padStart(2, "0")
        : "Could not save in the browser. Download your answers before closing the page.";
    }
    return d;
  }

  function download(name, text, type) {
    var blob = new Blob([text], { type: type || "text/markdown;charset=utf-8" });
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  function copy(text, status) {
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text; document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); status.textContent = "Copied."; } catch (e) { status.textContent = "Could not copy. Select the text and copy it yourself."; }
      ta.remove();
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { status.textContent = "Copied."; }, fallback);
    } else fallback();
  }

  function showAi(box, text, status) {
    var ta = box.querySelector("textarea");
    ta.value = text;
    box.hidden = false;
    ta.style.height = "auto"; ta.style.height = Math.min(ta.scrollHeight + 4, 520) + "px";
    box.scrollIntoView({ behavior: "smooth", block: "nearest" });
    if (status) status.textContent = "The text is ready. Copy it into your AI assistant.";
  }

  function startTemplate(tmpl) {
    var status = tmpl.querySelector(".tmpl-status");
    var aibox = tmpl.querySelector(".tmpl-ai");
    fill(tmpl, load());
    var timer;
    tmpl.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(function () { save(tmpl, status); }, 300); });
    tmpl.addEventListener("change", function () { save(tmpl, status); });
    all(tmpl, "textarea:not([readonly])").forEach(function (t) {
      var grow = function () { t.style.height = "auto"; t.style.height = (t.scrollHeight + 2) + "px"; };
      t.addEventListener("input", grow); grow();
    });
    tmpl.addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-do]"); if (!b) return;
      var d = save(tmpl, status);
      var md = d["_md." + tmpl.dataset.tmpl];
      var act = b.dataset.do;
      if (act === "copy") copy(md, status);
      if (act === "download") download("dataflow-template-" + tmpl.dataset.tmpl + ".md", md);
      if (act === "ai") showAi(aibox, aiText([tmpl.dataset.tmpl], d), status);
      if (act === "copyai") copy(aibox.querySelector("textarea").value, status);
      if (act === "print") window.print();
      if (act === "clear" && window.confirm("Clear all fields in template " + tmpl.dataset.tmpl + "? The fields about the statistic are kept.")) {
        var dd = load(), id = tmpl.dataset.tmpl;
        Object.keys(dd).forEach(function (k) {
          if (k.indexOf(id + ".") === 0 || ["_md.", "_t.", "_task.", "_list."].some(function (p) { return k === p + id; })) delete dd[k];
        });
        store(dd);
        all(tmpl, "[data-k]").forEach(function (el) {
          if (el.dataset.k.indexOf("common.") === 0) return;
          if (el.type === "checkbox") el.checked = false; else if (/^(INPUT|TEXTAREA|SELECT)$/.test(el.tagName)) el.value = "";
        });
        aibox.hidden = true;
        status.textContent = "The template has been cleared.";
      }
    });
  }

  function startOverview(root) {
    var d = load();
    all(document, "[data-status-tmpl]").forEach(function (el) {
      var t = d["_t." + el.dataset.statusTmpl];
      el.textContent = t ? "started " + new Date(t).toLocaleDateString("en-GB") : "not started";
      el.classList.toggle("tmpl-started", !!t);
    });
    var status = root.querySelector(".tmpl-status");
    var aibox = root.querySelector(".tmpl-ai");
    if (root.dataset.wired) return;
    root.dataset.wired = "1";
    root.addEventListener("click", function (ev) {
      var b = ev.target.closest("button[data-do]"); if (!b) return;
      var dd = load();
      var done = ORDER.filter(function (k) { return dd["_md." + k]; });
      var act = b.dataset.do;
      if ((act === "all" || act === "ai") && !done.length) { status.textContent = "You have not filled in any template yet."; return; }
      if (act === "all") download("dataflow-templates-" + (dd["common.short"] || "all").replace(/[^\w-]+/g, "_") + ".md",
        done.map(function (k) { return dd["_md." + k]; }).join("\n---\n\n"));
      if (act === "ai") showAi(aibox, aiText(done, dd), status);
      if (act === "copyai") copy(aibox.querySelector("textarea").value, status);
      if (act === "backup") download("dataflow-templates-backup.json", JSON.stringify(dd, null, 1), "application/json");
      if (act === "restore") root.querySelector("input[type=file]").click();
      if (act === "delete" && window.confirm("Delete all answers in all templates in this browser?")) {
        try { window.localStorage.removeItem(LS); } catch (e) { /* nothing to do */ }
        aibox.hidden = true;
        status.textContent = "All answers have been deleted."; startOverview(root);
      }
    });
    var file = root.querySelector("input[type=file]");
    if (file) {
      file.addEventListener("change", function () {
        var f = file.files[0]; if (!f) return;
        f.text().then(function (t) {
          try {
            var inp = JSON.parse(t), dd = load();
            Object.keys(inp).forEach(function (k) { dd[k] = inp[k]; });
            store(dd); status.textContent = "Answers restored from the file."; startOverview(root);
          } catch (e) { status.textContent = "The file could not be read."; }
        });
      });
    }
  }

  function start() {
    all(document, ".tmpl").forEach(startTemplate);
    var o = document.querySelector(".tmpl-overview");
    if (o) startOverview(o);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start); else start();
})();
