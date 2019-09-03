import tkinter as tk
from tkinter import ttk


class ProgressBar:
    def __init__(self, master=None, n_process=1):
        self.master = master
        self.n_process = n_process

        self.n_tot = 0
        self.n_bars = [tk.IntVar(0) for _ in range(n_process)]
        self.bars = list()

        self.__createUI()
    
    def __createUI(self):
        if self.master is not None:
            self.f_main = ttk.Frame(self.master)
        else:
            self.f_main = tk.Toplevel()
        
        for _ in range(self.n_process):
            bar = ttk.Progressbar(self.f_main, orient="horizontal")
            bar.pack(fill="x", expand=True, padx=5, pady=5)
            self.bars.append(bar)
    
    def pack(self, **kwargs):
        if self.master is not None:
            self.f_main.pack(**kwargs)



if __name__ == "__main__":
    root = tk.Tk()
    pbar = ProgressBar(root, n_process=3)
    pbar.pack()
    root.mainloop()
