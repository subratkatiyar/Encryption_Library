import tkinter as tk
from tkinter import messagebox

from chatroom_gui import ChatroomGUI
from fireDatabase import user_auth
from variables import Variables

from welcome_gui import WelcomeGUI


class LoginGUI(tk.Frame):
    userLoginStat = False
    password = None
    login_button = None

    def menuBar(self, master):
        return ""

    def getBindButton(self):
        return self.login_button, False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        Variables.storeEmail = tk.StringVar(master, value='')

        self.Frame1 = tk.Frame(self)
        self.Frame1.place(x=60, y=80, height=215, width=485)
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        self.email_label = tk.Label(self.Frame1)
        self.email_label.place(x=60, y=40, height=21, width=109)
        self.email_label.configure(activebackground="#f9f9f9")
        self.email_label.configure(justify='left')
        self.email_label.configure(text='Email')
        # self.email_label.pack()

        self.email_login_entry = tk.Entry(self.Frame1, textvariable=Variables.storeEmail)
        self.email_login_entry.place(x=200, y=30, height=33, width=246)
        self.email_login_entry.configure(background="white")
        self.email_login_entry.configure(font="TkFixedFont")
        self.email_login_entry.configure(selectbackground="blue")
        self.email_login_entry.configure(selectforeground="white")
        # self.email_login_entry.pack()
        self.email_login_entry.focus()

        self.pass_label = tk.Label(self.Frame1)
        self.pass_label.place(x=70, y=90, height=21, width=109)
        self.pass_label.configure(activebackground="#f9f9f9")
        self.pass_label.configure(text='''Password''')
        # self.pass_label.pack()

        self.password = tk.StringVar(self, value='')
        self.pass_login_entry = tk.Entry(self.Frame1, textvariable=self.password)
        self.pass_login_entry.place(x=200, y=80, height=33, width=246)
        self.pass_login_entry.configure(show="*", background="white")
        self.pass_login_entry.configure(font="TkFixedFont")
        self.pass_login_entry.configure(selectbackground="blue")
        self.pass_login_entry.configure(selectforeground="white")
        # self.pass_login_entry.pack()

        self.login_button = tk.Button(self.Frame1,
                                      command=lambda: self.loginUser(
                                          self.email_login_entry.get(),
                                          self.pass_login_entry.get(),
                                          controller
                                      ))
        self.login_button.place(x=200, y=160, height=31, width=71)
        self.login_button.configure(activebackground="#f9f9f9")
        self.login_button.configure(text='''Login''')
        # self.login_button.pack(pady=(20, 0))

        self.Label1 = tk.Label(self)
        self.Label1.place(x=190, y=320, height=21, width=219)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(text='''Don't have an account?''')
        # self.Label1.pack(pady=(50, 0))

        self.create_user_button = tk.Button(self,
                                            command=lambda: self.storeEmailAndSwitch(
                                                self.email_login_entry.get(), controller))
        self.create_user_button.place(x=260, y=350, height=31, width=71)
        self.create_user_button.configure(activebackground="#f9f9f9")
        self.create_user_button.configure(text='''Create''')
        # self.create_user_button.pack()

        self.backBtn = tk.Button(self, command=lambda: controller.show_frame(WelcomeGUI))
        # self.backBtn.place(x=30, y=310, height=31, width=71, bordermode='ignore')
        self.backBtn.place(x=20, y=10, height=31, width=71, bordermode='ignore')
        self.backBtn.configure(activebackground="#f6685e")
        self.backBtn.configure(background="#f6685e")
        self.backBtn.configure(text='''Back''')

    def loginUser(self, email, psw, cont):
        if email == '':
            messagebox.showerror('Error', 'Email not provided')
        elif email.find('@') == -1:
            messagebox.showwarning('Invalid', 'Invalid email address')
        elif psw == '':
            messagebox.showerror('Error', 'Password not provided')
        else:
            try:
                Variables.current_user = user_auth.login_user(email, psw)

            except Exception as e:
                x, y = e.args

                self.userLoginStat = False

                if y.find('INVALID_EMAIL') != -1 or y.find("EMAIL_NOT_FOUND") != -1:
                    messagebox.showerror('Error Login', "Invalid Email\nUser doesn't exist  ")
                elif y.find("INVALID_PASSWORD") != -1:
                    messagebox.showerror('Error Login', 'Invalid Password')

        if Variables.current_user['localId'] != '':
            self.userLoginStat = True
            messagebox.showinfo('Success', 'Login successful')

            self.password.set('')
            Variables.userExpiryTimeLeft = int(user_auth.currentUser['expiresIn'])/60
            Variables.storeUserID.set(str(user_auth.userID))
            Variables.storeEmail.set(email)
            Variables.storeName.set(str(user_auth.currentUser['displayName']))

            cont.show_frame(ChatroomGUI)

    def storeEmailAndSwitch(self, email, cont):
        self.userLoginStat = False
        Variables.storeEmail.set(email)

        cont.show_frame(SignupGUI)


"""
SIGNUP PAGE GUI
"""


class SignupGUI(tk.Frame):
    userSignupStat = False
    password = None
    signup_button = None

    def menuBar(self, master):
        return ""

    def getBindButton(self):
        return self.signup_button, False

    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)

        # Variables.email = tk.StringVar(self, value='')

        self.name_label = tk.Label(self)
        self.name_label.place(x=140, y=90, height=20, width=70)
        self.name_label.configure(activebackground="#f9f9f9")
        self.name_label.configure(text='''Name''')
        # self.name_label.pack()

        self.name_signup_entry = tk.Entry(self)
        self.name_signup_entry.place(x=230, y=80, height=33, width=256)
        self.name_signup_entry.configure(background="white")
        self.name_signup_entry.configure(font="TkFixedFont")
        self.name_signup_entry.configure(selectbackground="blue")
        self.name_signup_entry.configure(selectforeground="white")
        # self.name_signup_entry.pack()
        self.name_signup_entry.focus()

        self.email_label = tk.Label(self)
        self.email_label.place(x=150, y=140, height=20, width=50)
        self.email_label.configure(activebackground="#f9f9f9")
        self.email_label.configure(text='''Email''')
        # self.email_label.pack()

        self.email_signup_entry = tk.Entry(self, textvariable=Variables.storeEmail)
        self.email_signup_entry.place(x=230, y=130, height=33, width=256)
        self.email_signup_entry.configure(background="white")
        self.email_signup_entry.configure(font="TkFixedFont")
        self.email_signup_entry.configure(selectbackground="blue")
        self.email_signup_entry.configure(selectforeground="white")
        # self.email_signup_entry.pack()

        self.pass_label = tk.Label(self)
        self.pass_label.place(x=120, y=190, height=20, width=80)
        self.pass_label.configure(activebackground="#f9f9f9")
        self.pass_label.configure(text='''Password''')
        # self.pass_label.pack()

        self.password = tk.StringVar(self, value='')
        self.pass_signup_entry = tk.Entry(self, textvariable=self.password)
        self.pass_signup_entry.place(x=230, y=180, height=33, width=256)
        self.pass_signup_entry.configure(show="*", background="white")
        self.pass_signup_entry.configure(font="TkFixedFont")
        self.pass_signup_entry.configure(selectbackground="blue")
        self.pass_signup_entry.configure(selectforeground="white")
        # self.pass_signup_entry.pack()

        self.re_pass_label = tk.Label(self)
        self.re_pass_label.place(x=70, y=240, height=19, width=132)
        self.re_pass_label.configure(activebackground="#f9f9f9")
        self.re_pass_label.configure(text='''Re-enter Password''')
        # self.re_pass_label.pack()

        self.re_password = tk.StringVar(self, value='')
        self.re_pass_signup_entry = tk.Entry(self, textvariable=self.re_password)
        self.re_pass_signup_entry.place(x=230, y=230, height=33, width=256)
        self.re_pass_signup_entry.configure(show="*", background="white")
        self.re_pass_signup_entry.configure(font="TkFixedFont")
        self.re_pass_signup_entry.configure(selectbackground="blue")
        self.re_pass_signup_entry.configure(selectforeground="white")
        # self.re_pass_signup_entry.pack()

        self.signup_button = tk.Button(self)
        self.signup_button.place(x=260, y=280, height=31, width=71)
        self.signup_button.configure(activebackground="#f9f9f9")
        self.signup_button.configure(text='''Signup''',
                                     command=lambda: self.signupUser(
                                         self.name_signup_entry.get(),
                                         self.email_signup_entry.get(),
                                         self.pass_signup_entry.get(),
                                         self.re_pass_signup_entry.get(), controller))
        # self.signup_button.pack()

        self.back_button = tk.Button(self, command=lambda: self.goBack(self.email_signup_entry.get(), controller))
        self.back_button.place(x=20, y=10, height=31, width=71)
        self.back_button.configure(activebackground="#f9f9f9")
        self.back_button.configure(text='''Back''')
        # self.back_button.pack()

    def goBack(self, email, cont):
        self.userSignupStat = False
        Variables.storeEmail.set(email)

        cont.show_frame(LoginGUI)

    def signupUser(self, name, email, password, re_password, cont):
        if name == '':
            messagebox.showwarning('Warning', 'Name not provided')
        elif email == '':
            messagebox.showwarning('Warning', 'Email not provided')
        elif email.find('@') == -1:
            messagebox.showwarning('Invalid', 'Invalid email address')
        elif len(password) < 6:
            messagebox.showwarning('Short password', 'Password should be at least 6 characters long')
        elif password == re_password:
            try:
                Variables.current_user = user_auth.create_user(email, password, name)
            except Exception as e:
                x, y = e.args
                if y.find("EMAIL_EXISTS") != -1:
                    messagebox.showerror('Error Signup', 'User already exists.')
                else:
                    messagebox.showerror('Error Signup', 'Invalid Details')
        else:
            messagebox.showerror('Error', 'Password do not match!')

        if Variables.current_user['localId'] != '':
            self.userSignupStat = True
            messagebox.showinfo('Success', 'Signup is successful')

            self.password.set('')
            self.re_password.set('')

            Variables.storeUserID.set(str(user_auth.userID))
            Variables.storeEmail.set(email)
            Variables.storeName.set(str(user_auth.currentUser['displayName']))

            cont.show_frame(ChatroomGUI)
        else:
            self.userSignupStat = False
