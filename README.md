# Corsica 555 Gravel — 29 May 2026

Public race dashboard for the BikingMan Corsica 555 Gravel ultra. Built
as a single static HTML page from the route GPX, POI GPX, and OSM
surface analysis.

**Live site:** https://tomverin.github.io/corsica-555/

## Contents

- `index.html` — interactive dashboard: map (Leaflet) + elevation
  profile + climbs / descents / aero / risk sectors / POIs with
  projected pass-through times.
- `terrain_analysis.md` — full terrain analysis (climbs, descents,
  aero, surface, race-defining sequences, key risk sectors).
- `tyre-selection-alt.md` — tire decision (Race King 2.2 vs G-One
  RS 45 mm).
- `refueling_strategy.md` — fueling and pacing strategy for a 30 h
  target with no scheduled sleep.
- `checklist.md` — pre-race + in-race checklist.
- `personal-checklist.md` — per-location packing checklist (bike,
  bags, pockets).
- `briefing-summary.md` — official BikingMan briefing synthesis.
- `roadbook.md` — race roadbook.

## Race summary

- Distance: 487.1 km · D+ ~10 250 m raw / ~8 950 m smoothed
- High point: 1 291 m
- Off-road: ~74 km (~15 %), fragmented in blocks
- 2 checkpoints: CP1 Ghisoni km 164, CP2 Crocicchia km 333
- Start: Friday 29/05/2026 at 07:00 (Porto-Vecchio)
- Target finish: Saturday 30/05/2026 ~13:00 (Biguglia, ~30 h)

## How the site was built

Full build pipeline documented in [BUILD.md](BUILD.md). Source GPX +
POI + OSM analysis are processed with two stdlib-only Python scripts:

- [`scripts/analyze_gpx_osm_surface.py`](scripts/analyze_gpx_osm_surface.py)
  — produces the structured terrain JSON (climbs, descents, aero,
  surface sections) by cross-referencing the GPX with OSM via the
  Overpass API.
- [`scripts/build_corsica_site.py`](scripts/build_corsica_site.py) —
  assembles the GPX, POIs, terrain JSON, and the 7 markdown docs into
  a single self-contained `index.html` (~430 KB).

Both scripts are mirrored here as point-in-time copies. The canonical
versions live in the rider's private training-journal repo and evolve
with the rest of the daily workflow. Fork-friendly: see BUILD.md for
how to adapt the dashboard to another ultra route.

## License

Public race-planning material shared for friends and the BikingMan
community. No warranty.
