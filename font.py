import tkinter as tk
from tkinter import font

root = tk.Tk()

# Liste der verfügbaren Schriftarten
available_fonts = font.families()

for font_family in available_fonts:
    print(font_family)

root.destroy()
