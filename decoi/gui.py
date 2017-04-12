### gui

import sys
import tkinter as tk
from config import *



class SeatsChangeApp(tk.Tk):
    def __init__(self, seats=[]):
        tk.Tk.__init__(self)

        self.top_text = tk.Label(self, text="(x,y->a,b) x,y", borderwidth=0, width=10)
        self.top_text.pack(side="top")
        
        self.table = SimpleTable(self, row_length, col_length)
        self.seats_table(seats)
        

        self.table.pack(side="top", fill="x")

    def seats_table (self, seat_table):
        for seat in seat_table:
            self.table.set(seat['ago'][0], seat['ago'][1],
                         "%s,%s->%s,%s" % (seat['ago'][0], seat['ago'][1],
                                           seat['next'][0], seat['next'][1]))


        


class SimpleTable(tk.Frame):
    def __init__(self, parent, rows, columns):
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background="black")
        self._widgets = []

        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = tk.Label(self, text="", 
                                 borderwidth=0, width=10)
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)

        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)



if __name__ == "__main__":
    app = SeatsChangeApp()
    app.mainloop()
