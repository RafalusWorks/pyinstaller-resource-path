# pyinstaller-resource-path

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

A zero-dependency, copy-paste helper function that permanently eliminates `FileNotFoundError` when loading assets (images, icons, fonts, JSON) in PyInstaller-frozen apps.

Works out of the box across **Windows**, **macOS**, and **Linux** in both `--onefile` and `--onedir` builds.

Originally developed by [**Rafalus**](https://github.com/RafalusWorks) for the [`ctkforge`](https://github.com/RafalusWorks/ctkforge) ecosystem.

---

## The Problem

Relative paths like `"images/icon.png"` work on your machine during dev because Python checks the current working directory. 

The moment you freeze with PyInstaller, it blows up:
- **`--onefile`**: Bundled assets extract into an ephemeral temporary folder at runtime (`sys._MEIPASS`). Your app's working directory is not there.
- **`--onedir`**: Assets sit next to the binary (`sys.executable`), or inside `Contents/Resources/` on macOS app bundles, not wherever the user launched the shortcut from.

Hardcoding relative paths or guessing with `os.getcwd()` guarantees a crash on startup.

---

## The Solution

Drop [`resource_path.py`](resource_path.py) into your project and call it:

```python
from resource_path import resource_path

icon_path = resource_path("images/icon.png")
```

It resolves across a 4-tier fallback chain:
1. **Direct Path**: Checks if the target exists directly on disk or in the current working directory.
2. **`--onefile` Temporary Folder**: Checks `sys._MEIPASS / relative_path`.
3. **`--onedir` Application Directory**: Checks next to `sys.executable` (and `Contents/Resources` on macOS).
4. **Development Entry Point**: Checks next to the running script (`sys.argv[0]`).

Returns a `pathlib.Path` pointing to the real file, or `None` if it does not exist.

Zero dependencies. Just Python standard library `sys` and `pathlib.Path`.

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

### Option 1: Copy Files to Your Project Folder
Ensure `demo_ctk.py`, `resource_path.py`, and `images/` are in the same folder:

```text
your_project/
├── demo_ctk.py
├── resource_path.py
└── images/
    └── smug_developer.png
```

Install required libraries:
```bash
pip install customtkinter pillow pyinstaller
```

Run the demo:
```bash
python demo_ctk.py
```

### Option 2: Clone & Run
```bash
git clone https://github.com/RafalusWorks/pyinstaller-resource-path.git
cd pyinstaller-resource-path

pip install -r requirements.txt
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

## Project Structure

```text
pyinstaller-resource-path/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── resource_path.py      <-- The zero-dependency helper
├── demo_ctk.py           <-- Minimal CustomTkinter demonstration
└── images/
    └── smug_developer.png
```

---

## Author & License

- **Author**: [Rafalus](https://github.com/RafalusWorks)
- **Origin**: Extracted from [`ctkforge`](https://github.com/RafalusWorks/ctkforge)
- **License**: [MIT License](LICENSE)
