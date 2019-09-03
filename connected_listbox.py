import tkinter as tk
from tkinter import ttk

from .scroll_listbox import ScrollListbox


class ConnectedListbox(ttk.Frame):
    def __init__(
        self,
        master=None,
        list1=[],
        label1="",
        list2=[],
        label2="",
        width=30,
        height=15,
        style=None,
    ):
        ttk.Frame.__init__(self, master)

        l = ttk.Label(self, text=label1, anchor="center", style=style)
        l.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        self.__slb1 = ScrollListbox(
            self, width=width, height=height, selectmode="extended"
        )
        self.__slb1.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        self.__slb1.lb.insert("end", *list1)

        f = ttk.Frame(self)
        f.grid(row=1, column=1, padx=5, pady=5)
        b = ttk.Button(f, text=">>", width=3, command=self.__allTo2)
        b.pack(padx=5, pady=5)
        b = ttk.Button(f, text=">", width=3, command=self.__goTo2)
        b.pack(padx=5, pady=5)
        b = ttk.Button(f, text="<", width=3, command=self.__goTo1)
        b.pack(padx=5, pady=5)
        b = ttk.Button(f, text="<<", width=3, command=self.__allTo1)
        b.pack(padx=5, pady=5)

        l = ttk.Label(self, text=label2, anchor="center", style=style)
        l.grid(row=0, column=2, sticky="ew", padx=5, pady=5)
        self.__slb2 = ScrollListbox(
            self, width=width, height=height, selectmode="extended"
        )
        self.__slb2.grid(row=1, column=2, sticky="ew", padx=5, pady=5)
        self.__slb2.lb.insert("end", *list2)

    def __goTo1(self):
        indicices = self.__slb2.lb.curselection()
        if len(indicices) == 0:
            return

        for i in reversed(indicices):
            cur = self.__slb2.lb.get(i)
            self.__slb2.lb.delete(i)
            self.__slb1.lb.insert("end", cur)

    def __allTo1(self):
        l = self.__slb2.lb.get(0, "end")
        self.__slb2.lb.delete(0, "end")
        self.__slb1.lb.insert("end", *l)

    def __goTo2(self):
        indicices = self.__slb1.lb.curselection()
        if len(indicices) == 0:
            return

        for i in reversed(indicices):
            cur = self.__slb1.lb.get(i)
            self.__slb1.lb.delete(i)
            self.__slb2.lb.insert("end", cur)

    def __allTo2(self):
        l = self.__slb1.lb.get(0, "end")
        self.__slb1.lb.delete(0, "end")
        self.__slb2.lb.insert("end", *l)

    def get(self):
        """
        Return (list1, list2)
        """

        return self.__slb1.lb.get(0, "end"), self.__slb2.lb.get(0, "end")

    def clear(self, side):
        """
        Clear a list

        Parameters:
        -----------
        side : The side to clear = ["right", "left"]
        """

        if side == "left":
            self.__slb1.lb.delete(0, "end")
        elif side == "right":
            self.__slb2.lb.delete(0, "end")
        else:
            raise ValueError('"side" should be left or right')
