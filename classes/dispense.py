#! /usr/bin/env python
from __future__ import print_function
__author__ = 'ebo'

try:
    import Tkinter as tk
    import ttk
except ImportError:
    import tkinter as tk
    from tkinter import ttk
from classes.stock import *
from classes.auto import AutocompleteEntry
from tkMessageBox import showerror


class DispenseDrug:
    def __init__(self, master):
        self.master = master
        self.search_frame = ttk.Frame(self.master)
        # bring the UI elements on the board

        self.search_lbl = ttk.Label(self.search_frame, text="Search Medicine", foreground='blue')
        self.qty_lbl = ttk.Label(self.search_frame, text="Qty", foreground='blue')

        self.search_lbl.grid(row=0, column=0)
        self.qty_lbl.grid(row=0, column=1)

        # self.search_entry = ttk.Entry(self.search_frame, width=40, foreground='black')

        # initialise the search entry with autocomplete
        try:
            all_drug_names = sql.session.query_drug_names_for_autocomplete()
            # print(all_drug_names)

            # prepare list to receive autocomplete source content
            autocomplete_source = []
            for each_row in all_drug_names:
                # the autocomplete module accepts strings
                # so lets format the returned unicode to strings
                # and append that to the newly created list
                autocomplete_source.append(str(each_row[0]))

            self.search_entry = AutocompleteEntry(self.search_frame, width=40, foreground='black')
            # print(autocomplete_source)
            self.search_entry.set_completion_list(autocomplete_source)

        except IOError:
            print('Error processing data for autocomplete')
        # entry.pack()
        # entry.focus_set()

        self.search_entry.grid(row=1, column=0)
        self.search_entry.focus()
        self.qty_entry = ttk.Entry(self.search_frame, width=8, foreground='black')
        self.qty_entry.grid(row=1, column=1)

        self.search_btn = ttk.Button(self.search_frame, text="Search", command=self.search_drug)
        self.search_btn.grid(row=2, column=1)
        self.search_btn.bind()
        # pack them on the screen
        self.search_frame.pack(fill=BOTH, padx=10, pady=10)

        ########## search results to output here
        self.showInventoryFrame = ttk.Frame(self.master)
        self.showInventoryFrame.pack(expand=1, fill=BOTH, padx=10, pady=10)

        # imported table-like multi list box
        self.listBox = MultiListbox(self.showInventoryFrame, (("Drug Name", 30),
                                                              ("Price (GHS)", 5),
                                                              ("Qty", 5)))
        self.listBox.pack(expand=1, fill=BOTH)

        ########## search results to output here
        self.showTotalFrame = ttk.Frame(self.master)
        self.showTotalFrame.pack(fill=BOTH, padx=5, pady=5)

        self.total_lbl = ttk.Label(self.showTotalFrame, text="Total (GHS)", foreground='blue')
        self.total_lbl.pack(side=LEFT)
        self.total_entry = ttk.Entry(self.showTotalFrame, width=7, foreground='red')
        self.total_entry.pack(side=LEFT)

        ########## search operation buttons
        self.saleBtnsFrame = ttk.Frame(self.master)
        self.saleBtnsFrame.pack(fill=BOTH, padx=10, pady=5)

        self.delete_entry_btn = ttk.Button(self.saleBtnsFrame, text="Delete Entry",
                                           command=self.delete_entry)
        self.checkout_btn = ttk.Button(self.saleBtnsFrame, text="Checkout",
                                       command=self.checkout)
        self.checkout_btn.pack(side=RIGHT)
        self.delete_entry_btn.pack(side=RIGHT)

        self.clear_button = ttk.Button(self.saleBtnsFrame, text='Clear List', command=self.clear_sales_list)
        self.clear_button.pack(side=RIGHT)

        ## other init values
        # TODO: check (Am I polluting the 'self' namespace with all these bindings?)
        self.curr_pos = 0
        self.all_items_pos = []
        self.checkout_pressed = False

        ## the total_item_quantity stores the quantities of the
        #  searched items displayed in the listbox for further calculations
        self.total_item_quantity = []

    def search_drug(self):
        # get the entered search query
        search_query = self.search_entry.get()
        # for the quantity entry box,
        # if the user doesnt provide a quantity,
        # a default value of 1 is used instead.
        # Else the value is provided
        # TODO: Validate entry for ints, against strings and special chars
        if len(self.qty_entry.get()) == 0:
            buying_qty = 1
        else:
            buying_qty = self.qty_entry.get()
        # print(len(buying_qty))

        if self.checkout_pressed:
            self.listBox.delete(0, END)

        result_from_query = sql.session.query_drug(search_query.lower())
        # print(result_from_query)

        self.update_listbox(result_from_query, buying_qty)

        self.checkout_pressed = False

    def delete_entry(self):
        """
        Deletes an entry from the cart table.
        """
        # popup window
        try:
            # get index of selection
            get_selection = self.listBox.curselection()

            # print("Selection", get_selection)

            # use regex to compile information
            get_selection = str(get_selection)
            regex = re.compile('[0-9]')
            selected_index = regex.findall(get_selection)

            # print("Selected index", selected_index[0])

            # print("Popped", self.all_items_pos.pop(int(selected_index[0])))

            self.listBox.delete(selected_index[0])
        # tell user to make a selection first
        except TclError:
            showerror(title="Error !", message="Please make a selection in order to delete", parent=self.master)
        except IndexError:
            showerror(title="Error !", message="Please make a selection in order to delete", parent=self.master)

    def checkout(self):
        """
        Get all the drugs in the list box and total the price for sale
        """
        # delete the entry box before placing the results into it
        self.total_entry.delete(0, END)

        # ok, so I want to know if the checkout button has been pressed,
        # that way we can act intelligently and decide not to delete
        # the listbox and allow the client to peruse the items before selling.
        # This check is done before instantiating the search process
        self.checkout_pressed = True

        try:
            total_cost = 0

            # checkout_list_names = []
            for each_item in self.listBox.get(0, END):
                # checkout_list_names.append(each_item[0])
                cost_of_drug = float(each_item[1]) * float(each_item[2])
                total_cost += cost_of_drug
                # print(total_cost)

                # print(checkout_list_names)

                query_item = (str(each_item[0]),)
                drug_details = sql.session.query_drugs_for_checkout(query_item)
                print('current quantity', drug_details[0][0])

                if int(drug_details[0][0]) - int(each_item[2]) > 0:

                    new_quantity = int(drug_details[0][0]) - int(each_item[2])

                    update_values = (new_quantity, query_item[0])
                    print(update_values)
                    sql.session.update_quantity_after_checkout(update_values)

                    self.total_entry.delete(0, END)
                    self.total_entry.insert(0, total_cost)
                else:
                    out_of_stock_info = \
                        "Your remaining quantity of %s is %d" % (query_item, int(drug_details[0][0]))
                    showinfo(title="Out of Stock",
                             message=out_of_stock_info, parent=self.master)
            ## cleaning after myself like a good boy would
            # self.listBox.delete(0, END)
            self.search_entry.delete(0, END)
            self.qty_entry.delete(0, END)
        except IndexError:
            print("Index Error")

    def clear_sales_list(self):
        """
        Clear list.
        """
        # clears the list of things bought from the dispensary window
        # print(self)
        self.listBox.delete(0, END)
        # after that, reset the contents of the entry box. Make it empty
        self.search_entry.delete(0, END)

        # reset the list value of total item
        self.total_item_quantity = []
        # reset the value of the items position
        self.all_items_pos = []

        self.total_entry.delete(0, END)

    def update_listbox(self, result_from_query, buying_qty):
        for row in result_from_query:
            self.listBox.insert(END, (row[0], row[1], buying_qty))
        self.listBox.selection_set(0)
