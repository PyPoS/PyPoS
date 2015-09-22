#!/usr/bin/env python

__author__ = 'ebo'

from Tkinter import *  # get widget classes
from tkMessageBox import askokcancel  # get canned std dialog
import ttk


# subclass our GUI
class Quitter(Frame):
    # constructor method
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack()
        widget = ttk.Button(self, text="Quit", command=self.quit)
        widget.pack(side=LEFT)

    def quit(self):
        ans = askokcancel("Verify exit", "Are you sure you want to quit ?")
        if ans:
            Frame.quit(self)


if __name__ == "__main__":
    Quitter().mainloop()