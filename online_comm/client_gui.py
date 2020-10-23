import tkinter as tk
from tkinter import messagebox
from fireDatabase import user_auth


def vp_start_gui():
    start = StartGUI()
    start.mainloop()


current_user = None
storeEmail = ''


class StartGUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginGUI)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class LoginGUI(tk.Frame):
    userLoginStat = False

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.geometry("600x450+334+137")
        master.minsize(1, 1)
        master.maxsize(1351, 738)
        master.resizable(1, 1)
        master.title("Encrypted Chat")
        master.configure(highlightcolor="black")

        self.email_label = tk.Label(self)
        self.email_label.place(relx=0.124, rely=0.186, height=21, width=109)
        self.email_label.configure(activebackground="#f9f9f9")
        self.email_label.configure(justify='left')
        self.email_label.configure(text='''Email''')
        self.email_label.pack()

        email = tk.StringVar(self, value=storeEmail)
        self.email_login_entry = tk.Entry(self, textvariable=email)
        self.email_login_entry.place(relx=0.412, rely=0.14, height=33, relwidth=0.507)
        self.email_login_entry.configure(background="white")
        self.email_login_entry.configure(font="TkFixedFont")
        self.email_login_entry.configure(selectbackground="blue")
        self.email_login_entry.configure(selectforeground="white")
        self.email_login_entry.pack()

        self.pass_label = tk.Label(self)
        self.pass_label.place(relx=0.144, rely=0.419, height=21, width=109)
        self.pass_label.configure(activebackground="#f9f9f9")
        self.pass_label.configure(text='''Password''')
        self.pass_label.pack()

        self.pass_login_entry = tk.Entry(self)
        self.pass_login_entry.place(relx=0.412, rely=0.372, height=33, relwidth=0.507)
        self.pass_login_entry.configure(background="white")
        self.pass_login_entry.configure(font="TkFixedFont")
        self.pass_login_entry.configure(selectbackground="blue")
        self.pass_login_entry.configure(selectforeground="white")
        self.pass_login_entry.pack()

        self.login_button = tk.Button(self, command=lambda: self.loginUser(
            self.email_login_entry.get(), self.pass_login_entry.get(), master))
        self.login_button.place(relx=0.412, rely=0.744, height=31, width=71)
        self.login_button.configure(activebackground="#f9f9f9")
        self.login_button.configure(text='''Login''')
        self.login_button.pack()

        self.Label1 = tk.Label(self)
        self.Label1.place(relx=0.317, rely=0.622, height=21, width=219)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Don't have an account?''')
        self.Label1.pack()

        self.signup_button = tk.Button(self, command=lambda: self.storeEmailAndSwitch(
            self.email_login_entry.get(), master))
        self.signup_button.place(relx=0.433, rely=0.689, height=31, width=71)
        self.signup_button.configure(activebackground="#f9f9f9")
        self.signup_button.configure(text='''Create''')
        self.signup_button.pack()

    def loginUser(self, email, password, root):
        global current_user

        if email == '':
            messagebox.showerror('Error', 'Email not provided')
        elif password == '':
            messagebox.showerror('Error', 'Password not provided')

        current_user = user_auth.login_user(email, password)

        if current_user is not None:
            self.userLoginStat = True
            messagebox.showinfo('Success', 'Login successful')
            root.switch_frame(ChatroomGUI)
        else:
            self.userLoginStat = False

    def storeEmailAndSwitch(self, email, root):
        global storeEmail

        self.userLoginStat = False
        if email != '':
            storeEmail = email

        root.switch_frame(SignupGUI)


"""
SIGNUP PAGE GUI
"""


class SignupGUI(tk.Frame):
    userSignupStat = False

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        master.geometry("600x450+334+137")
        master.minsize(1, 1)
        master.maxsize(1351, 738)
        master.resizable(1, 1)
        master.title("Encrypted Chat")
        master.configure(highlightcolor="black")

        self.name_label = tk.Label(self)
        self.name_label.place(relx=0.167, rely=0.2, height=20, width=110)
        self.name_label.configure(activebackground="#f9f9f9")
        self.name_label.configure(text='''Name''')
        self.name_label.pack()

        self.name_signup_entry = tk.Entry(self)
        self.name_signup_entry.place(relx=0.383, rely=0.178, height=33, relwidth=0.427)
        self.name_signup_entry.configure(background="white")
        self.name_signup_entry.configure(font="TkFixedFont")
        self.name_signup_entry.configure(selectbackground="blue")
        self.name_signup_entry.configure(selectforeground="white")
        self.name_signup_entry.pack()

        self.email_label = tk.Label(self)
        self.email_label.place(relx=0.167, rely=0.333, height=20, width=110)
        self.email_label.configure(activebackground="#f9f9f9")
        self.email_label.configure(text='''Email''')
        self.email_label.pack()

        e = tk.StringVar(self, value=storeEmail)
        self.email_signup_entry = tk.Entry(self, textvariable=e)
        self.email_signup_entry.place(relx=0.383, rely=0.311, height=33, relwidth=0.427)
        self.email_signup_entry.configure(background="white")
        self.email_signup_entry.configure(font="TkFixedFont")
        self.email_signup_entry.configure(selectbackground="blue")
        self.email_signup_entry.configure(selectforeground="white")
        self.email_signup_entry.pack()

        self.pass_label = tk.Label(self)
        self.pass_label.place(relx=0.183, rely=0.467, height=20, width=110)
        self.pass_label.configure(activebackground="#f9f9f9")
        self.pass_label.configure(text='''Password''')
        self.pass_label.pack()

        self.pass_signup_entry = tk.Entry(self)
        self.pass_signup_entry.place(relx=0.383, rely=0.444, height=33, relwidth=0.427)
        self.pass_signup_entry.configure(background="white")
        self.pass_signup_entry.configure(font="TkFixedFont")
        self.pass_signup_entry.configure(selectbackground="blue")
        self.pass_signup_entry.configure(selectforeground="white")
        self.pass_signup_entry.pack()

        self.re_pass_label = tk.Label(self)
        self.re_pass_label.place(relx=0.183, rely=0.467, height=20, width=110)
        self.re_pass_label.configure(activebackground="#f9f9f9")
        self.re_pass_label.configure(text='''Re-enter Password''')
        self.re_pass_label.pack()

        self.re_pass_signup_entry = tk.Entry(self)
        self.re_pass_signup_entry.place(relx=0.383, rely=0.444, height=33, relwidth=0.427)
        self.re_pass_signup_entry.configure(background="white")
        self.re_pass_signup_entry.configure(font="TkFixedFont")
        self.re_pass_signup_entry.configure(selectbackground="blue")
        self.re_pass_signup_entry.configure(selectforeground="white")
        self.re_pass_signup_entry.pack()

        self.signup_button = tk.Button(self)
        self.signup_button.place(relx=0.433, rely=0.6, height=31, width=71)
        self.signup_button.configure(activebackground="#f9f9f9")
        self.signup_button.configure(text='''Signup''', command=lambda: self.signupUser(
            self.name_signup_entry.get(),
            self.email_signup_entry.get(),
            self.pass_signup_entry.get(),
            self.re_pass_signup_entry.get(), master))
        self.signup_button.pack()

        self.back_button = tk.Button(self, command=lambda: master.switch_frame(LoginGUI))
        self.back_button.place(relx=0.067, rely=0.067, height=31, width=71)
        self.back_button.configure(activebackground="#f9f9f9")
        self.back_button.configure(text='''Back''')
        self.back_button.pack()

    def signupUser(self, name, email, password, re_password, root):
        global current_user
        flag = False

        if password == re_password:
            flag = True
            current_user = user_auth.create_user(name, email, password)
        else:
            flag = False
            messagebox.showerror('Error', 'Password do not match!')

        if current_user is not None and flag is True:
            self.userSignupStat = True
            messagebox.showinfo('Success', 'Signup is successful')
            root.switch_frame(ChatroomGUI)
        else:
            self.userSignupStat = False


"""
CHATROOM GUI
"""


class ChatroomGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        master.geometry("600x450+316+136")
        master.minsize(1, 1)
        master.maxsize(1351, 738)
        master.resizable(1, 1)
        master.title("Encrypted Chat")
        master.configure(highlightcolor="black")

        self.Label1 = tk.Label(self)
        self.Label1.place(relx=0.027, rely=0.222, height=21, width=354)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''CREATE CHATROOM''')
        self.Label1.pack()

        self.Label2 = tk.Label(self)
        self.Label2.place(relx=0.067, rely=0.178, height=21, width=89)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(text='''Chatroom ID''')
        self.Label2.pack()

        self.Entry1 = tk.Entry(self)
        self.Entry1.place(relx=0.333, rely=0.156, height=33, relwidth=0.443)
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="blue")
        self.Entry1.configure(selectforeground="white")
        self.Entry1.pack()

        self.Button1 = tk.Button(self)
        self.Button1.place(relx=0.817, rely=0.156, height=31, width=71)
        self.Button1.configure(activebackground="#f9f9f9")
        self.Button1.configure(text='''Generate''')
        self.Button1.pack()

        self.Label3 = tk.Label(self)
        self.Label3.place(relx=0.067, rely=0.289, height=21, width=119)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(text='''Create password''')
        self.Label3.pack()

        self.Entry2 = tk.Entry(self)
        self.Entry2.place(relx=0.333, rely=0.267, height=33, relwidth=0.443)
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="blue")
        self.Entry2.configure(selectforeground="white")
        self.Entry2.pack()

        self.Button2 = tk.Button(self)
        self.Button2.place(relx=0.417, rely=0.378, height=31, width=131)
        self.Button2.configure(activebackground="#f9f9f9")
        self.Button2.configure(text='''Create Chatroom''')
        self.Button2.pack()

        self.Label4 = tk.Label(self)
        self.Label4.place(relx=0.083, rely=0.667, height=21, width=89)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(text='''Chatroom ID''')
        self.Label4.pack()

        self.Label5 = tk.Label(self)
        self.Label5.place(relx=0.083, rely=0.756, height=21, width=99)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(text='''Enter password''')
        self.Label5.pack()

        self.Label6 = tk.Label(self)
        self.Label6.place(relx=0.026, rely=0.222, height=21, width=359)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(text='''JOIN CHATROOM''')
        self.Label6.pack()

        self.Entry3 = tk.Entry(self)
        self.Entry3.place(relx=0.333, rely=0.644, height=33, relwidth=0.443)
        self.Entry3.configure(background="white")
        self.Entry3.configure(font="TkFixedFont")
        self.Entry3.configure(selectbackground="blue")
        self.Entry3.configure(selectforeground="white")
        self.Entry3.pack()

        self.Entry4 = tk.Entry(self)
        self.Entry4.place(relx=0.333, rely=0.733, height=33, relwidth=0.443)
        self.Entry4.configure(background="white")
        self.Entry4.configure(font="TkFixedFont")
        self.Entry4.configure(selectbackground="blue")
        self.Entry4.configure(selectforeground="white")
        self.Entry4.pack()

        self.Button3 = tk.Button(self)
        self.Button3.place(relx=0.417, rely=0.844, height=31, width=131)
        self.Button3.configure(activebackground="#f9f9f9")
        self.Button3.configure(text='''Join Chatroom''')
        self.Button3.pack()


if __name__ == '__main__':
    # vp_start_gui()
    root = StartGUI()
    root.mainloop()
