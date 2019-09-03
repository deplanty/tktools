import tkinter as tk
from tkinter import ttk


class ScrollFrame(ttk.Frame):
    """
    A pure Tkinter scrollable frame that actually works!
    Use the ``f`` attribute to place widgets inside the scrollable frame

    :Example:

        import tkinter as tk
        root = tk.Tk()
        frame = ScrollFrame(root)
        frame.pack()
        ttk.Label(frame.f, text="Example").pack()
        frame.clear()
        root.mainloop()
    """

    def __init__(self, master, width=None, height=None, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = ttk.Scrollbar(self, orient="vertical")
        self.canvas = canvas = tk.Canvas(
            self, width=width, height=height, border=0, highlightthickness=0
        )
        vscrollbar.config(command=canvas.yview)
        canvas.config(yscrollcommand=vscrollbar.set)
        vscrollbar.grid(row=0, column=1, sticky="ns")
        canvas.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.f = f = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=f, anchor="nw")

        def _configure_interior(event):
            """
            Track changes to the canvas and frame width and sync them,
            Also updating the scrollbar
            """

            self.update()
            # update the scrollbars to match the size of the inner frame
            size = (f.winfo_reqwidth(), f.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            # if f.winfo_reqwidth() != canvas.winfo_width():
            #     # update the canvas's width to fit the inner frame
            #     canvas.config(width=f.winfo_reqwidth())

        f.bind("<Configure>", _configure_interior)

        def _configure_canvas(event):
            self.update()
            if f.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind("<Configure>", _configure_canvas)

    def clear(self):
        """
        Clear all the element in frame
        """

        for child in self.f.winfo_children():
            child.destroy()

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)