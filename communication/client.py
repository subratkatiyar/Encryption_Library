import os
import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
from aes_implementation import AESCipher

# cwd = os.getcwd()
# print(os.path.dirname(path))


HEADER = 64
PORT = 1234
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
PRIVATE_KEY = ""

cipher = AESCipher()

# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Name Label
        self.userName = Label(self.login,
                              text="Name: ",
                              font="Helvetica 12")

        self.userName.place(relheight=0.1,
                            relx=0.1,
                            rely=0.30)

        self.encryptKey = Label(self.login,
                                text="Encryption Key: ",
                                font="Helvetica 12")

        self.encryptKey.place(relheight=0.1,
                              relx=0.1,
                              rely=0.42)

        # create a entry box for
        # typing the message
        self.userNameEnter = Entry(self.login,
                                   font="Helvetica 14")

        self.userNameEnter.place(relwidth=0.4,
                                 relheight=0.1,
                                 relx=0.4,
                                 rely=0.3)

        self.encryptKeyEnter = Entry(self.login,
                                     font="Helvetica 14")

        self.encryptKeyEnter.place(relwidth=0.4,
                                   relheight=0.1,
                                   relx=0.4,
                                   rely=0.42)

        # set the focus of the curser
        # self.userNameEnter.focus()

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.userNameEnter.get(), self.encryptKeyEnter.get()))

        self.go.place(relx=0.4,
                      rely=0.55)
        # self.Window.bind('<Return>',.invoke)
        # self.Window.bind('<Return>', lambda event=None:  self.go.invoke())
        self.Window.mainloop()

    def goAhead(self, name, private_key):
        global PRIVATE_KEY
        PRIVATE_KEY = private_key
        # print(PRIVATE_KEY)
        self.login.destroy()
        self.layout(name)

        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()

    # function to receive messages
    def receive(self):
        global PRIVATE_
        while True:
            try:
                message = client.recv(1024)  # .decode(FORMAT)
                message = cipher.decrypt(message, PRIVATE_KEY)
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, message + "\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
            except Exception as e:
                # an error will be printed on the command line or console if there's an error
                self.textCons.config(state=NORMAL)
                self.textCons.insert(
                    END, f"Disconnected: An error occurred as {e}\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                client.close()
                break

    # function to send messages
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = f"{self.name}: {self.msg}"
            message = cipher.encrypt(message, PRIVATE_KEY)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)
            break


# create a GUI class object
g = GUI()
