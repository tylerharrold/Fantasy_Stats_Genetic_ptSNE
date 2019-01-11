import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.filename = filedialog.askopenfilename(initialdir = "/" , title="Select file", filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
print (root.filename)
