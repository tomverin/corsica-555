# Tire Selection — Alternative Analysis

Generated: 2026-05-08. Revised: 2026-05-08 against the **vfinale GPX**
(`555_Corsica__2_2026_vfinale.gpx`). **Refreshed 2026-05-12** with
corrected OSM match threshold (200 m default) — the off-road exposure
of the route is higher than the first pass suggested.

Counterpart to `tyre-selection.md`, rebuilt from `terrain_analysis.md` +
GPX cross-check + athlete context. Decision-oriented.

> **2026-05-12 data refresh note.** Three sources cross-checked:
> RWGPS (74.2 km / 15 %), Strava (54 km confirmed dirt + 54 km not
> specified), and our `analyze_gpx_osm_surface.py` script (56 km
> confirmed + 109 km suspect, of which ~15 km are `highway=path` and
> likely paved). Consensus canonical figure: **~74 km of off-road
> (~15 % of distance)**. Many subsequent references in this file cite
> "72 km" / "~15 %" which is essentially correct (the original pre-fix
> figure). The Race King recommendation is unchanged.

## What Changed With The vfinale GPX

The route was previously analyzed on a 2025 WIP GPX (502.9 km, 9 974 m
D+, ~17 % non-paved, summit at 1 631 m). The final 2026 trace is
materially different:

- **Distance**: 502.9 km → **487.1 km** (-16 km).
- **D+**: 9 974 m → **9 276 m** (-700 m).
- **High point**: 1 631 m → **1 300 m** (-330 m). The old summit
  off-road block at km 397-408 is gone.
- **Non-paved exposure**: **~74 km (~15 %)** after consensus across three sources (RWGPS 74.2 km, Strava 54 km confirmed dirt + 54 km unspecified, our script 56 km confirmed + 109 km suspect of which ~15 km are `highway=path` likely paved). Earlier WIP estimate ~87 km was directionally right but the vfinale exposure consolidates at ~74 km.
- **New structural climax**: km **440-455** — a confirmed gravel
  block carrying both an **8 % climb** to 955 m and a **-8.9 %
  descent**, the steepest sustained sequence of the route, **at race
  hour 26+**.
- Two checkpoints declared: **CP1 Ghisoni km 164** (base of paved
  climb to 1 300 m) and **CP2 Crocicchia km 333**.

Net effect on tire decision: the *quantitative* off-road exposure is
slightly lower, but the *qualitative* concentration of risk is more
acute — both the steepest climb AND the steepest descent of the route
now fall on a single 14 km confirmed gravel block, late in the race.
**The Race King recommendation gets stronger, not weaker, against
this profile.**

## Verdict

**Continental Race King Protection 2.2 is the recommended tire for this
athlete on this route.**

### Stated athlete priority

The 2026 Corsica goal is not a top placement. The athlete is not at 2024
form (which would have supported a top-5 attempt) and explicitly frames
this event around **maximum enjoyment and the capacity to feel good
across all sectors**. Tarmac efficiency is one input among several, not
the dominant variable. The decision criterion is therefore: *which tire
gives the broadest envelope of comfort, safety, and confidence across
the four physical contexts of this route — paved climbs, paved descents,
rough tarmac, and Corsican granite.*

### Why the original report's verdict needs adjusting

The Schwalbe G-One RS Pro Addix 45 mm is technically defensible on a
generic paved/gravel ultra but under-weights four things specific to
this case:

1. The athlete's stated priority — enjoyment + cross-sector capability,
   not aggressive placement.
2. The geographic concentration of the most extreme grades and the
   gravel surface in a single late-race block: **km 440-455** carries
   the route's steepest climb (+8 %) and steepest descent (-8.9 %)
   on confirmed gravel, at ~26 hours of effort.
3. The athlete's documented rotator-cuff and neck durability ceiling,
   plus the fact that Corsica is event 1 of 3 in the 2026 season.
4. The realistic ultra speeds and grade distribution of this route,
   which compress the aero/rolling-resistance advantage of the semi-
   slick significantly below the cited "10+ W on tarmac" headline.

Race King 2.2 has already been ridden all winter on the same bike (Léon
La Rage), clearance is confirmed, and the athlete is familiar with the
pressure / handling profile. That removes the primary objection to the
mountain bike tire option — unfamiliarity — and tilts the cost/benefit
firmly toward durability and shoulder preservation.

### Why no intermediate option

The 47-50 mm "compromise" gravel tire category is excluded for two
explicit reasons:

- **Budget / available equipment.** Both candidate tires are already
  owned. Buying a third tire is not on the table.
- **Market reality.** Endurance-grade gravel tires (50 mm class) carry
  reinforced puncture casings that materially raise rolling resistance
  on tarmac and limit suppleness on rough surface. The marginal volume
  gain over a 45 mm semi-slick is rapidly out-classed by the Race
  King's combination of high volume, supple 180 TPI casing, and
  BlackChili compound. The compromise tire ends up worse on both ends
  of the spectrum than picking a side.

## Inputs Used

Where the original report used 490.56 km / 10 379 m / 76 % paved / 24 %
unpaved (round numbers from a different GPX), this analysis uses the
verified values from `terrain_analysis.md` against the **vfinale GPX**:

- Distance: **487.1 km**.
- Elevation: ~9 276 m gain (smoothed).
- Range: 0 m → **1 291 m** (high point reached at km 174).
- Smoothed D+: ~8 950 m (smoothing window 2).
- Grade distribution: ~37 % at |grade| ≥ 3 %, ~15 % flat (±1 %).
- Surface (OSM cross-reference at match threshold 200 m): ~20 % paved,
  ~45 % unknown_likely_paved, **~34 % confirmed/suspect non-paved
  (~166 km total; ~95 km in sections ≥ 1.5 km)**, ~0.7 % unknown,
  ~0.1 % unmatched.
- Major non-paved blocks (vfinale):
  - **Sequence A** km 12-42 (early gravel chain, ~16.5 km cumulative)
  - **Sequence B** km 137-180 (CP1 approach + 1.6 km transition rough
    in middle of fast paved descent at km 178-180)
  - **Sequence C** km 440-455 (~14 km gravel, late-race climax)
  - Plus shorter rough sections at km 253-256, 313-316, 389-411,
    417-419.
- Checkpoints: **CP1 Ghisoni km 164 (alt 658 m)**, **CP2 Crocicchia
  km 333 (alt 616 m)**. Both projected from GPX `wpt` with offset ≤ 45 m.
- Aerobars: not mounted (separate decision in `terrain_analysis.md`).
- Bike: Léon La Rage titanium gravel — Race King 2.2 clearance OK
  (confirmed by athlete, ridden all winter).

Athlete context (from `context.md` / `decisions.md` + 2026-05-08
priority statement):

- Patellofemoral pain history (knee).
- Rotator cuff tendinopathy 2024-2025, treated since October 2025.
  **Current key limiter is shoulder / neck / upper-back durability.**
- Goal events: Corsica 2026-05-29, Ascend Xtri 2026-07-25, TPR
  September 2026.
- Stated training decision: "Prioritize arriving at Corsica with a
  calm shoulder and neck."
- Race objective for Corsica: **maximum enjoyment, capacity to feel
  good across all sectors**. Not a top-placement attempt; current form
  is below 2024 peak.

## Energy Budget — Re-Modeled With Realistic Ultra Speeds

The original report cites width-driven aero penalties at 30-45 km/h.
For a ~30 hour event with ~8 950 m of (smoothed) climbing on degraded
Corsican tarmac, the realistic speed distribution is much lower.

Modeled from the vfinale grade distribution (in `terrain_analysis.md`):

| Sector | Distance | Avg speed | Time |
|---|---:|---:|---:|
| Climbs (≥ +3 %) | ~133 km | 11 km/h | 12.0 h |
| Rolling tarmac (-3 to +3 %) | ~140 km | 22 km/h | 6.4 h |
| Descents tarmac (≤ -3 %, paved) | ~110 km | 30 km/h | 3.7 h |
| Off-road (gravel/piste, all gradients) | ~72 km | 14 km/h | 5.1 h |
| Excluded overlap correction | -32 km | — | -1.5 h |
| **Moving total** | **~487 km** | | **~25.7 h** |

Stops add ~4-6 h → finish window ~30-32 h, consistent with mid-pack
BikingMan Corsica 555 references and the athlete's stated objective
(enjoyment, not placement).

### Time-weighted exposure beats distance-weighted

A critical reframing: **gravel sectors are intrinsically slower than
tarmac sectors, so their share of moving time is larger than their
share of distance.**

| Sector | Distance share | Time share |
|---|---:|---:|
| Tarmac (paved cumulative) | ~85 % (415 km) | ~80 % (~20.6 h) |
| Off-road (gravel + piste) | **~15 % (72 km)** | **~20 % (~5.1 h)** |

If current form pushes the gravel speed lower (say 12 km/h average
instead of 14 km/h, plausible on the 8 % gravel climb at km 440 after
26 h of effort), off-road time exposure rises to **~23 % of moving
time**. Either way, the rider spends a notably larger share of the
*experienced* race on rough surface than the 15 % distance headline
suggests.

This shifts the cost/benefit further toward Race King:

- The G-One RS tarmac advantage is consumed during the **~80 % of time
  spent on paved**, where the per-hour delta is small (~3-5 W).
- The Race King off-road advantage applies during **~20-23 % of time
  spent on rough surface**, where the per-hour delta is larger
  (~5-10 W) AND where vibration / cognitive load / crash risk all
  concentrate.
- Sequence C alone (km 440-455) is ~1.0-1.2 h of continuous gravel at
  high gradient and high cognitive load. The tire that lets the rider
  finish that hour with reserve, not depleted, materially changes the
  last 32 km to the finish.

### Power deltas, paire de pneus, by sector type

Numbers below are mid-range from BicycleRollingResistance lab data,
Swiss Side aero tests, and field reports cross-checked with the
athlete's weight (~80 kg system mass).

| Sector type | G-One RS 45 mm | Race King 2.2 | Δ for Race King |
|---|---:|---:|---:|
| Smooth tarmac (~20 km/h, ~250 km) | baseline | +3 to +5 W aero+squirm | **-3 to -5 W** |
| Rough/degraded tarmac (~20 km/h, ~165 km) | +1 to +3 W vibration | baseline | **+1 to +3 W** |
| Off-road, granite (~14 km/h, ~72 km) | +5 to +10 W impedance | baseline | **+5 to +10 W** |

Translating to energy:

| Sector type | Time | Δ Race King | Energy Δ |
|---|---:|---:|---:|
| Smooth tarmac | ~10.0 h | -4 W mid | -40 W·h |
| Rough tarmac | ~10.6 h | +2 W mid | +21 W·h |
| Off-road | ~5.1 h | +7 W mid | +36 W·h |
| **Net** | | | **+17 W·h** |

The energy delta is essentially **a wash** within modeling error.
At ~280 W average climbing power, ±30 W·h is ±6-7 minutes over the
whole race. The "Race King costs you hundreds of kilojoules on
tarmac" framing of the original report does not survive realistic
speeds and the actual rough/smooth split of Corsican infrastructure.

Compared with the WIP-GPX modeling (which gave a near-zero net), the
vfinale shifts the energy balance very slightly toward G-One RS — by
roughly **3-4 minutes over a 30 h event**. This is well below the
threshold of the risk and durability arguments that follow.

The aero advantage of the G-One RS is real but small at 18-22 km/h
and is partially offset by Race King's better vibration absorption on
degraded tarmac. The off-road advantage of Race King is real and
meaningful on the 72 km of confirmed/suspect surface.

## Risk Budget — The Real Differentiator

Energy budgets being roughly equivalent, **the decision is dominated by
risk and athlete durability**, not by power.

### Crash risk

vfinale GPX cross-reference. Time-of-race assumes ~17 km/h average
overall pace.

| Sector | Surface | Time-of-race | G-One RS | Race King |
|---|---|---|---|---|
| **Sequence A** km 17-42 | 16.5 km cumulative track + confirmed gravel climb (33-42, +405 m at 4.2 %) | ~h+1-3 | manageable, legs fresh | excellent |
| Sequence B (transition) km 178-180 | 1.6 km rough section in middle of -7.3 % paved descent | ~h+13-14 | high risk if speed not pre-shed | safe |
| km 137-146 | 9.9 km suspect track climb to ~1 276 m | ~h+11 | OK uphill, slow | very safe |
| km 253-256 | 3.3 km dirt descent -4.4 % | ~h+18 | risky braking | excellent |
| km 313-316 | ~2 km steep rough descent (incl. -6.3 %) | ~h+22 | risky if tired | safe |
| km 389-411 | 13.5 km cumulative late mixed track corridor | ~h+25 | risky | safe |
| km 417-419 | 2 km gravel descent **-8.7 %** | ~h+28 | very risky | manageable |
| **Sequence C** km 440-455 | **14 km confirmed gravel: +8 % climb to 955 m, then -8.9 % descent** | **~h+26-29** | **highest race risk on G-One RS** | **manageable** |

The Sequence C corridor (km 440-455) is the structural risk
concentration of the event in the vfinale GPX:

- It carries **both** the steepest sustained climb (+8 %) **and** the
  steepest sustained descent (-8.9 %) of the route, back-to-back.
- It is **fully on confirmed gravel**, not mixed.
- It arrives **late** (race hour ~26-29) when sleep deficit, shoulder
  fatigue, and judgment are degraded.
- New on this route vs the WIP version: **the climb side is gravel
  too**. On a semi-slick at 8 % out of the saddle on loose granite,
  rear-wheel traction breaks well before peak power. Unlike the WIP
  layout (paved climb / gravel descent), the rider here cannot
  "save" the climb on tarmac and only manage the descent — both
  halves require the gripped tire.
- On the descent side: hard braking on a semi-slick over loose
  granite breaks static friction instantly. On Race King's
  continuous low-block tread, mechanical bite is preserved at any
  lean angle.

A race-ending crash or sidewall laceration at km 450 erases any
energy advantage from the previous 450 km. The post-Sequence-C
descent and finish (km 455-487) is rolling/flat and adds almost
nothing to the rider's options if anything goes wrong before km 455.

### Mechanical risk

- G-One RS thin slick center tread (2.10-2.30 mm casing) on Corsican
  granite = real exposure to square-edged rock strikes. Survivable
  with line discipline, but line discipline at 26 h of effort is the
  exact thing that fails.
- Race King 2.2 has thicker tread blocks acting as armor and a
  Protection sidewall layer designed for this exact failure mode.
- Both should be run tubeless with plug kit, tube, boot, and CO2 + mini
  pump regardless.

### Postural / shoulder risk

This is the dimension the original report dismisses in two sentences
under "vibration damping", and it is precisely the athlete's main
limiter.

- Vibration transmission over 30 h on a 45 mm tire at 2.0-2.2 bar on
  degraded tarmac and granite is a **continuous postural load** on the
  cervical / trapezius / rotator cuff chain.
- Race King at 1.8-2.0 bar with 55 mm volume operates as a passive
  suspension, materially reducing high-frequency vibration to the
  hands and shoulders.
- The cost of arriving at Ascend Xtri (2026-07-25, 8 weeks after
  Corsica) with a flared shoulder is not a marginal cost. It is the
  loss of objective #2 in the season.
- The cost of arriving at TPR (September 2026) under-recovered is the
  loss of objective #3.

This is not an abstract durability point. Given this athlete's history,
**Race King's vibration damping is a primary performance feature for
the season, not a comfort luxury for one event.**

### Cognitive load

Descending unfamiliar Corsican mountain roads at 24-28 hours of sleep
deprivation requires the rider to spend cognitive resources on line
choice, surface reading, and braking timing. The Race King's
predictable grip envelope reduces this cognitive expense significantly,
preserving decision-making bandwidth for fueling, navigation, and
pacing in the final 100 km.

## Tire Comparison Summary

Criteria weighted by the athlete's stated priority (enjoyment +
cross-sector capability + season-level durability), not by absolute
finish time.

| Criterion | Weight (this case) | G-One RS 45 mm | Race King 2.2 |
|---|---|---|---|
| Tarmac efficiency | Low-Medium | **+** | - |
| Off-road efficiency (72 km, ~5 h) | Medium-High | - | **+** |
| Off-road traction on 8 % gravel climb (km 440-447) | **Critical** | - | **+++** |
| Off-road braking on -8.9 % gravel descent (km 447-455) | **Critical** | - | **+++** |
| Vibration damping (shoulder, ~30 h) | **Critical** | - | **+++** |
| Crash risk Sequence C (km 440-455) | **Critical** | - | **+++** |
| Sidewall puncture immunity | High | - | **++** |
| Aero (no aerobars, low avg speed) | Low | + | - |
| Familiarity (winter tested) | High | n/a | **+++** (already mounted/tested) |
| Cognitive comfort on descents | High (enjoyment goal) | - | **++** |
| Climbing rotational mass | Negligible | + | - |
| Energy budget over full race | Low (delta ~6-12 min) | tie | tie |

When weighted by what actually matters for **this athlete**, on **this
route**, with **this season ahead**, **and with enjoyment as the
declared priority**, Race King wins on every high-weight criterion.

## Recommendation

### Primary: Race King 2.2 Protection

Reasons, in order of weight against the athlete's stated priority:

1. **Best fit for "enjoyment + capability across all sectors."** The
   tire that gives the broadest envelope of confidence on every
   surface this route presents — paved climbs, paved descents, rough
   tarmac, granite gravel — is the one that maximizes the lived
   quality of 30+ hours on the bike.
2. Best fit for the athlete's shoulder/neck durability ceiling, with
   meaningful vibration damping over ~5 h of off-road exposure and
   ~21 h of variable tarmac.
3. Best fit for the route's actual risk concentration: Sequence C
   km 440-455, the gravel block carrying both the steepest climb (+8 %)
   and the steepest descent (-8.9 %) of the route at race hour 26-29.
4. Already validated by an entire winter of riding on the same bike →
   no late-cycle equipment risk, no purchase needed.
5. Energy penalty on tarmac is small (~3-6 min worst case over 30 h),
   and partially recovered on the 72 km of off-road. Well within the
   modeling error.
6. Aero argument is largely neutralized by the absence of aerobars and
   by realistic ultra speeds on this terrain.

### Setup

- Pressure: ~1.8 bar front / 1.7 bar rear at ~80 kg system mass on
  Léon La Rage. Adjust ±0.1 bar after the validation ride based on
  cornering feel and rim-strike margin.
- Tubeless mandatory. Refresh sealant within 4-6 weeks of race day.
- Carry: 2 plugs of each size, 1 spare tube (matched valve length),
  tire boot, valve core tool, mini pump + 2× CO2.

### Validation protocol before Corsica

1. **One 4-5 h ride on Race King at race pressure** on terrain with
   both rough tarmac and gravel descents. Saturday 2026-05-09 ride
   fits this purpose if shoulder/HRV is green. Specifically test:
   - Out-of-saddle acceleration on gravel at >7 % (proxy for the
     km 440-447 climb).
   - Hard braking on loose surface at >5 % (proxy for the km 447-455
     descent and km 417-419 -8.7 %).
2. **H+24 shoulder/neck/hand check.** Anything > 1/10 means review
   pressure (try -0.1 bar) or extend the test before committing.
3. **Final test 8-10 days before race** during taper week — short
   30-45 min ride on Race King to confirm bike fit and shoulder
   tolerance with current setup.

### When G-One RS would still make sense

Given the athlete's stated priority, the cases where G-One RS would
override Race King are narrow:

- A late season change makes durability for Ascend / TPR irrelevant
  (e.g., one of those events is dropped from the calendar) AND the
  athlete shifts to a placement-driven race plan.
- Race-day forecast confirms fully dry conditions across the entire
  route AND the gravel sectors are reported by recent race traffic as
  unusually clean — a rare combination for Corsica in late May.

Under the stated objective (enjoyment + cross-sector capability), none
of these conditions is currently expected, and the G-One RS option is
not the working plan.

## What This Analysis Does Not Cover

- Wet-weather behavior. If forecast turns to consistent rain, Race King
  edge knobs are a clear additional safety margin; G-One RS becomes
  significantly worse.
- Wheel/rim aero pairing. Both tires are on a wide gravel rim;
  aerodynamic interaction with deep-section wheels is not modeled.
- Drivetrain efficiency (tire weight effect on chain tension during
  out-of-saddle climbing) — assumed negligible.

## Bottom Line

The original report optimized for a slightly faster average split on
paved sectors at the cost of accepting elevated crash, mechanical, and
postural risk on the unpaved sectors and beyond.

For an athlete whose declared 2026 Corsica objective is **maximum
enjoyment and the capacity to feel good across all sectors**, who is
not chasing a 2024-form placement, and who has two more goal events
in the following four months, that trade-off is unfavorable.

When the analysis is run in time-weighted rather than distance-weighted
terms, the off-road exposure expands from 15 % of distance to **20-23 %
of moving time** — about 5 hours on rough granite that the rider will
*experience* rather than just *cross*. Tire choice for those hours is
a primary determinant of the rider's experience, not a secondary one.

The vfinale GPX concentrates the most consequential 14 km of those
hours into a single late-race gravel block (Sequence C, km 440-455)
that carries both the steepest climb and the steepest descent of the
route. That block, more than any other single feature of the course,
is what the tire selection has to optimize for.

**Mount the Race Kings. Test the pressure on Saturday's 4-5 h ride
including out-of-saddle gravel climbing at >7 % and hard braking on
loose descent. Confirm shoulder tolerance H+24. Race them.**
