import tkinter as tk
from tkinter import ttk


class ScrollListbox(ttk.Frame):
    """
    A scrollable listbox widget
    """

    def __init__(self, master=None, **kwargs):
        ttk.Frame.__init__(self, master)

        font = "Calibri 12"

        f = ttk.Frame(self, relief="groove", border=1)
        f.grid(row=0, column=0, sticky="ns")
        self.lb = tk.Listbox(
            f,
            relief="flat",
            highlightthickness=0,
            activestyle="none",
            font=font,
            **kwargs,
        )
        sb = ttk.Scrollbar(f, command=self.lb.yview)
        self.lb.configure(yscrollcommand=sb.set)
        self.lb.grid(row=0, column=0, sticky="ns")
        sb.grid(row=0, column=1, sticky="ns")

        f.rowconfigure(0, weight=True)
        self.rowconfigure(0, weight=True)

    def clear(self):
        """
        Clear all the items in listbox
        """
        self.lb.delete(0, "end")

    def insert(self, *args):
        """
        Insert all arguments ``args`` at the end of the listbox
        """
        self.lb.insert("end", *args)

    def get(self, index):
        """
        Return the item from the listbox at given ``index``.
        Or return all the item if ``index`` is "all"
        Or return the current selection if ``index`` is "current"
        """

        if index == "current":
            return self.lb.curselection()
        elif index == "all":
            return self.lb.get(0, "end")
        else:
            return self.lb.get(index)

    def setColor(self, index, color):
        self.lb.itemconfig(index, bg=color)

    def unselectAll(self):
        self.lb.select_clear(0, "end")