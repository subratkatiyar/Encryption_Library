import tkinter as tk
from tkinter import messagebox

from chatbox_gui import ChatBox
from chatroom_gui import ChatroomGUI
from client_gui import LoginGUI, SignupGUI
from create_join_chatroom_gui import CreateChatroomGUI, JoinChatroomGUI
from fireDatabase import firebaseDB, user_auth
from variables import Variables


# def vp_start_gui():
#     start = StartGUI()
#     start.mainloop()


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
        _allFrames = (LoginGUI, SignupGUI, ChatroomGUI, CreateChatroomGUI, JoinChatroomGUI, ChatBox)
        for F in _allFrames:
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginGUI)

    def show_frame(self, cont):
        frame = self.frames[cont]
        menubar = frame.menuBar(self)
        self.configure(menu=menubar)
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if user_auth.CHATROOM_ID != '':
                firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('attendees').child(
                    user_auth.userID).remove()
                firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('chats').child('temp').remove()

            Variables.threadFlag = True
            Variables.receive_thread.join()
            self.destroy()


if __name__ == '__main__':
    # vp_start_gui()
    start = StartApp()
    start.mainloop()
