import threading
import time
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from datetime import date, datetime
from tkinter import messagebox
from tkinter import ttk

from fireDatabase import user_auth, firebaseDB
from firebaseChats import fetch_msg, upload_msg
from variables import Variables


def fetch_attendees():
    try:
        return firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('attendees').get()

    except Exception:
        raise Exception('ERROR_GET_ATTENDEES')


class ChatBox(tk.Frame):
    log = {}
    previous_log = {}
    previous_attendee = ''
    attendee = ''
    MsgSendBtn = None

    # new_msg = ''

    def getBindButton(self):
        return self.MsgSendBtn, True

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.TSeparator1 = ttk.Separator(self)
        self.TSeparator1.place(x=0, y=40, width=600)

        self.Label1 = tk.Label(self)
        self.Label1.place(x=320, y=10, height=21, width=89)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Messages''')

        self.ScrolledAttendeesTextBox = tkscrolled.ScrolledText(self, undo=True)
        self.ScrolledAttendeesTextBox.place(x=0, y=50, height=385, width=171)
        self.ScrolledAttendeesTextBox.configure(background="white", font="TkTextFont")
        self.ScrolledAttendeesTextBox.configure(selectbackground="blue", selectforeground="white")
        self.ScrolledAttendeesTextBox.configure(state=tk.DISABLED, wrap="word")

        self.ScrolledChatTextBox = tkscrolled.ScrolledText(self, undo=True)
        self.ScrolledChatTextBox.place(x=180, y=50, height=314, width=411)
        self.ScrolledChatTextBox.configure(background="white", font="TkTextFont")
        self.ScrolledChatTextBox.configure(selectbackground="blue", selectforeground="white")
        self.ScrolledChatTextBox.configure(state=tk.NORMAL, wrap="word")
        self.ScrolledChatTextBox.insert(tk.END, f"- - - - - - - - - - - - - - - - -  {date.today()} "
                                                f"- - - - - - - - - - - - - - - - -\n")
        self.ScrolledChatTextBox.configure(state=tk.DISABLED)

        self.ScrolledNewMsgEntry = tkscrolled.ScrolledText(self, undo=True)
        # self.ScrolledNewMsgEntry.place(x=180, y=370, height=64, width=331)
        self.ScrolledNewMsgEntry.place(x=180, y=370, height=64, width=306)
        self.ScrolledNewMsgEntry.configure(background="white", font="TkTextFont")
        self.ScrolledNewMsgEntry.configure(selectbackground="blue", selectforeground="white")
        self.ScrolledNewMsgEntry.configure(wrap=tk.WORD)
        self.ScrolledNewMsgEntry.focus_set()

        self.MsgSendBtn = tk.Button(self,
                                    command=lambda: self.sendMessage(
                                        self.ScrolledChatTextBox, self.ScrolledNewMsgEntry, controller))
        # self.MsgSendBtn.place(x=520, y=380, height=41, width=71)
        self.MsgSendBtn.place(x=490, y=370, height=51, width=101)
        self.MsgSendBtn.configure(activebackground="#00e676")
        self.MsgSendBtn.configure(background="#00e676")
        self.MsgSendBtn.configure(text='''Send''')

        self.Label2 = tk.Label(self)
        self.Label2.place(x=40, y=10, height=21, width=70)
        self.Label2.configure(text='''Attendees''')

        self.Label3 = tk.Label(self)
        self.Label3.place(x=490, y=420, height=21, width=104)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(font="-family {Ubuntu Mono} -size 8")
        self.Label3.configure(text='''[Ctrl+Enter to send]''')

        # Initialize threads
        Variables.receive_thread = threading.Thread(target=self.receiveMessage, args=(self.ScrolledChatTextBox,))
        Variables.getAttendees_thread = threading.Thread(target=self.getAttendees,
                                                         args=(self.ScrolledAttendeesTextBox,))

        Variables.getAttendees_thread.daemon = True     # TODO important for getAttendees_thread to join()

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

    def sendMessage(self, chats_box, msg_entry, cont):
        self.doNotUse()
        msg = msg_entry.get("1.0", 'end-1c')
        msg_entry.delete('1.0', tk.END)

        if msg == 'q' or msg == 'Q':
            cont.on_closing(del_temp=False)
        elif msg == '':
            pass
        else:
            _time = f"{datetime.now().time().strftime('%H:%M')}"

            try:
                chats_box.configure(state=tk.NORMAL)
                chats_box.insert(tk.END, f"You:  {msg}\n")
                chats_box.configure(state=tk.DISABLED)
                upload_msg(msg)
            except Exception as e:
                e = str(e)

                length = len(f"You:  {msg}\n") + 1
                chats_box.configure(state=tk.NORMAL)
                chats_box.delete(f'end-{length}c', tk.END)
                chats_box.configure(state=tk.DISABLED)

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
                    chats_box.configure(state=tk.NORMAL)
                    chats_box.insert(tk.END, f"{self.log['user']}:  {self.log['msg']}\n")
                    chats_box.configure(state=tk.DISABLED)
        print('receiveMessage thread broken')

    def doNotUse(self):
        pass

    def getAttendees(self, attendees_box):
        while True:
            if Variables.threadFlag:
                break

            all_attendees = firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('attendees').get()

            self.attendee = ''
            for temp in all_attendees.each():
                if temp.val()['name'] != 'dummyName' and Variables.threadFlag is False:
                    self.attendee = self.attendee + f"{temp.val()['name']}\n{temp.val()['email']}\n" \
                                                    f"+++ {temp.val()['status']} +++ \n\n"

            if self.previous_attendee != self.attendee:
                self.previous_attendee = self.attendee

                attendees_box.configure(state=tk.NORMAL)
                attendees_box.delete('1.0', tk.END)

                attendees_box.insert(tk.END, self.attendee)
                attendees_box.configure(state=tk.DISABLED)
            time.sleep(1)
        print('getAttendees thread broken\n')
