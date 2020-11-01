import socket
import threading
import tkinter as tk
import tkinter.scrolledtext as tkscrolled
from tkinter import messagebox

from aes_implementation import cipher
from variables import Variables
from welcome_gui import WelcomeGUI

# TODO fuser -k 12397/tcp
# to kill a port

HEADER = 64
PORT = 1234
SERVER = socket.gethostname()
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
# cipher = _aes.AESCipher('*')


# Create a new client socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(ADDRESS)
except Exception as e:
    print("Please run server.py first for Local Network")

storeName = ''


class LocalNetworkGUI(tk.Frame):
    def menuBar(self, master):
        self.doNotUse()
        # menubar = tk.Menu(master)
        return ""

    def getBindButton(self):
        self.doNotUse()
        return self.Button1, False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.Label1 = tk.Label(self)
        self.Label1.place(x=150, y=50, height=41, width=299)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(font="-family {DejaVu Sans} -size 16 -weight bold", text='''Please login to continue''')

        self.Label2 = tk.Label(self)
        self.Label2.place(x=70, y=130, height=31, width=69)
        self.Label2.configure(activebackground="#f9f9f9", font="-family {DejaVu Sans} -size 12")
        self.Label2.configure(text='''Name:''')

        self.userNameEnter = tk.Entry(self)
        self.userNameEnter.place(x=220, y=130, height=33, width=246)
        self.userNameEnter.configure(background="white")
        self.userNameEnter.configure(font="TkFixedFont", selectbackground="blue", selectforeground="white")

        self.Label3 = tk.Label(self)
        self.Label3.place(x=70, y=190, height=31, width=139)
        self.Label3.configure(activebackground="#f9f9f9", font="-family {DejaVu Sans} -size 12")
        self.Label3.configure(text='''Encryption Key:''')

        self.key_var = tk.StringVar(self, value="")
        self.encryptKeyEnter = tk.Entry(self, textvariable=self.key_var)
        self.encryptKeyEnter.place(x=220, y=190, height=33, width=246)
        self.encryptKeyEnter.configure(show="*", background="white")
        self.encryptKeyEnter.configure(font="TkFixedFont", selectbackground="blue", selectforeground="white")

        self.Button1 = tk.Button(self,
                                 command=lambda: self.goAhead(
                                     self.userNameEnter.get(),
                                     self.encryptKeyEnter.get(),
                                     controller))
        self.Button1.place(x=240, y=260, height=41, width=131)
        self.Button1.configure(activebackground="#f9f9f9", font="-family {DejaVu Sans} -size 12 -weight bold")
        self.Button1.configure(text='''Continue''')

        self.backBtn = tk.Button(self, command=lambda: controller.show_frame(WelcomeGUI))
        self.backBtn.place(x=20, y=10, height=31, width=71, bordermode='ignore')
        self.backBtn.configure(activebackground="#f6685e")
        self.backBtn.configure(background="#f6685e")
        self.backBtn.configure(text='''Back''')

    def goAhead(self, name, private_key, cont):
        self.doNotUse()
        # global PRIVATE_KEY
        # PRIVATE_KEY = private_key
        if name == '':
            messagebox.showerror("Error", 'Name is not provided')
        elif private_key == '':
            messagebox.showerror("Error", "Encryption key not provided")
        else:
            global storeName
            # cipher = _aes.AESCipher(private_key)  # TODO
            storeName = name
            self.key_var.set("")

            cont.show_frame(LocalChatBoxGUI)

    def doNotUse(self):
        pass


class LocalChatBoxGUI(tk.Frame):
    msg = ''
    buttonMsg = None
    cont = None

    def menuBar(self, master):
        self.doNotUse()
        menubar = tk.Menu(master, font="TkMenuFont")
        menubar.add_command(label=f"User: {storeName}  ")
        menubar.add_command(label="Leave", command=self.leaveLocalChat)

        return menubar

    def getBindButton(self):
        return self.buttonMsg, True

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.cont = controller

        self.ScrolledLocalChatBox = tkscrolled.ScrolledText(self, undo=True)
        self.ScrolledLocalChatBox.place(x=0, y=10, height=354, width=581)
        self.ScrolledLocalChatBox.configure(bg="#17202A", fg="white", selectbackground="blue", selectforeground="white")
        self.ScrolledLocalChatBox.configure(font="-family {DejaVu Sans} -size 12")
        self.ScrolledLocalChatBox.configure(padx="10", pady="5")
        self.ScrolledLocalChatBox.configure(state=tk.DISABLED, wrap="word")

        self.entryMsg = tk.Entry(self)
        self.entryMsg.place(x=10, y=370, height=73, width=436)
        self.entryMsg.configure(background="#2C3E50", font="TkFixedFont")
        self.entryMsg.configure(foreground="white", selectbackground="blue", selectforeground="white")
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self, command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(x=460, y=370, height=41, width=101)
        self.buttonMsg.configure(font="-family {DejaVu Sans} -size 10 -weight bold")
        self.buttonMsg.configure(text='''Send''')

        self.Label1 = tk.Label(self)
        self.Label1.place(x=460, y=420, height=15, width=104)
        self.Label1.configure(font="-family {Ubuntu Mono} -size 8")
        self.Label1.configure(text='''[Ctrl+Enter] to send''')

        Variables.localRcv_thread = threading.Thread(target=self.receive)
        Variables.localRcv_thread.daemon = True
        Variables.localRcv_thread.start()

    def leaveLocalChat(self):
        # try:
        #     self.msg = "!DISCONNECT"
        #     self.sendMessage()
        # except:
        #     print('[LEAVING] Server is not running. Cannot disconnect.')

        self.cont.show_frame(LocalNetworkGUI)

    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.msg = msg
        self.entryMsg.delete(0, tk.END)
        self.sendMessage()

    # function to receive messages
    def receive(self):
        while True:
            if Variables.threadFlag:
                break
            try:
                message = client.recv(1024)  # .decode(FORMAT)
                message = cipher.decrypt(message)
                self.ScrolledLocalChatBox.config(state=tk.NORMAL)
                self.ScrolledLocalChatBox.insert(tk.END, message + "\n")
                self.ScrolledLocalChatBox.config(state=tk.DISABLED)
                self.ScrolledLocalChatBox.see(tk.END)
            except Exception as e:
                # an error will be printed on the command line or console if there's an error
                self.ScrolledLocalChatBox.config(state=tk.NORMAL)
                self.ScrolledLocalChatBox.insert(
                    tk.END, f"Disconnected: An error occurred as {e}\n")
                self.ScrolledLocalChatBox.config(state=tk.DISABLED)
                self.ScrolledLocalChatBox.see(tk.END)
                client.close()
                break

    # function to send messages
    def sendMessage(self):
        global storeName

        # while True:
        message = f"{storeName}: {self.msg}"
        message = cipher.encrypt(message)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        # break

    def doNotUse(self):
        pass
