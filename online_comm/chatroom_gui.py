import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from create_join_chatroom_gui import CreateChatroomGUI, JoinChatroomGUI
from fireDatabase import user_auth, firebaseAuth
from variables import Variables

"""
CHATROOM GUI
"""


class ChatroomGUI(tk.Frame):
    def menuBar(self, master):
        self.doNotUse()
        menubar = tk.Menu(master, font="TkMenuFont")
        return menubar

    def getBindButton(self):
        self.doNotUse()
        return None, False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        Variables.storeUserID = tk.StringVar(master, value='')
        Variables.storeName = tk.StringVar(master, value='')

        self.Frame1 = tk.Frame(self)
        self.Frame1.place(relx=0.2, rely=0.133, relheight=0.144, relwidth=0.592)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.282, rely=0.308, height=25, width=159)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Welcome to Chatrooms''')

        self.TSeparator1 = ttk.Separator(self)
        self.TSeparator1.place(relx=0.0, rely=0.2, relwidth=0.2)

        self.TSeparator2 = ttk.Separator(self)
        self.TSeparator2.place(relx=0.8, rely=0.2, relwidth=0.192)

        self.create_chat_btn = tk.Button(self, command=lambda: self.createChatroomBtn(controller))
        self.create_chat_btn.place(relx=0.367, rely=0.378, height=31, width=161)
        self.create_chat_btn.configure(activebackground="#f9f9f9")
        self.create_chat_btn.configure(text='''Create new chatroom''')

        self.join_chat_btn = tk.Button(self, command=lambda: controller.show_frame(JoinChatroomGUI))
        self.join_chat_btn.place(relx=0.367, rely=0.489, height=31, width=161)
        self.join_chat_btn.configure(activebackground="#f9f9f9")
        self.join_chat_btn.configure(text='''Join a chatroom''')

        self.Labelframe1 = tk.LabelFrame(self)
        self.Labelframe1.place(relx=0.017, rely=0.667, relheight=0.3, relwidth=0.967)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Current User''')

        self.sign_out_btn = tk.Button(self.Labelframe1, command=lambda: self.signOutUser(controller))
        self.sign_out_btn.place(relx=0.828, rely=0.593, height=31, width=81, bordermode='ignore')
        self.sign_out_btn.configure(activebackground="#f6685e")
        self.sign_out_btn.configure(background="#f6685e")
        self.sign_out_btn.configure(text='''Sign out''')

        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.034, rely=0.222, height=21, width=69, bordermode='ignore')
        self.Label2.configure(text='''User ID''')

        self.Label3 = tk.Label(self.Labelframe1)
        self.Label3.place(relx=0.034, rely=0.444, height=21, width=69, bordermode='ignore')
        self.Label3.configure(text='''Name''')

        self.Label4 = tk.Label(self.Labelframe1)
        self.Label4.place(relx=0.034, rely=0.667, height=21, width=69, bordermode='ignore')
        self.Label4.configure(text='''Email''')

        self.user_id_entry = tk.Entry(self.Labelframe1, textvariable=Variables.storeUserID)
        self.user_id_entry.place(relx=0.172, rely=0.222, height=23, relwidth=0.269, bordermode='ignore')
        self.user_id_entry.configure(background="white")
        self.user_id_entry.configure(font="TkFixedFont")
        self.user_id_entry.configure(state='readonly')

        self.user_name_entry = tk.Entry(self.Labelframe1, textvariable=Variables.storeName)
        self.user_name_entry.place(relx=0.172, rely=0.444, height=23, relwidth=0.269, bordermode='ignore')
        self.user_name_entry.configure(background="white")
        self.user_name_entry.configure(font="TkFixedFont")
        self.user_name_entry.configure(state='readonly')

        self.user_email_entry = tk.Entry(self.Labelframe1, textvariable=Variables.storeEmail)
        self.user_email_entry.place(relx=0.172, rely=0.667, height=23, relwidth=0.269, bordermode='ignore')
        self.user_email_entry.configure(background="white")
        self.user_email_entry.configure(font="TkFixedFont")
        self.user_email_entry.configure(state='readonly')

    def createChatroomBtn(self, cont):
        self.doNotUse()
        cont.show_frame(CreateChatroomGUI)
        messagebox.showinfo('Chatroom ID', "Chatroom id copied to clipboard")

    def signOutUser(self, cont):
        self.doNotUse()

        from client_gui import LoginGUI
        firebaseAuth.current_user = None
        user_auth.currentUser = None
        user_auth.userID = None

        cont.show_frame(LoginGUI)

    def doNotUse(self):
        pass
