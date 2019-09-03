import re
import tkinter as tk
from tkinter import ttk
import webbrowser


class LabelMailto(ttk.Label):
    def __init__(self, master, text, to, subject, msg):
        ttk.Label.__init__(self, master, text=text, cursor="hand2", style="Link.TLabel")

        self.to = to
        self.subject = subject
        self.msg = msg

        self.bind("<Button-1>", self.mailto)

    def mailto(self, event):
        to = ",".join(self.to)
        subject = self.convert(self.subject)
        msg = self.convert(self.msg)
        webbrowser.open_new(f"mailto:{to}&subject={subject}&body={msg}")

    def convert(self, text):
        text = re.sub(r" ", "%20", text)
        text = re.sub(r"\n", "%0D", text)
        text = re.sub(r"<", "%3C", text)
        text = re.sub(r">", "%3E", text)
        return text