import time
import tkinter as tk
from tkinter import ttk


class Progressbar(tk.Toplevel):
    """
    Create a progress bar to display the progress of events

    kwargs:
        - status (str)
        - n (int > 0)
        - n_max (int > n)
    """

    def __init__(self, master=None, **kwargs):
        tk.Toplevel.__init__(self, master)

        self.status = ""

        self.n = tk.IntVar(0)
        self.n_max = 10
        self.percent = tk.StringVar("")

        self.__setArgs(kwargs)

        self.withdraw()
        self.createUI()
        self.centerUI()
        self.resizable(False, False)
        self.deiconify()
        self.grab_set()
        self.loop()

    def createUI(self):
        """
        Create the UI
        """

        self.title("Progression")

        f = ttk.Frame(self)
        f.pack(fill="both", padx=10, pady=10)

        l = ttk.Label(f, textvariable=self.percent, anchor="w")
        l.pack(fill="x")

        self.bar = ttk.Progressbar(
            f,
            orient="horizontal",
            length=400,
            mode="determinate",
            maximum=self.n_max,
            variable=self.n,
        )
        self.bar.pack(padx=5, pady=5)

        f_btn = ttk.Frame(f)
        f_btn.pack(fill="x")
        self.b_ok = ttk.Button(f_btn, text="Ok", state="disabled", command=self.btn_ok)
        self.b_ok.pack(side="right", padx=5, pady=5)

        self.__updatePercent()
        self.__updateProgressbar()
        self.__updateBtnOk()

    def centerUI(self):
        """
        Center the UI on screen
        """

        self.update()
        w_screen = self.winfo_screenwidth()
        h_screen = self.winfo_screenheight()
        w = self.winfo_width()
        h = self.winfo_height()
        pos_x = w_screen // 2 - w // 2
        pos_y = h_screen // 2 - h // 2
        self.geometry("%dx%d+%d+%d" % (w, h, pos_x, pos_y))
    
    def loop(self):
        self.update()
        self.after(100, self.loop)

    def set(self, **kwargs):
        """
        Set variables values

        kwargs:
            - status (str)
            - n (int > 0)
            - n_max (int > n)
        """

        self.__setArgs(kwargs)
        self.__updatePercent()
        self.__updateProgressbar()
        self.__updateBtnOk()

    def step(self, delta=1, pause=0.01):
        """
        Next step of the progression
        A pause time can be set to let the changes be visible (in seconds)
        """

        time.sleep(pause)

        if self.n.get() + delta <= self.n_max:
            self.n.set(self.n.get() + delta)

        self.__updatePercent()
        self.__updateBtnOk()
        self.update()

    def waitOk(self):
        """
        Wait for the user to press "Ok" button
        """

        self.b_ok.config(state="enabled")
        self.wait_window()

    def btn_ok(self, *args):
        """
        Press ok to close the window when progress ends
        """

        self.grab_release()
        self.destroy()

    def __updatePercent(self):
        """
        Update percentage
        """

        n = self.n.get()
        status = self.status

        if self.n_max == 0:
            p = status
        else:
            if status != "":
                p = "%03d%% - %s" % (100.0 * n / self.n_max, status)
            else:
                p = "%03d%%" % (100.0 * n / self.n_max)
        self.percent.set(p)

    def __updateProgressbar(self):
        """
        Update the progressbar
        """

        self.bar.config(maximum=self.n_max)

    def __updateBtnOk(self):
        """
        Update the Ok Button
        """

        if self.n.get() >= self.n_max:
            self.b_ok.config(state="enabled")
        else:
            self.b_ok.config(state="disabled")

    def __setArgs(self, kwargs):
        """
        Set variable values from the kwargs for the `init` and `set` function
        """

        if "status" in kwargs:
            self.status = kwargs["status"]

        if "n" in kwargs:
            self.n.set(kwargs["n"])

        if "n_max" in kwargs:
            if kwargs["n_max"] < self.n.get():
                self.n.set(kwargs["n_max"])
            self.n_max = kwargs["n_max"]

class ProgressBar:
    def __init__(self, master=None, n_maxs=1, linked=False):
        if master is not None:
            self.f_main = ttk.Frame(master)
        else:
            self.f_main = tk.Toplevel()
        try:
            self.n_process = len(n_maxs)
            self.n_maxs = n_maxs
        except:
            self.n_process = 1
            self.n_maxs = [n_maxs]
        self.linked = linked

        self.n_tot = 0
        self.n_bars = [tk.IntVar(0) for _ in self.n_maxs]
        self.bars = list()

        self.__createUI()
    
    def __createUI(self):
        
        for var, maxi in zip(self.n_bars, self.n_maxs):
            bar = ttk.Progressbar(self.f_main, orient="horizontal", variable=var, maximum=maxi)
            bar.pack(fill="x", expand=True, padx=5, pady=5)
            self.bars.append(bar)
    
    def step(self, bar=0, delta=1):
        """
        #TODO: docstring and fix bugs in this function
        
        Args:
            bar (int, optional): corresponding progressbar. Defaults to 0.
            delta (int, optional): delta value to add to the progressbar. Defaults to 1.
        """

        # Get current value for the bar
        n = self.n_bars[bar].get()
        # If next step is in the range
        if n+delta <= self.n_maxs[bar]:
            self.n_bars[bar].set(n+delta)
        # else
        else:
            # If linked
            if self.linked:
                # Go backt to 0
                self.n_bars[bar].set(0)
                # Add delta to the next bar
                if bar < self.n_process:
                    self.step(bar+delta)
        self.f_main.update()
    
    def pack(self, **kwargs):
        self.f_main.pack(**kwargs)


if __name__ == "__main__":
    import time

    pbar = ProgressBar(n_maxs=[100, 5], linked=True)
    for x in range(500):
        pbar.step()
        time.sleep(0.01)
    time.sleep(2)
