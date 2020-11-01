import sys
import tkinter as tk
from tkinter import messagebox

from chatbox_gui import ChatBox
from chatroom_gui import ChatroomGUI
from client_gui import LoginGUI, SignupGUI
from create_join_chatroom_gui import CreateChatroomGUI, JoinChatroomGUI
from fireDatabase import firebaseDB, user_auth
from variables import Variables
from welcome_gui import WelcomeGUI
from local_network_gui import LocalNetworkGUI, LocalChatBoxGUI
from file_encrypt_gui import FileEncryptGUI


def vp_start_gui():
    start = StartApp()
    start.mainloop()


class StartApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.geometry("600x450")
        self.minsize(1, 1)
        self.maxsize(1360, 738)
        self.resizable(1, 1)
        self.title("Encrypted Chat")
        self.configure(highlightcolor="black")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        _allFrames = (WelcomeGUI, LoginGUI, SignupGUI, ChatroomGUI, CreateChatroomGUI, JoinChatroomGUI, ChatBox,
                      LocalChatBoxGUI, LocalNetworkGUI, FileEncryptGUI)
        for F in _allFrames:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeGUI)

    def show_frame(self, cont):
        frame = self.frames[cont]

        menubar = frame.menuBar(self)
        if menubar is not None:
            self.configure(menu=menubar)

        button, is_send = frame.getBindButton()
        if button is not None:
            if is_send:
                self.bind('<Return>', lambda *args: None)
                self.bind('<Control-Return>', lambda event=None: button.invoke())
            else:
                self.bind('<Control-Return>', lambda *args: None)
                self.bind('<Return>', lambda event=None: button.invoke())
        else:
            self.bind('<Return>', lambda *args: None)
            self.bind('<Control-Return>', lambda *args: None)

        frame.tkraise()

    def on_closing(self, del_temp=True):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            if user_auth.CHATROOM_NAME != 'chatroom_0':
                if del_temp:
                    firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('attendees').child(
                        user_auth.userID).update({'status': 'offline'})
                    firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('chats').child('temp').remove()
                else:
                    firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('attendees').child(
                        user_auth.userID).update({'status': 'offline'})

                Variables.threadFlag = True
                Variables.firebaseReceive_thread.join()
                print('msg joined')
                # Variables.getAttendees_thread.join()        # TODO not joined
                print('ended')
                sys.exit()
                # os._exit(0)


if __name__ == '__main__':
    vp_start_gui()
