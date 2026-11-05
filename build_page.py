#!/usr/bin/env python3
"""Assemble sre.html: static markup + inline architecture SVG (from diag.svg)."""
import os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
svg = open(os.path.join(HERE, "diag.svg")).read()
today = datetime.date(2026, 11, 4).strftime("%B %-d, %Y")
iso = datetime.date(2026, 11, 4).isoformat()

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Self-Maintaining Home Automation &middot; Smartihats</title>
  <meta name="description" content="A home automation stack that monitors, diagnoses, and repairs itself: an autonomous SRE agent keeps the smart home healthy, with all AI inference running locally on the home's own hardware.">
  <meta name="color-scheme" content="light dark">
  <style>
    :root {
      --bg: #f6f7f9; --card: #ffffff; --ink: #1c2330; --muted: #5b6575;
      --line: #e3e7ee; --accent: #2f6fed; --accent-soft: #e8f0fe;
      --ok: #1d9e6f; --ok-soft: #e4f6ee;
      --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
    }
    @media (prefers-color-scheme: dark) {
      :root { --bg:#0f141c; --card:#171f2b; --ink:#e8edf5; --muted:#94a0b3;
        --line:#263245; --accent:#6ea8ff; --accent-soft:#1b2b45; --ok:#48c793; --ok-soft:#143527; }
    }
    * { box-sizing: border-box; }
    body { margin:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Inter,Arial,sans-serif;
      background:var(--bg); color:var(--ink); line-height:1.6; }
    .wrap { max-width:1080px; margin:0 auto; padding:2.5rem 1.25rem 4rem; }
    a { color:var(--accent); text-decoration:none; }
    a:hover { text-decoration:underline; }
    header { margin-bottom:1.25rem; }
    .kicker { font-size:.8rem; font-weight:600; letter-spacing:.12em; text-transform:uppercase; color:var(--accent); }
    h1 { font-size:clamp(1.7rem,4.5vw,2.5rem); margin:.3rem 0 .6rem; letter-spacing:-.02em; line-height:1.15; }
    header p.sub { margin:0; color:var(--muted); max-width:64ch; font-size:1.05rem; }
    .badges { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:1rem; }
    .badge { font-size:.8rem; font-weight:500; padding:.3rem .7rem; border-radius:999px;
      background:var(--card); border:1px solid var(--line); color:var(--muted); }
    .badge b { color:var(--ink); font-weight:600; }
    .badge.ok { border-color:transparent; background:var(--ok-soft); color:var(--ok); }
    section { margin-top:3rem; }
    h2 { font-size:1.25rem; margin:0 0 .35rem; letter-spacing:-.01em; }
    .lede { color:var(--muted); max-width:62ch; margin:0 0 1.25rem; }
    .diagram { background:var(--card); border:1px solid var(--line); border-radius:14px;
      padding:1rem 1.25rem; overflow-x:auto; }
    .diagram svg { display:block; width:100%; max-width:1100px; margin:0 auto; height:auto; }
    /* the SVG has its own light look; on dark, give it a light card so ink stays legible */
    @media (prefers-color-scheme: dark) { .diagram { background:#ffffff; } }
    .diagram-foot { display:flex; justify-content:space-between; align-items:center; gap:1rem;
      flex-wrap:wrap; margin-top:.9rem; }
    .diagram-foot .cap { color:var(--muted); font-size:.85rem; }
    .grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:1rem; }
    .card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:1.1rem 1.2rem; }
    .card .ic { font-size:1.25rem; line-height:1; }
    .card h3 { font-size:1rem; margin:.7rem 0 .35rem; }
    .card p { margin:0; color:var(--muted); font-size:.92rem; }
    .flow { list-style:none; margin:.25rem 0 0; padding:0; counter-reset:step; }
    .flow li { counter-increment:step; position:relative; padding:.5rem 0 .5rem 2.6rem;
      border-bottom:1px dashed var(--line); }
    .flow li:last-child { border-bottom:none; }
    .flow li::before { content:counter(step); position:absolute; left:0; top:.5rem;
      width:1.9rem; height:1.9rem; border-radius:50%; background:var(--accent-soft);
      color:var(--accent); font-weight:600; font-size:.85rem;
      display:flex; align-items:center; justify-content:center; }
    .principles { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:1rem; }
    .principle { background:var(--card); border-left:3px solid var(--accent); border-radius:0 10px 10px 0;
      padding:.85rem 1.1rem; }
    .principle b { display:block; margin-bottom:.2rem; }
    .principle span { color:var(--muted); font-size:.9rem; }
    footer { margin-top:3.5rem; padding-top:1.5rem; border-top:1px solid var(--line);
      color:var(--muted); font-size:.85rem; }
    footer .disclaimer { margin-top:.6rem; font-size:.8rem; }
    p.mono { font-family:var(--mono); font-size:.82rem; background:var(--card);
      border:1px solid var(--line); border-radius:8px; padding:.6rem .8rem; display:inline-block; }
  </style>
</head>
<body>
<div class="wrap">

  <header>
    <div class="kicker">Smartihats &middot; Home Automation</div>
    <h1>A smart home that keeps itself running</h1>
    <p class="sub">A self-maintaining automation stack: an autonomous SRE agent watches over the
      home, diagnoses trouble before it becomes an outage, and repairs it &mdash; with every AI
      model running locally on the home&rsquo;s own hardware.</p>
    <div class="badges">
      <span class="badge ok">Local-first &middot; no data leaves the home</span>
      <span class="badge"><b>1</b> SRE agent &middot; monitors &amp; repairs</span>
      <span class="badge"><b>1</b> gateway &middot; any model</span>
      <span class="badge"><b>3</b> model classes &middot; chat / vision / code</span>
    </div>
  </header>

  <section id="architecture">
    <h2>Architecture &amp; design</h2>
    <p class="lede">Everything runs in one place. The agent talks to a single model gateway, and
      that gateway is the only thing that ever reaches the models &mdash; so any model, from any
      provider, can be swapped in without rewiring the rest of the stack.</p>
    <div class="diagram">
    __SVG__
      <div class="diagram-foot">
        <span class="cap">Figure 1 &mdash; Control loop on the left, AI stack on the right. Solid = on the repair path; dashed = inference only.</span>
        <a href="/diagram/architecture.excalidraw" target="_blank" rel="noopener">Open the editable Excalidraw &nearr;</a>
      </div>
    </div>
  </section>

  <section id="how">
    <h2>How a repair actually happens</h2>
    <p class="lede">When something in the home misbehaves, the agent works a fixed, evidence-first loop:</p>
    <ol class="flow">
      <li><b>Detect.</b> A health signal &mdash; an integration down, a service error, a device that stops updating &mdash; raises an event.</li>
      <li><b>Diagnose.</b> The agent reads logs and system state before touching anything, and pinpoints the root cause.</li>
      <li><b>Repair with least disruption.</b> Reload a config before restarting a service; restart one container before the whole stack.</li>
      <li><b>Verify.</b> The fix isn&rsquo;t done until the affected pieces are observed actually working again.</li>
      <li><b>Notify &amp; remember.</b> A plain-language report reaches the household, and the lesson is recorded to avoid repeating it.</li>
    </ol>
  </section>

  <section id="capabilities">
    <h2>Capabilities</h2>
    <p class="lede">Four things the stack does, all behind the one gateway.</p>
    <div class="grid">
      <div class="card">
        <div class="ic">&#128295;</div>
        <h3>Monitoring &amp; repair</h3>
        <p>Continuously watches the smart home for failure and restores it with the least disruptive action, verifying each fix.</p>
      </div>
      <div class="card">
        <div class="ic">&#9881;</div>
        <h3>Model-agnostic gateway</h3>
        <p>One interface fronts every model. Swap models or providers without changing a line of the agent &mdash; cloud or local, local by default.</p>
      </div>
      <div class="card">
        <div class="ic">&#128065;</div>
        <h3>Local vision</h3>
        <p>Understands images by isolating objects from prompts &mdash; the kind of perception that lets a home see what it needs, on-site.</p>
      </div>
      <div class="card">
        <div class="ic">&#128187;</div>
        <h3>Autonomous coding</h3>
        <p>A CLI agent that writes and runs code for maintenance tasks, routed through the same gateway so it shares the same models and guardrails.</p>
      </div>
    </div>
  </section>

  <section id="principles">
    <h2>Design principles</h2>
    <p class="lede">The rules the whole system follows.</p>
    <div class="principles">
      <div class="principle"><b>Local-first</b><span>Inference stays on the home&rsquo;s hardware. No telemetry, no cloud dependency.</span></div>
      <div class="principle"><b>Evidence before action</b><span>Look before you leap: diagnose from logs and state, never guess at a fix.</span></div>
      <div class="principle"><b>Least disruptive recovery</b><span>The smallest safe change wins &mdash; a reload before a restart, one service before the whole stack.</span></div>
      <div class="principle"><b>Human-in-the-loop</b><span>Risky operations are surfaced for approval, and every significant change is reported in plain language.</span></div>
      <div class="principle"><b>Verify, then report</b><span>A repair only counts as done once the system is observed healthy again.</span></div>
      <div class="principle"><b>Leave it better</b><span>Each incident is a chance to harden the stack against the next one.</span></div>
    </div>
  </section>

  <footer>
    <p>Last updated: <time datetime="__ISO__">__TODAY__</time> &middot;
       Stack: Hermes SRE agent, Home Assistant, local model gateway, local open-weights models, and an autonomous coding agent.</p>
    <p class="disclaimer">Public summary. Hostnames, IP addresses, ports, file paths, hardware, model versions, and credentials are intentionally omitted.
    Component names refer to public, open-source projects and generic roles, not to any specific installation.</p>
  </footer>

</div>
</body>
</html>
"""

# embed SVG into the diagram card, then dates
HTML = HTML.replace('__SVG__', svg.replace('\n', '\n    '))
HTML = HTML.replace('__TODAY__', today).replace('__ISO__', iso)

out = os.path.join(HERE, "sre.html")
open(out, "w").write(HTML)
print("wrote", out, len(HTML), "bytes")
