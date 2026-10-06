"""Minimal CustomTkinter demo demonstrating zero-dependency PyInstaller resource loading.

Author: Rafalus
Repository: https://github.com/RafalusWorks/pyinstaller-resource-path
"""

import customtkinter as ctk
from PIL import Image

from resource_path import resource_path

img_path = resource_path("images/smug_developer.png")


app = ctk.CTk()
app.title("Resource Path Demo")

img = ctk.CTkImage(Image.open(img_path), size=(180, 180))

ctk.CTkLabel(app, image=img, text="").pack(padx=50, pady=50)

if __name__ == "__main__":
    app.mainloop()
