import enum
import tkinter as tk
from tkinter import ttk


class ScrollText(tk.Frame):
    """
    A scrollable text widget
    """

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master)

        class State(enum.Enum):
            OUT = enum.auto()
            IN = enum.auto()
            IN_FOCUS = enum.auto()

        self.__enum = State
        self.__write_state = self.__enum.OUT
        if "state" in kwargs:
            self.__state = kwargs["state"]
        else:
            kwargs["state"] = self.__state = "normal"

        self.config(background="#888888")
        sb = ttk.Scrollbar(self)
        self.txt = tk.Text(self, yscrollcommand=sb.set, relief="flat", **kwargs)
        sb.config(command=self.txt.yview)
        self.txt.pack(side="left", fill="both", expand=True, padx=1, pady=1)
        sb.pack(side="left", fill="y")

        if kwargs["state"] == "normal":
            self.txt.bind("<Enter>", self.__onEnter)
            self.txt.bind("<Leave>", self.__onLeave)
            self.txt.bind("<FocusIn>", self.__onFocusIn)
            self.txt.bind("<FocusOut>", self.__onFocusOut)

    def __onEnter(self, *args):
        if self.__write_state != self.__enum.IN_FOCUS:
            self.config(bg="#000000")
            self.__write_state = self.__enum.IN

    def __onLeave(self, *args):
        if self.__write_state != self.__enum.IN_FOCUS:
            self.config(bg="#888888")
            self.__write_state = self.__enum.OUT

    def __onFocusIn(self, *args):
        self.config(bg="#2288FF")
        self.__write_state = self.__enum.IN_FOCUS

    def __onFocusOut(self, *args):
        self.config(bg="#888888")
        self.__write_state = self.__enum.OUT

    def get(self):
        return self.txt.get("1.0", "end-1c")

    def set(self, text):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.insert("1.0", text)
        self.txt.configure(state=self.__state)
