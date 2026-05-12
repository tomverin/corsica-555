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

Source GPX + POI + OSM analysis from the private training journal,
processed with [`analyze_gpx_osm_surface.py`](https://github.com/) and
[`build_corsica_site.py`](https://github.com/) (custom Python tools,
stdlib only).

## License

Public race-planning material shared for friends and the BikingMan
community. No warranty.
