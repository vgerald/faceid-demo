#!/usr/bin/env python3
"""Generate the SRE architecture diagram in two formats:
   1. hermes-sre.excalidraw  (editable Excalidraw JSON)
   2. diag.svg               (self-contained inline SVG for the page)
Same data structure drives both -> they stay consistent.
"""
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- palette (excalidraw skill colors) ----
C = dict(
    household="#a5d8ff", sre="#d0bfff", ha="#c3fae8", devices="#fff3bf",
    gateway="#ffd8a8", models="#b2f2bb", coder="#ffd8a8", note="#ffffff",
)
INK = "#1e1e1e"

# x, y, w, h   (canvas 1100 x 660)
BOXES = [
    # id,        color,        x,    y,    w,    h,   title,             subtitle
    ("household",C["household"],50,  250, 210, 100, "Household",        "phone alerts & approvals"),
    ("sre",      C["sre"],      340, 250, 290, 180, "Hermes SRE Agent", "monitors \u00b7 diagnoses \u00b7 repairs"),
    ("coder",    C["coder"],    790,  60, 250,  90, "Coding Assistant", "autonomous CLI agent"),
    ("gateway",  C["gateway"],  790, 195, 250, 120, "Model Gateway",    "one API for every model"),
    ("models",   C["models"],   790, 460, 250, 130, "Local Models",     "chat \u00b7 code \u00b7 vision \u00b7 memory"),
    ("ha",       C["ha"],       50,  470, 210, 100, "Smart Home Hub",   "Home Assistant"),
    ("devices",  C["devices"],  340, 470, 290, 100, "Cameras & Sensors","lights \u00b7 locks \u00b7 presence"),
]

ARROWS = [
    # id,  x1,   y1,   x2,   y2,   label, style
    ("a1", 260,  300,  340,  300, "instructions \u2194 alerts", None),   # household -> sre
    ("a2", 485,  430,  485,  470, "inspect \u00b7 repair \u00b7 reports", None),  # sre -> devices
    ("a6", 340,  400,  180,  470, "state & alarms", None),             # sre -> ha (diagonal, empty corridor)
    ("a3", 630,  300,  790,  300, "prompts", "dashed"),                # sre -> gateway
    ("a4", 915,  150,  915, 195, "requests", "dashed"),                # coder -> gateway (vertical)
    ("a5", 915,  315,  915, 460, "routes by task", None),              # gateway -> models (vertical)
]

def excalidraw_elements():
    els = []
    # title (standalone text, centered)
    title = "Self-maintaining Smart Home \u2014 Architecture"
    els.append(dict(type="text", id="title", x=330, y=20, width=440, height=30,
                    text=title, fontSize=24, fontFamily=1, strokeColor=INK,
                    originalText=title, autoResize=True))
    # caption note under models
    note = "all inference on-prem \u2014 data never leaves the home"
    els.append(dict(type="text", id="note", x=770, y=608, width=300, height=20,
                    text=note, fontSize=16, fontFamily=1, strokeColor="#5b6575",
                    originalText=note, autoResize=True, textAlign="center"))
    for (bid, color, x, y, w, h, t, sub) in BOXES:
        tid = "t_" + bid
        main = f"{t}\n{sub}" if sub else t
        els.append(dict(type="rectangle", id=bid, x=x, y=y, width=w, height=h,
                        roundness={"type": 3}, backgroundColor=color, fillStyle="solid",
                        strokeWidth=2, opacity=100, strokeColor=INK,
                        boundElements=[{"id": tid, "type": "text"}]))
        els.append(dict(type="text", id=tid, x=x+10, y=y+10, width=w-20,
                        height=h-20, text=main, fontSize=18, fontFamily=1,
                        strokeColor=INK, textAlign="center", verticalAlign="middle",
                        containerId=bid, originalText=main, autoResize=True))
    for (aid, x1, y1, x2, y2, label, style) in ARROWS:
        tid = "t_" + aid
        dx, dy = x2-x1, y2-y1
        els.append(dict(type="arrow", id=aid, x=x1, y=y1, width=abs(dx), height=abs(dy),
                        points=[[0,0],[dx,dy]], endArrowhead="arrow", strokeColor=INK,
                        strokeStyle=style or "solid",
                        boundElements=(dict(id=tid, type="text") and [{"id": tid, "type": "text"}]) if label else None))
        if label:
            els.append(dict(type="text", id=tid, x=(x1+x2)/2-60, y=(y1+y2)/2-22,
                            width=120, height=20, text=label, fontSize=14, fontFamily=1,
                            strokeColor=INK, textAlign="center", verticalAlign="middle",
                            containerId=aid, originalText=label, autoResize=True))
    # cleanup: drop None boundElements
    for e in els:
        e["boundElements"] = e.get("boundElements") or []
        e.setdefault("opacity", 100)
        e.setdefault("strokeWidth", 2 if e["type"]!="text" else 0)
        e.setdefault("fillStyle", "solid") if e["type"] in ("rectangle","arrow") else None
    return els

def svg():
    S = []
    S.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 660" '
             'role="img" aria-label="Architecture diagram of a self-maintaining smart home" '
             'style="font-family:Segoe Print, Comic Sans MS, cursive, sans-serif">')
    S.append('<defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="3" '
             'orient="auto" markerUnits="strokeWidth"><path d="M0,0 L9,3 L0,6 Z" fill="#1e1e1e"/></marker></defs>')
    # hand-drawn helpers: slight rotation per box, wobbly underline for title
    S.append('<text x="550" y="42" text-anchor="middle" font-size="26" fill="#1e1e1e" '
             'transform="rotate(-0.5 550 42)">Self-maintaining Smart Home \u2014 Architecture</text>')
    S.append('<path d="M330,58 Q450,52 700,60" stroke="#1e1e1e" stroke-width="2" fill="none" '
             'stroke-linecap="round"/>')
    for (bid, color, x, y, w, h, t, sub) in BOXES:
        rot = {"sre":-0.4,"models":0.5,"ha":0.3,"gateway":-0.5,"coder":0.4,"household":0.3,"devices":-0.3}.get(bid, 0)
        S.append(f'<g transform="rotate({rot} {x+w/2} {y+h/2})">')
        S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{color}" '
                 f'stroke="#1e1e1e" stroke-width="2.5" stroke-linejoin="round"/>')
        cy = y + h/2
        if sub:
            S.append(f'<text x="{x+w/2}" y="{cy-4}" text-anchor="middle" font-size="19" '
                     f'fill="#1e1e1e" font-weight="bold">{t}</text>')
            S.append(f'<text x="{x+w/2}" y="{cy+20}" text-anchor="middle" font-size="14" '
                     f'fill="#444a55">{sub}</text>')
        else:
            S.append(f'<text x="{x+w/2}" y="{cy+6}" text-anchor="middle" font-size="19" '
                     f'fill="#1e1e1e" font-weight="bold">{t}</text>')
        S.append('</g>')
    for (aid, x1, y1, x2, y2, label, style) in ARROWS:
        dash = ' stroke-dasharray="7 6"' if style == "dashed" else ""
        # slight curve for organic feel
        bend = 10 if (x1==x2) else -10
        cx, cy2 = ((x1+x2)/2+bend, (y1+y2)/2) if (x1==x2) else ((x1+x2)/2, (y1+y2)/2+bend)
        S.append(f'<path d="M{x1},{y1} Q{cx},{cy2} {x2},{y2}" fill="none" stroke="#1e1e1e" '
                 f'stroke-width="2.5" stroke-linecap="round"{dash} marker-end="url(#ar)"/>')
        if label:
            # keep labels on canvas (a6 diagonal sits near left edge)
            lx = max(20, min(1080, 0.25*(x1+2*cx+x2)))
            ly = max(70, min(575, 0.25*(y1+2*cy2+y2) - 8))
            S.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="middle" font-size="13" fill="#39404c">{label}</text>')
    S.append('<text x="915" y="626" text-anchor="middle" font-size="14" fill="#5b6575">'
             'all inference on-prem \u2014 data never leaves the home</text>')
    S.append('</svg>')
    return "\n".join(S)

if __name__ == "__main__":
    env = dict(type="excalidraw", version=2, source="hermes-agent",
               elements=excalidraw_elements(), appState=dict(viewBackgroundColor="#ffffff"),
               files={})
    with open(os.path.join(OUT, "hermes-sre.excalidraw"), "w") as f:
        json.dump(env, f, indent=2)
    with open(os.path.join(OUT, "diag.svg"), "w") as f:
        f.write(svg())
    print("wrote hermes-sre.excalidraw + diag.svg in", OUT)
