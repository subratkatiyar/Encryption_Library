import tkinter as tk
import uuid
from tkinter import messagebox
from tkinter import ttk

import pyperclip

from chatbox_gui import ChatBox
from fireDatabase import create_chat_room, join_chat_room
from variables import Variables


class CreateChatroomGUI(tk.Frame):
    # chat_id = None

    def menuBar(self, master):
        menubar = tk.Menu(master, font="TkMenuFont")
        return menubar

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.Frame1 = tk.Frame(self)
        self.Frame1.place(relx=0.2, rely=0.133, relheight=0.144, relwidth=0.592)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.31, rely=0.308, height=25, width=119)
        self.Label1.configure(text='''Create Chatroom''')

        self.TSeparator1 = ttk.Separator(self)
        self.TSeparator1.place(relx=0.0, rely=0.2, relwidth=0.2)

        self.TSeparator2 = ttk.Separator(self)
        self.TSeparator2.place(relx=0.8, rely=0.2, relwidth=0.192)

        self.Label2 = tk.Label(self)
        self.Label2.place(relx=0.1, rely=0.378, height=21, width=99)
        self.Label2.configure(text='''Chatroom ID''')

        chat_id = tk.StringVar(self, value=str(uuid.uuid4()))
        self.chat_id_entry = tk.Entry(self, textvariable=chat_id)
        self.chat_id_entry.place(relx=0.283, rely=0.356, height=33, relwidth=0.507)
        self.chat_id_entry.configure(background="white")
        self.chat_id_entry.configure(font="TkFixedFont")
        self.chat_id_entry.configure(state='readonly')

        self.Label3 = tk.Label(self)
        self.Label3.place(relx=0.067, rely=0.489, height=21, width=109)
        self.Label3.configure(text='''Create password''')

        self.password_entry = tk.Entry(self)
        self.password_entry.place(relx=0.283, rely=0.467, height=33, relwidth=0.507)
        self.password_entry.configure(background="white")
        self.password_entry.configure(font="TkFixedFont")
        self.password_entry.configure(selectbackground="blue")
        self.password_entry.configure(selectforeground="white")

        self.Button1 = tk.Button(self, command=lambda: chat_id.set(str(uuid.uuid4())))
        self.Button1.place(relx=0.817, rely=0.356, height=31, width=81)
        self.Button1.configure(text='''Generate''')

        self.create_room_btn = tk.Button(self,
                                         command=lambda: self.createChatroom(
                                             self.chat_id_entry, self.password_entry.get(), controller
                                         ))
        self.create_room_btn.place(relx=0.383, rely=0.622, height=31, width=131)
        self.create_room_btn.configure(background="#33eb91")
        self.create_room_btn.configure(text='''Create Chatroom''')

        self.Button2 = tk.Button(self, command=lambda: pyperclip.copy(str(self.chat_id_entry.get())))
        self.Button2.place(relx=0.817, rely=0.622, height=31, width=81)
        self.Button2.configure(text='''Copy ID''')

        self.Button3 = tk.Button(self, command=lambda: self.goBack(controller))
        self.Button3.place(relx=0.05, rely=0.622, height=31, width=71)
        self.Button3.configure(text='''Back''')

    def goBack(self, cont):
        self.doNotUse()
        from chatroom_gui import ChatroomGUI
        cont.show_frame(ChatroomGUI)

    def createChatroom(self, _id_entry, key, cont):
        self.doNotUse()

        if key == '':
            messagebox.showinfo('Password', "Chatroom password not provided")
        elif len(key) < 5:
            messagebox.showinfo('Password', "Password length should be\nat least 5 characters long")
        else:
            try:
                pyperclip.copy(str(_id_entry.get()))
                Variables.chatroomData = create_chat_room(_id_entry.get(), key)
                cont.show_frame(ChatBox)

            except Exception as e:
                e = str(e)
                if e.find("CHATROOM_EXISTS") != -1:
                    messagebox.showerror('Error', 'Chatroom already exists')
                elif e.find("ERROR_UPLOAD_DATA") != -1:
                    messagebox.showerror('Error', "Error creating chatroom\nCheck your internet.  ")
                else:
                    messagebox.showerror('Error', "Error creating chatroom\nSomething went wrong.  ")

    # def genChatID(self):
    #     self.chatID = ''
    #     for _ in range(16):
    #         self.chatID = self.chatID + str(randint(0, 10))
    #
    #     self.chat_id.set(value=self.chatID)

    def doNotUse(self):
        pass


class JoinChatroomGUI(tk.Frame):
    def menuBar(self, master):
        menubar = tk.Menu(master, font="TkMenuFont")
        return menubar

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.Frame1 = tk.Frame(self)
        self.Frame1.place(relx=0.2, rely=0.133, relheight=0.144, relwidth=0.592)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.338, rely=0.308, height=25, width=119)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Join Chatroom''')

        self.TSeparator1 = ttk.Separator(self)
        self.TSeparator1.place(relx=0.0, rely=0.2, relwidth=0.2)

        self.TSeparator2 = ttk.Separator(self)
        self.TSeparator2.place(relx=0.8, rely=0.2, relwidth=0.192)

        self.Label2 = tk.Label(self)
        self.Label2.place(relx=0.1, rely=0.378, height=21, width=99)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''Chatroom ID''')

        chat_id = tk.StringVar(self, value='')
        self.chat_id_entry = tk.Entry(self, textvariable=chat_id)
        self.chat_id_entry.place(relx=0.283, rely=0.356, height=33, relwidth=0.507)
        self.chat_id_entry.configure(background="white")
        self.chat_id_entry.configure(font="TkFixedFont")
        self.chat_id_entry.configure(selectbackground="blue")
        self.chat_id_entry.configure(selectforeground="white")

        self.Label3 = tk.Label(self)
        self.Label3.place(relx=0.133, rely=0.489, height=21, width=79)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(cursor="fleur")
        self.Label3.configure(text='''Password''')

        self.password_entry = tk.Entry(self)
        self.password_entry.place(relx=0.283, rely=0.467, height=33, relwidth=0.507)
        self.password_entry.configure(background="white")
        self.password_entry.configure(font="TkFixedFont")
        self.password_entry.configure(selectbackground="blue")
        self.password_entry.configure(selectforeground="white")

        self.join_room_btn = tk.Button(self,
                                       command=lambda: self.joinChatroom(
                                           self.chat_id_entry.get(), self.password_entry.get(), controller
                                       ))
        self.join_room_btn.place(relx=0.383, rely=0.622, height=31, width=131)
        self.join_room_btn.configure(activebackground="#f9f9f9")
        self.join_room_btn.configure(background="#33eb91")
        self.join_room_btn.configure(text='''Join Chatroom''')

        self.Button1 = tk.Button(self, command=lambda: chat_id.set(str(pyperclip.paste())))
        self.Button1.place(relx=0.75, rely=0.622, height=31, width=121)
        self.Button1.configure(activebackground="#f9f9f9")
        self.Button1.configure(text='''Paste Copied ID''')

        self.Button2 = tk.Button(self, command=lambda: self.goBack(controller))
        self.Button2.place(relx=0.05, rely=0.622, height=31, width=71)
        self.Button2.configure(activebackground="#f9f9f9")
        self.Button2.configure(text='''Back''')

    def goBack(self, cont):
        self.doNotUse()
        from chatroom_gui import ChatroomGUI
        cont.show_frame(ChatroomGUI)

    def joinChatroom(self, _id, key, cont):
        self.doNotUse()

        if _id == '':
            messagebox.showinfo('Chatroom ID', "Chatroom ID not provided")
        elif key == '':
            messagebox.showinfo('Password', "Chatroom password not provided")
        else:
            try:
                Variables.chatroomData = join_chat_room(_id, key)
                cont.show_frame(ChatBox)

            except Exception as e:
                e = str(e)
                if e.find("INVALID_CHATROOM_PASSWORD") != -1:
                    messagebox.showerror('Error', 'Invalid password for the chatroom')
                elif e.find("ERROR_JOINING_CHATROOM") != -1:
                    messagebox.showerror('Error', "Error Joining chatroom\nCheck your internet.  ")
                elif e.find("CHATROOM_NOT_EXIST") != -1:
                    messagebox.showerror('Error', "Chatroom with this ID\ndoes not exist")

    def doNotUse(self):
        pass
