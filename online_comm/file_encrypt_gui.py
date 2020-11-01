import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from welcome_gui import WelcomeGUI


class FileEncryptGUI(tk.Frame):
    def menuBar(self, master):
        return ""

    def getBindButton(self):
        return None, False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        self.Frame1 = tk.Frame(self)
        self.Frame1.place(x=120, y=50, height=65, width=355)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(x=110, y=20, height=25, width=149)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(font="-family {DejaVu Sans} -size 14 -weight bold")
        self.Label1.configure(text='''File Encrypt''')

        self.TSeparator1 = ttk.Separator(self)
        self.TSeparator1.place(x=0, y=80, width=120)

        self.TSeparator2 = ttk.Separator(self)
        self.TSeparator2.place(x=475, y=80, width=120)

        self.Button1 = tk.Button(self, command=lambda: filedialog.askopenfilename())
        self.Button1.place(x=200, y=150, height=41, width=211)
        self.Button1.configure(activebackground="#f9f9f9")
        self.Button1.configure(font="-family {DejaVu Sans} -size 11")
        self.Button1.configure(text='''Pick a file to Encrypt''')

        self.Listbox1 = tk.Listbox(self)
        self.Listbox1.place(x=20, y=250, height=176, width=544)
        self.Listbox1.configure(background="white")
        self.Listbox1.configure(font="TkFixedFont")

        self.Listbox1.insert(0, "/home/user/program-directory/encryptedFiles/file-1.txt")
        self.Listbox1.insert(1, "/home/user/program-directory/encryptedFiles/file-2.txt")
        self.Listbox1.insert(2, "/home/user/program-directory/encryptedFiles/file-3.txt")
        self.Listbox1.insert(3, "/home/user/program-directory/encryptedFiles/file-4.txt")
        self.Listbox1.insert(4, "/home/user/program-directory/encryptedFiles/file-5.txt")

        self.Label2 = tk.Label(self)
        self.Label2.place(x=10, y=220, height=21, width=159)
        self.Label2.configure(font="-family {DejaVu Sans} -size 10")
        self.Label2.configure(text='''Output file location:''')

        self.TScale1 = ttk.Scale(self, from_=0, to=1.0)
        self.TScale1.place(x=560, y=250, height=170, width=17)
        self.TScale1.configure(orient="vertical")
        self.TScale1.configure(takefocus="")
        self.TScale1.configure(cursor="fleur")

        self.TScale2 = ttk.Scale(self, from_=0, to=1.0)
        self.TScale2.place(x=20, y=420, height=17, width=540)
        self.TScale2.configure(takefocus="")

        self.backBtn = tk.Button(self, command=lambda: controller.show_frame(WelcomeGUI))
        self.backBtn.place(x=20, y=10, height=31, width=71, bordermode='ignore')
        self.backBtn.configure(activebackground="#f6685e")
        self.backBtn.configure(background="#f6685e")
        self.backBtn.configure(text='''Back''')
