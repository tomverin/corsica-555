#!/usr/bin/env python3
"""Analyse GPX grade and OSM surface/highway tags.

The GPX format usually contains geometry and elevation, but no surface data.
This script queries OpenStreetMap through Overpass, matches each resampled GPX
segment to the closest OSM way, then summarizes likely paved/unpaved sections.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EARTH_RADIUS_M = 6_371_000.0
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

GRADE_BUCKETS = [
    ("<= -6 %", float("-inf"), -6.0),
    ("-6 to -3 %", -6.0, -3.0),
    ("-3 to -1 %", -3.0, -1.0),
    ("-1 to +1 %", -1.0, 1.0),
    ("+1 to +3 %", 1.0, 3.0),
    ("+3 to +6 %", 3.0, 6.0),
    (">= +6 %", 6.0, float("inf")),
]


@dataclass(frozen=True)
class Point:
    lat: float
    lon: float
    ele: float
    dist_m: float = 0.0


@dataclass
class WaySegment:
    way_id: int
    ax: float
    ay: float
    bx: float
    by: float
    tags: dict[str, str]


def haversine_m(a: Point, b: Point) -> float:
    lat1 = math.radians(a.lat)
    lat2 = math.radians(b.lat)
    dlat = math.radians(b.lat - a.lat)
    dlon = math.radians(b.lon - a.lon)
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.atan2(math.sqrt(h), math.sqrt(1 - h))


def project(lat: float, lon: float, lat0: float) -> tuple[float, float]:
    return (lon * 111_320.0 * math.cos(math.radians(lat0)), lat * 110_540.0)


def point_segment_distance_m(px: float, py: float, seg: WaySegment) -> float:
    vx = seg.bx - seg.ax
    vy = seg.by - seg.ay
    wx = px - seg.ax
    wy = py - seg.ay
    length2 = vx * vx + vy * vy
    if length2 == 0:
        return math.hypot(px - seg.ax, py - seg.ay)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / length2))
    cx = seg.ax + t * vx
    cy = seg.ay + t * vy
    return math.hypot(px - cx, py - cy)


def local_name(tag: str) -> str:
    """Strip XML namespace from a tag, e.g. '{ns}trkpt' -> 'trkpt'."""
    return tag.rsplit("}", 1)[-1]


def parse_gpx(path: Path) -> list[Point]:
    root = ET.parse(path).getroot()
    points: list[Point] = []
    for point_el in root.iter():
        if local_name(point_el.tag) not in {"trkpt", "rtept"}:
            continue
        ele_text = None
        for child in point_el:
            if local_name(child.tag) == "ele":
                ele_text = child.text
                break
        points.append(
            Point(
                lat=float(point_el.attrib["lat"]),
                lon=float(point_el.attrib["lon"]),
                ele=float(ele_text) if ele_text else 0.0,
            )
        )
    return points


def combine_points(paths: Iterable[Path]) -> list[Point]:
    combined: list[Point] = []
    total_dist = 0.0
    previous: Point | None = None
    for path in paths:
        for point in parse_gpx(path):
            if previous is not None:
                total_dist += haversine_m(previous, point)
            combined.append(Point(point.lat, point.lon, point.ele, total_dist))
            previous = point
    return combined


def resample(points: list[Point], step_m: float) -> list[Point]:
    if not points:
        return []
    samples = [points[0]]
    target = step_m
    for a, b in zip(points, points[1:]):
        segment_m = b.dist_m - a.dist_m
        if segment_m <= 0:
            continue
        while target <= b.dist_m:
            ratio = (target - a.dist_m) / segment_m
            samples.append(
                Point(
                    lat=a.lat + ratio * (b.lat - a.lat),
                    lon=a.lon + ratio * (b.lon - a.lon),
                    ele=a.ele + ratio * (b.ele - a.ele),
                    dist_m=target,
                )
            )
            target += step_m
    if samples[-1].dist_m < points[-1].dist_m:
        samples.append(points[-1])
    return samples


def smooth_elevation(points: list[Point], radius: int) -> list[Point]:
    if radius <= 0:
        return points
    smoothed: list[Point] = []
    for i, point in enumerate(points):
        lo = max(0, i - radius)
        hi = min(len(points), i + radius + 1)
        ele = sum(p.ele for p in points[lo:hi]) / (hi - lo)
        smoothed.append(Point(point.lat, point.lon, ele, point.dist_m))
    return smoothed


# ---------------------------------------------------------------------------
# Elevation-derived structured features: climbs, descents, aero, profile
# ---------------------------------------------------------------------------


def compute_local_grades(samples: list[Point], span_m: float = 300.0) -> list[float]:
    """Centered-window grade at each sample, in percent.

    For each sample i, walks back to span_m/2 and forward to span_m/2 along
    the route, then computes (delta_ele / delta_dist) * 100.
    """
    n = len(samples)
    if n < 2:
        return [0.0] * n
    grades = [0.0] * n
    for i in range(n):
        a, b = i, i
        while a > 0 and samples[i].dist_m - samples[a].dist_m < span_m / 2:
            a -= 1
        while b < n - 1 and samples[b].dist_m - samples[i].dist_m < span_m / 2:
            b += 1
        dx = samples[b].dist_m - samples[a].dist_m
        if dx < 1.0:
            grades[i] = 0.0
        else:
            grades[i] = (samples[b].ele - samples[a].ele) / dx * 100.0
    return grades


def _detect_grade_runs(
    samples: list[Point],
    grades: list[float],
    start_grade: float,
    extend_grade: float,
    descending: bool,
) -> list[tuple[int, int]]:
    """Find index ranges (i, j) where grade meets start_grade and stays
    above extend_grade (or below, if descending).

    The range is inclusive on the left, exclusive on the right (Python style).
    """
    runs: list[tuple[int, int]] = []
    n = len(samples)
    i = 0
    while i < n:
        if descending:
            in_start = grades[i] <= start_grade
        else:
            in_start = grades[i] >= start_grade
        if not in_start:
            i += 1
            continue
        j = i + 1
        while j < n:
            if descending:
                if grades[j] > extend_grade:
                    break
            else:
                if grades[j] < extend_grade:
                    break
            j += 1
        runs.append((i, j))
        i = j + 1
    return runs


def detect_climbs(
    samples: list[Point],
    grades: list[float],
    min_km: float = 1.5,
    min_gain: float = 60.0,
    start_grade: float = 2.5,
    extend_grade: float = 1.0,
) -> list[dict]:
    """Detect climbs as contiguous runs above start_grade, extending while
    grade stays above extend_grade. Filter by min length and min gain.
    """
    climbs: list[dict] = []
    for i, j in _detect_grade_runs(samples, grades, start_grade, extend_grade, descending=False):
        if j <= i:
            continue
        start = samples[i]
        end = samples[min(j, len(samples) - 1)]
        length_km = (end.dist_m - start.dist_m) / 1000
        gain_m = end.ele - start.ele
        if length_km < min_km or gain_m < min_gain:
            continue
        climbs.append(
            {
                "start_km": start.dist_m / 1000,
                "end_km": end.dist_m / 1000,
                "length_km": length_km,
                "gain_m": gain_m,
                "top_alt_m": end.ele,
                "avg_grade_pct": (gain_m / (length_km * 1000) * 100) if length_km > 0 else 0.0,
            }
        )
    return climbs


def detect_descents(
    samples: list[Point],
    grades: list[float],
    min_km: float = 1.5,
    min_loss: float = 60.0,
    start_grade: float = -2.5,
    extend_grade: float = -1.0,
) -> list[dict]:
    """Detect descents as contiguous runs below start_grade (a negative
    number), extending while grade stays below extend_grade.
    """
    descents: list[dict] = []
    for i, j in _detect_grade_runs(samples, grades, start_grade, extend_grade, descending=True):
        if j <= i:
            continue
        start = samples[i]
        end = samples[min(j, len(samples) - 1)]
        length_km = (end.dist_m - start.dist_m) / 1000
        loss_m = start.ele - end.ele
        if length_km < min_km or loss_m < min_loss:
            continue
        descents.append(
            {
                "start_km": start.dist_m / 1000,
                "end_km": end.dist_m / 1000,
                "length_km": length_km,
                "loss_m": loss_m,
                "bottom_alt_m": end.ele,
                "avg_grade_pct": -(loss_m / (length_km * 1000) * 100) if length_km > 0 else 0.0,
            }
        )
    return descents


def detect_aero_sections(
    samples: list[Point],
    grades: list[float],
    max_grade_abs: float = 1.5,
    min_len_km: float = 3.0,
) -> list[dict]:
    """Detect aero-eligible sections: contiguous samples where |grade| stays
    below max_grade_abs, of total length >= min_len_km.
    """
    sections: list[dict] = []
    n = len(samples)
    i = 0
    while i < n:
        if abs(grades[i]) > max_grade_abs:
            i += 1
            continue
        j = i
        while j < n and abs(grades[j]) <= max_grade_abs:
            j += 1
        start = samples[i]
        end = samples[min(j - 1, n - 1)]
        length_km = (end.dist_m - start.dist_m) / 1000
        if length_km >= min_len_km:
            elev_delta = end.ele - start.ele
            sections.append(
                {
                    "start_km": start.dist_m / 1000,
                    "end_km": end.dist_m / 1000,
                    "length_km": length_km,
                    "start_alt_m": start.ele,
                    "end_alt_m": end.ele,
                    "avg_grade_pct": (elev_delta / max(length_km * 1000, 1)) * 100,
                }
            )
        i = j + 1
    return sections


def elevation_profile(samples: list[Point], step_km: float = 25.0) -> list[dict]:
    """Sample the elevation profile at every step_km along the route, plus the
    final point. Returns a list of {km, ele_m}.
    """
    if not samples:
        return []
    profile: list[dict] = []
    target_km = 0.0
    total_km = samples[-1].dist_m / 1000
    for sample in samples:
        sample_km = sample.dist_m / 1000
        if sample_km >= target_km:
            profile.append({"km": target_km, "ele_m": sample.ele})
            target_km += step_km
            if target_km > total_km:
                break
    last = samples[-1]
    last_km = last.dist_m / 1000
    if not profile or abs(profile[-1]["km"] - last_km) > 0.5:
        profile.append({"km": last_km, "ele_m": last.ele})
    return profile


# ---------------------------------------------------------------------------
# Waypoints (CP / POI / generic markers from <wpt>)
# ---------------------------------------------------------------------------


def parse_waypoints(paths: Iterable[Path]) -> list[dict]:
    """Extract <wpt> elements (name, type, comment, lat/lon) from one or
    more GPX files.
    """
    waypoints: list[dict] = []
    for path in paths:
        root = ET.parse(path).getroot()
        for wpt in root.iter():
            if local_name(wpt.tag) != "wpt":
                continue
            name = ""
            wtype = ""
            comment = ""
            for child in wpt:
                tag = local_name(child.tag)
                text = (child.text or "").strip()
                if not text:
                    continue
                if tag == "name":
                    name = text
                elif tag == "type":
                    wtype = text
                elif tag == "cmt":
                    comment = text
                elif tag == "desc" and not comment:
                    comment = text
            waypoints.append(
                {
                    "lat": float(wpt.attrib["lat"]),
                    "lon": float(wpt.attrib["lon"]),
                    "name": name,
                    "type": wtype,
                    "comment": comment,
                }
            )
    return waypoints


def locate_waypoints(
    waypoints: list[dict],
    samples: list[Point],
    max_offset_m: float = 200.0,
) -> list[dict]:
    """For each waypoint, find the nearest sample on the route and attach
    km, nearest elevation, and offset_m. Drops waypoints farther than
    max_offset_m from the route.
    """
    if not samples or not waypoints:
        return []
    located: list[dict] = []
    for wpt in waypoints:
        wpt_point = Point(wpt["lat"], wpt["lon"], 0.0)
        best_i = 0
        best_d = float("inf")
        for i, sample in enumerate(samples):
            d = haversine_m(wpt_point, sample)
            if d < best_d:
                best_d = d
                best_i = i
        if best_d > max_offset_m:
            continue
        nearest = samples[best_i]
        located.append(
            {
                **wpt,
                "km": nearest.dist_m / 1000,
                "nearest_alt_m": nearest.ele,
                "offset_m": best_d,
            }
        )
    located.sort(key=lambda w: w["km"])
    return located


# ---------------------------------------------------------------------------
# Cross-reference between climbs/descents/aero and surface sections
# ---------------------------------------------------------------------------


def cross_reference_surface(
    start_km: float,
    end_km: float,
    sections: list[dict],
    min_overlap_km: float = 0.3,
) -> str:
    """Describe how a [start_km, end_km] feature window overlaps the merged
    unpaved/suspect sections. Returns a short human-readable label suitable
    for a Markdown table cell.
    """
    feature_len = max(end_km - start_km, 0.01)
    overlaps: list[tuple[dict, float]] = []
    for section in sections:
        a = max(start_km, section["start_km"])
        b = min(end_km, section["end_km"])
        overlap = b - a
        if overlap >= min_overlap_km:
            overlaps.append((section, overlap))
    if not overlaps:
        return "likely paved"
    total_overlap = sum(o for _, o in overlaps)
    ratio = total_overlap / feature_len
    refs = ", ".join(
        f"{s['start_km']:.1f}-{s['end_km']:.1f}" for s, _ in overlaps
    )
    if ratio >= 0.8:
        return f"**UNPAVED** ({refs})"
    if ratio >= 0.3:
        return f"partial unpaved ({refs})"
    return f"mostly paved, brief rough ({refs})"


def overpass_query(south: float, west: float, north: float, east: float, timeout_s: int, retries: int = 2) -> dict:
    query = f"""
[out:json][timeout:{timeout_s}];
(
  way["highway"]({south:.6f},{west:.6f},{north:.6f},{east:.6f});
);
out body;
>;
out skel qt;
"""
    data = urllib.parse.urlencode({"data": query}).encode()
    request = urllib.request.Request(OVERPASS_URL, data=data, headers={"User-Agent": "training-journal-osm-surface/1.0"})
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout_s + 30) as response:
                return json.loads(response.read().decode())
        except Exception as exc:  # noqa: BLE001 - keep stdlib-only script resilient.
            last_error = exc
            if attempt < retries:
                time.sleep(2.0 + attempt * 3.0)
    raise last_error


def split_box(south: float, west: float, north: float, east: float) -> list[tuple[float, float, float, float]]:
    mid_lat = (south + north) / 2
    mid_lon = (west + east) / 2
    return [
        (south, west, mid_lat, mid_lon),
        (south, mid_lon, mid_lat, east),
        (mid_lat, west, north, mid_lon),
        (mid_lat, mid_lon, north, east),
    ]


def route_chunks(points: list[Point], chunk_km: float) -> list[list[Point]]:
    chunks: list[list[Point]] = []
    current: list[Point] = []
    start_dist = points[0].dist_m if points else 0.0
    for point in points:
        if current and (point.dist_m - start_dist) / 1000.0 > chunk_km:
            chunks.append(current)
            current = [current[-1], point]
            start_dist = current[0].dist_m
        else:
            current.append(point)
    if current:
        chunks.append(current)
    return chunks


def load_or_fetch_osm(points: list[Point], cache_path: Path, timeout_s: int, chunk_km: float | None = None) -> dict:
    if cache_path.exists():
        return json.loads(cache_path.read_text())

    all_elements: dict[tuple[str, int], dict] = {}

    if chunk_km:
        boxes = []
        for chunk in route_chunks(points, chunk_km):
            margin = 0.015
            boxes.append(
                (
                    min(p.lat for p in chunk) - margin,
                    min(p.lon for p in chunk) - margin,
                    max(p.lat for p in chunk) + margin,
                    max(p.lon for p in chunk) + margin,
                )
            )
    else:
        margin = 0.01
        south = min(p.lat for p in points) - margin
        north = max(p.lat for p in points) + margin
        west = min(p.lon for p in points) - margin
        east = max(p.lon for p in points) + margin
        boxes = []
        slices = 3
        for i in range(slices):
            w = west + (east - west) * i / slices
            e = west + (east - west) * (i + 1) / slices
            boxes.append((south, w, north, e))

    for idx, (south, west, north, east) in enumerate(boxes, start=1):
        print(f"Fetching OSM box {idx}/{len(boxes)}...", file=sys.stderr)
        try:
            payloads = [overpass_query(south, west, north, east, timeout_s)]
        except Exception as exc:  # noqa: BLE001
            print(f"  box failed ({exc}); retrying as 4 smaller boxes", file=sys.stderr)
            payloads = []
            for sub_idx, box in enumerate(split_box(south, west, north, east), start=1):
                print(f"  fetching sub-box {sub_idx}/4", file=sys.stderr)
                payloads.append(overpass_query(*box, timeout_s))
        for payload in payloads:
            for element in payload.get("elements", []):
                key = (element.get("type", ""), int(element.get("id", 0)))
                all_elements[key] = element
        time.sleep(0.5)

    result = {"elements": list(all_elements.values())}
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(json.dumps(result))
    return result


def build_way_segments(osm: dict, lat0: float) -> list[WaySegment]:
    nodes: dict[int, tuple[float, float]] = {}
    ways: list[dict] = []
    for element in osm.get("elements", []):
        if element.get("type") == "node":
            nodes[int(element["id"])] = (float(element["lat"]), float(element["lon"]))
        elif element.get("type") == "way":
            ways.append(element)

    segments: list[WaySegment] = []
    for way in ways:
        tags = way.get("tags", {})
        refs = way.get("nodes", [])
        for a_ref, b_ref in zip(refs, refs[1:]):
            if a_ref not in nodes or b_ref not in nodes:
                continue
            alat, alon = nodes[a_ref]
            blat, blon = nodes[b_ref]
            ax, ay = project(alat, alon, lat0)
            bx, by = project(blat, blon, lat0)
            segments.append(WaySegment(int(way["id"]), ax, ay, bx, by, tags))
    return segments


def classify(tags: dict[str, str] | None) -> str:
    if not tags:
        return "unmatched"
    highway = tags.get("highway", "")
    surface = tags.get("surface", "")
    tracktype = tags.get("tracktype", "")

    paved_surfaces = {"asphalt", "paved", "concrete", "concrete:plates", "concrete:lanes", "sett", "paving_stones"}
    unpaved_surfaces = {
        "unpaved",
        "gravel",
        "fine_gravel",
        "dirt",
        "earth",
        "ground",
        "grass",
        "sand",
        "mud",
        "compacted",
        "pebblestone",
        "woodchips",
    }

    if surface in paved_surfaces:
        return "paved"
    if surface in unpaved_surfaces:
        return "unpaved"
    if highway in {"track", "path", "bridleway", "cycleway"}:
        if tracktype and tracktype not in {"grade1"}:
            return "unpaved"
        return "suspect_unpaved"
    if highway in {"motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential", "service", "living_street"}:
        return "unknown_likely_paved"
    return "unknown"


def build_spatial_index(way_segments: list[WaySegment], cell_m: float = 500.0) -> dict[tuple[int, int], list[WaySegment]]:
    index: dict[tuple[int, int], list[WaySegment]] = defaultdict(list)
    for segment in way_segments:
        min_x = min(segment.ax, segment.bx)
        max_x = max(segment.ax, segment.bx)
        min_y = min(segment.ay, segment.by)
        max_y = max(segment.ay, segment.by)
        ix0 = math.floor(min_x / cell_m)
        ix1 = math.floor(max_x / cell_m)
        iy0 = math.floor(min_y / cell_m)
        iy1 = math.floor(max_y / cell_m)
        for ix in range(ix0, ix1 + 1):
            for iy in range(iy0, iy1 + 1):
                index[(ix, iy)].append(segment)
    return index


def nearby_segments(
    index: dict[tuple[int, int], list[WaySegment]],
    px: float,
    py: float,
    cell_m: float = 500.0,
    radius_cells: int = 1,
) -> list[WaySegment]:
    ix = math.floor(px / cell_m)
    iy = math.floor(py / cell_m)
    candidates: list[WaySegment] = []
    seen: set[int] = set()
    for dx in range(-radius_cells, radius_cells + 1):
        for dy in range(-radius_cells, radius_cells + 1):
            for segment in index.get((ix + dx, iy + dy), []):
                key = id(segment)
                if key not in seen:
                    candidates.append(segment)
                    seen.add(key)
    return candidates


def matched_segments(samples: list[Point], way_segments: list[WaySegment], threshold_m: float) -> list[dict]:
    lat0 = sum(p.lat for p in samples) / len(samples)
    spatial_index = build_spatial_index(way_segments)
    matched: list[dict] = []
    for a, b in zip(samples, samples[1:]):
        mid_lat = (a.lat + b.lat) / 2
        mid_lon = (a.lon + b.lon) / 2
        px, py = project(mid_lat, mid_lon, lat0)
        best: WaySegment | None = None
        best_dist = float("inf")
        candidates = nearby_segments(spatial_index, px, py, radius_cells=1)
        if not candidates:
            candidates = nearby_segments(spatial_index, px, py, radius_cells=3)
        for segment in candidates:
            distance = point_segment_distance_m(px, py, segment)
            if distance < best_dist:
                best_dist = distance
                best = segment
        tags = best.tags if best is not None and best_dist <= threshold_m else None
        dist_km = (b.dist_m - a.dist_m) / 1000
        gain_m = max(0.0, b.ele - a.ele)
        loss_m = max(0.0, a.ele - b.ele)
        matched.append(
            {
                "start_km": a.dist_m / 1000,
                "end_km": b.dist_m / 1000,
                "dist_km": dist_km,
                "gain_m": gain_m,
                "loss_m": loss_m,
                "grade_pct": 100 * (b.ele - a.ele) / max(1.0, b.dist_m - a.dist_m),
                "class": classify(tags),
                "tags": tags or {},
                "match_distance_m": best_dist if tags else None,
            }
        )
    return matched


def summarize(rows: list[dict]) -> dict[str, dict[str, float]]:
    summary: dict[str, dict[str, float]] = defaultdict(lambda: {"dist_km": 0.0, "gain_m": 0.0, "loss_m": 0.0})
    for row in rows:
        bucket = summary[row["class"]]
        bucket["dist_km"] += row["dist_km"]
        bucket["gain_m"] += row["gain_m"]
        bucket["loss_m"] += row["loss_m"]
    return dict(summary)


def summarize_grades(rows: list[dict]) -> dict[str, dict[str, float]]:
    summary: dict[str, dict[str, float]] = {
        label: {"dist_km": 0.0, "gain_m": 0.0, "loss_m": 0.0} for label, _, _ in GRADE_BUCKETS
    }
    for row in rows:
        grade = row["grade_pct"]
        for label, lo, hi in GRADE_BUCKETS:
            if lo <= grade < hi:
                bucket = summary[label]
                bucket["dist_km"] += row["dist_km"]
                bucket["gain_m"] += row["gain_m"]
                bucket["loss_m"] += row["loss_m"]
                break
    return summary


def merge_sections(rows: list[dict], wanted: set[str], min_km: float, gap_km: float) -> list[dict]:
    sections: list[dict] = []
    current: dict | None = None
    for row in rows:
        is_wanted = row["class"] in wanted
        if is_wanted:
            if current is None:
                current = {
                    "start_km": row["start_km"],
                    "end_km": row["end_km"],
                    "dist_km": row["dist_km"],
                    "gain_m": row["gain_m"],
                    "loss_m": row["loss_m"],
                    "classes": defaultdict(float),
                    "highways": defaultdict(float),
                    "surfaces": defaultdict(float),
                    "tracktypes": defaultdict(float),
                }
            elif row["start_km"] - current["end_km"] <= gap_km:
                current["end_km"] = row["end_km"]
                current["dist_km"] += row["dist_km"]
                current["gain_m"] += row["gain_m"]
                current["loss_m"] += row["loss_m"]
            else:
                if current["dist_km"] >= min_km:
                    sections.append(current)
                current = {
                    "start_km": row["start_km"],
                    "end_km": row["end_km"],
                    "dist_km": row["dist_km"],
                    "gain_m": row["gain_m"],
                    "loss_m": row["loss_m"],
                    "classes": defaultdict(float),
                    "highways": defaultdict(float),
                    "surfaces": defaultdict(float),
                    "tracktypes": defaultdict(float),
                }
            tags = row["tags"]
            current["classes"][row["class"]] += row["dist_km"]
            current["highways"][tags.get("highway", "unknown")] += row["dist_km"]
            current["surfaces"][tags.get("surface", "unknown")] += row["dist_km"]
            current["tracktypes"][tags.get("tracktype", "unknown")] += row["dist_km"]
        elif current is not None and row["start_km"] - current["end_km"] > gap_km:
            if current["dist_km"] >= min_km:
                sections.append(current)
            current = None
    if current is not None and current["dist_km"] >= min_km:
        sections.append(current)
    return sections


def top_tag(counter: defaultdict[str, float]) -> str:
    if not counter:
        return "unknown"
    key, value = max(counter.items(), key=lambda item: item[1])
    return f"{key} ({value:.1f} km)"


def serialize_section(section: dict) -> dict:
    return {
        "start_km": section["start_km"],
        "end_km": section["end_km"],
        "dist_km": section["dist_km"],
        "gain_m": section["gain_m"],
        "loss_m": section["loss_m"],
        "avg_grade_pct": 100 * (section["gain_m"] - section["loss_m"]) / max(1.0, section["dist_km"] * 1000),
        "classes": dict(section["classes"]),
        "highways": dict(section["highways"]),
        "surfaces": dict(section["surfaces"]),
        "tracktypes": dict(section["tracktypes"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("gpx", nargs="+", type=Path)
    parser.add_argument("--cache", type=Path, default=Path(".cache/osm_surface.json"))
    parser.add_argument("--step-m", type=float, default=200.0)
    parser.add_argument("--smooth-radius", type=int, default=2)
    parser.add_argument(
        "--match-threshold-m",
        type=float,
        default=200.0,
        help=(
            "Max distance (m) between a sample midpoint and the closest OSM "
            "way to count as matched. 70 = strict (urban/clean GPS), "
            "120 = moderate, 200 = mountain/forest (default)."
        ),
    )
    parser.add_argument("--min-section-km", type=float, default=0.8)
    parser.add_argument("--merge-gap-km", type=float, default=0.4)
    parser.add_argument("--timeout-s", type=int, default=180)
    parser.add_argument(
        "--chunk-km",
        type=float,
        default=None,
        help="Fetch OSM data in route-corridor chunks instead of one broad bounding box.",
    )
    parser.add_argument(
        "--grade-span-m",
        type=float,
        default=300.0,
        help="Centered window length used to compute local grade at each sample.",
    )
    parser.add_argument(
        "--profile-step-km",
        type=float,
        default=25.0,
        help="Step distance for the elevation profile table.",
    )
    parser.add_argument("--climb-min-km", type=float, default=1.5)
    parser.add_argument("--climb-min-gain", type=float, default=60.0)
    parser.add_argument("--climb-start-grade", type=float, default=2.5)
    parser.add_argument("--climb-extend-grade", type=float, default=1.0)
    parser.add_argument("--descent-min-km", type=float, default=1.5)
    parser.add_argument("--descent-min-loss", type=float, default=60.0)
    parser.add_argument(
        "--descent-start-grade",
        type=float,
        default=2.5,
        help="Absolute value; treated as -X% as the start threshold.",
    )
    parser.add_argument(
        "--descent-extend-grade",
        type=float,
        default=1.0,
        help="Absolute value; treated as -X% as the extend threshold.",
    )
    parser.add_argument("--aero-max-grade-abs", type=float, default=1.5)
    parser.add_argument("--aero-min-len-km", type=float, default=3.0)
    parser.add_argument("--waypoint-max-offset-m", type=float, default=200.0)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    points = combine_points(args.gpx)
    samples = smooth_elevation(resample(points, args.step_m), args.smooth_radius)
    if len(samples) < 2:
        print("Not enough GPX points", file=sys.stderr)
        return 1

    osm = load_or_fetch_osm(points, args.cache, args.timeout_s, chunk_km=args.chunk_km)
    lat0 = sum(p.lat for p in points) / len(points)
    ways = build_way_segments(osm, lat0)
    rows = matched_segments(samples, ways, args.match_threshold_m)
    sections = merge_sections(
        rows,
        {"unpaved", "suspect_unpaved"},
        min_km=args.min_section_km,
        gap_km=args.merge_gap_km,
    )
    summary = summarize(rows)
    grade_summary = summarize_grades(rows)

    # Elevation-derived structured features and waypoints.
    grades = compute_local_grades(samples, span_m=args.grade_span_m)
    climbs = detect_climbs(
        samples,
        grades,
        min_km=args.climb_min_km,
        min_gain=args.climb_min_gain,
        start_grade=args.climb_start_grade,
        extend_grade=args.climb_extend_grade,
    )
    descents = detect_descents(
        samples,
        grades,
        min_km=args.descent_min_km,
        min_loss=args.descent_min_loss,
        start_grade=-args.descent_start_grade,
        extend_grade=-args.descent_extend_grade,
    )
    aero_sections = detect_aero_sections(
        samples,
        grades,
        max_grade_abs=args.aero_max_grade_abs,
        min_len_km=args.aero_min_len_km,
    )
    profile = elevation_profile(samples, step_km=args.profile_step_km)
    waypoints = locate_waypoints(
        parse_waypoints(args.gpx),
        samples,
        max_offset_m=args.waypoint_max_offset_m,
    )

    # Cross-reference each elevation feature against merged unpaved sections.
    for feature in climbs + descents + aero_sections:
        feature["surface_cross_ref"] = cross_reference_surface(
            feature["start_km"], feature["end_km"], sections
        )

    total_km = sum(row["dist_km"] for row in rows)
    total_gain = sum(row["gain_m"] for row in rows)
    total_loss = sum(row["loss_m"] for row in rows)
    unmatched_km = summary.get("unmatched", {}).get("dist_km", 0.0)

    lines: list[str] = []
    lines.append("# GPX Terrain Analysis")
    lines.append("")
    lines.append(f"- GPX files: {', '.join(str(path) for path in args.gpx)}")
    lines.append(f"- Distance: {total_km:.1f} km.")
    lines.append(f"- Smoothed gain/loss: +{total_gain:.0f} m / -{total_loss:.0f} m.")
    lines.append(f"- OSM ways loaded: {sum(1 for e in osm.get('elements', []) if e.get('type') == 'way')}.")
    lines.append(f"- Match threshold: {args.match_threshold_m:.0f} m; unmatched: {unmatched_km:.1f} km.")
    lines.append(f"- Unpaved section merge: min {args.min_section_km:.1f} km; gap {args.merge_gap_km:.1f} km.")
    if samples:
        ele_values = [s.ele for s in samples]
        lines.append(
            f"- Elevation range: {min(ele_values):.0f} m to {max(ele_values):.0f} m."
        )
    lines.append("")

    if waypoints:
        lines.append("## Waypoints / Checkpoints")
        lines.append("")
        lines.append("| Name | Type | Km | Alt | Offset | Note |")
        lines.append("|---|---|---:|---:|---:|---|")
        for wpt in waypoints:
            note = wpt.get("comment", "") or ""
            note_short = note if len(note) <= 60 else note[:57] + "..."
            lines.append(
                f"| {wpt['name'] or '-'} | {wpt.get('type', '') or '-'} | "
                f"{wpt['km']:.1f} | {wpt['nearest_alt_m']:.0f} m | "
                f"{wpt['offset_m']:.0f} m | {note_short} |"
            )
        lines.append("")

    if profile:
        lines.append("## Elevation Profile")
        lines.append("")
        lines.append("| Km | Elevation |")
        lines.append("|---:|---:|")
        for row in profile:
            lines.append(f"| {row['km']:.1f} | {row['ele_m']:.0f} m |")
        lines.append("")

    lines.append("## Grade Summary")
    lines.append("")
    lines.append("| Grade | Distance | Share | Gain | Loss |")
    lines.append("|---|---:|---:|---:|---:|")
    for label, _, _ in GRADE_BUCKETS:
        values = grade_summary[label]
        if values["dist_km"] <= 0:
            continue
        lines.append(
            f"| {label} | {values['dist_km']:.1f} km | {100 * values['dist_km'] / total_km:.1f} % | "
            f"{values['gain_m']:.0f} m | {values['loss_m']:.0f} m |"
        )
    lines.append("")

    if climbs:
        lines.append(
            f"## Major Climbs (>= {args.climb_min_km:.1f} km, >= {args.climb_min_gain:.0f} m gain)"
        )
        lines.append("")
        lines.append(
            "| Km range | Length | Gain | Avg grade | Top alt | Surface cross-ref |"
        )
        lines.append("|---:|---:|---:|---:|---:|---|")
        for climb in climbs:
            lines.append(
                f"| {climb['start_km']:.1f}-{climb['end_km']:.1f} | "
                f"{climb['length_km']:.1f} km | +{climb['gain_m']:.0f} m | "
                f"{climb['avg_grade_pct']:.1f} % | {climb['top_alt_m']:.0f} m | "
                f"{climb['surface_cross_ref']} |"
            )
        lines.append("")

    if descents:
        lines.append(
            f"## Major Descents (>= {args.descent_min_km:.1f} km, >= {args.descent_min_loss:.0f} m loss)"
        )
        lines.append("")
        lines.append(
            "| Km range | Length | Loss | Avg grade | Bottom alt | Surface cross-ref |"
        )
        lines.append("|---:|---:|---:|---:|---:|---|")
        for descent in descents:
            lines.append(
                f"| {descent['start_km']:.1f}-{descent['end_km']:.1f} | "
                f"{descent['length_km']:.1f} km | -{descent['loss_m']:.0f} m | "
                f"{descent['avg_grade_pct']:.1f} % | {descent['bottom_alt_m']:.0f} m | "
                f"{descent['surface_cross_ref']} |"
            )
        lines.append("")

    if aero_sections:
        lines.append(
            f"## Aero-Eligible Sections (|grade| <= {args.aero_max_grade_abs:.1f} %, "
            f">= {args.aero_min_len_km:.1f} km)"
        )
        lines.append("")
        lines.append(
            "| Km range | Length | Avg grade | Start alt | End alt | Surface cross-ref |"
        )
        lines.append("|---:|---:|---:|---:|---:|---|")
        for section in aero_sections:
            lines.append(
                f"| {section['start_km']:.1f}-{section['end_km']:.1f} | "
                f"{section['length_km']:.1f} km | "
                f"{section['avg_grade_pct']:+.2f} % | "
                f"{section['start_alt_m']:.0f} m | {section['end_alt_m']:.0f} m | "
                f"{section['surface_cross_ref']} |"
            )
        aero_total = sum(s["length_km"] for s in aero_sections)
        lines.append("")
        lines.append(
            f"Total aero-eligible distance: {aero_total:.1f} km / {total_km:.1f} km "
            f"({100 * aero_total / total_km:.1f} %)."
        )
        lines.append("")

    lines.append("## Surface Summary")
    lines.append("")
    lines.append("| Class | Distance | Share | Gain | Loss |")
    lines.append("|---|---:|---:|---:|---:|")
    order = ["paved", "unknown_likely_paved", "unpaved", "suspect_unpaved", "unknown", "unmatched"]
    for klass in order:
        values = summary.get(klass)
        if not values:
            continue
        lines.append(
            f"| {klass} | {values['dist_km']:.1f} km | {100 * values['dist_km'] / total_km:.1f} % | "
            f"{values['gain_m']:.0f} m | {values['loss_m']:.0f} m |"
        )
    lines.append("")

    lines.append("## Main Unpaved / Suspect Sections")
    lines.append("")
    lines.append("| Km range | Dist | Avg grade | Gain | Loss | Main highway | Main surface | Main tracktype |")
    lines.append("|---:|---:|---:|---:|---:|---|---|---|")
    for section in sections:
        avg_grade = 100 * (section["gain_m"] - section["loss_m"]) / max(1.0, section["dist_km"] * 1000)
        lines.append(
            f"| {section['start_km']:.1f}-{section['end_km']:.1f} | {section['dist_km']:.1f} km | "
            f"{avg_grade:+.1f} % | "
            f"+{section['gain_m']:.0f} m | -{section['loss_m']:.0f} m | "
            f"{top_tag(section['highways'])} | {top_tag(section['surfaces'])} | {top_tag(section['tracktypes'])} |"
        )
    lines.append("")
    lines.append("## Interpretation Notes")
    lines.append("")
    lines.append("- OSM surface data is incomplete; treat this as route intelligence, not official truth.")
    lines.append("- `unknown_likely_paved` usually means normal roads without explicit `surface=*` tags.")
    lines.append("- `suspect_unpaved` flags tracks, paths, bridleways, or cycleways lacking explicit surface tags.")
    lines.append("- Climbs/descents are derived from the smoothed GPX elevation; raw D+/D- from a head unit may differ.")
    lines.append("- Surface cross-ref labels: `likely paved` = no overlap with merged unpaved sections; `partial unpaved` = 30-80 % overlap; `**UNPAVED**` = >= 80 % overlap.")
    lines.append("- Check high-consequence sectors manually before making tyre or pacing decisions.")
    report = "\n".join(lines) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(report)
    if args.json_out:
        payload = {
            "gpx_files": [str(path) for path in args.gpx],
            "distance_km": total_km,
            "gain_m": total_gain,
            "loss_m": total_loss,
            "match_threshold_m": args.match_threshold_m,
            "elevation_profile": profile,
            "waypoints": waypoints,
            "climbs": climbs,
            "descents": descents,
            "aero_sections": aero_sections,
            "surface_summary": summary,
            "grade_summary": grade_summary,
            "sections": [serialize_section(section) for section in sections],
            "rows": rows,
        }
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, indent=2))
    print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
