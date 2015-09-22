#! /usr/bin/env python
from __future__ import print_function
__author__ = 'ebo'

from Tkinter import *
import ttk


class AppHelp:
    def __init__(self, master):
        self.master = master
        self.search_frame = ttk.Frame(self.master)
        # bring the UI elements on the board
        self.master.title("Help")

        self.text_instruction = Text(self.master, width=44, height=5)
        self.text_instruction.insert(END, '\nWKD HEALTHCARE POINT OF SALES SYSTEM')
        self.text_instruction.insert(END, '\n')

        self.text_instruction.config(state=DISABLED)
        self.text_instruction.pack()
