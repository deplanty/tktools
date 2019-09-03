import tkinter as tk
from tkinter import ttk

import tktools


class Example(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.__createUI()
        self.mainloop()
    
    def __createUI(self):
        l1 = [0, 1, 2, 3, 4, 5, 6]
        l2 = [7, 8, 9]
        self.cl = tktools.ConnectedListbox(self, l1, "Keep", l2, "Archive")
        self.cl.pack(fill="y", expand=True, padx=5, pady=5)

        f = ttk.Frame(self)
        f.pack()
        b = ttk.Button(f, text="Ok", command=self.__btn_ok)
        b.pack(side="left", padx=5, pady=5)
        b = ttk.Button(f, text="Cancel", command=self.__btn_cancel)
        b.pack(side="left", padx=5, pady=5)

    def __btn_ok(self):
        l1, l2 = self.cl.get()
        print("List 1", l1)
        print("List 2", l2)
        self.after(500, self.destroy)
    
    def __btn_cancel(self):
        self.cl.clear()
        print("Lists cleared")
        self.after(500, self.destroy)


if __name__ == "__main__":
    Example()