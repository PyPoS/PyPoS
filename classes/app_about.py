#! /usr/bin/env python
from __future__ import print_function
__author__ = 'ebo'

from Tkinter import *
import ttk


class AppAbout:
    def __init__(self, master):
        self.master = master
        self.search_frame = ttk.Frame(self.master)
        # bring the UI elements on the board
        self.master.title("About App")

        self.text_instruction = Text(self.master, width=44, height=5)
        self.text_instruction.insert(END, '\nWKD HEALTHCARE POINT OF SALES SYSTEM')

        self.text_instruction.insert(END, '\nVersion 0.01 (BETA)')
        self.text_instruction.insert(END, '\n')
        self.text_instruction.insert(END, '\nPowered by Open Source Software')

        self.text_instruction.config(state=DISABLED, background='#73B9FE')
        self.text_instruction.pack()

        self.search_frame.pack()

