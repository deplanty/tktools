import tkinter as tk
from tkinter import ttk

import tktools


class Example(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        self.__createUI()
        self.__fillTable()
        self.mainloop()
    
    def __createUI(self):
        self.table = tktools.Table(self)
        self.table.pack(side="left", fill="y", expand=True)

        f = ttk.Frame()
        f.pack(side="left")
        b = ttk.Button(self, text="Add line", command=self.__btn_add)
        b.pack(padx=5, pady=5)
        b = ttk.Button(self, text="Sort lines", command=self.__btn_sort)
        b.pack(padx=5, pady=5)
        b = ttk.Button(self, text="Show", command=self.__btn_show)
        b.pack(padx=5, pady=5)
        b = ttk.Button(self, text="Show selected", command=self.__btn_showSelected)
        b.pack(padx=5, pady=5)

    def __fillTable(self):
        array = [
            ["ID", "Name", "Country", "Value", "Usefull"],
            ["001", "Jon", "North", 30, "True"],
            ["002", "Dany", "South", 20, "True"],
            ["003", "Bran", "Westeros", 99, "False"]
        ]

        self.table.set(array, header=True, id_col=0)
        self.table.block(0)
        self.table.choice(1, list_choices=["North", "South", "Westeros"])
        self.table.toggle(3, values=["True", "False"])
    
    def __btn_add(self):
        self.table.add()
        print("In progress")
    
    def __btn_sort(self):
        self.table.sort()
        print("In progress")

    def __btn_show(self):
        array = self.table.get()
        print(*array, sep="\n")
    
    def __btn_showSelected(self):
        iid, line = self.table.selected()
        print(iid, *line)
    

if __name__ == "__main__":
    Example()