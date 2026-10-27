# Twisted bilayer BaTiO₃ — interlayer spacing relaxations

Supporting repository for the author response on the twist-angle dependence of the **average BaO–BaO interlayer spacing** in related AO–AO perovskite bilayers (LAMMPS + DeepMD).

> **Main result for peer review:** see [`data/interlayer_spacing_summary.csv`](data/interlayer_spacing_summary.csv)  
> Over commensurate cells (1,2)–(1,13), \(d_{\mathrm{rel}}\) remains ~3.07–3.18 Å and varies by **&lt; 0.12 Å**.

## Repository layout

```text
.
├── README.md
├── .gitignore
├── data/                         # extracted tables (primary deliverable)
│   ├── interlayer_spacing_summary.csv
│   ├── interlayer_spacing_summary.md
│   └── max_dr_vs_theta.csv       # max in-plane Ti displacement vs angle
├── figures/
│   ├── fig1_max_dr_vs_theta.png  # main figure (Lee comparison + full range)
│   ├── max_dr_vs_theta_lee_style.png
│   └── max_dr_vs_theta_full.png
├── scripts/
│   └── measure_interlayer_spacing.py
├── potentials/
│   ├── README.md
│   └── model.pb                  # single copy of the DeepMD potential
└── calculations/                 # full per-angle LAMMPS jobs
    ├── twist12/  ...  twist113/  # = (1,2) ... (1,13)
    │   ├── in.txt
    │   ├── dp.sh
    │   ├── BTO.data
    │   ├── BTO_before_relax.xyz
    │   ├── BTO_relaxed.xyz
    │   ├── BTO_relaxed.data
    │   ├── log.lammps
    │   ├── run.log / err
    │   ├── restart.BTO_relaxed
    │   └── MODEL_PB.txt          # how to link potentials/model.pb
```

Naming: `calculations/twist1m` ↔ commensurate index `(1,m)` (e.g. `twist16` = (1,6), `twist110` = (1,10)).

## Protocol

- System: twisted bilayer BaTiO₃, BaO–BaO interface
- In-plane lattice fixed; initial interlayer distance **3.2 Å**
- Relaxation: LAMMPS `fix box/relax z 0.0` + CG minimize (`calculations/*/in.txt`)
- \(d_{\mathrm{rel}}\): Ba–Ba spacing across the BaO–BaO interface (same atom IDs before/after)
- Reference: Lee et al., *Sci. Adv.* **10**, eadq0293 (2024)

## Figure

[`figures/fig1_max_dr_vs_theta.png`](figures/fig1_max_dr_vs_theta.png) — maximum in-plane Ti displacement \(\max(\delta\mathbf{r}^{\mathrm{Ti}})\) vs twist angle:

- **(a)** comparison with Lee *et al.* DFT (digitized) in the overlapping angle window  
- **(b)** DeepMD results over the full (1,2)–(1,13) range  

Corresponding numbers: [`data/max_dr_vs_theta.csv`](data/max_dr_vs_theta.csv).

## Quick check of the interlayer-spacing table

```bash
python scripts/measure_interlayer_spacing.py
```

## Re-running a relaxation

1. Copy `potentials/model.pb` into the target `calculations/twistXX/` directory (or symlink it).
2. From that directory, run LAMMPS with `in.txt` (see also `dp.sh`).
3. Recompute spacings with `scripts/measure_interlayer_spacing.py`.

Large MD trajectories (`relax_traj.xyz`) are omitted on purpose (regenerable; not required for the table).

## Potential / training data

The DeepMD potential file is included under `potentials/` so the relaxations can be reproduced. **Training details and the DFT dataset are not released here** and will be reported in a separate publication. See [`potentials/README.md`](potentials/README.md).

## Citation

Please cite the related SrTiO₃ / DeepH manuscript (Phys. Rev. B, Accession Code BU16156) and Lee et al., *Sci. Adv.* **10**, eadq0293 (2024). The BaTiO₃ DeepMD potential should additionally be cited via its forthcoming separate paper when available.
