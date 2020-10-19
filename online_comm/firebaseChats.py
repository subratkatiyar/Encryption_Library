import os
import threading
from datetime import datetime, date

from fireDatabase import firebaseDB
from fireDatabase import CHATROOM_NAME, user_auth


# TODO's
# DONE give different key when upload chat else overwrite when Hour and minute is same
# first fetch message then prompt to send

class FirebaseChats:
    msg_log = None
    new_msg = ''

    def fetch_msg(self):
        try:
            self.msg_log = firebaseDB.child('chat_rooms').child(CHATROOM_NAME).child('chats').get()

        except Exception as e:
            print('Error fetching messages:', e)
            print('Trying again...\n')

    def upload_msg(self):
        try:
            firebaseDB.child('chat_rooms').child(CHATROOM_NAME).child('chats').child(
                f"{date.today()}_{datetime.now().time()}").set(
                {
                    'msg': self.new_msg,
                    'user': user_auth.currentUser['displayName'],
                }
            )

        except Exception as e:
            print('Error sending message: ', e)
            print('Try again')
            return

    def send_chat(self):
        self.new_msg = input('Enter your msg: ')

        if self.new_msg == 'q' or self.new_msg == 'Q':
            exit(0)

        threading.Thread(target=self.upload_msg()).start()

    def receive_chat(self):
        threading.Thread(target=self.fetch_msg()).start()

        os.system('clear')
        print('received chat')
        for log in self.msg_log.each():
            print(f"\n{log.val()['user']} --> {log.val()['msg']}")
            print(f"at {log.key()} \n\n")

# OUTPUT RECEIVED

# Enter q/Q to quit anytime
# Enter your msg: my name subrat
# received chat
#
# Gagan --> my name subrat
# at 2020-10-15_22:36
#
#
#
# Gagan --> my name subrat
# at 2020-10-15_22:40
#
#
#
# Enter q/Q to quit anytime
# Enter your msg: TERM environment variable not set.