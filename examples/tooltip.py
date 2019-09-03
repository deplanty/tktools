import tkinter as tk
from tkinter import ttk

import tktools


class Example(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.__createUI()
        self.mainloop()
    
    def __createUI(self):
        e = ttk.Entry(self)
        e.pack(fill="x", padx=5, pady=5)
        tktools.Tooltip(e, "Useless entry")

        f = ttk.Frame(self)
        f.pack()
        b = ttk.Button(f, text="Ok")
        b.pack(side="left", padx=5, pady=5)
        tktools.Tooltip(b, "Validate and close")

        b = ttk.Button(f, text="Cancel")
        b.pack(side="left", padx=5, pady=5)
        tktools.Tooltip(b, "Cancel and close")


if __name__ == "__main__":
    Example()