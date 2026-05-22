# Morphospaces

TraitBlender currently includes three morphospaces:

- **[Shell (Default)](shell.md)** – a 3D shell model based on Contreras-Figueroa & Aragón (2023)
- **[Circle Grid](circle-grid.md)** – a white cube with a 4×4 grid of black circles on top
- **[ATLAS](atlas.md)** – PCA + local RBF deformation of a template mesh from an ATLAS DATABASE export

Each morphospace has a **name** (e.g. "Shell (Default)", "Circle Grid", "ATLAS") used in the GUI and in config files, and:

- **traits** – columns in the dataset (per-specimen values)
- **hyperparameters** – extra settings that affect how the model is generated (set in the Configuration panel)

Follow the links above for the full list of parameters, default values, and ranges that make sense in practice.
