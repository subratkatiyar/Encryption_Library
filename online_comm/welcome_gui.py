import tkinter as tk

from PIL import Image, ImageTk


class WelcomeGUI(tk.Frame):
    def menuBar(self, master):
        self.doNotUse()
        return ""

    def getBindButton(self):
        self.doNotUse()
        return None, False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.Frame1 = tk.Frame(self)
        self.Frame1.place(x=-10, y=-10, height=465, width=305)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#1C1C1C")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(x=50, y=190, height=32, width=218)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(background="#1C1C1C")
        self.Label1.configure(font="-family {DejaVu Sans} -size 18 -weight bold")
        self.Label1.configure(foreground="#FFFFFF")
        self.Label1.configure(text='''Encrypted Chat''')

        self.Label2 = tk.Label(self.Frame1)
        self.Label2.place(x=100, y=230, height=31, width=109)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(background="#1C1C1C")
        self.Label2.configure(font="-family {DejaVu Sans} -size 18 -weight bold")
        self.Label2.configure(foreground="#FFFFFF")
        self.Label2.configure(text='''Library''')

        self.Label3 = tk.Label(self.Frame1)
        self.Label3.place(x=50, y=280, height=31, width=219)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(background="#1C1C1C")
        self.Label3.configure(font="-family {DejaVu Sans} -size 12")
        self.Label3.configure(foreground="#FFFFFF")
        self.Label3.configure(text='''Secure Messaging Library''')

        load = Image.open("assets/logo.png")
        render = ImageTk.PhotoImage(load)
        self.Label4 = tk.Label(self.Frame1, image=render)
        self.Label4.image = render
        self.Label4.place(x=90, y=40, height=132, width=132)

        self.Label5 = tk.Label(self)
        self.Label5.place(x=320, y=50, height=41, width=249)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(font="-family {DejaVu Sans} -size 18 -weight bold")
        self.Label5.configure(text='''Choose a network''')

        self.Frame2 = tk.Frame(self)
        self.Frame2.place(x=320, y=100, height=145, width=255)
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")

        self.Button1 = tk.Button(self.Frame2, command=lambda: self.onlineFirebase(controller))
        self.Button1.place(x=40, y=20, height=41, width=181)
        self.Button1.configure(text='''Online Firebase''')

        self.Button2 = tk.Button(self.Frame2, command=lambda: self.localNetwork(controller))
        self.Button2.place(x=40, y=80, height=41, width=181)
        self.Button2.configure(text='''Local Network''')

        self.Frame3 = tk.Frame(self)
        self.Frame3.place(x=320, y=270, height=85, width=255)
        self.Frame3.configure(borderwidth="2")
        self.Frame3.configure(relief="groove")

        self.Button4 = tk.Button(self.Frame3, command=lambda: self.fileEncrypt(controller))
        self.Button4.place(x=40, y=20, height=41, width=181)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(state='active')
        self.Button4.configure(text='''File Encrypt''')

    def onlineFirebase(self, cont):
        self.doNotUse()
        from client_gui import LoginGUI
        cont.show_frame(LoginGUI)

    def localNetwork(self, cont):
        self.doNotUse()
        from client import LocalNetworkGUI
        cont.show_frame(LocalNetworkGUI)

    def fileEncrypt(self, cont):
        self.doNotUse()
        from file_encrypt_gui import FileEncryptGUI
        cont.show_frame(FileEncryptGUI)

    def doNotUse(self):
        pass
