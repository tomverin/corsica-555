#!/usr/bin/env python3
"""Build a self-contained interactive HTML page for the Corsica 555 race.

Pipeline overview
-----------------

1. Source inputs (under corsica-555-2026/):
   - `555_Corsica__2_2026_vfinale.gpx` — official race track + 2 CP waypoints
   - `555-gravel-poi.gpx` — 172 POIs along the route (from onroutemap.de)
   - `terrain_analysis.raw.json` — output of `analyze_gpx_osm_surface.py`
   - 7 markdown docs (terrain_analysis, tyre-selection-alt, refueling_strategy,
     checklist, personal-checklist, briefing-summary, roadbook)

2. This script:
   - Parses the track GPX (~19k points) and downsamples to ~3k points.
   - Parses the POI GPX, filters to POIs within 200 m of the route.
   - Loads the terrain JSON (climbs, descents, aero, surface sections).
   - Computes pass-through clock times at each km (grade × surface speed model
     calibrated for the 30 h target with no scheduled sleep).
   - Embeds everything (route geometry, POIs, terrain analysis, markdown
     content) into a single self-contained HTML page (~430 KB).
   - Renders Markdown via marked.js (CDN) inside a sidebar+viewer panel.

3. Output: `corsica-555-2026/site/index.html` (open directly in any browser,
   no server required).

External dependencies (loaded from CDN at runtime, no install needed):
- Leaflet 1.9.4 + Leaflet.markercluster 1.5.3 — map and clustering
- marked 12.0 — markdown rendering

To deploy the result publicly to https://tomverin.github.io/corsica-555/
use `scripts/deploy_corsica_site.sh` which builds, syncs to the public
repo, commits, and pushes.
"""

from __future__ import annotations

import json
import math
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORSICA = ROOT / "corsica-555-2026"
TRACK_GPX = CORSICA / "555_Corsica__2_2026_vfinale.gpx"
POI_GPX = CORSICA / "555-gravel-poi.gpx"
TERRAIN_JSON = CORSICA / "terrain_analysis.raw.json"
OUT_HTML = CORSICA / "site" / "index.html"

DOCS = [
    ("terrain_analysis.md", "Terrain analysis",
     "Profile, climbs, descents, aero, surface, race-defining sequences, risk sectors."),
    ("tyre-selection-alt.md", "Tyre selection",
     "Race King 2.2 vs G-One RS — alternative analysis with the athlete's priority framing."),
    ("refueling_strategy.md", "Refueling strategy",
     "Water + solid food + caffeine plan for the 30 h target with no scheduled sleep."),
    ("checklist.md", "Race checklist",
     "Full pre-race and in-race checklist (admin, gear, tactical km-by-km)."),
    ("personal-checklist.md", "Personal checklist",
     "Per-location packing (on body, bike, top tube, frame bag, saddle bag)."),
    ("briefing-summary.md", "Briefing summary",
     "Synthesis of the official BikingMan briefing."),
    ("roadbook.md", "Roadbook",
     "Compact roadbook for race-day reference."),
]

NS = "{http://www.topografix.com/GPX/1/1}"
RACE_START = datetime(2026, 5, 29, 7, 0)


def haversine_m(la1: float, lo1: float, la2: float, lo2: float) -> float:
    R = 6_371_000.0
    p1, p2 = math.radians(la1), math.radians(la2)
    dp = math.radians(la2 - la1)
    dl = math.radians(lo2 - lo1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def parse_track(path: Path) -> list[dict]:
    root = ET.parse(path).getroot()
    pts: list[dict] = []
    cum = 0.0
    prev = None
    for tp in root.iter(f"{NS}trkpt"):
        lat = float(tp.attrib["lat"])
        lon = float(tp.attrib["lon"])
        ele_el = tp.find(f"{NS}ele")
        ele = float(ele_el.text) if ele_el is not None and ele_el.text else 0.0
        if prev is not None:
            cum += haversine_m(prev[0], prev[1], lat, lon)
        pts.append({"lat": lat, "lon": lon, "ele": ele, "km": cum / 1000})
        prev = (lat, lon)
    return pts


def downsample(pts: list[dict], target: int = 2500) -> list[dict]:
    if len(pts) <= target:
        return pts
    step = max(1, len(pts) // target)
    out = [pts[i] for i in range(0, len(pts), step)]
    if out[-1] is not pts[-1]:
        out.append(pts[-1])
    return out


def parse_pois(path: Path) -> list[dict]:
    root = ET.parse(path).getroot()
    pois: list[dict] = []
    for w in root.iter(f"{NS}wpt"):
        name_el = w.find(f"{NS}name")
        type_el = w.find(f"{NS}type")
        desc_el = w.find(f"{NS}desc")
        km, dist_m = None, None
        if desc_el is not None and desc_el.text:
            m = re.search(r"Route kilometer:\s*([\d.]+)", desc_el.text)
            if m:
                km = float(m.group(1))
            m = re.search(r"Distance to route:\s*(\d+)", desc_el.text)
            if m:
                dist_m = int(m.group(1))
        pois.append(
            {
                "lat": float(w.attrib["lat"]),
                "lon": float(w.attrib["lon"]),
                "name": (name_el.text or "").strip() if name_el is not None else "",
                "type": (type_el.text or "").strip() if type_el is not None else "",
                "km": km,
                "dist_m": dist_m,
            }
        )
    return [p for p in pois if p["km"] is not None and (p["dist_m"] is None or p["dist_m"] <= 200)]


def grade_speed(grade_pct: float, offroad: bool) -> float:
    """Same model as the refueling strategy (Race King, ~30 h target)."""
    g = grade_pct
    if offroad:
        if g >= 6: return 7.0
        if g >= 3: return 10.0
        if g >= 1: return 14.0
        if g >= -1: return 18.0
        return 22.0
    if g >= 6: return 9.0
    if g >= 3: return 13.0
    if g >= 1: return 19.0
    if g >= -1: return 24.0
    if g >= -3: return 29.0
    if g >= -6: return 33.0
    return 36.0


def compute_passage_times(track: list[dict], sections: list[dict]) -> list[float]:
    """Cumulative moving hours at each track point given grade + surface."""
    n = len(track)
    if n < 2:
        return [0.0] * n

    def is_offroad(km: float) -> bool:
        for s in sections:
            if s["start_km"] <= km <= s["end_km"]:
                return True
        return False

    # Precompute smoothed grades over ~300 m windows
    grades = [0.0] * n
    for i in range(n):
        a, b = i, i
        while a > 0 and (track[i]["km"] - track[a]["km"]) * 1000 < 150:
            a -= 1
        while b < n - 1 and (track[b]["km"] - track[i]["km"]) * 1000 < 150:
            b += 1
        dx = (track[b]["km"] - track[a]["km"]) * 1000
        if dx > 1:
            grades[i] = (track[b]["ele"] - track[a]["ele"]) / dx * 100
    times = [0.0]
    for i in range(1, n):
        seg_km = track[i]["km"] - track[i - 1]["km"]
        speed = grade_speed(grades[i], is_offroad(track[i]["km"]))
        times.append(times[-1] + (seg_km / speed if speed > 0 else 0))
    return times


def time_at_km(km: float, track: list[dict], times: list[float]) -> float:
    """Linear interpolation of cumulative moving time at a given km."""
    if not track:
        return 0.0
    for i in range(1, len(track)):
        if track[i]["km"] >= km:
            t0 = track[i - 1]["km"]
            t1 = track[i]["km"]
            if t1 == t0:
                return times[i]
            ratio = (km - t0) / (t1 - t0)
            return times[i - 1] + ratio * (times[i] - times[i - 1])
    return times[-1]


def planned_stops_at_km(km: float) -> float:
    """30 h-target lean schedule (no sleep) — small stops only."""
    stops = [
        (60, 0.10),
        (110, 0.15),
        (164, 0.30),  # CP1
        (200, 0.05),
        (333, 0.30),  # CP2
        (385, 0.15),
        (433, 0.20),  # last fuel before Sequence C
    ]
    return sum(dt for k, dt in stops if km >= k)


def clock_at_km(km: float, track: list[dict], times: list[float]) -> str:
    moving = time_at_km(km, track, times)
    stops = planned_stops_at_km(km)
    when = RACE_START + timedelta(hours=moving + stops)
    return when.strftime("%a %H:%M")


def categorize_poi(t: str) -> str:
    if t in {"Bakery", "Supermarket", "Convenience Store", "Fast Food", "Café", "Ice Cream Parlor", "Kiosk"}:
        return "FOOD"
    if t == "Drinking Water":
        return "WATER"
    if t == "Gas Station":
        return "GAS"
    return "MISC"


HTML_TEMPLATE = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Corsica 555 — 29 May 2026</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
      integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css" />
<script src="https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js"></script>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.0/marked.min.js"></script>
<style>
:root {
  --bg: #0d1117;
  --panel: #161b22;
  --panel2: #1f262e;
  --text: #e6edf3;
  --muted: #8b949e;
  --accent: #f0883e;
  --green: #56d364;
  --red: #f85149;
  --orange: #d29922;
  --blue: #58a6ff;
  --border: #30363d;
}
* { box-sizing: border-box }
body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
       background: var(--bg); color: var(--text); }
header { padding: 16px 24px; background: var(--panel); border-bottom: 1px solid var(--border); }
header h1 { margin: 0 0 8px 0; font-size: 22px; }
header .meta { color: var(--muted); font-size: 13px; }
.stats { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; }
.stat { background: var(--panel2); padding: 8px 14px; border-radius: 6px; }
.stat .v { font-size: 18px; font-weight: 600; }
.stat .l { color: var(--muted); font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }
nav.tabs { display: flex; gap: 4px; padding: 0 24px; background: var(--panel); border-bottom: 1px solid var(--border); overflow-x: auto; }
nav.tabs button { background: none; border: none; color: var(--muted); padding: 12px 16px; font-size: 14px; cursor: pointer; border-bottom: 2px solid transparent; }
nav.tabs button:hover { color: var(--text); }
nav.tabs button.active { color: var(--accent); border-bottom-color: var(--accent); }
section.tab { display: none; padding: 16px 24px; }
section.tab.active { display: block; }
#leaflet-map { height: 55vh; min-height: 360px; border-radius: 6px; border: 1px solid var(--border); }
.map-legend { margin-top: 12px; display: flex; gap: 16px; flex-wrap: wrap; font-size: 13px; color: var(--muted); }
.map-legend span { display: inline-flex; align-items: center; gap: 6px; }
.map-legend .swatch { width: 12px; height: 12px; border-radius: 2px; display: inline-block; }
#profile-wrap { background: var(--panel); border: 1px solid var(--border); border-radius: 6px; padding: 16px; }
#profile-chart { width: 100%; height: 360px; display: block; }
#profile-tooltip { position: absolute; pointer-events: none; background: rgba(0,0,0,0.85); color: white; padding: 8px 12px; border-radius: 4px; font-size: 12px; display: none; z-index: 10; max-width: 240px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
table th, table td { padding: 8px 10px; text-align: left; border-bottom: 1px solid var(--border); }
table th { background: var(--panel2); color: var(--muted); font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; position: sticky; top: 0; }
table tr:hover { background: var(--panel2); }
.unpaved { color: var(--red); font-weight: 600; }
.partial { color: var(--orange); }
.likely-paved { color: var(--green); }
.brief-rough { color: var(--muted); }
.tabs-mini { display: flex; gap: 4px; margin-bottom: 12px; }
.tabs-mini button { background: var(--panel2); border: 1px solid var(--border); color: var(--text); padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; }
.tabs-mini button.active { background: var(--accent); border-color: var(--accent); color: var(--bg); }
.scrollable { max-height: 70vh; overflow-y: auto; border: 1px solid var(--border); border-radius: 6px; }
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin: 16px 0; }
.kpi { background: var(--panel); border: 1px solid var(--border); border-radius: 6px; padding: 12px 16px; }
.kpi .l { color: var(--muted); font-size: 11px; text-transform: uppercase; }
.kpi .v { font-size: 20px; font-weight: 600; margin-top: 4px; }
.kpi .s { color: var(--muted); font-size: 11px; margin-top: 4px; }
.risk-sector { background: var(--panel); border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 6px; padding: 14px 18px; margin-bottom: 12px; }
.risk-sector h4 { margin: 0 0 8px 0; font-size: 15px; }
.risk-sector .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 13px; }
.risk-sector .grid .label { color: var(--muted); }
.docs-list a { display: block; padding: 12px 16px; background: var(--panel); border: 1px solid var(--border); border-radius: 6px; color: var(--text); text-decoration: none; margin-bottom: 8px; }
.docs-list a:hover { border-color: var(--accent); }
.docs-list .desc { color: var(--muted); font-size: 12px; margin-top: 4px; }
.docs-layout { display: grid; grid-template-columns: 280px 1fr; gap: 16px; height: calc(100vh - 200px); min-height: 600px; }
.docs-sidebar { background: var(--panel); border: 1px solid var(--border); border-radius: 6px; overflow-y: auto; padding: 8px; }
.docs-sidebar .doc-link { display: block; padding: 10px 12px; border-radius: 4px; color: var(--text); text-decoration: none; cursor: pointer; margin-bottom: 4px; border: 1px solid transparent; }
.docs-sidebar .doc-link:hover { background: var(--panel2); border-color: var(--border); }
.docs-sidebar .doc-link.active { background: var(--panel2); border-color: var(--accent); }
.docs-sidebar .doc-link .title { font-size: 13px; font-weight: 600; }
.docs-sidebar .doc-link .desc { color: var(--muted); font-size: 11px; margin-top: 2px; }
.docs-viewer { background: var(--panel); border: 1px solid var(--border); border-radius: 6px; overflow-y: auto; padding: 24px 32px; }
.docs-viewer .viewer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 1px solid var(--border); }
.docs-viewer .viewer-header h2 { margin: 0; font-size: 16px; color: var(--muted); font-weight: 400; }
.docs-viewer .viewer-header a { color: var(--blue); text-decoration: none; font-size: 12px; }
.docs-viewer .viewer-header a:hover { text-decoration: underline; }
.md-content { font-size: 14px; line-height: 1.6; color: var(--text); }
.md-content h1 { font-size: 24px; border-bottom: 1px solid var(--border); padding-bottom: 8px; margin-top: 0; }
.md-content h2 { font-size: 18px; margin-top: 28px; border-bottom: 1px solid var(--border); padding-bottom: 4px; }
.md-content h3 { font-size: 16px; margin-top: 22px; color: var(--accent); }
.md-content h4 { font-size: 14px; margin-top: 18px; color: var(--orange); }
.md-content p { margin: 12px 0; }
.md-content ul, .md-content ol { padding-left: 24px; }
.md-content li { margin: 4px 0; }
.md-content code { background: var(--panel2); padding: 2px 6px; border-radius: 3px; font-size: 12px; font-family: SF Mono, Menlo, Consolas, monospace; }
.md-content pre { background: var(--panel2); border: 1px solid var(--border); border-radius: 4px; padding: 12px 16px; overflow-x: auto; }
.md-content pre code { background: none; padding: 0; }
.md-content blockquote { border-left: 4px solid var(--accent); margin: 12px 0; padding: 4px 16px; color: var(--muted); }
.md-content table { font-size: 12px; margin: 12px 0; }
.md-content table th { background: var(--panel2); }
.md-content a { color: var(--blue); text-decoration: none; }
.md-content a:hover { text-decoration: underline; }
.md-content strong { color: var(--accent); }
.md-content hr { border: none; border-top: 1px solid var(--border); margin: 24px 0; }
@media (max-width: 800px) { .docs-layout { grid-template-columns: 1fr; height: auto; } .docs-sidebar { max-height: 200px; } }
.filter-bar { display: flex; gap: 8px; margin-bottom: 12px; flex-wrap: wrap; }
.filter-bar input, .filter-bar select { background: var(--panel2); border: 1px solid var(--border); color: var(--text); padding: 6px 10px; border-radius: 4px; font-size: 13px; }
.badge { display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 11px; font-weight: 600; }
.badge.food { background: rgba(240, 136, 62, 0.2); color: var(--accent); }
.badge.water { background: rgba(88, 166, 255, 0.2); color: var(--blue); }
.badge.gas { background: rgba(86, 211, 100, 0.2); color: var(--green); }
.badge.misc { background: rgba(139, 148, 158, 0.2); color: var(--muted); }
.cp-marker { background: var(--accent); color: var(--bg); border-radius: 50%; width: 28px; height: 28px; line-height: 28px; text-align: center; font-weight: 700; font-size: 12px; box-shadow: 0 0 0 2px var(--bg); }
.poi-icon { background: none !important; border: none !important; }
.poi-icon-inner {
  width: 26px; height: 26px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; line-height: 1;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(0,0,0,0.4);
  transition: transform 0.1s ease;
}
.poi-icon:hover .poi-icon-inner { transform: scale(1.18); }
.poi-icon-inner.water { background: #58a6ff; }
.poi-icon-inner.food { background: #f0883e; }
.poi-icon-inner.gas { background: #56d364; }
.poi-icon-inner.misc { background: #8b949e; }
/* Marker clusters — match the dark theme */
.marker-cluster-small { background: rgba(86, 211, 100, 0.4); }
.marker-cluster-small div { background: rgba(86, 211, 100, 0.8); color: white; }
.marker-cluster-medium { background: rgba(240, 136, 62, 0.4); }
.marker-cluster-medium div { background: rgba(240, 136, 62, 0.8); color: white; }
.marker-cluster-large { background: rgba(248, 81, 73, 0.4); }
.marker-cluster-large div { background: rgba(248, 81, 73, 0.85); color: white; }
.marker-cluster div { font-weight: 600; }
.position-marker { background: none !important; border: none !important; }
.position-marker-inner {
  width: 20px; height: 20px; border-radius: 50%;
  background: white;
  border: 3px solid #f0883e;
  box-shadow: 0 0 0 2px rgba(13, 17, 23, 0.5), 0 0 16px rgba(240, 136, 62, 0.85);
}
/* Position info panel + slider */
.position-bar {
  background: var(--panel); border: 1px solid var(--border); border-radius: 6px;
  padding: 12px 16px; margin-top: 12px;
  display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 12px;
  align-items: center;
}
.position-bar .item .l { color: var(--muted); font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }
.position-bar .item .v { font-size: 14px; font-weight: 600; margin-top: 2px; }
.position-bar .item.poi .v { font-size: 12px; font-weight: 400; color: var(--blue); }
.position-bar .item.surface .v.unpaved { color: #f85149; }
.position-bar .item.surface .v.suspect { color: #d29922; }
.position-bar .item.surface .v.paved { color: #56d364; }
.slider-wrap {
  background: var(--panel); border: 1px solid var(--border); border-radius: 6px;
  padding: 16px 20px; margin-top: 8px;
}
.slider-wrap .slider-label { display: flex; justify-content: space-between; color: var(--muted); font-size: 11px; margin-bottom: 8px; }
.slider-wrap input[type=range] {
  -webkit-appearance: none; width: 100%; height: 6px; border-radius: 3px;
  background: var(--panel2); outline: none;
}
.slider-wrap input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none; appearance: none; width: 22px; height: 22px;
  border-radius: 50%; background: var(--accent); cursor: grab;
  border: 2px solid white; box-shadow: 0 0 8px rgba(240,136,62,0.6);
}
.slider-wrap input[type=range]::-moz-range-thumb {
  width: 22px; height: 22px; border-radius: 50%; background: var(--accent);
  cursor: grab; border: 2px solid white; box-shadow: 0 0 8px rgba(240,136,62,0.6);
}
.slider-wrap input[type=range]:active::-webkit-slider-thumb { cursor: grabbing; }
.slider-buttons { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
.slider-buttons button {
  background: var(--panel2); border: 1px solid var(--border); color: var(--text);
  padding: 4px 10px; border-radius: 4px; cursor: pointer; font-size: 11px;
}
.slider-buttons button:hover { border-color: var(--accent); }
</style>
</head>
<body>
<header>
  <h1>Corsica 555 Gravel — 29 May 2026</h1>
  <div class="meta">Camping Îlots d'Or → San Damiano · Friday 07:00 → Saturday ~13:00 (target 30 h) · Solo · Race King 2.2 · No aerobars</div>
  <div class="stats">__STATS__</div>
</header>
<nav class="tabs">
  <button class="active" data-tab="overview">Carte + Profil</button>
  <button data-tab="climbs">Climbs</button>
  <button data-tab="descents">Descents</button>
  <button data-tab="aero">Aero</button>
  <button data-tab="unpaved">Off-road</button>
  <button data-tab="risks">Risk Sectors</button>
  <button data-tab="pois">POI / Fueling</button>
  <button data-tab="docs">Documents</button>
</nav>
<section class="tab active" id="tab-overview">
  <div id="leaflet-map"></div>
  <div class="map-legend">
    <span><span class="swatch" style="background:#56d364"></span> Paved (confirmed or likely)</span>
    <span><span class="swatch" style="background:#f85149"></span> Confirmed unpaved</span>
    <span><span class="swatch" style="background:#d29922"></span> Suspect (track/path, no surface tag)</span>
    <span><span class="swatch" style="background:var(--accent);border-radius:50%"></span> Checkpoint (1/2)</span>
    <span>💧 Water · 🥖 Bakery · 🛒 Supermarket · 🏪 Store · 🍔 Fast food · ☕ Café · 🍦 Ice cream · 🎪 Kiosk · ⛽ Gas · 🚻 Toilets</span>
  </div>
  <div id="profile-wrap" style="position: relative; margin-top: 16px;">
    <svg id="profile-chart" preserveAspectRatio="none"></svg>
    <div id="profile-tooltip"></div>
  </div>
  <div class="position-bar">
    <div class="item"><div class="l">Position</div><div class="v" id="info-km">0.0 km</div></div>
    <div class="item"><div class="l">Altitude</div><div class="v" id="info-alt">0 m</div></div>
    <div class="item surface"><div class="l">Surface</div><div class="v paved" id="info-surface">paved</div></div>
    <div class="item"><div class="l">Heure projetée</div><div class="v" id="info-clock">Fri 07:00</div></div>
    <div class="item poi"><div class="l">POI le plus proche</div><div class="v" id="info-poi">—</div></div>
  </div>
  <div class="slider-wrap">
    <div class="slider-label"><span>km 0 — Porto-Vecchio</span><span>km 487 — Biguglia</span></div>
    <input type="range" id="profile-slider" min="0" max="487" step="0.2" value="0" />
    <div class="slider-buttons">
      <button data-km="0">🏁 Start</button>
      <button data-km="164">CP1 Ghisoni</button>
      <button data-km="174">High point (1 291 m)</button>
      <button data-km="251">Climb 1 066 m</button>
      <button data-km="333">CP2 Crocicchia</button>
      <button data-km="378">Bakery breakfast</button>
      <button data-km="433">Last fuel pre-Seq C</button>
      <button data-km="440">Sequence C start</button>
      <button data-km="455">Sequence C end</button>
      <button data-km="487">🏁 Finish</button>
    </div>
  </div>
</section>
<section class="tab" id="tab-climbs">
  <div class="kpi-grid">__CLIMB_KPIS__</div>
  <div class="scrollable">
    <table>
      <thead><tr><th>Km</th><th>Length</th><th>Gain</th><th>Avg grade</th><th>Top alt</th><th>Surface</th></tr></thead>
      <tbody>__CLIMBS_ROWS__</tbody>
    </table>
  </div>
</section>
<section class="tab" id="tab-descents">
  <div class="kpi-grid">__DESCENT_KPIS__</div>
  <div class="scrollable">
    <table>
      <thead><tr><th>Km</th><th>Length</th><th>Loss</th><th>Avg grade</th><th>Bottom alt</th><th>Surface</th></tr></thead>
      <tbody>__DESCENTS_ROWS__</tbody>
    </table>
  </div>
</section>
<section class="tab" id="tab-aero">
  <p style="color: var(--muted)">Aero-eligible sections at default thresholds (|grade| ≤ 1.5 %, length ≥ 3 km). Cross-referenced with surface.</p>
  <table>
    <thead><tr><th>Km</th><th>Length</th><th>Avg grade</th><th>Start alt</th><th>End alt</th><th>Surface</th></tr></thead>
    <tbody>__AERO_ROWS__</tbody>
  </table>
</section>
<section class="tab" id="tab-unpaved">
  <p style="color: var(--muted)">All non-paved or suspect sectors ≥ 1.5 km. Confirmed unpaved (red) is where OSM has explicit surface=gravel/dirt/etc. Suspect (orange) is highway=track/path without explicit surface tag.</p>
  <div class="scrollable">
    <table>
      <thead><tr><th>Km</th><th>Length</th><th>Avg grade</th><th>Gain</th><th>Loss</th><th>Main highway</th><th>Surface</th></tr></thead>
      <tbody>__UNPAVED_ROWS__</tbody>
    </table>
  </div>
</section>
<section class="tab" id="tab-risks">
  <p style="color: var(--muted)">Eight terrain-risk sectors where multiple stress factors stack. Order is by km, not by risk.</p>
  __RISK_SECTORS__
</section>
<section class="tab" id="tab-pois">
  <div class="filter-bar">
    <input id="poi-filter" placeholder="Filtrer par nom ou type..." />
    <select id="poi-cat">
      <option value="">Toutes catégories</option>
      <option value="FOOD">Food / shop</option>
      <option value="WATER">Drinking water</option>
      <option value="GAS">Gas station</option>
      <option value="MISC">Autres</option>
    </select>
    <select id="poi-km">
      <option value="">Tout le parcours</option>
      <option value="0,100">km 0-100</option>
      <option value="100,200">km 100-200</option>
      <option value="200,300">km 200-300</option>
      <option value="300,400">km 300-400</option>
      <option value="400,488">km 400-fin</option>
    </select>
  </div>
  <p style="color: var(--muted); font-size: 12px">Heures de passage projetées en mode 30h sans pause sommeil (Friday 7:00 start, ~26.7 h moving + ~1.5 h stops).</p>
  <div class="scrollable">
    <table>
      <thead><tr><th>Km</th><th>Heure</th><th>Catégorie</th><th>Type</th><th>Nom</th><th>Offset</th></tr></thead>
      <tbody id="poi-tbody"></tbody>
    </table>
  </div>
</section>
<section class="tab" id="tab-docs">
  <div class="docs-layout">
    <aside class="docs-sidebar" id="docs-sidebar">__DOCS_SIDEBAR__</aside>
    <div class="docs-viewer">
      <div class="viewer-header">
        <h2 id="viewer-title">Select a document</h2>
        <a id="viewer-raw" href="#" target="_blank" style="display:none">Open raw .md ↗</a>
      </div>
      <div class="md-content" id="viewer-body">
        <p style="color: var(--muted)">Choose a document from the sidebar to view it here. Rendered with marked.js. Internal links between docs are intercepted for in-page navigation.</p>
      </div>
    </div>
  </div>
</section>
<script>
const DATA = __DATA_JSON__;

// --- Tab handling
document.querySelectorAll('nav.tabs button').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('nav.tabs button').forEach(b => b.classList.toggle('active', b === btn));
    document.querySelectorAll('section.tab').forEach(s => s.classList.toggle('active', s.id === 'tab-' + btn.dataset.tab));
    if (btn.dataset.tab === 'overview') { setTimeout(() => map.invalidateSize(), 50); drawProfile(); }
  });
});

// --- Map
const trackLatLngs = DATA.track.map(p => [p.lat, p.lon]);
const map = L.map('leaflet-map').setView([42.2, 9.2], 9);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '© OpenStreetMap'
}).addTo(map);

// Build colored polyline segments based on surface class along the route.
function classAtKm(km) {
  for (const s of DATA.unpaved_sections) {
    if (km >= s.start_km && km <= s.end_km) {
      // Use the "classes" field if present to disambiguate confirmed vs suspect
      const total = (s.classes && Object.values(s.classes).reduce((a,b)=>a+b,0)) || 0;
      const unp = (s.classes && s.classes.unpaved) || 0;
      return unp > total * 0.5 ? 'unpaved' : 'suspect';
    }
  }
  return 'paved';
}
function colorFor(klass) {
  if (klass === 'unpaved') return '#f85149';
  if (klass === 'suspect') return '#d29922';
  return '#56d364';
}
let currentSegmentClass = null;
let segmentBuffer = [];
const trackLines = [];
for (const p of DATA.track) {
  const k = classAtKm(p.km);
  if (k !== currentSegmentClass) {
    if (segmentBuffer.length > 1) {
      trackLines.push(L.polyline(segmentBuffer, { color: colorFor(currentSegmentClass), weight: 4, opacity: 0.85 }).addTo(map));
    }
    segmentBuffer = segmentBuffer.length ? [segmentBuffer[segmentBuffer.length - 1]] : [];
    currentSegmentClass = k;
  }
  segmentBuffer.push([p.lat, p.lon]);
}
if (segmentBuffer.length > 1) {
  trackLines.push(L.polyline(segmentBuffer, { color: colorFor(currentSegmentClass), weight: 4, opacity: 0.85 }).addTo(map));
}
map.fitBounds(L.latLngBounds(trackLatLngs));

// Checkpoints
for (const wpt of DATA.waypoints) {
  const icon = L.divIcon({ className: 'cp-marker', html: wpt.name.startsWith('CP1') ? '1' : '2', iconSize: [28, 28] });
  L.marker([wpt.lat, wpt.lon], { icon }).bindPopup(
    `<b>${wpt.name}</b><br>km ${wpt.km.toFixed(1)} — alt ${Math.round(wpt.nearest_alt_m)} m`
  ).addTo(map);
}

// POIs — type-specific emoji icons inside colored circles, marker clustered.
function categorizePoi(t) {
  if (['Bakery','Supermarket','Convenience Store','Fast Food','Café','Ice Cream Parlor','Kiosk'].includes(t)) return 'FOOD';
  if (t === 'Drinking Water') return 'WATER';
  if (t === 'Gas Station') return 'GAS';
  return 'MISC';
}
const POI_EMOJI = {
  'Bakery': '🥖',
  'Supermarket': '🛒',
  'Convenience Store': '🏪',
  'Fast Food': '🍔',
  'Café': '☕',
  'Ice Cream Parlor': '🍦',
  'Kiosk': '🎪',
  'Drinking Water': '💧',
  'Gas Station': '⛽',
  'Toilets': '🚻',
  'Other': '📍',
};
const POI_CLASS = { FOOD: 'food', WATER: 'water', GAS: 'gas', MISC: 'misc' };
function poiDivIcon(poi) {
  const cat = categorizePoi(poi.type);
  const emoji = POI_EMOJI[poi.type] || '📍';
  return L.divIcon({
    className: 'poi-icon',
    html: `<div class="poi-icon-inner ${POI_CLASS[cat]}">${emoji}</div>`,
    iconSize: [26, 26],
    iconAnchor: [13, 13],
    popupAnchor: [0, -13],
  });
}
const clusterOpts = {
  spiderfyOnMaxZoom: true,
  showCoverageOnHover: false,
  maxClusterRadius: 45,
};
const poiLayers = {
  FOOD: L.markerClusterGroup(clusterOpts),
  WATER: L.markerClusterGroup(clusterOpts),
  GAS: L.markerClusterGroup(clusterOpts),
  MISC: L.markerClusterGroup(clusterOpts),
};
for (const poi of DATA.pois) {
  const cat = categorizePoi(poi.type);
  const m = L.marker([poi.lat, poi.lon], { icon: poiDivIcon(poi) });
  m.bindPopup(`<b>${poi.name || poi.type}</b><br><span style="opacity:0.7">${poi.type}</span><br>km ${poi.km.toFixed(1)} — ${poi.clock}` + (poi.dist_m != null ? `<br><span style="opacity:0.6;font-size:11px">${poi.dist_m} m off route</span>` : ''));
  poiLayers[cat].addLayer(m);
}
poiLayers.FOOD.addTo(map);
poiLayers.WATER.addTo(map);
L.control.layers(null, {
  '🍔 Food / shops': poiLayers.FOOD,
  '💧 Water fountains': poiLayers.WATER,
  '⛽ Gas stations': poiLayers.GAS,
  '🚻 Toilets / misc': poiLayers.MISC
}, { collapsed: false }).addTo(map);

// --- Elevation profile (SVG)
const svg = document.getElementById('profile-chart');
const tooltip = document.getElementById('profile-tooltip');
function drawProfile() {
  const wrap = document.getElementById('profile-wrap');
  const W = wrap.clientWidth - 32;
  const H = 360;
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.innerHTML = '';
  const padding = { l: 50, r: 16, t: 16, b: 30 };
  const xLeft = padding.l, xRight = W - padding.r;
  const yTop = padding.t, yBot = H - padding.b;
  const totalKm = DATA.track[DATA.track.length - 1].km;
  const maxEle = Math.max(...DATA.track.map(p => p.ele)) * 1.05;
  const minEle = 0;
  const xOf = km => xLeft + (km / totalKm) * (xRight - xLeft);
  const yOf = ele => yBot - ((ele - minEle) / (maxEle - minEle)) * (yBot - yTop);

  // Background bands for unpaved sectors
  for (const s of DATA.unpaved_sections) {
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', xOf(s.start_km));
    rect.setAttribute('y', yTop);
    rect.setAttribute('width', xOf(s.end_km) - xOf(s.start_km));
    rect.setAttribute('height', yBot - yTop);
    const total = (s.classes && Object.values(s.classes).reduce((a,b)=>a+b,0)) || 0;
    const unp = (s.classes && s.classes.unpaved) || 0;
    rect.setAttribute('fill', unp > total * 0.5 ? '#f85149' : '#d29922');
    rect.setAttribute('opacity', '0.12');
    svg.appendChild(rect);
  }

  // Bands for major climbs
  for (const c of DATA.climbs) {
    const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
    rect.setAttribute('x', xOf(c.start_km));
    rect.setAttribute('y', yTop);
    rect.setAttribute('width', xOf(c.end_km) - xOf(c.start_km));
    rect.setAttribute('height', yBot - yTop);
    rect.setAttribute('fill', '#f0883e');
    rect.setAttribute('opacity', '0.07');
    svg.appendChild(rect);
  }

  // Y axis grid
  for (let e = 0; e <= maxEle; e += 200) {
    const y = yOf(e);
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', xLeft); line.setAttribute('x2', xRight);
    line.setAttribute('y1', y); line.setAttribute('y2', y);
    line.setAttribute('stroke', '#30363d'); line.setAttribute('stroke-width', '0.5');
    svg.appendChild(line);
    const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    label.setAttribute('x', xLeft - 8); label.setAttribute('y', y + 4);
    label.setAttribute('fill', '#8b949e'); label.setAttribute('font-size', '10');
    label.setAttribute('text-anchor', 'end');
    label.textContent = e + ' m';
    svg.appendChild(label);
  }

  // X axis ticks every 50 km
  for (let km = 0; km <= totalKm; km += 50) {
    const x = xOf(km);
    const tick = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    tick.setAttribute('x1', x); tick.setAttribute('x2', x);
    tick.setAttribute('y1', yBot); tick.setAttribute('y2', yBot + 4);
    tick.setAttribute('stroke', '#8b949e'); tick.setAttribute('stroke-width', '0.5');
    svg.appendChild(tick);
    const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    lbl.setAttribute('x', x); lbl.setAttribute('y', yBot + 18);
    lbl.setAttribute('fill', '#8b949e'); lbl.setAttribute('font-size', '10');
    lbl.setAttribute('text-anchor', 'middle');
    lbl.textContent = km + ' km';
    svg.appendChild(lbl);
  }

  // Profile area (filled)
  let path = `M ${xOf(0)} ${yBot} `;
  for (const p of DATA.track) {
    path += `L ${xOf(p.km)} ${yOf(p.ele)} `;
  }
  path += `L ${xOf(totalKm)} ${yBot} Z`;
  const profile = document.createElementNS('http://www.w3.org/2000/svg', 'path');
  profile.setAttribute('d', path);
  profile.setAttribute('fill', 'rgba(240, 136, 62, 0.25)');
  profile.setAttribute('stroke', '#f0883e');
  profile.setAttribute('stroke-width', '1.2');
  svg.appendChild(profile);

  // CP markers
  for (const wpt of DATA.waypoints) {
    const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
    line.setAttribute('x1', xOf(wpt.km)); line.setAttribute('x2', xOf(wpt.km));
    line.setAttribute('y1', yTop); line.setAttribute('y2', yBot);
    line.setAttribute('stroke', '#f0883e'); line.setAttribute('stroke-width', '1');
    line.setAttribute('stroke-dasharray', '3,3');
    svg.appendChild(line);
    const lbl = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    lbl.setAttribute('x', xOf(wpt.km)); lbl.setAttribute('y', yTop + 12);
    lbl.setAttribute('fill', '#f0883e'); lbl.setAttribute('font-size', '11');
    lbl.setAttribute('font-weight', '600');
    lbl.setAttribute('text-anchor', 'middle');
    lbl.textContent = wpt.name.split(' - ')[0];
    svg.appendChild(lbl);
  }

  // POI dots (water + food only to avoid clutter)
  for (const poi of DATA.pois) {
    const cat = categorizePoi(poi.type);
    if (cat !== 'WATER' && cat !== 'FOOD') continue;
    const c = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    c.setAttribute('cx', xOf(poi.km)); c.setAttribute('cy', yBot - 2);
    c.setAttribute('r', '2.5');
    c.setAttribute('fill', cat === 'WATER' ? '#58a6ff' : '#f0883e');
    c.setAttribute('opacity', '0.7');
    svg.appendChild(c);
  }

  // Persistent cursor line (driven by updatePosition)
  const cursorLine = document.createElementNS('http://www.w3.org/2000/svg', 'line');
  cursorLine.setAttribute('y1', yTop); cursorLine.setAttribute('y2', yBot);
  cursorLine.setAttribute('stroke', '#f0883e'); cursorLine.setAttribute('stroke-width', '1.5');
  cursorLine.setAttribute('opacity', '0.85'); cursorLine.setAttribute('pointer-events', 'none');
  svg.appendChild(cursorLine);
  // Expose to outer scope for updates
  svg._cursorLine = cursorLine;
  svg._xOf = xOf;
  svg._xLeft = xLeft;
  svg._xRight = xRight;
  svg._totalKm = totalKm;

  // Hover behavior: shows ephemeral tooltip + moves the persistent cursor
  svg.addEventListener('mousemove', e => {
    const rect = svg.getBoundingClientRect();
    const ratio = (e.clientX - rect.left) / rect.width;
    const px = ratio * W;
    if (px < xLeft || px > xRight) { tooltip.style.display = 'none'; return; }
    const km = ((px - xLeft) / (xRight - xLeft)) * totalKm;
    let best = DATA.track[0], bd = Infinity;
    for (const p of DATA.track) {
      const d = Math.abs(p.km - km);
      if (d < bd) { bd = d; best = p; }
    }
    tooltip.style.display = 'block';
    tooltip.style.left = (e.clientX - rect.left + 12) + 'px';
    tooltip.style.top = (e.clientY - rect.top - 60) + 'px';
    tooltip.innerHTML = `<b>km ${km.toFixed(1)}</b><br>${Math.round(best.ele)} m<br><span style="color:#f0883e">${clockTimeAtKm(km)}</span><br><span style="opacity:0.7">click to pin</span>`;
  });
  svg.addEventListener('mouseleave', () => { tooltip.style.display = 'none'; });
  svg.addEventListener('click', e => {
    const rect = svg.getBoundingClientRect();
    const ratio = (e.clientX - rect.left) / rect.width;
    const px = ratio * W;
    if (px < xLeft || px > xRight) return;
    const km = ((px - xLeft) / (xRight - xLeft)) * totalKm;
    updatePosition(km, true);
  });
}
window.addEventListener('resize', () => { drawProfile(); updatePosition(currentKm, false); });
drawProfile();

// --- Unified position state (driven by slider, buttons, or profile click)
let currentKm = 0;
let positionMarker = null;
const totalKmGlobal = DATA.track[DATA.track.length - 1].km;

function findNearestTrackPoint(km) {
  let best = DATA.track[0], bd = Infinity;
  for (const p of DATA.track) {
    const d = Math.abs(p.km - km);
    if (d < bd) { bd = d; best = p; }
  }
  return best;
}

function findNearestPoi(km) {
  let bestP = null, bestD = Infinity;
  for (const poi of DATA.pois) {
    const d = Math.abs(poi.km - km);
    if (d < bestD) { bestD = d; bestP = poi; }
  }
  return { poi: bestP, distKm: bestD };
}

function updatePosition(km, panMap) {
  km = Math.max(0, Math.min(km, totalKmGlobal));
  currentKm = km;
  const sample = findNearestTrackPoint(km);
  const klass = classAtKm(km);
  const clock = clockTimeAtKm(km);
  const { poi, distKm } = findNearestPoi(km);

  // Info panel
  document.getElementById('info-km').textContent = km.toFixed(1) + ' km';
  document.getElementById('info-alt').textContent = Math.round(sample.ele) + ' m';
  const surfaceEl = document.getElementById('info-surface');
  surfaceEl.textContent = klass;
  surfaceEl.className = 'v ' + klass;
  document.getElementById('info-clock').textContent = clock;
  document.getElementById('info-poi').textContent = poi
    ? `${poi.type} — ${poi.name || '-'} (km ${poi.km.toFixed(1)}, Δ ${(distKm * 1000).toFixed(0)} m)`
    : '—';

  // Profile cursor
  if (svg._cursorLine && svg._xOf) {
    const x = svg._xOf(km);
    svg._cursorLine.setAttribute('x1', x);
    svg._cursorLine.setAttribute('x2', x);
  }

  // Map marker (persistent, distinct from POI icons)
  if (positionMarker) map.removeLayer(positionMarker);
  positionMarker = L.marker([sample.lat, sample.lon], {
    icon: L.divIcon({
      className: 'position-marker',
      html: '<div class="position-marker-inner"></div>',
      iconSize: [20, 20],
      iconAnchor: [10, 10],
    }),
    interactive: false,
    keyboard: false,
    zIndexOffset: 1000,
  }).addTo(map);
  if (panMap) {
    map.panTo([sample.lat, sample.lon], { animate: true });
  }

  // Sync slider
  const slider = document.getElementById('profile-slider');
  if (slider && Math.abs(parseFloat(slider.value) - km) > 0.05) {
    slider.value = km;
  }
}

// Wire slider
const slider = document.getElementById('profile-slider');
slider.max = totalKmGlobal.toFixed(1);
slider.addEventListener('input', e => updatePosition(parseFloat(e.target.value), false));
slider.addEventListener('change', e => updatePosition(parseFloat(e.target.value), true));

// Quick-jump buttons
document.querySelectorAll('.slider-buttons button').forEach(btn => {
  btn.addEventListener('click', () => updatePosition(parseFloat(btn.dataset.km), true));
});

// Keyboard arrows: 1 km / 10 km steps
document.addEventListener('keydown', e => {
  if (document.activeElement.tagName === 'INPUT' && document.activeElement.id !== 'profile-slider') return;
  if (e.key === 'ArrowLeft') { updatePosition(currentKm - (e.shiftKey ? 10 : 1), true); e.preventDefault(); }
  if (e.key === 'ArrowRight') { updatePosition(currentKm + (e.shiftKey ? 10 : 1), true); e.preventDefault(); }
});

// Initial position
updatePosition(0, false);

// --- POI table with filter
function renderPois() {
  const filter = document.getElementById('poi-filter').value.toLowerCase();
  const cat = document.getElementById('poi-cat').value;
  const kmRange = document.getElementById('poi-km').value;
  let kmMin = 0, kmMax = 1000;
  if (kmRange) { const [a, b] = kmRange.split(',').map(Number); kmMin = a; kmMax = b; }
  const tbody = document.getElementById('poi-tbody');
  tbody.innerHTML = '';
  const filtered = DATA.pois
    .filter(p => p.km >= kmMin && p.km <= kmMax)
    .filter(p => !cat || categorizePoi(p.type) === cat)
    .filter(p => !filter || (p.name + ' ' + p.type).toLowerCase().includes(filter))
    .sort((a, b) => a.km - b.km);
  for (const p of filtered) {
    const c = categorizePoi(p.type);
    const cls = c === 'FOOD' ? 'food' : c === 'WATER' ? 'water' : c === 'GAS' ? 'gas' : 'misc';
    tbody.innerHTML += `<tr><td>${p.km.toFixed(1)}</td><td>${p.clock}</td>` +
      `<td><span class="badge ${cls}">${c}</span></td>` +
      `<td>${p.type}</td><td>${p.name || '-'}</td><td>${p.dist_m ?? '-'} m</td></tr>`;
  }
}
document.getElementById('poi-filter').addEventListener('input', renderPois);
document.getElementById('poi-cat').addEventListener('change', renderPois);
document.getElementById('poi-km').addEventListener('change', renderPois);
renderPois();

// Compute clock time at km on the fly using a precomputed lookup
function clockTimeAtKm(km) {
  // Find closest precomputed POI clock or interpolate from track-times
  let bestIdx = 0, bd = Infinity;
  for (let i = 0; i < DATA.track_times.length; i++) {
    const d = Math.abs(DATA.track_times[i].km - km);
    if (d < bd) { bd = d; bestIdx = i; }
  }
  return DATA.track_times[bestIdx].clock;
}

// --- Markdown documents viewer
if (window.marked) {
  marked.setOptions({ gfm: true, breaks: false });
}
function openDoc(filename) {
  const content = DATA.docs[filename];
  if (!content) return;
  const title = (DATA.docs_meta.find(d => d.file === filename) || {}).title || filename;
  document.getElementById('viewer-title').textContent = title;
  const rawLink = document.getElementById('viewer-raw');
  rawLink.href = filename;
  rawLink.style.display = '';
  const body = document.getElementById('viewer-body');
  body.innerHTML = window.marked ? marked.parse(content) : '<pre>' + content.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])) + '</pre>';
  // Intercept internal MD links to switch viewer instead of leaving the page
  body.querySelectorAll('a').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (href.endsWith('.md') && DATA.docs[href.replace(/^\\.?\\//, '')]) {
      a.addEventListener('click', e => {
        e.preventDefault();
        const f = href.replace(/^\\.?\\//, '');
        openDoc(f);
        document.querySelectorAll('.docs-sidebar .doc-link').forEach(el => {
          el.classList.toggle('active', el.dataset.file === f);
        });
        document.querySelector('.docs-viewer').scrollTop = 0;
      });
    }
  });
  document.querySelectorAll('.docs-sidebar .doc-link').forEach(el => {
    el.classList.toggle('active', el.dataset.file === filename);
  });
}
document.querySelectorAll('.docs-sidebar .doc-link').forEach(el => {
  el.addEventListener('click', e => {
    e.preventDefault();
    openDoc(el.dataset.file);
    document.querySelector('.docs-viewer').scrollTop = 0;
  });
});
// Open the first doc by default when the user lands on the Documents tab
let docsOpened = false;
document.querySelector('nav.tabs button[data-tab="docs"]').addEventListener('click', () => {
  if (!docsOpened && DATA.docs_meta.length) {
    openDoc(DATA.docs_meta[0].file);
    docsOpened = true;
  }
});
</script>
</body>
</html>
"""


def render_stats(meta: dict) -> str:
    items = [
        ("DISTANCE", f"{meta['distance_km']:.1f} km"),
        ("D+ RAW", "~10 250 m"),
        ("D+ SMOOTHED", f"{meta['gain_m']:.0f} m"),
        ("HIGH POINT", "1 291 m"),
        ("OFF-ROAD", "~74 km / 15 %"),
        ("CP1", "Ghisoni km 164"),
        ("CP2", "Crocicchia km 333"),
    ]
    return "".join(
        f'<div class="stat"><div class="v">{v}</div><div class="l">{l}</div></div>'
        for l, v in items
    )


def render_climb_kpis(climbs: list[dict]) -> str:
    if not climbs:
        return ""
    total = sum(c["gain_m"] for c in climbs)
    longest = max(climbs, key=lambda c: c["length_km"])
    steepest = max(climbs, key=lambda c: c["avg_grade_pct"])
    highest = max(climbs, key=lambda c: c["top_alt_m"])
    return (
        f'<div class="kpi"><div class="l">Total climbs</div><div class="v">{len(climbs)}</div><div class="s">+{total:.0f} m cumulated gain</div></div>'
        f'<div class="kpi"><div class="l">Longest</div><div class="v">{longest["length_km"]:.1f} km</div><div class="s">km {longest["start_km"]:.0f}-{longest["end_km"]:.0f}</div></div>'
        f'<div class="kpi"><div class="l">Steepest</div><div class="v">{steepest["avg_grade_pct"]:.1f} %</div><div class="s">km {steepest["start_km"]:.0f}-{steepest["end_km"]:.0f}</div></div>'
        f'<div class="kpi"><div class="l">Highest point</div><div class="v">{highest["top_alt_m"]:.0f} m</div><div class="s">km {highest["end_km"]:.0f}</div></div>'
    )


def render_descent_kpis(descents: list[dict]) -> str:
    if not descents:
        return ""
    total = sum(d["loss_m"] for d in descents)
    longest = max(descents, key=lambda d: d["length_km"])
    steepest = min(descents, key=lambda d: d["avg_grade_pct"])
    return (
        f'<div class="kpi"><div class="l">Total descents</div><div class="v">{len(descents)}</div><div class="s">-{total:.0f} m cumulated loss</div></div>'
        f'<div class="kpi"><div class="l">Longest</div><div class="v">{longest["length_km"]:.1f} km</div><div class="s">km {longest["start_km"]:.0f}-{longest["end_km"]:.0f}</div></div>'
        f'<div class="kpi"><div class="l">Steepest</div><div class="v">{steepest["avg_grade_pct"]:.1f} %</div><div class="s">km {steepest["start_km"]:.0f}-{steepest["end_km"]:.0f}</div></div>'
    )


def surface_html(label: str) -> str:
    if not label:
        return ""
    if label.startswith("**UNPAVED"):
        return f'<span class="unpaved">{label.replace("**", "")}</span>'
    if "partial unpaved" in label:
        return f'<span class="partial">{label}</span>'
    if "brief rough" in label:
        return f'<span class="brief-rough">{label}</span>'
    return f'<span class="likely-paved">{label}</span>'


def render_climbs_rows(climbs: list[dict]) -> str:
    return "".join(
        f"<tr><td>{c['start_km']:.1f}-{c['end_km']:.1f}</td>"
        f"<td>{c['length_km']:.1f} km</td>"
        f"<td>+{c['gain_m']:.0f} m</td>"
        f"<td>{c['avg_grade_pct']:.1f} %</td>"
        f"<td>{c['top_alt_m']:.0f} m</td>"
        f"<td>{surface_html(c.get('surface_cross_ref', ''))}</td></tr>"
        for c in climbs
    )


def render_descents_rows(descents: list[dict]) -> str:
    return "".join(
        f"<tr><td>{d['start_km']:.1f}-{d['end_km']:.1f}</td>"
        f"<td>{d['length_km']:.1f} km</td>"
        f"<td>-{d['loss_m']:.0f} m</td>"
        f"<td>{d['avg_grade_pct']:.1f} %</td>"
        f"<td>{d['bottom_alt_m']:.0f} m</td>"
        f"<td>{surface_html(d.get('surface_cross_ref', ''))}</td></tr>"
        for d in descents
    )


def render_aero_rows(aero_sections: list[dict]) -> str:
    return "".join(
        f"<tr><td>{a['start_km']:.1f}-{a['end_km']:.1f}</td>"
        f"<td>{a['length_km']:.1f} km</td>"
        f"<td>{a['avg_grade_pct']:+.2f} %</td>"
        f"<td>{a['start_alt_m']:.0f} m</td>"
        f"<td>{a['end_alt_m']:.0f} m</td>"
        f"<td>{surface_html(a.get('surface_cross_ref', ''))}</td></tr>"
        for a in aero_sections
    )


def render_unpaved_rows(sections: list[dict]) -> str:
    rows = []
    for s in sections:
        klass = "unpaved" if s.get("classes", {}).get("unpaved", 0) > s["dist_km"] * 0.5 else "partial"
        top_hw = max(s.get("highways", {"unknown": 0}).items(), key=lambda x: x[1])[0] if s.get("highways") else "unknown"
        top_sf = max(s.get("surfaces", {"unknown": 0}).items(), key=lambda x: x[1])[0] if s.get("surfaces") else "unknown"
        rows.append(
            f'<tr class="{klass}"><td>{s["start_km"]:.1f}-{s["end_km"]:.1f}</td>'
            f"<td>{s['dist_km']:.1f} km</td>"
            f"<td>{s['avg_grade_pct']:+.1f} %</td>"
            f"<td>+{s['gain_m']:.0f} m</td>"
            f"<td>-{s['loss_m']:.0f} m</td>"
            f"<td>{top_hw}</td>"
            f"<td>{top_sf}</td></tr>"
        )
    return "".join(rows)


RISK_SECTORS = [
    {
        "title": "1. km 17-42 — Early Gravel/Track Climbing",
        "exposure": "~17 km rough/suspect across km 17-25 + 33-42",
        "profile": "Mostly uphill, +718 m combined",
        "risk": "Early legs, temptation to push hard. Spending margin here is paid for at km 440+.",
        "plan": "Seated, controlled. Eat before km 17. Warm-up, not test.",
        "clock": "h+1 to h+3 (Fri morning)",
    },
    {
        "title": "2. km 136-149 — Long Suspect Climbing Track",
        "exposure": "~12.4 km on track",
        "profile": "+2.8 %, +442 m",
        "risk": "Long enough to become muscular and postural if loose.",
        "plan": "Endurance climb, not race segment. Cadence and upper body relaxed.",
        "clock": "h+11 (Fri evening)",
    },
    {
        "title": "3. km 178-184 — Mid-Descent Rough Section",
        "exposure": "~5.0 km within larger paved descent from high point",
        "profile": "-6.0 %, -299 m",
        "risk": "Highest-speed paved descent suddenly hits rough surface.",
        "plan": "Shed speed BEFORE km 178. Hoods. Walk if uncertain.",
        "clock": "h+14 (Fri night)",
    },
    {
        "title": "4. km 253-256 — Dirt Descent",
        "exposure": "~3.2 km dirt",
        "profile": "-4.5 %, -144 m",
        "risk": "Not huge, but enough for braking/line-choice mistakes.",
        "plan": "Hoods. Brake before turns. No drops on loose surface.",
        "clock": "h+18 (Sat early morning)",
    },
    {
        "title": "5. km 313-316 — Short Steep Rough Descent",
        "exposure": "~1.6 km at -5.3 %",
        "profile": "Short but steep on track",
        "risk": "High pinch/slide potential if tired.",
        "plan": "Speed cap. Active bike handling.",
        "clock": "h+22 (Sat early morning)",
    },
    {
        "title": "6. km 388-412 — Late Mixed Track Corridor",
        "exposure": "~16 km cumulative track + 4 km of dirt (km 394-398)",
        "profile": "Rolling/descending with grade2/3 tracks",
        "risk": "Late-race fatigue and repeated transitions between road/track.",
        "plan": "Reset before entering. Eat/drink on road before sector.",
        "clock": "h+25 (Sat late morning)",
    },
    {
        "title": "7. km 417-419 — Very Steep Rough Descent",
        "exposure": "2.2 km at -8.5 %",
        "profile": "Single steepest rough descent of the route",
        "risk": "High consequence if loose.",
        "plan": "Explicit speed cap. Walking a bad subsection is a valid race tactic.",
        "clock": "h+28 (Sat morning)",
    },
    {
        "title": "8. km 441-455 — Biggest Late Gravel/Track Block",
        "exposure": "~14 km, +522 / -616 m",
        "profile": "Most committing climb (+8 % to ~942 m) + steepest sustained descent of the route",
        "risk": "**Sequence C** — structural climax at 26+ hours of effort.",
        "plan": "Enter fed, hydrated, mentally reset. Ride for control, not speed.",
        "clock": "h+27 to h+29 (Sat noon)",
    },
]


def render_risk_sectors() -> str:
    out = []
    for s in RISK_SECTORS:
        out.append(
            f'<div class="risk-sector"><h4>{s["title"]}</h4>'
            f'<div class="grid">'
            f'<div><span class="label">Race clock:</span> {s["clock"]}</div>'
            f'<div><span class="label">Exposure:</span> {s["exposure"]}</div>'
            f'<div><span class="label">Profile:</span> {s["profile"]}</div>'
            f'<div><span class="label">Risk:</span> {s["risk"]}</div>'
            f'<div style="grid-column: 1 / -1"><span class="label">Plan:</span> {s["plan"]}</div>'
            f"</div></div>"
        )
    return "".join(out)


def render_docs_sidebar(available: list[tuple[str, str, str]]) -> str:
    out = []
    for fname, title, desc in available:
        out.append(
            f'<a class="doc-link" href="#" data-file="{fname}">'
            f'<div class="title">{title}</div>'
            f'<div class="desc">{desc}</div>'
            f'</a>'
        )
    return "".join(out)


def load_docs() -> tuple[dict, list[tuple[str, str, str]]]:
    """Read each MD doc from the corsica folder. Return embed dict + sidebar list."""
    embed: dict[str, str] = {}
    available: list[tuple[str, str, str]] = []
    for fname, title, desc in DOCS:
        path = CORSICA / fname
        if path.exists():
            embed[fname] = path.read_text(encoding="utf-8")
            available.append((fname, title, desc))
    return embed, available


def build():
    track = parse_track(TRACK_GPX)
    track_full = track
    track_down = downsample(track, target=3000)
    pois_all = parse_pois(POI_GPX)
    terrain = json.loads(TERRAIN_JSON.read_text())

    # Time projection table at every 1 km
    times = compute_passage_times(track_full, terrain.get("sections", []))
    track_times = []
    for km_int in range(0, int(track_full[-1]["km"]) + 1):
        when = RACE_START + timedelta(hours=time_at_km(km_int, track_full, times) + planned_stops_at_km(km_int))
        track_times.append({"km": km_int, "clock": when.strftime("%a %H:%M")})

    # Annotate POIs with passage clock
    for p in pois_all:
        when = RACE_START + timedelta(hours=time_at_km(p["km"], track_full, times) + planned_stops_at_km(p["km"]))
        p["clock"] = when.strftime("%a %H:%M")

    docs_embed, docs_available = load_docs()

    data = {
        "track": [{"lat": p["lat"], "lon": p["lon"], "ele": round(p["ele"], 1), "km": round(p["km"], 3)} for p in track_down],
        "track_times": track_times,
        "waypoints": terrain["waypoints"],
        "pois": pois_all,
        "climbs": terrain["climbs"],
        "descents": terrain["descents"],
        "aero_sections": terrain["aero_sections"],
        "unpaved_sections": terrain["sections"],
        "surface_summary": terrain["surface_summary"],
        "docs": docs_embed,
        "docs_meta": [{"file": f, "title": t, "desc": d} for f, t, d in docs_available],
    }

    html_out = HTML_TEMPLATE
    html_out = html_out.replace("__STATS__", render_stats(terrain))
    html_out = html_out.replace("__CLIMB_KPIS__", render_climb_kpis(terrain["climbs"]))
    html_out = html_out.replace("__DESCENT_KPIS__", render_descent_kpis(terrain["descents"]))
    html_out = html_out.replace("__CLIMBS_ROWS__", render_climbs_rows(terrain["climbs"]))
    html_out = html_out.replace("__DESCENTS_ROWS__", render_descents_rows(terrain["descents"]))
    html_out = html_out.replace("__AERO_ROWS__", render_aero_rows(terrain["aero_sections"]))
    html_out = html_out.replace("__UNPAVED_ROWS__", render_unpaved_rows(terrain["sections"]))
    html_out = html_out.replace("__RISK_SECTORS__", render_risk_sectors())
    html_out = html_out.replace("__DOCS_SIDEBAR__", render_docs_sidebar(docs_available))
    html_out = html_out.replace("__DATA_JSON__", json.dumps(data, ensure_ascii=False))

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(html_out, encoding="utf-8")
    print(f"Wrote {OUT_HTML} ({OUT_HTML.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    build()
