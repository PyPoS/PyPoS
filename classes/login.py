#!/usr/bin/env python
__author__ = 'ebo'

from Tkinter import Tk, Label, Entry, Button, TclError
import sys


class Login(object):
    def __init__(self):
        self.tries = 3

    """
        Login class for authenticating the user before they begin using the system.
        Just to make sure no unauthorised persons make changes to the data
    """
    # set variables with values which are liable to change here
    window_title = 'Williams Chemicals'
    window_size = '350x200'
    window_color = '#dae0ef'
    login_btn_color = '#efe8e3'
    title_text = 'Login to Williams Chemicals'
    user_label = 'Username'
    pass_label = 'Password'
    message_success = 'Authenticated'
    message_failed = 'Username OR Password incorrect'
    message_failed_attempts = 'You have made 3 failed attempts. \n\nShutting down...'
    login_btn = 'Login'

    def show_screen(self):
        window = Tk()

        def shutdown():
            sys.exit()

        # overrides
        window.protocol('WM_DELETE_WINDOW', shutdown)

        # set window properties
        window.title(Login.window_title)
        window.geometry(Login.window_size)
        window.configure(bg=Login.window_color)

        title_bar = Label(window, text=Login.title_text, bg=Login.window_color)
        user_label = Label(window, text=Login.user_label, bg=Login.window_color)
        pass_label = Label(window, text=Login.pass_label, bg=Login.window_color)
        message = Label(window, bg=Login.window_color)

        def authenticate():
            try:
                db = open('db/user_db.csv', "r")

                line = db.readlines()

                username = usr_box.get()
                password = pswd_box.get()

                # print username.get()
                # print line[1].strip()
                # print password.get()
                #print line[2].strip()
                #print line[0].strip()

                usr = line[1].strip()
                pswd = line[2].strip()

                #print usr, ' ', pswd
                while username == usr and password == pswd:
                    # message.configure(text=Login.message_success)
                    db.close()
                    window.destroy()
                else:
                    #print usr
                    self.tries -= 1
                    message.configure(text=Login.message_failed)
                    if self.tries < 1:
                        db.close()
                        message.configure(text=Login.message_failed_attempts)
                        # python code to wait for say... 3 seconds before shutting down.
                        sys.exit()
            except IOError:
                print "Error: Could not find specified file"
            except TclError:
                print "Login window closing"

        usr_box = Entry(window)
        pswd_box = Entry(window, show='*')

        login_btn = Button(window, text=Login.login_btn, command=authenticate, bg=Login.login_btn_color)

        title_bar.pack()
        user_label.pack()
        usr_box.pack()
        pass_label.pack()
        pswd_box.pack()
        login_btn.pack()
        message.pack()
        return window