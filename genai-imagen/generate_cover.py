#!/usr/bin/env python3
"""Generate a strange attractor PNG for the cover page.

Usage:
    python3 generate_cover.py --attractor dejong
    python3 generate_cover.py -l

Each attractor is a 2D map or a 3D ODE system (rendered with mplot3d).
"""

import math
import os
import sys
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Match the wp-bg / wp-text colors from tufte-notes.sty
BG = "#FDF6EF"
TEXT = "#2D1B0E"

DPI = 300
FIG_SIZE = 4
ITERATIONS = 1_000_000
BURN_IN = 1_000
POINT_SIZE = 0.3
ALPHA = 0.15
MAX_3D_POINTS = 40_000  # downsampled for 3D scatter performance
CLIP = 1e3  # discard trajectory points beyond this


# ── 2D discrete maps ──────────────────────────────────────────────

def _clamped(val):
    return math.isfinite(val) and abs(val) < CLIP


def dejong(iterations, burn_in, params):
    a, b, c, d = params["a"], params["b"], params["c"], params["d"]
    x, y = 0.1, 0.1
    xs, ys = [], []
    for i in range(iterations):
        x, y = math.sin(a * y) - math.cos(b * x), math.sin(c * x) - math.cos(d * y)
        if _clamped(x) and _clamped(y) and i >= burn_in:
            xs.append(x); ys.append(y)
    return np.array(xs), np.array(ys)


def duffing(iterations, burn_in, params):
    a, b, w = params["a"], params["b"], params["w"]
    dt = 0.02
    tau = 2.0 * math.pi / w
    s = [0.1, 0.0, 0.0]
    xs, ys, zs = [], [], []
    for i in range(iterations):
        def f(state):
            x, y, z = state
            return [y, -b * y + a * x - x ** 3 + math.cos(w * z), w]
        s = _rk4_step(f, s, dt)
        s[2] = s[2] % tau
        if _clamped(s[0]) and _clamped(s[1]):
            if i * dt >= burn_in * dt:
                xs.append(s[0]); ys.append(s[1]); zs.append(s[2])
    return np.array(xs), np.array(ys), np.array(zs)


def ikeda(iterations, burn_in, params):
    mu = params["mu"]
    x, y = 0.1, 0.1
    xs, ys = [], []
    for i in range(iterations):
        theta = 0.4 - 6.0 / (1.0 + x * x + y * y)
        ct, st = math.cos(theta), math.sin(theta)
        x, y = 1.0 + mu * (x * ct - y * st), mu * (x * st + y * ct)
        if _clamped(x) and _clamped(y) and i >= burn_in:
            xs.append(x); ys.append(y)
    return np.array(xs), np.array(ys)


def symmetric_icon(iterations, burn_in, params):
    a, b, c, d = params["a"], params["b"], params["c"], params["d"]
    x, y = 0.1, 0.1
    xs, ys = [], []
    for i in range(iterations):
        x, y = math.sin(a * y) + c * math.cos(a * x), math.sin(b * x) + d * math.cos(b * y)
        if _clamped(x) and _clamped(y) and i >= burn_in:
            xs.append(x); ys.append(y)
    return np.array(xs), np.array(ys)


def cubic_strange(iterations, burn_in, params):
    a1, a2, a3, a4, a5, a6 = (params["a1"], params["a2"], params["a3"],
                               params["a4"], params["a5"], params["a6"])
    x, y = 0.1, 0.1
    xs, ys = [], []
    for i in range(iterations):
        nx = math.sin(a1 * x + a2 * y + a3 * x ** 3)
        ny = math.sin(a4 * x + a5 * y + a6 * y ** 3)
        x, y = nx, ny
        if i >= burn_in:
            xs.append(x); ys.append(y)
    return np.array(xs), np.array(ys)


def fractal_dreams(iterations, burn_in, params):
    a, b, c, d = params["a"], params["b"], params["c"], params["d"]
    x, y = 0.1, 0.1
    xs, ys = [], []
    for i in range(iterations):
        x, y = math.sin(a * y) + math.sin(b * x), math.sin(c * x) + math.sin(d * y)
        if _clamped(x) and _clamped(y) and i >= burn_in:
            xs.append(x); ys.append(y)
    return np.array(xs), np.array(ys)


# ── 3D ODE systems (solved with RK4) ─────────────────────────────

def _rk4_step(f, s, dt):
    k1 = f(s)
    k2 = f([si + 0.5 * dt * k1i for si, k1i in zip(s, k1)])
    k3 = f([si + 0.5 * dt * k2i for si, k2i in zip(s, k2)])
    k4 = f([si + dt * k3i for si, k3i in zip(s, k3)])
    return [si + dt * (k1i + 2 * k2i + 2 * k3i + k4i) / 6.0
            for si, k1i, k2i, k3i, k4i in zip(s, k1, k2, k3, k4)]


def aizawa(iterations, burn_in, params):
    a, b, c, d, e, f = (params["a"], params["b"], params["c"],
                         params["d"], params["e"], params["f"])
    dt = 0.01
    s = [0.1, 0.0, 0.0]
    xs, ys, zs = [], [], []
    for i in range(iterations):
        def rhs(state):
            x, y, z = state
            dx = (z - b) * x - d * y
            dy = d * x + (z - b) * y
            dz = (c + a * z - z ** 3 / 3.0
                  - (x * x + y * y) * (1.0 + e * z)
                  + f * z * x ** 3)
            return [dx, dy, dz]
        s = _rk4_step(rhs, s, dt)
        if _clamped(s[0]) and _clamped(s[1]) and _clamped(s[2]):
            if i * dt >= burn_in * dt:
                xs.append(s[0]); ys.append(s[1]); zs.append(s[2])
    return np.array(xs), np.array(ys), np.array(zs)


def sprott_b(iterations, burn_in, params):
    a, b, c = params["a"], params["b"], params["c"]
    dt = 0.01
    s = [0.1, 0.0, 0.0]
    xs, ys, zs = [], [], []
    for i in range(iterations):
        def f(state):
            x, y, z = state
            dx = a * y * z
            dy = b * x - c * y
            dz = 1.0 - x * y
            return [dx, dy, dz]
        s = _rk4_step(f, s, dt)
        if _clamped(s[0]) and _clamped(s[1]) and _clamped(s[2]):
            if i * dt >= burn_in * dt:
                xs.append(s[0]); ys.append(s[1]); zs.append(s[2])
    return np.array(xs), np.array(ys), np.array(zs)


# ── Registry ──────────────────────────────────────────────────────

ATTRACTORS = {
    "dejong": {
        "fn": dejong,
        "params": {"a": 1.4, "b": -2.3, "c": 2.4, "d": -2.1},
        "dim": 2,
        "description": "De Jong attractor",
    },
    "duffing": {
        "fn": duffing,
        "params": {"a": 0.35, "b": 0.3, "w": 1.0},
        "dim": 3,
        "description": "Duffing oscillator",
    },
    "ikeda": {
        "fn": ikeda,
        "params": {"mu": 0.9},
        "dim": 2,
        "description": "Ikeda map",
    },
    "symmetric-icon": {
        "fn": symmetric_icon,
        "params": {"a": 1.5, "b": -1.5, "c": 0.5, "d": 0.5},
        "dim": 2,
        "description": "Symmetric Icon attractor",
    },
    "cubic-strange": {
        "fn": cubic_strange,
        "params": {"a1": -1.2, "a2": -1.1, "a3": -1.0, "a4": -0.9, "a5": -0.8, "a6": 1.2},
        "dim": 2,
        "description": "Cubic Strange attractor",
    },
    "fractal-dreams": {
        "fn": fractal_dreams,
        "params": {"a": 1.468, "b": 2.407, "c": 0.194, "d": 1.438},
        "dim": 2,
        "description": "Fractal Dreams (SSSS) attractor",
    },
    "aizawa": {
        "fn": aizawa,
        "params": {"a": 0.95, "b": 0.7, "c": 0.6, "d": 3.5, "e": 0.25, "f": 0.1},
        "dim": 3,
        "description": "Aizawa (Langford) attractor",
    },
    "sprott-b": {
        "fn": sprott_b,
        "params": {"a": 0.4, "b": 1.2, "c": 1.0},
        "dim": 3,
        "description": "Sprott B attractor",
    },
}


# ── Helpers ───────────────────────────────────────────────────────

def compute_limits(xs, ys, pad=0.2):
    lo_x, hi_x = np.percentile(xs, [1, 99])
    lo_y, hi_y = np.percentile(ys, [1, 99])
    rx = max(hi_x - lo_x, 1e-6)
    ry = max(hi_y - lo_y, 1e-6)
    cx, cy = (lo_x + hi_x) / 2, (lo_y + hi_y) / 2
    half = max(rx, ry) / 2 * (1 + pad)
    return cx - half, cx + half, cy - half, cy + half


def compute_limits_3d(xs, ys, zs, pad=0.2):
    lo_x, hi_x = np.percentile(xs, [1, 99])
    lo_y, hi_y = np.percentile(ys, [1, 99])
    lo_z, hi_z = np.percentile(zs, [1, 99])
    rx = max(hi_x - lo_x, 1e-6)
    ry = max(hi_y - lo_y, 1e-6)
    rz = max(hi_z - lo_z, 1e-6)
    cx, cy, cz = (lo_x + hi_x) / 2, (lo_y + hi_y) / 2, (lo_z + hi_z) / 2
    half = max(rx, ry, rz) / 2 * (1 + pad)
    return (cx - half, cx + half, cy - half, cy + half, cz - half, cz + half)


# ── Main ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Generate a strange attractor PNG for the cover page")
    parser.add_argument(
        "--attractor", "-a",
        choices=list(ATTRACTORS),
        default="dejong",
        help="Which attractor to render (default: dejong)")
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available attractors and exit")
    args = parser.parse_args()

    if args.list:
        print("Available attractors:")
        for name, info in ATTRACTORS.items():
            dim = f"{info['dim']}D"
            print(f"  {name:20s} {dim:4s} {info['description']}")
        sys.exit(0)

    os.makedirs("cover", exist_ok=True)

    info = ATTRACTORS[args.attractor]
    print(f"Generating {info['description']} ({info['dim']}D)...", file=sys.stderr)
    result = info["fn"](ITERATIONS, BURN_IN, info["params"])

    if len(result[0]) == 0:
        print("No points generated!", file=sys.stderr)
        sys.exit(1)

    fig = plt.figure(figsize=(FIG_SIZE, FIG_SIZE), dpi=DPI, facecolor=BG)

    if info["dim"] == 3:
        xs, ys, zs = result
        step = max(1, len(xs) // MAX_3D_POINTS)
        xs, ys, zs = xs[::step], ys[::step], zs[::step]
        print(f"  {len(result[0])} generated, {len(xs)} rendered", file=sys.stderr)

        ax = fig.add_axes([0, 0, 1, 1], projection="3d")
        ax.set_facecolor(BG)
        ax.scatter(xs, ys, zs, s=POINT_SIZE * 5, c=TEXT, alpha=ALPHA * 3, linewidths=0)
        ax.view_init(elev=25, azim=-60)

        xlo, xhi, ylo, yhi, zlo, zhi = compute_limits_3d(xs, ys, zs)
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ylo, yhi)
        ax.set_zlim(zlo, zhi)
        ax.set_box_aspect((1, 1, 1))
        ax.axis("off")
    else:
        xs, ys = result
        print(f"  {len(xs)} points", file=sys.stderr)

        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_facecolor(BG)
        ax.scatter(xs, ys, s=POINT_SIZE, c=TEXT, alpha=ALPHA, linewidths=0)

        xlo, xhi, ylo, yhi = compute_limits(xs, ys)
        ax.set_xlim(xlo, xhi)
        ax.set_ylim(ylo, yhi)
        ax.set_aspect("equal")
        ax.axis("off")

    out = "cover/attractor-image.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

    sz = os.path.getsize(out)
    print(f"  -> {out} ({sz} bytes)", file=sys.stderr)


if __name__ == "__main__":
    main()
