__author__ = 'ebo'



def donothing():
   filewin = Toplevel(window)
   button = Button(filewin, text="Do nothing button")
   button.pack()
def about():
   filenu = Toplevel(window)

   filenu.geometry('300x170+500+250')
   filenu.iconbitmap(r'c:\Python34\qnxx.ico')
   filenu.resizable(False,False)

   label = ttk.Label(filenu,text = 'This program was designed by KangaSOFT for Queen Elizabeth II Hall',foreground ='blue')
   label.pack()
   label.config(wraplength = 300)



def index():
   #filenu = Toplevel(window)

   #filenu.geometry('300x170+500+250')
   #filenu.iconbitmap(r'c:\Python34\DLLs\qnxx.ico')
   #filenu.resizable(False,False)

   messagebox.showinfo(title = 'Usage',message = 'Switch between the windows to search,display or add a new resident to the database after entering the correct password')



menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)

#filemenu.add_command(label="New", command=donothing)#create a new database
#filemenu.add_command(label="Open", command=donothing)
#filemenu.add_command(label="Save", command=donothing)
#filemenu.add_command(label="Save as...", command=donothing)
filemenu.add_command(label="Close",)



filemenu.add_separator()

filemenu.add_command(label="Exit", command=window.quit)
logo = PhotoImage(file = 'C:\\Python34\\qnxx.gif').subsample(15,15)
filemenu.entryconfig('Close',image = logo,compound = 'left')

menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)


editmenu.add_separator()

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=index)
kanga = PhotoImage(file = 'C:\\Python34\\qnxx.gif').subsample(5,5)
helpmenu.entryconfig("Help Index",image = kanga,compound = 'left')
helpmenu.add_command(label="About...", command=about)
helpmenu.entryconfig("About...",image = kanga,compound = 'left')
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)
