#! /usr/bin/env python
from __future__ import print_function

from Tkinter import *
from PIL import Image, ImageTk
from classes.stock import *
from classes.dispense import DispenseDrug
from classes.app_help import AppHelp
from classes.app_about import AppAbout
from classes.new_db import NewDb

from classes import client
from PIL import Image, ImageTk
import sql


class MainClass:
    """
    The mother.
    """

    def __init__(self, master):
        self.master = master
        self.master.geometry("600x600+500+250")
        # self.master.wm_iconbitmap(r'favicon.ico')

        self.style = ttk.Style()
        self.master.title("WKD Healthcare")

        self.style.configure("TLabel", foreground="black", font='Courier 10')
        ttk.Style().configure("TButton", padding=3, relief="flat",
                              background="#ccc", font='Courier 10')

        # # possible themes we could use. Checked the ttk docs and they are:
        # # alt, clam, classic
        self.style.theme_use("clam")

        self.menubar = Menu(self.master)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Help", command=self.app_help)
        self.helpmenu.add_command(label="About", command=self.app_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        # adding settings menu drop-down
        self.settings_menu = Menu(self.menubar, tearoff=0)
        self.settings_menu.add_command(label="Synchronize", command=self.sync_database)
        self.menubar.add_cascade(label="Settings", menu=self.settings_menu)

        self.master.config(menu=self.menubar)
        self.left_frame = ttk.Frame(self.master, relief=RAISED, borderwidth=1)

        # background image
        self.img_back = PhotoImage(file="res/home-bg.png")
        self.lbl_background = ttk.Label(self.left_frame, style="BW.TLabel", borderwidth=0)
        self.lbl_background.place(x=150, y=50)
        self.lbl_background['image'] = self.img_back

        intro_label = ttk.Label(self.left_frame,
                                text='Point of Sales System designed for WKD Healthcare.\n\n'
                                     'Action buttons are on the right\n\n'
                                     'If you need any assistance, check the Help\n'
                                     'section in the toolbar menu above.').place(x=50, y=250)
        self.left_frame.pack(fill=BOTH, expand=1, side=LEFT)

        ## Buttons!
        self.btns_frame = ttk.Frame(self.master)

        self.btn_products = ttk.Button(self.btns_frame,
                                       command=self.dispense_drug)
        self.dispense_icon = PhotoImage(file="res/dispense_icon.png")
        self.btn_products['image'] = self.dispense_icon
        self.btn_products.pack(side='top')
        dispense_label = ttk.Label(self.btns_frame, text="Dispense Drug").pack()

        self.btn_manage_stock = ttk.Button(self.btns_frame,
                                           command=self.update_stock_window)
        self.manage_stock_icon = PhotoImage(file="res/manage_stock.png")
        self.btn_manage_stock['image'] = self.manage_stock_icon
        self.btn_manage_stock.pack(side='top', pady=10)
        manage_stock_label = ttk.Label(self.btns_frame, text="Manage Stock").pack()

        self.btn_export_stock = ttk.Button(self.btns_frame,
                                           command=self.export_to_csv)
        self.export_stock_icon = PhotoImage(file="res/export_to_excel.png")
        self.btn_export_stock['image'] = self.export_stock_icon
        self.btn_export_stock.pack(side='top', pady=10)
        export_stock_label = ttk.Label(self.btns_frame, text="Export Stock").pack()

        # imported table-like multi list box
        self.listBox = MultiListbox(self.left_frame, (("Drug Name", 25),
                                                      ("Expiring Date", 15)))
        self.listBox.place(x=50, y=400)

        self.btns_frame.pack(side=RIGHT, padx=40)

        self.notify_of_expiring_drugs()

    def notify_of_expiring_drugs(self):
        list_of_drugs = sql.session.query_for_expiring_drugs()
        self.listBox.delete(0, END)
        self.update_listbox(list_of_drugs)

    def update_listbox(self, db_table):
        for row in db_table:
            self.listBox.insert(END, (row[0],
                                      row[1]))
        self.listBox.selection_set(0)

    def create_new_db(self):
        new_db_window = Toplevel(self.master)
        new_db = NewDb(new_db_window)
        print("Now running", new_db)

    def app_help(self):
        help_window = Toplevel(self.master)
        app_help = AppHelp(help_window)
        print("Now running", app_help)

    def app_about(self):
        about_window = Toplevel(self.master)
        app_about = AppAbout(about_window)
        print("Now running", app_about)

    @staticmethod
    def sync_database():
        stock = sql.session.get_all()
        # print(stock[0])
        client.connect_to_server(stock)

    def dispense_drug(self):
        dispense_window = Toplevel(self.master)
        dispense = DispenseDrug(dispense_window)
        print("Now running", dispense)

    def update_stock_window(self):
        update_stock = Toplevel(self.master)
        stock = StockClass(update_stock)
        print("Now running", stock)

    def close_windows(self):
        self.master.destroy()

    def export_to_csv(self):
        # popup window
        ans = askokcancel("Verify Export Action",
                          "You are about to export your database contents into an excel "
                          "spreadsheet.\n\nPress OK to continue.",
                          parent=self.master)
        if ans:
            infile_list = sql.session.get_all()
            # print(infile_list)
            outfile = open("db/excel_stock.csv", 'w')

            outfile.write('Drug Name, Quantity, Price, Total, Expiring Date, Category\n')

            for line in infile_list:
                row = line[0], str(line[1]), str(line[2]), str(line[3]), line[4], line[5], '\n'
                print(', '.join(row))
                outfile.write(', '.join(row))

            outfile.close()
            showinfo(title="Stock data exported!",
                     message="Your stock data has been exported to 'db/excel_stock.csv'.",
                     parent=self.master)


root = Tk()
MainClass(root)
root.mainloop()
