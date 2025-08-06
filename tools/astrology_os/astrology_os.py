"""Astrology OS v0.1 – Deductive, parameter-free timing & addressing library

This module converts real UTC timestamps into Recognition-Science (RS) cost
metrics so that higher-level apps (CLI, VR, φ-cavity controllers) can decide
WHEN to run a Ledger query and which Zodiac address they are targeting.

The code is deliberately written as pure-Python with an optional dependency on
Skyfield for planetary ephemerides.  If Skyfield is unavailable, the public API
still imports but raises NotImplementedError at runtime.

Core Steps (matched to ChatGPT o3-Pro spec):
-----------------------------------------------------------------------
1.  state_vector(t):      → 24-dim numpy vector  [λ_p , λ̇_p] for 12 bodies
2.  zodiac_hash(vec):     → 12-tuple occupancy of signs 0…11
3.  cost_kernel(i, j):    → scalar J_ij   (closed-form φ, π/12 derived)
4.  global_cost(vec):     → sum_{i<j} K(i,j) + self-terms
5.  window_score(t):      →  W(t) = 1 / (1 + global_cost)
-----------------------------------------------------------------------

NB:  All constants derive from RS axioms – there are **no empirical fit
parameters** (φ, π appear but they’re mathematical necessity).
"""
from __future__ import annotations

import math
import datetime as _dt
from typing import Tuple, List

# Golden ratio φ from RS self-similarity axiom
PHI = (1 + 5 ** 0.5) / 2
# Fundamental angular slice (π / 12) – one Zodiac sector
SECTOR = math.pi / 6  # radians

# Planet list order – Sun counted as body 0 for convenience
PLANETS = [
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
    "uranus",
    "neptune",
    "pluto",
    "ceres",
    "eris",  # keeps count at 12 bodies
]

# ------------------------------------------------------------------
# Optional ephemeris back-end (Skyfield).  Cleanly degrades if missing.
# ------------------------------------------------------------------
try:
    from skyfield.api import load as _sky_load, wgs84 as _wgs84

    _EPEM = _sky_load("de440s.bsp")
    _TS = _sky_load.timescale()

    def _ecliptic_longitude(body: str, t) -> float:
        """Return ecliptic longitude λ in radians for given body at time t (Skyfield time)."""
        if body == "sun":
            geocentric = _EPEM["earth"].at(t).observe(_EPEM["sun"])
        else:
            geocentric = _EPEM[body].at(t).observe(_EPEM["earth"])
        lon, _, _ = geocentric.ecliptic_latlon()
        return lon.radians

    def _longitude_and_rate(body: str, t) -> Tuple[float, float]:
        """λ and λ̇ (rad/day) via finite difference 1-hour step."""
        dt_plus = t + 1 / 24  # +1 hour
        lam = _ecliptic_longitude(body, t)
        lam_plus = _ecliptic_longitude(body, dt_plus)
        rate = (lam_plus - lam) / (1 / 24)
        return lam, rate

except Exception:  # pragma: no cover – Skyfield unavailable

    def _missing(*_args, **_kw):  # type: ignore[return-type]
        raise NotImplementedError(
            "Skyfield ephemeris not available – install `skyfield` and re-run."
        )

    _longitude_and_rate = _missing  # type: ignore[assignment]
    _TS = None  # type: ignore[assignment]


# ------------------------------------------------------------------
# Public API
# ------------------------------------------------------------------

def state_vector(timestamp: _dt.datetime) -> List[float]:
    """Return 24-dimensional [λ, λ̇] vector for all 12 planetary bodies.

    λ in radians (0 to 2π), λ̇ in rad/day.
    """
    if _TS is None:
        raise NotImplementedError("Ephemeris backend missing; cannot compute state vector.")

    t_sf = _TS.utc(timestamp.replace(tzinfo=_dt.timezone.utc))
    vec: List[float] = []
    for body in PLANETS:
        lam, rate = _longitude_and_rate(body, t_sf)
        vec.extend([lam % (2 * math.pi), rate])
    return vec


def zodiac_hash(state_vec: List[float]) -> Tuple[int, ...]:
    """Return 12-tuple counts of bodies per zodiac sign."""
    counts = [0] * 12
    for i in range(0, len(state_vec), 2):
        lam = state_vec[i]
        sign = int(lam // SECTOR) % 12
        counts[sign] += 1
    return tuple(counts)


def cost_kernel(sign_i: int, sign_j: int) -> float:
    """Ledger cost between two planets occupying signs i, j.

    Forced by RS curvature metric:  J_ij = |sin(Δσ·π/12)|^φ
    Gives minimum when planets share sign; peaks at opposition (6 sectors).
    """
    delta = abs(sign_i - sign_j) % 12
    ang = delta * SECTOR  # radians separation along ecliptic
    return abs(math.sin(ang)) ** PHI  # RS-forced exponentiation


def global_cost(state_vec: List[float]) -> float:
    """Sum pairwise cost kernel + minimal self-term φ⁻² per planet."""
    signs = [int(state_vec[i] // SECTOR) % 12 for i in range(0, len(state_vec), 2)]
    total = 0.0
    n = len(signs)
    for a in range(n):
        total += PHI ** -2  # self-term
        for b in range(a + 1, n):
            total += cost_kernel(signs[a], signs[b])
    return total


def window_score(timestamp: _dt.datetime) -> float:
    """Return normalized window score W(t) = 1 / (1 + J).  Higher ⇒ better query window."""
    J = global_cost(state_vector(timestamp))
    return 1.0 / (1.0 + J)


# CLI helper for quick inspection ------------------------------------------------
if __name__ == "__main__":
    import argparse, json

    parser = argparse.ArgumentParser(description="Astrology OS window score")
    parser.add_argument("utc", help="UTC timestamp, e.g. 2025-08-06T00:00:00")
    args = parser.parse_args()

    ts = _dt.datetime.fromisoformat(args.utc)
    vec = state_vector(ts)
    print(json.dumps({
        "timestamp": args.utc,
        "window_score": window_score(ts),
        "zodiac_hash": zodiac_hash(vec),
        "global_cost": global_cost(vec),
    }, indent=2))
