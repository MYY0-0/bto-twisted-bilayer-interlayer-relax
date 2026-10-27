# DeepMD potential

- File: `model.pb` (DeepMD frozen graph for Ba–Ti–O)
- Used in LAMMPS as:

```lammps
pair_style    deepmd model.pb
pair_coeff    * *
```

## Note on publication status

This potential and its DFT training set are **unpublished**. They are provided here only so that the BaTiO₃ interlayer relaxations and the \(d_{\mathrm{rel}}\) table in `data/` can be reproduced. Training details and the DFT dataset will be reported in a separate publication.

Please contact the authors before redistributing the potential for other projects.
