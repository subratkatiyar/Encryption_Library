import threading
import tkinter as tk
from datetime import date, datetime
from tkinter import ttk
import tkinter.scrolledtext as tkscrolled

from fireDatabase import user_auth, firebaseDB
from firebaseChats import fetch_msg, upload_msg
from variables import Variables
from tkinter import messagebox


class ChatBox(tk.Frame):
    log = {}
    previous_log = {}
    # new_msg = ''

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.TSeparator1 = ttk.Separator(self)
        self.TSeparator1.place(x=0, y=40, width=600)

        self.Label1 = tk.Label(self)
        self.Label1.place(x=320, y=10, height=21, width=89)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Messages''')

        # TODO replace text with scrolled text

        # self.ChatScrollbar = tk.Scrollbar(self, orient='vertical')
        # self.ChatTextBox = tk.Text(self)
        # self.ChatTextBox.place(x=180, y=50, height=314, width=396)
        # self.ChatTextBox.configure(background="white", font="TkTextFont")
        # self.ChatTextBox.configure(selectbackground="blue", selectforeground="white")
        # self.ChatTextBox.configure(state='disabled', wrap="word")
        #
        # self.ChatScrollbar.config(command=self.ChatTextBox.yview)
        # self.ChatScrollbar.place(x=576, y=50, height=314, width=15)

        self.ScrolledChatTextBox = tkscrolled.ScrolledText(self, undo=True)
        self.ScrolledChatTextBox.place(x=180, y=50, height=314, width=411)
        self.ScrolledChatTextBox.configure(background="white", font="TkTextFont")
        self.ScrolledChatTextBox.configure(selectbackground="blue", selectforeground="white")
        self.ScrolledChatTextBox.configure(state='disabled', wrap="word")

        self.NewMsgScrollbar = tk.Scrollbar(self, orient='vertical')
        self.NewMsgEntry = tk.Text(self)
        self.NewMsgEntry.place(x=180, y=370, height=64, width=316)
        self.NewMsgEntry.configure(background="white", font="TkTextFont", wrap="word")
        self.NewMsgEntry.configure(selectbackground="blue", selectforeground="white")

        self.NewMsgScrollbar.config(command=self.NewMsgEntry.yview)
        self.NewMsgScrollbar.place(x=496, y=370, height=64, width=15)

        self.MsgSendBtn = tk.Button(self,
                                    command=lambda: self.sendMessage(
                                        self.ScrolledChatTextBox, self.NewMsgEntry, master
                                    ))
        self.MsgSendBtn.place(x=520, y=380, height=41, width=71)
        self.MsgSendBtn.configure(activebackground="#00e676")
        self.MsgSendBtn.configure(background="#00e676")
        self.MsgSendBtn.configure(text='''Send''')

        Variables.receive_thread = threading.Thread(target=self.receiveMessage, args=(self.ScrolledChatTextBox,))
        Variables.receive_thread.start()

        self.Label2 = tk.Label(self)
        self.Label2.place(relx=0.067, rely=0.022, height=21, width=70)
        self.Label2.configure(text='''Attendees''')

        self.AttendeesScrollbar = tk.Scrollbar(self, orient='vertical')
        self.AttendeesTextBox = tk.Text(self)
        self.AttendeesTextBox.place(x=0, y=50, height=394, width=156)
        self.AttendeesTextBox.configure(background="white", font="TkTextFont")
        self.AttendeesTextBox.configure(selectbackground="blue", selectforeground="white")
        self.AttendeesTextBox.configure(state='disabled', wrap="word")

        self.AttendeesScrollbar.config(command=self.AttendeesTextBox.yview)
        self.AttendeesScrollbar.place(x=156, y=50, height=394, width=15)

    def menuBar(self, master):
        self.doNotUse()

        menubar = tk.Menu(master, font="TkMenuFont")

        # sub_menu = tk.Menu(master, tearoff=0)
        # menubar.add_cascade(menu=sub_menu, label="Profile")
        # sub_menu.add_command(label="WTF")

        sub_menu = tk.Menu(master, tearoff=0)
        menubar.add_cascade(menu=sub_menu, label="Chatroom")
        sub_menu.add_command(label="Stats")
        sub_menu.add_command(label="Details")
        sub_menu.add_command(label="Delete chatroom", state="disabled")
        sub_menu1 = tk.Menu(master, tearoff=0)
        menubar.add_cascade(menu=sub_menu1, label="User")
        sub_menu1.add_command(label="Change state")
        sub_menu1.add_command(label="My Profile")
        sub_menu1.add_command(label="Sign Out")
        menubar.add_command(label="Leave")

        return menubar

    def sendMessage(self, chats_box, msg_entry, mst):
        self.doNotUse()
        msg = msg_entry.get("1.0", 'end-1c')

        if msg == 'q' or msg == 'Q':
            firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('attendees').child(
                user_auth.userID).remove()
            # firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('chats').child('temp').remove()
            Variables.threadFlag = True
            Variables.receive_thread.join()
            mst.destroy()

        time = f"{date.today()}_{datetime.now().time().strftime('%H:%M:%S')}"

        try:
            chats_box.insert(tk.END, f" You:  {msg}")
            msg_entry.delete('1.0', tk.END)
            upload_msg(msg)
        except Exception as e:
            e = str(e)
            # chats_box.delete(tk.END - 1, tk.END)
            if e.find('ERROR_SEND_MSG') != -1:
                messagebox.showerror('Message', "Error sending message.\nCheck your internet.  ")

    def receiveMessage(self, chats_box):
        while True:
            if Variables.threadFlag:
                break
            try:
                self.log = fetch_msg().val()
            except Exception as e:
                e = str(e)
                if e.find('ERROR_GET_MSG') != -1:
                    messagebox.showerror('Message', "Error receiving message.\nCheck your internet.  ")

            if self.previous_log != self.log and self.log is not None:
                self.previous_log = self.log

                if Variables.current_user['displayName'] != self.log['user'] and self.log['user'] != "dummy":
                    chats_box.insert(tk.END, f" {self.log['user']}:  {self.log['msg']}")

    def doNotUse(self):
        pass
