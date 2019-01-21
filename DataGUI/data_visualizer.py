import tkinter as tk
from tkinter import filedialog
from pathlib import Path

current_dir = Path.cwd()
root = tk.Tk()
root.filename = filedialog.askopenfilename(initialdir = str(current_dir) , title="Select file")
print (root.filename)
