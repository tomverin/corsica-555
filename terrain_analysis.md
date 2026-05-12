# Corsica 555 2026 - Terrain Analysis

Generated from `555_Corsica__2_2026_vfinale.gpx` on 2026-05-12 via
`scripts/analyze_gpx_osm_surface.py`.

Run parameters (canonical for this route): `--match-threshold-m 200`
(mountain default), `--chunk-km 15`, `--min-section-km 1.5`. Other
parameters at script defaults.

Surface analysis uses OpenStreetMap highway/surface/tracktype tags
matched to the GPX. The GPX itself does not contain surface data, so
this remains an estimate. Many Corsican roads in OSM have no explicit
`surface` tag; unknown secondary/tertiary roads are likely paved
unless listed as `track`, `dirt`, `gravel`, or suspect below.

## GPX Summary

- Distance: **487.1 km**.
- Smoothed gain/loss: **+8 946 m / -8 956 m**.
- Elevation range: **-1 m to 1 291 m**.
- Match threshold: 200 m; unmatched: 0.4 km (0.1 %).
- OSM ways loaded: 14 666.
- Unpaved section merge: min 1.5 km; gap 0.4 km.

Compared with the previous WIP GPX, the final trace is shorter and
less high: roughly -16 km, -700 m D+, and a lower high point. The
route is still very mountainous, but the old 1 600 m off-road summit
is gone.

## Checkpoints

Two checkpoints declared in the GPX as `wpt` features:

| CP | Location | Km | Alt | Offset | Comment |
|---|---|---:|---:|---:|---|
| CP1 | Village de Ghisoni | **164.0** | **658 m** | 7 m | At the foot of the route's highest paved climb (km 164-175, +631 m at 6.1 % to 1 291 m). Feeding / regroup window before this ascent. |
| CP2 | Village de Crocicchia | **333.4** | **616 m** | 45 m | Sits before the long descent toward ~150 m (km 343-352, -5.3 %). Pacing window into the second half. |

Both checkpoints have ride-window opening times tied to the 200 km/day
rule.

## Elevation Profile (every 25 km)

| Km | Elevation |
|---:|---:|
| 0.0 | 12 m — departure Porto-Vecchio |
| 25.0 | 669 m — early climbing block already done |
| 50.0 | 943 m |
| 75.0 | 726 m |
| 100.0 | 1 039 m |
| 125.0 | 694 m |
| 150.0 | 1 098 m |
| 175.0 | 1 274 m — high point reached at km 174 (1 291 m) |
| 200.0 | 661 m |
| 225.0 | 642 m |
| 250.0 | 974 m — second altitude block (1 066 m at km 251) |
| 275.0 | 433 m |
| 300.0 | 671 m |
| 325.0 | 597 m — CP2 km 333 |
| 350.0 | 240 m |
| 375.0 | 553 m |
| 400.0 | 33 m — descent back to coast |
| 425.0 | 20 m |
| 450.0 | 747 m — punchy late climb to 942 m (top km 447) |
| 475.0 | 27 m — after the steepest descent |
| 487.1 | 1 m — finish Biguglia |

## Grade Distribution

500 m centered-window grade buckets:

| Grade | Distance | Share | Gain | Loss |
|---|---:|---:|---:|---:|
| ≤ -6 % | 41.8 km | 8.6 % | 0 m | 3 168 m |
| -6 to -3 % | 91.2 km | 18.7 % | 0 m | 4 176 m |
| -3 to -1 % | 73.4 km | 15.1 % | 0 m | 1 411 m |
| -1 to +1 % | 74.5 km | 15.3 % | 170 m | 201 m |
| +1 to +3 % | 69.0 km | 14.2 % | 1 368 m | 0 m |
| +3 to +6 % | 92.0 km | 18.9 % | 4 137 m | 0 m |
| ≥ +6 % | 45.2 km | 9.3 % | 3 270 m | 0 m |

Structural reading: still very mountainous. About **270 km are at an
absolute grade of at least 3 %**, so the route remains dominated by
climbing and descending rather than sustained flat speed.

## Major Climbs (≥ 1.5 km, ≥ 60 m gain)

| Km range | Length | Gain | Avg grade | Top alt | Surface cross-ref |
|---:|---:|---:|---:|---:|---|
| 12.2-21.4 | 9.2 km | +476 m | 5.2 % | 555 m | partial unpaved (17.4-24.6) |
| 22.4-26.8 | 4.4 km | +237 m | 5.4 % | 786 m | partial unpaved (17.4-24.6) |
| 33.8-41.2 | 7.4 km | +397 m | 5.4 % | 977 m | **UNPAVED** (32.4-42.4) |
| 62.6-68.0 | 5.4 km | +267 m | 4.9 % | 941 m | mostly paved, brief rough (66.4-69.2) |
| 75.6-79.2 | 3.6 km | +195 m | 5.4 % | 925 m | partial unpaved (74.4-77.4) |
| 83.8-94.8 | 11.0 km | +335 m | 3.0 % | 1 188 m | likely paved |
| 117.4-122.2 | 4.8 km | +210 m | 4.4 % | 650 m | likely paved |
| 126.2-131.0 | 4.8 km | +150 m | 3.1 % | 821 m | likely paved |
| 135.4-138.4 | 3.0 km | +126 m | 4.2 % | 940 m | **UNPAVED** (136.0-148.8) |
| 139.0-146.6 | 7.6 km | +329 m | 4.3 % | 1 275 m | **UNPAVED** (136.0-148.8) |
| **164.2-174.6** | **10.4 km** | **+631 m** | **6.1 %** | **1 291 m** ← route high point | likely paved |
| 186.2-191.6 | 5.4 km | +253 m | 4.7 % | 866 m | likely paved |
| 214.4-223.8 | 9.4 km | +479 m | 5.1 % | 672 m | likely paved |
| 227.2-230.0 | 2.8 km | +118 m | 4.2 % | 731 m | likely paved |
| **240.4-251.8** | **11.4 km** | **+700 m** | **6.1 %** | **1 066 m** | likely paved |
| 266.8-270.0 | 3.2 km | +147 m | 4.6 % | 687 m | likely paved |
| 279.6-284.6 | 5.0 km | +211 m | 4.2 % | 626 m | likely paved |
| 286.8-290.8 | 4.0 km | +189 m | 4.7 % | 805 m | partial unpaved (287.8-292.4) |
| 293.8-296.8 | 3.0 km | +113 m | 3.8 % | 807 m | likely paved |
| 305.4-310.0 | 4.6 km | +130 m | 2.8 % | 762 m | partial unpaved (308.2-310.0) |
| 352.4-361.6 | 9.2 km | +468 m | 5.1 % | 622 m | likely paved |
| 363.2-368.4 | 5.2 km | +237 m | 4.6 % | 862 m | likely paved |
| 411.0-413.8 | 2.8 km | +110 m | 3.9 % | 169 m | mostly paved, brief rough (404.4-411.6) |
| 415.2-416.8 | 1.6 km | +72 m | 4.5 % | 233 m | likely paved |
| 425.4-428.8 | 3.4 km | +103 m | 3.0 % | 132 m | partial unpaved (426.4-430.8) |
| **434.0-447.6** | **13.6 km** | **+911 m** | **6.7 %** | **942 m** | **partial unpaved** (440.8-454.8) |

Structural observations:

- **Three altitude-defining climbs**: km 164-175 to 1 291 m (paved,
  post-CP1), km 240-252 to 1 066 m (paved), km 139-147 to 1 275 m
  (partly suspect track).
- **The early gravel climb at km 33-41** is the first real durability
  test: ~7 km of climbing at 5.4 % on confirmed gravel, just after the
  legs warm up.
- **The late climb km 434-447** is the most committing of the route
  in difficulty × surface × race-clock terms. The first ~6 km
  (km 434-440) are paved and roll up to ~340 m; from km 440 onward the
  surface turns to confirmed gravel and the grade pushes toward 8 %
  on the final 7.7 km to 942 m. This is the structural climax of the
  new route. The auto-detector merges the two parts; the narrative
  below (Sequence C) keeps them tactically distinct.

## Major Descents (≥ 1.5 km, ≥ 60 m loss)

| Km range | Length | Loss | Avg grade | Bottom alt | Surface cross-ref |
|---:|---:|---:|---:|---:|---|
| 30.0-33.2 | 3.2 km | -146 m | -4.6 % | 572 m | mostly paved, brief rough (32.4-42.4) |
| 46.6-49.0 | 2.4 km | -73 m | -3.1 % | 900 m | **UNPAVED** (44.8-48.8) |
| 52.6-55.4 | 2.8 km | -83 m | -2.9 % | 860 m | mostly paved, brief rough (50.2-53.2) |
| 58.8-62.2 | 3.4 km | -160 m | -4.7 % | 665 m | likely paved |
| 69.0-73.6 | 4.6 km | -187 m | -4.1 % | 748 m | likely paved |
| 79.6-82.0 | 2.4 km | -63 m | -2.6 % | 854 m | likely paved |
| 95.2-98.0 | 2.8 km | -149 m | -5.3 % | 1 031 m | likely paved |
| **99.4-109.8** | **10.4 km** | **-650 m** | **-6.2 %** | 419 m | likely paved (longest paved descent) |
| 147.0-156.0 | 9.0 km | -445 m | -4.9 % | 823 m | mostly paved, brief rough (136.0-148.8) |
| 156.8-159.2 | 2.4 km | -79 m | -3.3 % | 734 m | likely paved |
| 174.8-185.6 | 10.8 km | -682 m | -6.3 % | 603 m | partial unpaved (178.2-183.6) |
| **195.4-209.6** | **14.2 km** | **-689 m** | **-4.9 %** | 223 m | mostly paved, brief rough (202.6-204.8) — longest descent overall |
| 224.4-226.6 | 2.2 km | -66 m | -3.0 % | 599 m | likely paved |
| 230.6-240.0 | 9.4 km | -364 m | -3.9 % | 360 m | likely paved |
| 252.2-254.8 | 2.6 km | -108 m | -4.2 % | 950 m | partial unpaved (253.2-256.4) |
| 255.6-258.2 | 2.6 km | -152 m | -5.9 % | 788 m | partial unpaved (253.2-256.4) |
| 259.0-265.0 | 6.0 km | -250 m | -4.2 % | 543 m | likely paved |
| 270.4-276.8 | 6.4 km | -293 m | -4.6 % | 384 m | likely paved |
| 291.8-293.6 | 1.8 km | -110 m | -6.1 % | 690 m | partial unpaved (287.8-292.4) |
| 297.6-300.6 | 3.0 km | -140 m | -4.7 % | 659 m | likely paved |
| 313.2-320.2 | 7.0 km | -284 m | -4.1 % | 540 m | mostly paved, brief rough (313.4-315.4) |
| 332.8-335.8 | 3.0 km | -95 m | -3.2 % | 550 m | **UNPAVED** (332.8-337.4) |
| 343.6-352.0 | 8.4 km | -445 m | -5.3 % | 147 m | likely paved |
| 368.8-377.4 | 8.6 km | -353 m | -4.1 % | 502 m | likely paved |
| 378.4-382.2 | 3.8 km | -136 m | -3.6 % | 351 m | likely paved |
| 385.6-390.6 | 5.0 km | -234 m | -4.7 % | 122 m | partial unpaved (387.8-393.2) |
| 391.4-393.4 | 2.0 km | -61 m | -3.0 % | 62 m | **UNPAVED** (387.8-393.2) |
| 398.6-401.4 | 2.8 km | -64 m | -2.3 % | 6 m | likely paved |
| 417.0-420.2 | 3.2 km | -213 m | **-6.6 %** | 13 m | partial unpaved (417.2-419.4) |
| **447.8-462.2** | **14.4 km** | **-922 m** | **-6.4 %** | 17 m | partial unpaved (440.8-454.8) — Sequence C descent + paved finish |

Structural observations:

- **Two long fully paved descents** stand out as places to let the
  bike run with confidence: km 99-110 (-6.2 % over 10 km) and km
  195-210 (-4.9 % over 14 km).
- **Steepest paved descent**: km 174-186 at -6.3 % overall, including
  a 3.4 km rough segment at km 178-184 that surface-changes mid-run.
- **The longest sustained descent of the route** (-6.4 % over 14.4 km)
  is the post-Sequence-C drop km 447-462. The first 7 km (447-455) are
  the confirmed gravel block; from km 455 the surface returns to
  paved for the final coastal rollout. Auto-detector merges both
  halves; the narrative keeps them distinct.

## Race-Defining Sequences

Combining elevation, surface, and race-clock fatigue, three structural
sequences dominate the experience. They are *not* the only hard parts —
they are the segments where multiple stress factors stack.

### Sequence A — Early gravel chain (km 12-42, race hour 1-3)

- Suspect track climb 17-25 (~7.2 km, +313 m), short paved transition,
  then fully gravel climb 33-42 (~10 km, +405 m, top ~977 m).
- ~17 km of rough climbing across the first 3 hours of the race.
- Risk: legs are fresh, temptation to push hard. Spending grip /
  shoulder margin here would be paid for at km 440+.
- Plan: seated, controlled, eat before km 17. Treat as warm-up, not
  test.

### Sequence B — CP1 to high point (km 137-186, race hour 11-15)

- Suspect track climb 137-147 (+329 m to ~1 275 m).
- Paved descent 147-156 (-4.9 %, -445 m).
- **CP1 Ghisoni at km 164 (alt 658 m)** — feeding window.
- Paved climb 164-175 (+631 m at 6.1 %) to **route high point 1 291 m**.
- Paved descent 175-178 starts the drop from the high point.
- Short rough descent 178-184 (3.4 km at -8.8 % within the larger
  descent block) — surface change at the worst speed.
- Paved descent 184-186 continues to ~603 m.
- Risk: this is the densest altitude variation of the route. Cold at
  top, short rough section while still descending fast.
- Plan: layer up at km 175. Feed at CP1. The km 178-184 rough section
  is the tactical focus — be on hoods and *expect* the surface change.

### Sequence C — Late gravel climax (km 434-462, race hour 26-29)

- Paved climb 434-440 (+~280 m, ramps things up).
- **Confirmed gravel block km 440-455** (~14 km, +522 / -616 m).
  - Climb 440-447 at high grade to ~942 m → most committing climb of
    the route.
  - Descent 447-455 → steepest sustained off-road descent of the route.
- Paved descent 455-462 (-280 m) to ~17 m near coast.
- Risk: this is the structural climax of the entire course. Highest
  grades on the route, confirmed gravel, **at 26+ hours of effort**
  with shoulder fatigue accumulated.
- Plan: explicit fuel/hydrate/posture reset at km 433 before the long
  climb. Walking subsections of the descent is a valid tactical
  choice. Speed cap enforced. After km 462 the route is essentially
  done at altitude — only ~25 km of low-altitude rolling remain.

## Surface Estimate

Matched to OSM road/path data with match threshold 200 m:

| Class | Distance | Share |
|---|---:|---:|
| paved | 98.7 km | 20.3 % |
| unknown_likely_paved | 219.2 km | 45.0 % |
| unpaved | 56.2 km | 11.5 % |
| suspect_unpaved | 109.4 km | 22.5 % |
| unknown | 3.2 km | 0.7 % |
| unmatched | 0.4 km | 0.1 % |

Working interpretation: the route is mostly road. Our script's
"suspect_unpaved" class is an **upper bound** because it flags any
`highway=track/path/bridleway/cycleway` without explicit `surface=*`
tag, and `highway=path` in particular is often paved in Corsica
(cyclable access, rural shortcut).

### External calibration (2026-05-12)

Three independent surface estimates triangulate the truth:

| Source | Paved | Off-road | Unspecified |
|---|---:|---:|---:|
| **RWGPS** | 413 km (85 %) | **74 km (15 %)** | 0.1 km |
| **Strava** | 380 km (78 %) | 54 km (11 %) confirmed | 54 km (11 %) |
| **Our script** | 318 km (65 %) | 56 km (11.5 %) confirmed | 109 km (22 %) suspect + 3 km unknown |

Reading: the **confirmed off-road** is the same across all three at
~54-56 km. The **likely real off-road** is ~74 km (RWGPS consensus =
Strava confirmed + half of "not specified" = our confirmed + tracks
minus paths). Our script over-flags `highway=path` (~15 km of paths
that are likely paved in Corsica) which inflates "suspect_unpaved".

**Canonical figure for race planning: ~74 km off-road (~15 %).**

The Strava/RWGPS-published surface mix should be the headline number;
our `terrain_analysis.md` remains the source of truth for km-precise
sector identification (`### Key Terrain-Risk Sectors`).

### Raw vs smoothed D+

Strava reports **D+ 10 267 m** (raw) and RWGPS reports similar (~10 250 m).
Our script reports **D+ 8 946 m smoothed**. The difference (~1 320 m) is
GPS-noise filtering. Both are correct: use Strava/RWGPS for
"what the bike computer will show", use our smoothed value for "real
climbing effort".

## Aero-Eligible Sections

### Strict (|grade| ≤ 1.5 %, length ≥ 3 km)

| Km range | Length | Avg grade | Surface | Usable? |
|---:|---:|---:|---|---|
| 109.8-115.4 | 5.6 km | -0.25 % | likely paved | yes — mid-altitude window between climbs |
| 159.2-162.2 | 3.0 km | -0.51 % | **UNPAVED** | **no** — flat section but on a path |
| 300.4-304.2 | 3.8 km | -0.46 % | likely paved | yes — fresh-half post-CP2 |
| 401.2-404.4 | 3.2 km | +0.34 % | likely paved | yes — return to coast |
| 481.4-487.1 | 5.7 km | -0.16 % | likely paved | yes — but final 6 km of the race |

Total strict aero-eligible: 21.3 km / 487.1 km (4.4 %).
Clean usable (excluding km 159-162 UNPAVED): ~18 km.

### Extended (|grade| ≤ 2.5 %, length ≥ 5 km)

| Km range | Length | Avg grade | Surface |
|---:|---:|---:|---|
| 0.0-5.0 | 5.0 km | +0.95 % | likely paved |
| 6.0-12.0 | 6.0 km | -0.32 % | likely paved |
| 109.2-115.4 | 6.2 km | -0.40 % | mostly paved, brief rough |
| 208.4-214.2 | 5.8 km | -0.94 % | likely paved |
| 319.6-325.4 | 5.8 km | +0.89 % | likely paved |
| 399.6-405.0 | 5.4 km | -0.22 % | mostly paved, brief rough |
| 461.0-477.0 | 16.0 km | -0.10 % | mostly paved, brief rough |
| 478.8-487.1 | 8.3 km | -0.23 % | mostly paved, brief rough |

Total extended aero-eligible: 58.5 km / 487.1 km (12.0 %).

## Main Unpaved / Suspect Sections (≥ 1.5 km)

| Km range | Dist | Avg grade | Gain | Loss | Main highway | Main surface | Main tracktype |
|---:|---:|---:|---:|---:|---|---|---|
| 17.4-24.6 | 7.2 km | +4.2 % | +313 m | -10 m | track (5.4 km) | unknown (7.2 km) | unknown (7.2 km) |
| 32.4-42.4 | 10.0 km | +3.4 % | +405 m | -68 m | track (8.8 km) | **gravel** (7.4 km) | grade3 (7.4 km) |
| 44.8-48.8 | 3.0 km | -1.1 % | +26 m | -60 m | track (1.8 km) | unknown (3.0 km) | unknown (2.8 km) |
| 50.2-53.2 | 2.8 km | -0.9 % | +13 m | -39 m | track (2.4 km) | unknown (2.8 km) | grade3 (2.0 km) |
| 66.4-69.2 | 2.6 km | +1.7 % | +55 m | -11 m | track (2.4 km) | unknown (2.6 km) | grade2 (2.2 km) |
| 74.4-77.4 | 1.6 km | +3.1 % | +60 m | -10 m | track (1.0 km) | unknown (1.6 km) | unknown (1.6 km) |
| 136.0-148.8 | 12.4 km | +2.8 % | +442 m | -92 m | track (10.8 km) | unknown (11.6 km) | unknown (11.0 km) |
| 159.0-162.4 | 3.2 km | -0.5 % | +8 m | -25 m | path (3.0 km) | unknown (3.2 km) | unknown (3.2 km) |
| 178.2-183.6 | 5.0 km | -6.0 % | +0 m | -299 m | track (5.0 km) | unknown (3.6 km) | grade2 (2.4 km) |
| 202.6-204.8 | 2.0 km | -5.7 % | +0 m | -114 m | track (1.6 km) | unknown (2.0 km) | unknown (2.0 km) |
| 253.2-256.4 | 3.2 km | -4.5 % | +1 m | -145 m | track (2.4 km) | unknown (2.0 km) | unknown (2.0 km) |
| 287.8-292.4 | 4.4 km | +1.6 % | +114 m | -43 m | track (3.6 km) | unknown (4.4 km) | grade3 (2.4 km) |
| 308.2-310.0 | 1.6 km | +1.6 % | +25 m | -0 m | path (1.0 km) | unknown (1.6 km) | unknown (1.6 km) |
| 313.4-315.4 | 1.6 km | -5.3 % | +0 m | -85 m | track (1.6 km) | unknown (1.6 km) | grade2 (1.4 km) |
| 332.8-337.4 | 3.8 km | -1.4 % | +18 m | -71 m | path (3.4 km) | unknown (3.8 km) | unknown (3.6 km) |
| 387.8-393.2 | 5.2 km | -3.9 % | +10 m | -210 m | track (4.6 km) | unknown (5.2 km) | unknown (5.2 km) |
| 394.4-396.0 | 1.6 km | -0.3 % | +6 m | -12 m | unclassified (1.6 km) | **dirt** (1.6 km) | unknown (1.6 km) |
| 396.6-398.6 | 2.0 km | +0.3 % | +23 m | -17 m | unclassified (1.8 km) | **dirt** (1.8 km) | unknown (2.0 km) |
| 404.4-411.6 | 5.6 km | +0.7 % | +66 m | -25 m | track (5.6 km) | unknown (5.6 km) | unknown (5.6 km) |
| 417.2-419.4 | 2.2 km | **-8.5 %** | +0 m | -188 m | track (2.2 km) | unknown (2.2 km) | grade3 (1.8 km) |
| 426.4-430.8 | 4.2 km | +0.3 % | +62 m | -48 m | path (3.4 km) | unknown (4.2 km) | unknown (4.2 km) |
| 431.4-433.4 | 1.8 km | -2.7 % | +0 m | -49 m | path (1.6 km) | unknown (1.8 km) | unknown (1.8 km) |
| 440.8-454.8 | 14.0 km | -0.7 % | +522 m | -616 m | track (11.0 km) | unknown (6.4 km) | grade2 (10.6 km) |

Total listed: ~95 km of unpaved or suspect non-paved sections ≥ 1.5 km.

## Key Terrain-Risk Sectors

### 1. km 17-42 - Early Gravel/Track Climbing

- Total rough/suspect exposure: ~17 km split across km 17-25 and 33-42.
- Profile: mostly uphill, ~+718 m combined gain.
- Risk: early legs make it tempting to push, but it is too early to spend
  shoulder, grip, or tire margin.
- Plan: climb seated/controlled, avoid torque spikes, eat before the first
  rough sector.

### 2. km 136-149 - Long Suspect Climbing Track

- Length: ~12.4 km.
- Profile: +2.8 %, ~+442 m.
- Risk: long enough to become muscular and postural, especially if loose.
- Plan: treat as an endurance climb, not a race segment. Keep cadence and upper
  body relaxed.

### 3. km 178-184 - Mid-Descent Rough Section

- Length: ~5.0 km within a larger paved descent from the high point.
- Profile: -6.0 %, ~-299 m.
- Risk: high speed paved descent suddenly hits rough surface. The new
  table flags this as the longest non-paved descent block in the
  middle of Sequence B.
- Plan: shed speed BEFORE km 178. Hoods. Walk if uncertain.

### 4. km 253-256 - Dirt Descent

- Length: ~3.2 km.
- Profile: -4.5 %, ~-144 m.
- Risk: not huge, but enough for braking/line-choice mistakes.
- Plan: hoods, brake before turns, no aero/drops if surface loose.

### 5. km 313-316 - Short Steep Rough Descent

- Length: ~1.6 km at -5.3 %.
- Risk: short but steep; high pinch/slide potential if tired.
- Plan: speed cap and active bike handling.

### 6. km 388-412 - Late Mixed Track Corridor

- Total rough/suspect exposure: ~16 km (387-411 with brief paved gaps).
- Profile: mostly rolling/descending, with confirmed dirt (km 394-398)
  and grade2/3 tracks.
- Risk: late-race fatigue and repeated transitions between road/track.
- Plan: reset before entering. Eat/drink on road before the sector.

### 7. km 417-419 - Very Steep Rough Descent

- Length: ~2.2 km.
- Profile: **-8.5 %**, ~-188 m.
- Risk: the single steepest listed rough descent. High consequence if loose.
- Plan: explicit speed cap. Walking a bad subsection is a valid race tactic.

### 8. km 441-455 - Biggest Late Gravel/Track Block

- Length: ~14 km.
- Profile: rolling with large accumulated up/down (+522 / -616 m),
  including the route's most committing climb to ~942 m and its
  steepest sustained descent.
- Risk: this is the key final technical sector. It arrives late, when
  reflexes, shoulders, and nutrition discipline are degraded.
- Plan: enter fed, hydrated, and mentally reset. Ride for control, not
  speed.

## Tire Implications

The final GPX reduces the headline non-paved exposure versus the WIP
route, but with the corrected matching the script now lists ~95 km of
unpaved or suspect sectors ≥ 1.5 km (and ~166 km total when all
suspect highway=track is counted). Steep descents and a long late
gravel block remain.

Current candidate setups:

- Schwalbe G-One RS 45 mm around 2.2 / 2.0 bar.
- Continental Race King 2.2.

Working interpretation:

- G-One RS 45 mm remains the faster all-round choice if the tracks
  are dry, compact, and you are confident descending them.
- Race King 2.2 is attractive if the priority is comfort, grip, and
  reduced cognitive/shoulder load on rough sectors.
- The new surface analysis tilts the case back toward Race King: the
  total rough exposure is higher than the previous numbers suggested,
  and the new "Key Terrain-Risk Sector" km 178-184 (mid-descent rough
  in Sequence B) is an additional decision point.

## Aerobar Implications

The vfinale route surfaces ~12 % of distance as extended aero-eligible
(58.5 km), but the strict (≤ 1.5 %, ≥ 3 km) usable share is much
smaller (~18 km), and the verdict remains **leave the aerobars off**.

### Aero-eligible sections, surface-checked

See the "Aero-Eligible Sections" auto-generated tables above. The
clean strict windows are:

- **km 110-115** (5.6 km, paved) — mid-race window between climbs.
- **km 300-304** (3.8 km, paved) — fresh second half post-CP2.
- **km 401-404** (3.2 km, paved) — return-to-coast section.
- **km 481-487** (5.7 km, paved) — finish straight.

km 159-162 is flat (3 km, -0.5 %) but on path/track — **never aero**.

### Verdict

- The athlete-priority framing already established (enjoyment +
  cross-sector capability, not placement; rotator cuff history;
  Ascend Xtri 8 weeks later) overrides the small efficiency gain.
- At realistic ultra speeds (~18-22 km/h on rolling tarmac), the
  width-driven aero penalty of riding without bars is on the order of
  3-5 W per pair, not the 10+ W the original tire report suggested.
- Total time gain from aerobars on this course is on the order of
  3-6 minutes over a 30-hour event, against a real postural cost on
  the limiter.
- The extended section km 461-477 (16 km, mostly paved) is the only
  long contiguous late-race aero window, but it falls right after the
  gravel climax — exactly when the shoulders need to recover, not
  work.

**Default recommendation: leave aerobars off the bike.** If still
mounted as an option, the only credible window is km 110-115 (early
mid-race, fresh) for a 12-15 min test dose. Veto on every other
section: any climb, any descent, any rough/suspect surface, anywhere
after km 350.

## Operational Notes

### Fueling/hydration windows (eat/drink BEFORE entering)

- km 17 — first suspect track climb starts
- km 33 — confirmed gravel climb to ~977 m starts
- km 136 — long suspect track climb to ~1 275 m
- km 164 — **CP1 Ghisoni (658 m)**: refuel here for the climb to 1 291 m
- km 178 — mid-descent rough section in Sequence B
- km 240 — long paved climb to 1 066 m
- km 253 — short dirt descent
- km 313 — short steep rough descent
- km 333 — **CP2 Crocicchia (616 m)**: refuel here for the long descent
- km 388 — late mixed track corridor (~16 km)
- km 417 — steep -8.5 % rough descent
- km 433 — entry into Sequence C (gravel climax, km 440-455)

### Critical descents (paved, where you can let the bike run)

- km 99-110 (-6.2 %, 10.4 km) — longest paved steep descent
- km 195-210 (-4.9 %, 14.2 km) — longest paved descent overall
- km 343-352 (-5.3 %, 8.4 km) — post-CP2 long descent to ~150 m

### Critical descents (rough — speed cap, hoods only)

- km 178-184 (5.0 km, -6.0 %) — long rough section in middle of fast paved descent
- km 253-256 (3.2 km, -4.5 %) — dirt block
- km 313-316 (~2 km, includes -5.3 % section) — short steep track
- km 417-419 (2.2 km, **-8.5 %**) — single steepest rough descent of the route
- km 447-455 (7.0 km on confirmed gravel within the -6.4 % descent block 447-462) — steepest sustained descent of the route, at 26+ hours of effort. **Highest-consequence descent of the day.**

### Body management on listed rough sectors

- Hands near brakes; cocottes by default, never drops on track.
- No aero position on any listed rough sector.
- Eat/drink on road *before* the sector — both hands free on rough.
- Rotate position every 15-20 min on smooth tarmac to spread load on
  cervicals / trapezius / lower back; preserve shoulder for the
  climaxes (Sequence C in particular).
- If anything in shoulder/neck rises above 2/10, slow further and
  consider walking subsections of km 447-455.

### Tactical priorities (in order)

1. Arrive at km 433 with reserves (food, water, shoulder fresh).
2. Survive Sequence C km 440-462 cleanly — no crash, no mechanical.
3. Use km 99-110 and km 195-210 as the recoverable speed windows.
4. Treat early gravel km 17-42 as warm-up, not test.
5. Feed thoroughly at CP1 (km 164) and CP2 (km 333).
