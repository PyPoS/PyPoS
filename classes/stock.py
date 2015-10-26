#!/usr/bin/env python
__author__ = 'ebo'

from classes.quitter import Quitter
from classes.multiListBox import MultiListbox
from tkMessageBox import askokcancel, showinfo, showerror
import re
import sql
# settling python2 and python3 differences
try:
    from Tkconstants import LEFT, BOTH, RIGHT, END
    from Tkinter import TclError, Toplevel
    import ttk
except ImportError:
    from tkinter import LEFT, BOTH, RIGHT, END
    from tkinter import TclError, Toplevel
    from tkinter import ttk


class StockClass:
    """
    Interface for stock entry.
    """

    def __init__(self, master):
        """
        Create, pack, and bind entry boxes and buttons for stock entry.
        """

        self.master = master
        self.frame = ttk.Frame(self.master)
        self.master.title("Williams Chemicals - Update Stock Records")
        # instructions
        self.instructionFrame = ttk.Frame(self.master)
        self.instructionFrame.pack()

        ttk.Label(self.instructionFrame,
                  text="Enter the Medicine information below") \
            .pack(pady=20)

        # entry boxes and column headers
        self.entryFrame = ttk.Frame(self.master)
        self.entryFrame.pack(padx=10)

        # column headings
        self.col1 = ttk.Label(self.entryFrame, text="Drug Name")
        self.col1.grid(row=0, column=0)

        self.col2 = ttk.Label(self.entryFrame, text="Quantity")
        self.col2.grid(row=0, column=1)

        self.col3 = ttk.Label(self.entryFrame, text="Price")
        self.col3.grid(row=0, column=2)

        self.col4 = ttk.Label(self.entryFrame, text="Total")
        self.col4.grid(row=0, column=3)

        self.col5 = ttk.Label(self.entryFrame, text="Expiring Date")
        self.col5.grid(row=0, column=4)

        self.col6 = ttk.Label(self.entryFrame, text="Category")
        self.col6.grid(row=0, column=5)

        # entry boxes
        self.drugBox = ttk.Entry(self.entryFrame, name="drug")
        self.drugBox.grid(row=1, column=0)

        self.qtyBox = ttk.Entry(self.entryFrame, name="qty")
        self.qtyBox.grid(row=1, column=1)

        self.priceBox = ttk.Entry(self.entryFrame, name="price")
        self.priceBox.grid(row=1, column=2)

        self.totalBox = ttk.Entry(self.entryFrame, name="total")
        self.totalBox.grid(row=1, column=3)

        self.expDateBox = ttk.Entry(self.entryFrame, name="expDate")
        self.expDateBox.grid(row=1, column=4)

        self.categoryBox = ttk.Entry(self.entryFrame, name="category")
        self.categoryBox.grid(row=1, column=5)

        # drug entry buttons
        self.entryBtnFrame = ttk.Frame(self.master)
        self.entryBtnFrame.pack()

        self.newEntryBtn = ttk.Button(self.entryBtnFrame, text="Enter Drug",
                                      command=self.add_stock)
        self.newEntryBtn.pack(side=LEFT)

        # Imported quit button
        Quitter(self.entryBtnFrame).pack(side=LEFT)

        #########################################################################
        # CURRENT STOCK DISPLAY                                                 #
        #########################################################################

        # title heading
        self.frameHeading = ttk.Frame(self.master)
        self.frameHeadingTitle = ttk.Label(self.frameHeading, text="Current Stock",
                                           font=("Arial", "12", "bold"))
        self.frameHeading.pack()
        self.frameHeadingTitle.pack(pady=10)

        # database to output here
        self.showInventoryFrame = ttk.Frame(self.master)
        self.showInventoryFrame.pack(expand=1, fill=BOTH, padx=10, pady=10)

        # imported table-like multi list box
        self.listBox = MultiListbox(self.showInventoryFrame, (("Drug Name", 30),
                                                              ("Quantity", 10),
                                                              ("Price", 10),
                                                              ("Total", 10),
                                                              ("Expiring Date", 15),
                                                              ("Category", 40)))
        self.listBox.pack(expand=1, fill=BOTH)

        # stock display buttons
        self.inventoryBtnFrame = ttk.Frame(self.master)
        self.inventoryBtnFrame.pack(fill=BOTH, padx=10, pady=20)

        self.fetchStock = ttk.Button(self.inventoryBtnFrame, text="Fetch Inventory",
                                     command=self.get_inven)
        self.fetchStock.pack(side=RIGHT)

        self.updateStock = ttk.Button(self.inventoryBtnFrame, text="Update Medicine",
                                      command=self.change_inven)
        self.updateStock.pack(side=RIGHT)

        self.deleteInven = ttk.Button(self.inventoryBtnFrame, text="Delete Entry",
                                      command=self.clear_entry)
        self.deleteInven.pack(side=RIGHT)

        self.clearInven = ttk.Button(self.inventoryBtnFrame, text="Clear Inventory",
                                     command=self.del_inven)
        self.clearInven.pack(side=RIGHT)

        #refresh list
        self.get_inven()

    def add_stock(self):
        # new_cat = ["%s," % self.categoryBox.get()]
        new_cat = self.categoryBox.get()
        record = (self.drugBox.get(), self.qtyBox.get(), self.priceBox.get(),
                  self.totalBox.get(), self.expDateBox.get(), new_cat,)

        sql.session.insert_drug(record)

        # clear the entry boxes to prepare them for new data
        self.drugBox.delete(0, END)
        self.qtyBox.delete(0, END)
        self.priceBox.delete(0, END)
        self.totalBox.delete(0, END)
        self.expDateBox.delete(0, END)
        self.categoryBox.delete(0, END)

        # refresh the list
        self.get_inven()

    def get_inven(self):
        stock = sql.session.get_all()
        # print stock
        self.listBox.delete(0, END)
        self.update_listbox(stock)

    def update_listbox(self, db_table):
        for row in db_table:
            self.listBox.insert(END, (row[0],
                                      int(row[1]),
                                      float(row[2]),
                                      int(row[3]),
                                      row[4],
                                      row[5]))
        self.listBox.selection_set(0)

    def clear_entry(self):
        """
        Deletes an entry from the database.

        Gets the highlighted selection, makes a list of all the separate words,
        'pops' the stock name entry, finds the stock name in the file,
        deletes the drug along with its details, then updates the inventory screen.
        """
        # popup window
        try:

            ans = askokcancel("Verify delete", "Are you sure you want to delete entry?", parent=self.master)
            if ans:
                # get index of selection
                self.getSelection = self.listBox.curselection()
                # get tuple from selection
                self.selectedEntry = self.listBox.get(self.getSelection)

                # # use regex to compile information
                self.getSelection = str(self.getSelection)

                regex = re.compile('[0-9]')
                self.selected_index = regex.findall(self.getSelection)

                list_item_position = int(self.selected_index[0]) + 1

                sql.session.delete_drug(list_item_position)

                # show confirmation and call get_inven to update the records
                showinfo(title="Drug removed", message="The Medicine has been removed from your inventory.",
                         parent=self.master)
                self.get_inven()

        # tell user to make a selection first
        except TclError:
            showerror(title="Error !", message="Please make a selection in order to delete", parent=self.master)

    def change_inven(self):
        """
        Allows modification of a database entry.
        Calls the update_drug function
        """
        try:
            # check if a selection was made

            # get index of selection
            self.getSelection = self.listBox.curselection()
            # get tuple from selection
            self.selectedEntry = self.listBox.get(self.getSelection)

            # lets unpack tuple
            (self.drug, self.qty, self.price, self.total, self.expDate,
             self.category) = self.selectedEntry

            # ---New 'edit medicine' window
            self.edit_window = Toplevel()
            self.edit_window.title("Edit selected entry")

            # Edit medicine window widgets
            ttk.Label(self.edit_window, text="Drug Name").grid(row=0, column=0)
            ttk.Label(self.edit_window, text="Quantity").grid(row=0, column=1)
            ttk.Label(self.edit_window, text="Price").grid(row=0, column=2)
            ttk.Label(self.edit_window, text="Total").grid(row=0, column=3)
            ttk.Label(self.edit_window, text="Expiring Date").grid(row=0, column=4)
            ttk.Label(self.edit_window, text="Category").grid(row=0, column=5)

            self.oldDrug = ttk.Entry(self.edit_window, name="drug")
            self.oldDrug.grid(row=1, column=0)

            self.oldQty = ttk.Entry(self.edit_window, name="qty")
            self.oldQty.grid(row=1, column=1)

            self.oldPrice = ttk.Entry(self.edit_window, name="price")
            self.oldPrice.grid(row=1, column=2)

            self.oldTotal = ttk.Entry(self.edit_window, name="total")
            self.oldTotal.grid(row=1, column=3)

            self.oldExpDate = ttk.Entry(self.edit_window, name="expDate")
            self.oldExpDate.grid(row=1, column=4)

            self.oldCat = ttk.Entry(self.edit_window, name="category")
            self.oldCat.grid(row=1, column=5)

            self.update = ttk.Button(self.edit_window, text="Update",
                                     command=self.update_drug).grid(row=2, column=2)
            self.cancel = ttk.Button(self.edit_window, text="Cancel",
                                     command=self.cancel_drug_update).grid(row=2, column=3)

            # edit this.medicine data
            self.oldDrug.insert(END, self.drug)
            self.oldQty.insert(END, self.qty)
            self.oldPrice.insert(END, self.price)
            self.oldTotal.insert(END, self.total)
            self.oldExpDate.insert(END, self.expDate)
            self.oldCat.insert(END, self.category)

        # tell user to make a selection first
        except TclError:
            showerror(title="Error !", message="Please make a selection in order to update", parent=self.master)

    def update_drug(self):
        """
        Change the values of a database entry.
        Called by change_inven Button.
        """
        self.newDrug = self.oldDrug.get()
        self.newQty = self.oldQty.get()
        self.newPrice = self.oldPrice.get()
        self.newTotal = self.oldTotal.get()
        self.newExpDate = self.oldExpDate.get()
        self.newCat = self.oldCat.get()

        # # use regex to compile information
        self.getSelection = str(self.getSelection)

        regex = re.compile('[0-9]')
        self.selected_index = regex.findall(self.getSelection)

        list_item_position = int(self.selected_index[0]) + 1
        self.newRecord = (self.newDrug, self.newQty, self.newPrice,
                          self.newTotal, self.newExpDate, self.newCat, list_item_position)

        sql.session.update_stock(self.newRecord)

        # call the get_inven() function to "refresh" list
        self.get_inven()

        self.edit_window.destroy()

    def cancel_drug_update(self):
        """
        Verify canceling of stock update.
        """
        self.edit_window.destroy()

    def del_inven(self):
        """
        Deletes all entries in database.
        """
        # popup window
        ans = askokcancel("Verify Delete Action",
                          "Are you 'REALLY' sure you want to clear your 'WHOLE' inventory ?",
                          parent=self.master)
        if ans:
            sql.session.delete_all_stock()
            self.get_inven()
            showinfo(title="Inventory cleared",
                     message="Your inventory database has been deleted.", parent=self.master)