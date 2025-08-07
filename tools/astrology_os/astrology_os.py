#!/usr/bin/env python3
"""
Astrology OS - Recognition Science Implementation
Author: Jonathan Washburn
"""
import math
import datetime as _dt
from typing import Tuple, List

PHI = (1 + 5**0.5) / 2
SECTOR = math.pi / 6

PLANETS = [
    "sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn",
    "uranus", "neptune", "pluto",
]

try:
    from skyfield.api import load as _sky_load
    _EPEM = _sky_load("de440.bsp")
    _TS = _sky_load.timescale()

    def _ecliptic_longitude(body: str, t) -> float:
        planet_map = {
            "sun": "sun", "moon": "moon", "mercury": "mercury", "venus": "venus",
            "mars": "mars barycenter", "jupiter": "jupiter barycenter",
            "saturn": "saturn barycenter", "uranus": "uranus barycenter",
            "neptune": "neptune barycenter", "pluto": "pluto barycenter"
        }
        ephemeris_id = planet_map.get(body, body)
        geocentric = _EPEM["earth"].at(t).observe(_EPEM[ephemeris_id]) if body != "sun" else _EPEM[ephemeris_id].at(t).observe(_EPEM["earth"])
        lon, _, _ = geocentric.ecliptic_latlon()
        return lon.radians

    def _longitude_and_rate(body: str, t) -> Tuple[float, float]:
        dt_plus = t + (1 / 24)
        lam, lam_plus = _ecliptic_longitude(body, t), _ecliptic_longitude(body, dt_plus)
        return lam, (lam_plus - lam) / (1 / 24)

except Exception:
    _longitude_and_rate = lambda *a, **k: (_ for _ in ()).throw(NotImplementedError("Skyfield not available."))

def state_vector(timestamp: _dt.datetime) -> List[float]:
    t_sf = _TS.from_datetime(timestamp)
    return [val for body in PLANETS for val in _longitude_and_rate(body, t_sf)]

def zodiac_hash(state_vec: List[float]) -> Tuple[int, ...]:
    signs = [0] * 12
    for lam in state_vec[0::2]:
        signs[int((lam % (2 * math.pi)) / SECTOR)] += 1
    return tuple(signs)

def cost_kernel(sign_i: int, sign_j: int) -> float:
    return abs(math.sin(abs(sign_i - sign_j) % 12 * SECTOR)) ** PHI

def global_cost(state_vec: List[float]) -> float:
    signs = [int((l % (2 * math.pi)) / SECTOR) for l in state_vec[0::2]]
    return sum(cost_kernel(signs[i], signs[j]) for i in range(len(signs)) for j in range(i + 1, len(signs)))

def window_score(timestamp: _dt.datetime) -> float:
    return 1 / (1 + global_cost(state_vector(timestamp)))

def generate_heatmap(year: int) -> dict:
    start_date = _dt.datetime(year, 1, 1, tzinfo=_dt.timezone.utc)
    scores = { (start_date + _dt.timedelta(days=i)).strftime('%Y-%m-%d'): window_score(start_date + _dt.timedelta(days=i)) for i in range(366) if (start_date + _dt.timedelta(days=i)).year == year }
    return {"year": year, "daily_scores": scores, "top_windows": [{"date": d, "score": s} for d, s in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:10]]}

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Astrology OS")
    parser.add_argument("utc_or_year", help="UTC timestamp or year for heatmap")
    args = parser.parse_args()
    if len(args.utc_or_year) == 4 and args.utc_or_year.isdigit():
        print(json.dumps(generate_heatmap(int(args.utc_or_year)), indent=2))
    else:
        ts = _dt.datetime.fromisoformat(args.utc_or_year)
        vec = state_vector(ts)
        print(json.dumps({"timestamp": args.utc_or_year, "window_score": window_score(ts), "zodiac_hash": zodiac_hash(vec), "global_cost": global_cost(vec)}, indent=2))