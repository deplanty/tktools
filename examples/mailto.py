import tkinter as tk
from tkinter import ttk

import tktools


class Example(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)

        style = ttk.Style()
        style.configure("Link.TLabel", foreground="#1530EE")

        self.__createUI()
        self.mainloop()
    
    def __createUI(self):
        msg = {
            "to": "jon.snow@got.com",
            "subject": "You know nothing",
            "msg": "I'm a free woman\nIngrid"
        }
        l = tktools.LabelMailto(self, "Send to Jon Snow", **msg, style="Link.TLabel")
        l.pack(padx=5, pady=5)

        msg = {
            "to": ["dany@got.com", "jon.snow@got.com"],
            "subject": "Secret",
            "msg": "I love you\nJoras"
        }
        l = tktools.LabelMailto(self, "Send to Dany", **msg, style="Link.TLabel")
        l.pack(padx=5, pady=5)
    

if __name__ == "__main__":
    Example()