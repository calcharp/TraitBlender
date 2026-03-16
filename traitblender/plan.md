# TraitBlender v2 Packaging, CI, and Containerization Plan

This document describes the **long-term packaging, CI/CD, and containerization strategy** for TraitBlender v2.

The goals are:

- Support **Blender 4.3+ extension system**
- Provide **prebuilt installable extension packages** for:
  - Linux
  - Windows
  - macOS
- Ensure **reproducible environments**
- Enable **headless HPC usage**
- Support **Docker + Apptainer/Singularity**
- Maintain **transparent dependency management**

This document is meant to guide both humans and automation agents (e.g., Cursor).

---

# Core Principles

## 1. Platform-Specific Extension Builds

TraitBlender will **not ship a single universal extension package**.

Instead, we produce **one extension zip per platform**:

```
traitblender-linux-x86_64.zip
traitblender-windows-x86_64.zip
traitblender-macos-arm64.zip
traitblender-macos-x86_64.zip (optional)
```

Each package contains:

- TraitBlender source code
- Blender manifest
- Only the **platform-appropriate wheels**

Users download **only one file** for their platform.

---

## 2. Wheels are Explicit and Visible

All wheels remain **checked into the repository** so dependencies remain:

- transparent
- reproducible
- inspectable

We **do not rely on runtime pip installs**.

Reasons:

- HPC nodes often block internet access
- Blender extensions expect bundled wheels
- reproducibility is critical

---

## 3. Manifest Is Generated Per Platform

We maintain a **manifest template**, not a single fixed manifest.

Reason:

`blender_manifest.toml` requires explicit wheel paths.

Therefore each build generates a manifest with the correct wheel paths.

Example:

```
manifest.template.toml
```

Converted to:

```
blender_manifest.toml
```

during packaging.

---

# Repository Structure

Proposed layout:

```
TraitBlender/

traitblender/
    __init__.py
    core/
    ui/
    assets/
    docs/
    blender_manifest.template.toml

packaging/
    wheels/
        linux/
        windows/
        macos/

    scripts/
        build_extension.py
        generate_manifest.py

docker/
    Dockerfile
    entrypoint.sh
    smoke_test.py

.github/
    workflows/
        build-extension.yml

dist/
```

Explanation:

| Folder | Purpose |
|------|------|
| `traitblender/` | Extension source code |
| `packaging/wheels/` | Platform-specific wheels |
| `packaging/scripts/` | Build scripts |
| `docker/` | Container environment |
| `.github/workflows/` | CI pipeline |
| `dist/` | Build artifacts |

---

# Wheels Organization

```
packaging/wheels/

linux/
    numpy.whl
    pandas.whl
    scipy.whl
    pillow.whl
    PyYAML.whl
    openpyxl.whl
    dearpygui.whl

windows/
    numpy.whl
    pandas.whl
    scipy.whl
    pillow.whl
    PyYAML.whl
    openpyxl.whl
    dearpygui.whl

macos/
    numpy.whl
    pandas.whl
    scipy.whl
    pillow.whl
    PyYAML.whl
    openpyxl.whl
    dearpygui.whl
```

Pure Python wheels (example):

```
six
python_dateutil
pytz
tzdata
et_xmlfile
```

can be shared across platforms if desired.

---

# Dependencies

## Core Dependencies

Required for TraitBlender functionality:

```
numpy
pandas
pillow
PyYAML
openpyxl
scipy
```

## UI Dependency

Used by dataset editor:

```
dearpygui
```

DearPyGUI is allowed because wheels exist for:

- Linux
- Windows
- macOS

If a platform lacks a compatible wheel, the CI build should **fail explicitly**.

---

# Blender Version

Target:

```
Blender 4.3.x
```

Reasons:

- stable extension API
- consistent Python ABI
- easier wheel compatibility

Avoid supporting multiple Blender versions initially.

---

# Packaging Workflow

The packaging system does the following:

1. Create temporary build directory
2. Copy extension source
3. Copy platform wheels
4. Generate manifest
5. Zip extension
6. Upload artifact

---

# GitHub Actions Strategy

We use a **matrix build** across operating systems.

Example matrix:

```
ubuntu-latest
windows-latest
macos-latest
```

Each job performs:

1. checkout repo
2. install python
3. run packaging script
4. create zip
5. upload artifact

Artifacts produced:

```
traitblender-linux-x86_64.zip
traitblender-windows-x86_64.zip
traitblender-macos-arm64.zip
```

Artifacts can optionally be attached to **GitHub Releases**.

---

# Packaging Script Responsibilities

The packaging script should:

```
1. determine platform
2. locate wheels directory
3. copy extension source
4. copy wheels
5. generate blender_manifest.toml
6. zip build
```

Example pseudo logic:

```
platform = detect_platform()

copy traitblender/

copy packaging/wheels/platform/*

render manifest.template.toml

zip build_dir -> dist/platform.zip
```

---

# Manifest Template

Example template:

```
id = "traitblender"
version = "2.0.0"
type = "add-on"

blender_version_min = "4.3.0"

wheels = [
    "wheels/numpy.whl",
    "wheels/pandas.whl",
    "wheels/pillow.whl",
    "wheels/PyYAML.whl",
    "wheels/scipy.whl",
    "wheels/openpyxl.whl",
    "wheels/dearpygui.whl"
]
```

Paths will be rewritten during build.

---

# Smoke Testing

Each CI build should optionally run a **basic smoke test**.

Example checks:

- Blender launches
- Extension installs
- Extension enables
- Python modules import successfully

Minimal command example:

```
blender --background --python smoke_test.py
```

Smoke test verifies:

```
import numpy
import pandas
import dearpygui
import traitblender
```

---

# Docker Strategy

Docker is **not used for desktop users**.

Docker exists to support:

- headless dataset generation
- reproducible compute
- HPC workflows

---

# Docker Image Goals

The Docker image should contain:

```
Blender 4.3
TraitBlender extension
Linux wheels
minimal runtime libs
```

The image should be able to:

```
run blender headless
load extension
generate dataset
export meshes
render images
```

---

# Dockerfile Strategy

The container should:

1. start from minimal Linux base
2. install Blender runtime libraries
3. download official Blender build
4. copy TraitBlender extension
5. install extension
6. run smoke test

---

# Example Runtime Command

```
blender --background \
    --python generate_dataset.py \
    -- config.json
```

---

# HPC Strategy

Many HPC systems use:

```
Apptainer / Singularity
```

These can consume Docker images directly.

Workflow:

```
Docker image -> Apptainer runtime
```

This avoids maintaining two container definitions.

---

# Filesystem Considerations

TraitBlender uses:

```
bpy.utils.extension_path_user()
```

to store user data.

Therefore containers should mount:

```
outputs/
cache/
configs/
```

as volumes.

Example:

```
docker run -v ./outputs:/outputs
```

---

# Order of Implementation

Recommended order:

### Phase 1

Finalize extension structure.

Tasks:

- confirm Blender 4.3 compatibility
- confirm dependency list
- verify extension loads locally

---

### Phase 2

Create packaging scripts.

Tasks:

- manifest template
- platform wheel directories
- extension build script

---

### Phase 3

Implement GitHub Actions CI.

Tasks:

- matrix build
- artifact upload
- packaging integration

---

### Phase 4

Test platform installs.

Verify:

- Linux
- Windows
- macOS

All packages install correctly.

---

### Phase 5

Create Docker container.

Tasks:

- Blender runtime
- extension install
- smoke test

---

### Phase 6

Add HPC documentation.

Tasks:

- Apptainer usage
- headless rendering examples
- dataset generation examples

---

# Cautionary Notes

## Wheel Compatibility

Wheels must match:

```
platform
architecture
Python version
```

Blender uses its own Python build.

Mismatch will cause import errors.

---

## macOS Architectures

macOS may require:

```
arm64
x86_64
```

Separate builds may be necessary.

---

## Avoid Runtime pip installs

Reasons:

- breaks reproducibility
- internet may not exist on HPC
- Blender extensions expect bundled dependencies

---

## Avoid Multi-Blender-Version Support Initially

Pin to:

```
Blender 4.3.x
```

Expand support later.

---

# Future Improvements

Potential future improvements:

- automated wheel fetching
- nightly CI builds
- automated Blender compatibility tests
- extension publishing to Blender extension registry
- container image registry (GHCR)

---

# Summary

TraitBlender v2 will:

- ship **platform-specific extension zips**
- bundle **platform wheels**
- build packages via **GitHub Actions matrix**
- support **Docker + HPC workflows**
- maintain **transparent dependency management**
- prioritize **reproducibility**

The repository structure and CI system should support these goals with minimal manual steps.