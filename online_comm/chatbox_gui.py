import threading
import time
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from datetime import date, datetime
from tkinter import messagebox
from tkinter import ttk

from fireDatabase import user_auth, firebaseDB, firebaseAuth
from firebaseChats import fetch_msg, upload_msg
from variables import Variables
from aes_implementation import cipher


class ChatBox(tk.Frame):
    log = {}
    previous_log = {}
    previous_attendee = ''
    attendee = ''
    MsgSendBtn = None
    cont = None
    total_msgs = 0

    def getBindButton(self):
        return self.MsgSendBtn, True

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.cont = controller

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
        self.ScrolledNewMsgEntry.place(x=180, y=370, height=64, width=306)
        self.ScrolledNewMsgEntry.configure(background="white", font="TkTextFont")
        self.ScrolledNewMsgEntry.configure(selectbackground="blue", selectforeground="white")
        self.ScrolledNewMsgEntry.configure(wrap=tk.WORD)
        self.ScrolledNewMsgEntry.focus_set()

        self.MsgSendBtn = tk.Button(self, command=lambda: self.sendMessage(
            self.ScrolledChatTextBox, self.ScrolledNewMsgEntry, controller))
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
        # started on create/join chatroom
        Variables.firebaseReceive_thread = threading.Thread(target=self.receiveMessage,
                                                            args=(self.ScrolledChatTextBox,))
        Variables.firebaseReceive_thread.daemon = True
        Variables.getAttendees_thread = threading.Thread(target=self.getAttendees,
                                                         args=(self.ScrolledAttendeesTextBox,))

        Variables.getAttendees_thread.daemon = True  # important for getAttendees_thread to join()

        Variables.firebaseReceive_thread.start()
        Variables.getAttendees_thread.start()

        # another thread
        user_expiry_thread = threading.Thread(target=self.updateUserExpiryTime)
        user_expiry_thread.daemon = True
        user_expiry_thread.start()

    def menuBar(self, master):
        self.doNotUse()
        menubar = tk.Menu(master, font="TkMenuFont")

        sub_menu = tk.Menu(master, tearoff=0)
        menubar.add_cascade(menu=sub_menu, label="Chatroom")
        sub_menu.add_command(label="Stats", command=self.chatsStats)
        sub_menu.add_command(label="Details", command=self.chatroomDetails)
        sub_menu.add_command(label="Delete chatroom", command=self.deleteChatroom)
        sub_menu1 = tk.Menu(master, tearoff=0)
        menubar.add_cascade(menu=sub_menu1, label="User")
        sub_menu1.add_command(label="Change state", command=self.changeState)
        sub_menu1.add_command(label="My Profile", command=self.displayProfile)
        sub_menu1.add_command(label="Sign Out", command=self.signOutUser)
        menubar.add_command(label="Leave", command=self.leaveFirebaseChat)
        return menubar

    def sendMessage(self, chats_box, msg_entry, cont):
        self.doNotUse()
        msg = msg_entry.get("1.0", 'end-1c')
        msg = msg.rstrip()

        if msg == 'q' or msg == 'Q':
            msg_entry.delete('1.0', tk.END)
            cont.on_closing(del_temp=False)
        elif msg == '':
            print('message is empty')
        elif Variables.current_status == 'offline':
            messagebox.showwarning("Cannot send message", "Please first set status to ONLINE\n\n"
                                                          "Under [user -> Change status]")
        else:
            msg_entry.delete('1.0', tk.END)
            msg = msg.rstrip()
            _time = f"{datetime.now().time().strftime('%H:%M')}"

            try:
                chats_box.configure(state=tk.NORMAL)
                chats_box.insert(tk.END, f"You:  {msg}\n")
                chats_box.configure(state=tk.DISABLED)
                self.total_msgs = self.total_msgs + 1

                # TODO encrypt the message
                encrypt_msg = cipher.encrypt(msg).hex()
                upload_msg(encrypt_msg)
            except Exception as e:
                e = str(e)

                length = len(f"You:  {msg}\n") + 1
                chats_box.configure(state=tk.NORMAL)
                chats_box.delete(f'end-{length}c', tk.END)
                chats_box.configure(state=tk.DISABLED)
                self.total_msgs = self.total_msgs - 1

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

                if user_auth.currentUser['displayName'] != self.log['user'] and self.log['user'] != "dummy":
                    # TODO Decrypted the received message
                    decrypt_msg = cipher.decrypt(bytes.fromhex(self.log['msg']))

                    chats_box.configure(state=tk.NORMAL)
                    chats_box.insert(tk.END, f"{self.log['user']}:  {decrypt_msg}\n")
                    chats_box.configure(state=tk.DISABLED)
        print('receiveMessage thread broken')

    def doNotUse(self):
        pass

    def getAttendees(self, attendees_box):
        while True:
            if Variables.threadFlag:
                break

            admin = Variables.chatroomData['created_userID']
            attendee_name_str = ''

            all_attendees = firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('attendees').get()

            self.attendee = ''
            for usr in all_attendees.each():
                is_admin = False

                if "name" in usr.val():
                    if usr.key() == admin:
                        is_admin = True
                        attendee_name_str = f"{usr.val()['name']} (Admin)"
                    if usr.key() == user_auth.userID:
                        if is_admin:
                            attendee_name_str = f"{usr.val()['name']} (Admin)(You)"
                        else:
                            attendee_name_str = f"{usr.val()['name']} (You)"
                    elif usr.key() != admin:
                        attendee_name_str = f"{usr.val()['name']}"

                    if usr.val()['name'] != 'dummyName' and Variables.threadFlag is False:
                        user_str = f"{attendee_name_str}\n{usr.val()['email']}\n- - {usr.val()['status']} - - \n\n"
                        self.attendee = self.attendee + user_str

            if self.previous_attendee != self.attendee:
                self.previous_attendee = self.attendee

                attendees_box.configure(state=tk.NORMAL)
                attendees_box.delete('1.0', tk.END)

                attendees_box.insert(tk.END, self.attendee)
                attendees_box.configure(state=tk.DISABLED)
            time.sleep(1)
        print('getAttendees thread broken\n')

    def leaveFirebaseChat(self):
        from chatroom_gui import ChatroomGUI

        if messagebox.askokcancel("Confirm leave", "Are you sure you want to leave"):
            temp_chatroom_name = user_auth.CHATROOM_NAME
            user_auth.CHATROOM_NAME = 'chatroom_0'

            self.cont.show_frame(ChatroomGUI)

            firebaseDB.child('chat_rooms').child(temp_chatroom_name).child('attendees').child(
                user_auth.userID).remove()

            self.ScrolledAttendeesTextBox.delete('1.0', tk.END)
            self.ScrolledChatTextBox.delete('1.0', tk.END)

    def signOutUser(self):
        self.doNotUse()
        from client_gui import LoginGUI
        if messagebox.askokcancel("Confirm Sign out", "Are you sure you want to\nSign Out"):

            temp_chatroom_name = user_auth.CHATROOM_NAME
            user_auth.CHATROOM_NAME = 'chatroom_0'
            self.cont.show_frame(LoginGUI)

            firebaseDB.child('chat_rooms').child(temp_chatroom_name).child('attendees').child(
                user_auth.userID).update({'status': 'offline'})

            firebaseAuth.current_user = None
            user_auth.currentUser = None
            user_auth.userID = None

            self.ScrolledAttendeesTextBox.delete('1.0', tk.END)
            self.ScrolledChatTextBox.delete('1.0', tk.END)

    def displayProfile(self):
        self.doNotUse()
        messagebox.showinfo("Profile", f"Name:   {user_auth.currentUser['displayName']}\n"
                                       f"Email:  {user_auth.currentUser['email']}\n"
                                       f"Expires in:  {Variables.userExpiryTimeLeft} minutes\n"
                                       f"Registered:  {user_auth.currentUser['registered']}\n"
                                       f"UserID:  {user_auth.userID}\n")

    def changeState(self):
        self.doNotUse()
        Variables.current_status = firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child(
            'attendees').child(user_auth.userID).get().val()['status']

        if Variables.current_status == 'ONLINE':
            firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('attendees').child(
                user_auth.userID).update({'status': 'offline'})
            Variables.current_status = 'offline'

        elif Variables.current_status == 'offline':
            firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('attendees').child(
                user_auth.userID).update({'status': 'ONLINE'})
            Variables.current_status = 'ONLINE'

    def deleteChatroom(self):
        self.doNotUse()
        from chatroom_gui import ChatroomGUI
        created_user_id = Variables.chatroomData['created_userID']

        if user_auth.userID == created_user_id:
            if messagebox.askokcancel("Confirm delete", "Delete chatroom forever?"):
                temp_chatroom_name = user_auth.CHATROOM_NAME
                user_auth.CHATROOM_NAME = 'chatroom_0'
                self.cont.show_frame(ChatroomGUI)

                firebaseDB.child('chat_rooms').child(temp_chatroom_name).remove()
                self.ScrolledAttendeesTextBox.delete('1.0', tk.END)
                self.ScrolledChatTextBox.delete('1.0', tk.END)

        else:
            messagebox.showerror("Error", "Sorry! You are not the admin")

    def chatroomDetails(self):
        self.doNotUse()
        messagebox.showinfo("Chatroom Details", f"Created By: {Variables.chatroomData['created_name']}\n"
                                                f"Chatroom Name: {user_auth.CHATROOM_NAME}\n"
                                                f"Chatroom ID: {Variables.chatroomData['chatroomID']}\n")

    def chatsStats(self):
        all_msg = str(self.ScrolledChatTextBox.get("1.0", 'end-1c'))
        word_count = len(all_msg.split())
        letter_count = len(all_msg.replace(" ", ""))

        messagebox.showinfo("Chat Stats", f"Word counts: {word_count}\n"
                                          f"Char counts: {letter_count}\n"
                                          f"Total msgs:  {self.total_msgs}\n")

    def updateUserExpiryTime(self):
        self.doNotUse()
        while True:
            if Variables.threadFlag:
                break
            Variables.userExpiryTimeLeft = Variables.userExpiryTimeLeft - 1
            time.sleep(60)
