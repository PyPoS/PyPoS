#! /usr/bin/env python
from __future__ import print_function
__author__ = 'ebo'

from Tkinter import BOTH
import ttk
import csv
from tkMessageBox import showinfo, showerror


class NewDb:
    def __init__(self, master):
        self.master = master
        self.search_frame = ttk.Frame(self.master)
        # bring the UI elements on the board
        self.master.title("New Database Information")

        self.search_lbl = ttk.Label(self.search_frame, text="Database Name", foreground='blue')
        self.search_lbl.grid(row=0, column=0)

        self.search_entry = ttk.Entry(self.search_frame, width=40, foreground='black')
        self.search_entry.grid(row=1, column=0)
        self.search_entry.focus()

        self.search_btn = ttk.Button(self.search_frame, text="Create", command=self.create_db)
        self.search_btn.grid(row=1, column=1)
        self.search_btn.bind()
        # pack them on the screen
        self.search_frame.pack(fill=BOTH, padx=10, pady=10)

    def create_db(self):
        new_file_name = "db/", str(self.search_entry.get()), ".csv"

        try:
            with open(''.join(new_file_name), 'a+') as db:
                writer = csv.writer(db)
                writer.writerow("")
                db.close()

            showinfo(title="Success", message="New database created successfully",
                     parent=self.master)
        except IOError:
            showerror(title="Alert !", message="An error occurred while creating the database",
                      parent=self.master)


