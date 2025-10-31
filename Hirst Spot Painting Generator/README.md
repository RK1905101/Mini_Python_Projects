# Hirst Spot Painting Generator

A small Python project that generates Hirst-style spot paintings. The code supports both an interactive Turtle-based renderer and a headless Pillow renderer that can export PNG images.

Quick overview
- Interactive renderer: opens a Turtle window and draws a grid of colored dots.
- Headless renderer: creates PNG images using Pillow (no GUI required).
- Palette extraction: uses `colorgram.py` when available, falls back to Pillow's adaptive quantization, and finally a built-in palette.

Features
- Generate spot paintings with configurable rows/columns, dot size, spacing and background color.
- Export to PNG (`--export`) for headless workflows.
- Deterministic output with `--seed`.
- Safe dry-run (`--no-window`) to print configuration without opening a GUI.

Files of interest
- `main.py` — CLI entrypoint (flags: `--rows`, `--cols`, `--dot-size`, `--spacing`, `--bg-color`, `--image`, `--export`, `--no-window`, `--seed`).
- `palette.py` — palette extraction utilities (tries colorgram -> Pillow -> built-in fallback).
- `renderer.py` — rendering backends (Turtle interactive and Pillow PNG export).

Requirements
- Python 3.8+ (virtualenv recommended)
- Pillow (for PNG export and palette fallback)
- colorgram.py (optional; install only if you prefer it)

Install
1. Create and activate a virtual environment (PowerShell example):

```powershell
python -m venv venv
& "${PWD}\venv\Scripts\Activate.ps1"
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Basic usage examples (PowerShell)

- Dry-run (prints configuration and palette, no GUI):

```powershell
python .\main.py --no-window
```

- Interactive Turtle window:

```powershell
python .\main.py
```

- Export a PNG (headless). Requires Pillow in your venv:

```powershell
python .\main.py --export my_painting.png --no-window
```

- Reproducible output with a seed:

```powershell
python .\main.py --export seed_painting.png --seed 42 --no-window
```

Changing layout
- Example: 12 rows, 8 columns, larger dots and more spacing:

```powershell
python .\main.py --rows 12 --cols 8 --dot-size 24 --spacing 60 --export big.png --no-window
```

Notes and troubleshooting
- If PNG export fails with an error about Pillow, run:

```powershell
pip install pillow
```

- If you want to use `colorgram.py` for palette extraction, install it in the venv:

```powershell
pip install colorgram.py
```

Development notes
- The project is modular: `palette.py` encapsulates color extraction strategies and `renderer.py` contains both interactive and headless renderers. This makes it easy to extend or replace backends.
- Recommended next steps: add a small test suite that validates PNG export and palette extraction, or add a simple GUI to tweak parameters.

License
- This repo doesn't include an explicit license. If you plan to publish, consider adding an appropriate LICENSE file.

Enjoy creating art!