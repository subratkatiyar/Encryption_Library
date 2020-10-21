import random
import string
import threading
from datetime import datetime, date

from fireDatabase import firebaseDB
from fireDatabase import user_auth


class FirebaseChats:
    msg_log = None
    new_msg = ''
    previous_log = None

    def fetch_msg(self):
        try:
            self.msg_log = firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child(
                'chats').child('temp').get()

        except Exception as e:
            print('Error fetching messages:', e)
            print('Trying again...\n')

    def upload_msg(self):
        time = f"{date.today()}_{datetime.now().time().strftime('%H:%M:%S')}"
        user_name = user_auth.currentUser['displayName']

        def random_char(y):
            return ''.join(random.choice(string.ascii_letters) for x in range(y))

        try:
            firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('chats').child('temp').set(
                {
                    'msg': self.new_msg,
                    'user': user_auth.currentUser['displayName'],
                    'time': time,
                }
            )
            firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('chats').child(
                f"{user_name}_{time}_{random_char(5)}").set(
                {
                    'msg': self.new_msg,
                    'user': user_name,
                }
            )

        except Exception as e:
            print('Error sending message: ', e)
            print('Try again')
            return

    def send_chat(self):
        while True:
            print('send chat')
            self.new_msg = input('Enter your msg: ')

            if self.new_msg == 'q' or self.new_msg == 'Q':
                firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('attendees').child(
                    user_auth.userID).remove()
                firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_NAME).child('chats').child('temp').remove()
                break
            self.upload_msg()

        exit(0)

    def receive_chat(self):
        while True:
            if self.new_msg == 'q' or self.new_msg == 'Q':
                break

            self.fetch_msg()
            log = self.msg_log.val()

            if self.previous_log != log and log is not None:
                self.previous_log = log
                print(f"\n{log['user']} --> {log['msg']}")
                print(f"at {log['time']} \n\n")

        exit(0)

        # os.system('clear')
        # print('received chat')
        # for log in self.msg_log.each():
        #     print(f"\n{log.val()['user']} --> {log.val()['msg']}")
        #     print(f"at {log.key()} \n\n")


chatsObj = FirebaseChats()
receive_thread = threading.Thread(target=chatsObj.receive_chat)
send_thread = threading.Thread(target=chatsObj.send_chat)
