import random
import string
from datetime import datetime, date

from fireDatabase import firebaseDB, user_auth


def fetch_msg():
    try:
        return firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child(
            'chats').child('temp').get()

    except Exception:
        raise Exception('ERROR_GET_MSG')


def upload_msg(msg):
    _time = f"{date.today()}_{datetime.now().time().strftime('%H:%M:%S')}"
    user_name = user_auth.currentUser['displayName']

    def random_char(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))

    try:
        firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('chats').child('temp').set(
            {
                'msg': msg,
                'user': user_name,
                'time': _time,
            }
        )
        firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('chats').child(
            f"{user_name}_{_time}_{random_char(5)}").set(
            {
                'msg': msg,
                'user': user_name,
            }
        )

    except Exception:
        raise Exception('ERROR_SEND_MSG')
        # return


# class FirebaseChats:
#     msg_log = None
#     new_msg = ''
#     previous_log = None
#
#     def send_chat(self, msg=''):
#         self.new_msg = input('Enter your msg: ')
#         self.new_msg = msg
#
#         if self.new_msg == 'q' or self.new_msg == 'Q':
#             firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('attendees').child(
#                 user_auth.userID).remove()
#             firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('chats').child('temp').remove()
#         self.upload_msg()
#
#     def receive_chat(self):
#         if self.new_msg == 'q' or self.new_msg == 'Q':
#             return None
#
#         log = self.fetch_msg().val()
#         # log = self.msg_log.val()
#
#         if self.previous_log != log and log is not None:
#             print('log is not none')
#             self.previous_log = log
#             print(f"\n{log['user']} --> {log['msg']}")
#             print(f"at {log['time']} \n\n")
#             return log
#         return log


# chatsObj = FirebaseChats()
# receive_thread = threading.Thread(target=chatsObj.receive_chat)
# send_thread = threading.Thread(target=chatsObj.send_chat)
