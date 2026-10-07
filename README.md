# pyinstaller-resource-path

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A zero-dependency, copy-paste helper function that permanently eliminates `FileNotFoundError` when loading assets (images, icons, fonts, JSON) in PyInstaller-frozen apps.

Works out of the box in both `--onefile` and `--onedir` builds.

Originally developed by [**Rafalus**](https://github.com/RafalusWorks) for the [`ctkforge`](https://github.com/RafalusWorks/ctkforge) ecosystem.

---

## The Problem

Relative paths like `"images/icon.png"` work on your machine during dev because Python checks the current working directory. 

The moment you freeze with PyInstaller, it blows up:
- **`--onefile`**: Bundled assets extract into an ephemeral temporary folder at runtime (`sys._MEIPASS`). Your app's working directory is not there.
- **`--onedir`**: Bundled assets are isolated inside the `_internal/` bundle directory (`sys._MEIPASS`), unreachable by standard relative paths.

Hardcoding relative paths or guessing with `os.getcwd()` guarantees a crash on startup.

> For an in-depth architectural breakdown, see [How It Works](docs/how-it-works.md).

---

## The Solution

Drop [`resource_path.py`](resource_path.py) into your project and call it:

```python
from resource_path import resource_path

icon_path = resource_path("images/icon.png")
```

It resolves across a clean 3-tier fallback chain:
1. **Frozen Bundle (`sys._MEIPASS`)**: Checks the internal package first (`_internal/` for `--onedir`, temp extraction folder for `--onefile`).
2. **Direct Path**: Checks if the target exists directly on disk or in the current working directory.
3. **Development Entry Point**: Checks next to the running script (`sys.argv[0]`).

Returns a `pathlib.Path` pointing to the real file, or `None` if it does not exist.

Zero dependencies. Just Python standard library `sys` and `pathlib.Path`.

> [!NOTE]
> - **DO**: Organize assets inside project subdirectories (e.g., `images/`, `assets/`) and pass relative paths.
> - **DON'T**: Pass absolute paths (`C:\...` or `/home/...`). They break portability across machines and trigger a `UserWarning`.

---

## Quick Start

### 1. Grab the Function
Copy [`resource_path.py`](resource_path.py) into your codebase.

### 2. Basic Usage
```python
from resource_path import resource_path

# Resolves across Dev, PyInstaller --onefile (_MEIPASS), and --onedir
icon_path = resource_path("images/icon.png")
```

### 3. CustomTkinter Example
```python
import customtkinter as ctk
from PIL import Image
from resource_path import resource_path

app = ctk.CTk()
app.title("Quick Start")

img_path = resource_path("images/smug_developer.png")
img = ctk.CTkImage(Image.open(img_path), size=(180, 180))

ctk.CTkLabel(app, image=img, text="").pack(padx=30, pady=30)
app.mainloop()
```

> **Note**: Make sure `smug_developer.png` sits inside the `images/` directory relative to your script.

---

## Running the Demo

Ensure `demo_ctk.py`, `resource_path.py`, and `images/` are in the same folder:

```text
your_project/
├── demo_ctk.py
├── resource_path.py
└── images/
    └── smug_developer.png
```

```bash
pip install customtkinter pillow pyinstaller
python demo_ctk.py
```

---

## Packaging the Demo into an Executable (PyInstaller)

Use `--add-data` to bundle your `images/` folder.

Path separator rules:
- **Windows**: Semicolon (`;`)
- **macOS / Linux**: Colon (`:`)
- **CustomTkinter**: Always pass `--collect-all customtkinter` or its themes and fonts will be missing from the build.

### Windows (PowerShell / Command Prompt)

**Single executable (`--onefile`):**
```powershell
pyinstaller --noconsole --onefile --collect-all customtkinter --add-data "images;images" demo_ctk.py
```

**Folder bundle (`--onedir`):**
```powershell
pyinstaller --noconsole --onedir --collect-all customtkinter --add-data "images;images" demo_ctk.py
```

### macOS & Linux (Bash / Zsh)

**Single executable (`--onefile`):**
```bash
pyinstaller --noconsole --onefile --collect-all customtkinter --add-data "images:images" demo_ctk.py
```

**Folder / App bundle (`--onedir`):**
```bash
pyinstaller --noconsole --onedir --collect-all customtkinter --add-data "images:images" demo_ctk.py
```
---

## Author & License

- **Author**: [Rafalus](https://github.com/RafalusWorks)
- **Origin**: Extracted from [`ctkforge`](https://github.com/RafalusWorks/ctkforge)
- **License**: [MIT License](LICENSE)
