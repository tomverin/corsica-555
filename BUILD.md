# How this site was built

This page documents the pipeline that produces `index.html`, the
interactive Corsica 555 race dashboard hosted at
https://tomverin.github.io/corsica-555/.

The canonical source for the build scripts lives in a separate
private repository (the rider's training journal). The two Python
scripts mirrored here under `scripts/` are point-in-time copies kept
for transparency and forkability — if you want to adapt this
dashboard for your own race, this is where to start.

## Pipeline overview

```
              GPX route                  GPX POIs
                  │                          │
                  ▼                          │
      analyze_gpx_osm_surface.py             │
                  │                          │
                  ▼                          ▼
       terrain_analysis.raw.json   ┌─── 7 .md docs
                  │                │           │
                  └────────┬───────┴───────────┘
                           ▼
                  build_corsica_site.py
                           │
                           ▼
                  site/index.html (~430 KB, self-contained)
                           │
                           ▼
                  GitHub Pages deploy
                           │
                           ▼
       https://tomverin.github.io/corsica-555/
```

## Inputs

1. **Track GPX** — the official race route from the BikingMan
   organization, ~19 000 trackpoints, includes 2 waypoints (CP1
   Ghisoni km 164, CP2 Crocicchia km 333).
2. **POI GPX** — 172 points of interest along the route, exported from
   [onroutemap.de](https://onroutemap.de) using the route GPX as
   input. Categories: bakery, supermarket, convenience store, café,
   fast food, ice cream parlor, kiosk, drinking water, gas station,
   toilets.
3. **Markdown docs** — 7 race-planning documents authored in the
   private repo and copied here:
   - `terrain_analysis.md` — full terrain analysis
   - `tyre-selection-alt.md` — tire decision
   - `refueling_strategy.md` — fueling + pacing plan
   - `checklist.md` — race checklist
   - `personal-checklist.md` — packing checklist
   - `briefing-summary.md` — official briefing synthesis
   - `roadbook.md` — compact roadbook

## Build step 1 — `analyze_gpx_osm_surface.py`

This script enriches the GPX with surface information from
OpenStreetMap.

What it does:

- Resamples the GPX at ~200 m steps and smooths the elevation.
- Queries the Overpass API for every `highway` way in the route
  corridor (split into 15 km chunks for long routes).
- Matches each resampled segment to the nearest OSM way within a
  threshold (default 200 m, tuned for mountain/forest routes).
- Classifies each segment as `paved` / `unknown_likely_paved` /
  `unpaved` / `suspect_unpaved` / `unknown` / `unmatched`.
- Detects climbs, descents, and aero-eligible sections from the
  smoothed elevation profile, with surface cross-reference labels.
- Outputs a Markdown report plus a JSON file with the structured
  data (climbs, descents, aero, surface sections, waypoints,
  elevation profile).

For the Corsica 555 the canonical run is:

```sh
python3 scripts/analyze_gpx_osm_surface.py \
  555_Corsica__2_2026_vfinale.gpx \
  --cache .cache/osm.json \
  --match-threshold-m 200 \
  --chunk-km 15 \
  --min-section-km 1.5 \
  --json-out terrain_analysis.raw.json
```

The cache file persists the Overpass response so reruns are
instantaneous. Delete it (or use a different name) to force a fresh
fetch.

## Build step 2 — `build_corsica_site.py`

This script consumes the GPX files, the terrain JSON, and the
markdown docs and emits a single self-contained `index.html`.

What it does:

- Parses the route GPX and downsamples to ~3 000 trackpoints (enough
  for Leaflet to render smoothly).
- Parses the POI GPX, filters to POIs within 200 m of the route.
- Reads the terrain JSON (climbs, descents, aero, surface
  sections, waypoints).
- Reads each of the 7 markdown docs.
- Computes pass-through clock times at each km using a grade × surface
  speed model calibrated for the 30 h target. The starting time
  (Friday 07:00) and a small "stop budget" at the checkpoints / key
  fuel windows are baked in.
- Builds the HTML page, embedding all data inline as a single JSON
  object. The Leaflet map, marker clustering, the elevation profile
  (hand-drawn SVG), the position slider, the markdown viewer (using
  marked.js), and all interactive bindings are produced as part of
  the embedded `<script>` block.

Run:

```sh
python3 scripts/build_corsica_site.py
# Outputs the file (here, in this public repo, that target is index.html
# next to this BUILD.md).
```

## Runtime dependencies

All loaded from public CDNs at runtime, no installation needed:

- [Leaflet 1.9.4](https://leafletjs.com/) — interactive map
- [Leaflet.markercluster 1.5.3](https://github.com/Leaflet/Leaflet.markercluster) — POI marker clustering
- [marked 12.0](https://marked.js.org/) — markdown to HTML rendering

Browser support: any modern browser with ES2017+ support. Tested on
Chrome, Safari, Firefox. Mobile responsive (the docs layout collapses
to a single column under 800 px width).

## File size

The final `index.html` is approximately 430 KB. Breakdown:

- Track geometry (3 000 points, lat/lon/ele/km): ~120 KB
- POI list (172 entries with clock times): ~30 KB
- Terrain analysis (climbs, descents, surface sections): ~70 KB
- Embedded markdown docs (7 files): ~120 KB
- Generated HTML (tables, sidebar, JS code, CSS): ~90 KB

## Deployment

The public site is served by GitHub Pages from the `main` branch of
this repo. Any push to `main` triggers a rebuild within ~30 s.

The rider deploys from a private workflow using
`scripts/deploy_corsica_site.sh` (lives only in the private repo)
which:

1. Rebuilds `index.html` from the private source GPX/JSON/markdown
2. Mirrors the HTML and the 7 markdown docs to this public repo
3. Mirrors the two build scripts under `scripts/`
4. Commits and pushes

## Forking for your own race

To adapt this dashboard for a different ultra event:

1. Drop your own route GPX into the working directory.
2. Optionally produce a POI GPX (via onroutemap.de, RWGPS, or
   manually).
3. Run `analyze_gpx_osm_surface.py` on the route to produce the
   surface JSON.
4. Adjust `build_corsica_site.py`:
   - Update the input filenames at the top of the file.
   - Update the `RISK_SECTORS` constant with your route's specific
     sectors.
   - Update the `DOCS` list with your own markdown docs.
   - Update the race-clock model (`grade_speed`, `planned_stops_at_km`,
     `RACE_START`) for your target finish time.
   - Update the static stats in `render_stats()` (distance, D+, etc.).
5. Run `build_corsica_site.py` and open `index.html`.

## License and disclaimer

This material is published for friends and the BikingMan community.
The race route belongs to BikingMan; the OSM data is © OSM
contributors (ODbL); the POIs are courtesy of onroutemap.de. The
analysis and the site itself are shared as-is, with no warranty.
Decisions made from this material are the rider's own.
