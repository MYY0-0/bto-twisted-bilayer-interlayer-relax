#!/usr/bin/env python3
"""Recompute BaO--BaO interlayer spacing from LAMMPS dump files.

Run from repository root:
  python scripts/measure_interlayer_spacing.py
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np

TYPE_TO_EL = {1: "Ba", 2: "Ti", 3: "O"}
ROOT = Path(__file__).resolve().parents[1]
CALC = ROOT / "calculations"


def read_lammps_dump(path: Path) -> tuple[np.ndarray, np.ndarray]:
    lines = path.read_text(encoding="utf-8").splitlines()
    natoms = None
    header = None
    rows: list[list[str]] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "ITEM: NUMBER OF ATOMS":
            natoms = int(lines[i + 1].strip())
            i += 2
            continue
        if line.startswith("ITEM: ATOMS"):
            header = line.split()[2:]
            i += 1
            while i < len(lines) and not lines[i].startswith("ITEM:"):
                parts = lines[i].split()
                if header and len(parts) >= len(header):
                    rows.append(parts[: len(header)])
                i += 1
            continue
        i += 1
    if natoms is None or header is None or len(rows) != natoms:
        raise ValueError(f"Failed to parse {path}")
    cols = {name: j for j, name in enumerate(header)}
    elems, pos = [], []
    for r in rows:
        t = int(float(r[cols["type"]]))
        elems.append(TYPE_TO_EL.get(t, "X"))
        pos.append([float(r[cols["x"]]), float(r[cols["y"]]), float(r[cols["z"]])])
    return np.array(elems), np.asarray(pos, dtype=float)


def cluster_z_planes(z: np.ndarray, tol: float = 0.05) -> np.ndarray:
    zs = np.sort(z)
    planes = [float(zs[0])]
    for val in zs[1:]:
        if val - planes[-1] > tol:
            planes.append(float(val))
    return np.array(planes, dtype=float)


def interface_plane_z(positions: np.ndarray) -> tuple[float, float]:
    planes = cluster_z_planes(positions[:, 2])
    gaps = np.diff(planes)
    i = int(np.argmax(gaps))
    return float(planes[i]), float(planes[i + 1])


def ba_plane_ids(
    positions: np.ndarray, elements: np.ndarray, z0: float, tol: float = 0.15
) -> np.ndarray:
    ba = np.where(elements == "Ba")[0]
    sel = ba[np.abs(positions[ba, 2] - z0) <= tol]
    if sel.size == 0:
        raise ValueError(f"No Ba near z={z0}")
    return sel


def parse_nm(name: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"twist(\d+)", name)
    if not m:
        return None
    digits = m.group(1)
    if digits.startswith("1") and len(digits) >= 2:
        return 1, int(digits[1:])
    return None


def twist_angle_deg(n: int, m: int) -> float:
    return math.degrees(2.0 * math.atan2(n, m))


def measure_folder(folder: Path) -> dict:
    elems_i, pos_i = read_lammps_dump(folder / "BTO_before_relax.xyz")
    _, pos_r = read_lammps_dump(folder / "BTO_relaxed.xyz")
    z_lo, z_hi = interface_plane_z(pos_i)
    lo_ids = ba_plane_ids(pos_i, elems_i, z_lo)
    hi_ids = ba_plane_ids(pos_i, elems_i, z_hi)
    d_ini = float(pos_i[hi_ids, 2].mean() - pos_i[lo_ids, 2].mean())
    d_rel = float(pos_r[hi_ids, 2].mean() - pos_r[lo_ids, 2].mean())
    nm = parse_nm(folder.name)
    return {
        "folder": folder.name,
        "nm": nm,
        "theta": twist_angle_deg(*nm) if nm else float("nan"),
        "d_ini": d_ini,
        "d_rel": d_rel,
        "delta": d_rel - d_ini,
    }


def main() -> None:
    folders = sorted(
        [p for p in CALC.iterdir() if p.is_dir() and p.name.startswith("twist")],
        key=lambda p: parse_nm(p.name) or (0, 0),
    )
    print("folder,(n,m),theta_t,d_ini,d_rel,delta")
    for f in folders:
        r = measure_folder(f)
        n, m = r["nm"]
        print(
            f"{r['folder']},({n},{m}),{r['theta']:.2f},"
            f"{r['d_ini']:.4f},{r['d_rel']:.4f},{r['delta']:+.4f}"
        )


if __name__ == "__main__":
    main()
