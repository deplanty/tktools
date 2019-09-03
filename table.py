import tkinter as tk
from tkinter import ttk


class Table(ttk.Frame):
    """
    Table with editable cells

    Args:
        master (tk.Widget): master of the table
        *args: ttk.Treeview arguments
        **kwargs: ttk.Treeview keyword arguments
    """

    def __init__(self, master, *args, **kwargs):
        ttk.Frame.__init__(self, master, *args, **kwargs)

        self.list_id = list()
        self.header = None
        self.blocked = set()
        self.toggled = dict()
        self.choices = dict()
        self.n_rows = 1
        self.n_cols = 0

        self.var_entry = tk.StringVar(self, "")

        self.tv = ttk.Treeview(self, selectmode="browse")
        self.tv.pack(side="left", fill="both", expand=True)
        sb = ttk.Scrollbar(self, command=self.tv.yview)
        self.tv.configure(yscrollcommand=sb.set)
        sb.pack(side="left", fill="y")

        self.tv.bind("<Double-Button-1>", self.__onDoubleClic)

    def __onDoubleClic(self, event):
        """
        Manage event when double clic on cell
        """

        # If no item is focused
        iid = self.tv.focus()
        if iid == "":
            return

        # Cannot select first column
        col = self.tv.identify_column(event.x)
        col = int(col.lstrip("#")) - 1
        if col < 0:
            return

        if col in self.blocked:
            return
        elif col in self.toggled:
            vals = list(self.tv.item(iid, "values"))
            vals[col] = self.toggleNext(col, vals[col])
            self.tv.item(iid, values=vals)
        else:
            self.__askValue(iid, col)

    def __askValue(self, iid, col):
        """
        Show the entry at the correct location on the treeview
        """

        def saveAndClose(*args):
            new = self.var_entry.get()
            item["values"][col] = new
            self.tv.item(iid, values=item["values"])
            close()

        def close(*args):
            e.destroy()

        def onTab(*args):
            def nextCol(iid, col):
                if col + 1 < self.n_cols:
                    new_col = col + 1
                else:
                    self.tv.focus_set()
                    ID_prev = self.tv.focus()
                    self.tv.event_generate("<Down>")
                    ID_cur = self.tv.focus()
                    if ID_prev != ID_cur:
                        iid = ID_cur
                        new_col = 0
                    else:
                        return iid, -1

                if new_col not in self.blocked and new_col not in self.toggled:
                    return iid, new_col
                else:
                    return nextCol(iid, new_col)

            saveAndClose()
            # Current row
            ID, new_col = nextCol(iid, col)
            if new_col != -1:
                self.__askValue(ID, new_col)

        item = self.tv.item(iid)
        self.var_entry.set(item["values"][col])

        bbox = self.tv.bbox(iid, column=col)
        bbox = {k: v for k, v in zip(["x", "y", "width", "height"], bbox)}

        if col in self.choices:
            e = ttk.Combobox(self, textvariable=self.var_entry, state="readonly")
            e.configure(values=self.choices[col])
            e.place(**bbox)
            e.bind("<<ComboboxSelected>>", saveAndClose)
            e.select_clear()
            e.grab_set()
            e.focus_set()
            e.after(100, lambda: e.event_generate("<Down>"))
        else:
            e = ttk.Entry(self, textvariable=self.var_entry)
            e.place(**bbox)
            e.select_range(0, "end")
            e.icursor("end")
            e.focus_set()
            e.bind("<FocusOut>", saveAndClose)

        e.bind("<Escape>", close)
        e.bind("<Return>", saveAndClose)
        e.bind("<Tab>", onTab)

    def __updateData(self, matrix, id_col=None):
        """
        Update the data contained in the table

        Args:
            matrix (list): matrix to set in the table
        """

        # Clear previous data
        for child in self.tv.get_children():
            self.tv.delete(child)

        self.list_id.clear()
        self.n_rows = 1

        # Set the data
        for line in matrix:
            if id_col is not None:
                iid = line.pop(id_col)
            else:
                iid = None

            iid = self.tv.insert("", "end", iid, text=self.n_rows, values=line)
            self.list_id.append(iid)
            self.n_rows += 1

    def set(self, matrix, header=False, id_col=None, widths=None):
        """
        Set the data in the table

        Args:
            matrix (list): data the display
            header (bool or list, optional): if False then do not set header, if True then use the first line oh the matrix, if list then use it as header
            id_col (int): column containing the IDs, if None, create them
            widths (list): size of each column
        """

        # Clear previous data
        for child in self.tv.get_children():
            self.tv.delete(child)

        # Get the header
        self.header = header
        if header is True:
            head = matrix.pop(0)
        elif isinstance(header, (list, tuple)):
            head = [x for x in header]
        else:
            n = len(matrix[0])
            head = [""] * n

        if id_col is not None:
            head.pop(id_col)

        # Set the header
        self.n_cols = len(head)
        self.tv.configure(columns=head)
        self.tv.column("#0", width=40)
        for i, label in enumerate(head, 1):
            iid = f"#{i}"
            self.tv.heading(iid, text=label)

        # Set the data
        self.__updateData(matrix, id_col)

        # Set columns size
        if widths is not None:
            for i, w in enumerate(widths, 1):
                iid = f"#{i}"
                self.tv.column(iid, width=w)

    def get(self):
        """
        Return the data of the table

        Returns:
            list: matrix of the table data
        """

        data = list()

        # Manage the header
        # If there is a header
        if self.header is True:
            # Get the titles (without the ID column)
            head = list()
            for i in range(self.n_cols):
                item = self.tv.heading(f"#{i+1}")
                head.append(item["text"])
            head.insert(0, "ID")
            data.append(head)
        # If the header was a list
        elif isinstance(self.header, list):
            data.append(self.header)

        # Stack data
        for iid in self.list_id:
            item = self.tv.item(iid)
            line = item["values"]
            # If the line is not empty
            if not all(x == "" for x in line):
                line = [str(x) for x in line]
                data.append([iid] + line)

        return data

    def add(self, iid=None, values=None):
        """
        Add a new line to the table.
        If values is not None, add values as the new line
        """

        if values is None:
            values = [""] * self.n_cols

        iid = self.tv.insert("", "end", iid, text=self.n_rows, values=values)
        self.list_id.append(iid)
        self.n_rows += 1

    def remove(self, iid):
        """
        Remove the element from its identifier

        Args:
            iid (int or str): identifier of the element
        """

        self.tv.delete(iid)
        self.list_id.remove(iid)

        # Update line numbers
        data = self.get()
        data.pop(0)
        self.__updateData(data, 0)

    def block(self, *cols):
        """
        Block the edition of some columns

        Args:
            cols (int): column numbers blocked
        """

        self.blocked.update(cols)

    def unblock(self, *cols):
        """
        Unblock the edition of some columns

        Args:
            cols (int or str): column numbers unblocked, if "all", unblock all
        """

        if cols == "all":
            self.blocked.clear()
        else:
            for c in cols:
                try:
                    self.blocked.remove(c)
                except:
                    pass

    def toggle(self, *cols, values=["•", "◘"]):
        """
        Toggle values of some columns

        Args:
            cols (int or str): column numbers affected
            values (list): list of item to cycle
        """

        for col in cols:
            self.toggled[col] = values

    def toggleNext(self, col, item):
        """
        Go to next item for the column from an item
        """

        i = self.toggled[col].index(item)
        if i + 1 >= len(self.toggled[col]):
            i = 0
        else:
            i += 1

        return self.toggled[col][i]

    def choice(self, *cols, list_choices):
        """
        Set the columns that are limited by some choices

        Args:
            cols (int): columns affected by the choices
            list_choices (list): list of selectable items
        """

        for col in cols:
            self.choices[col] = list_choices

    def sort(self, with_col=0):
        """
        Sort the table using values of the given column

        Args:
            with_col (int, optional): Defaults to 0. column used to sort the table
        """

        def sort(line):
            return str(line[with_col]).lower()

        # Get table data
        data = self.get()

        # Remove header to sort only the data
        header = data.pop(0)
        data = sorted(data, key=sort)
        data.insert(0, header)

        # Set the sorted data in the table
        data.pop(0)
        self.__updateData(data, 0)

    def selected(self):
        """
        Return the selected item
        """

        select = self.tv.selection()
        if len(select) == 0:
            return None
        else:
            return select[0]
