import pyrebase
import uuid
from datetime import datetime
import aes_implementation as _aes
import threading

# After storageBucket are not necessary
firebaseConfig = {
    "apiKey": "AIzaSyDJt212WpCmneIEZoy4lICFahAJF1vVPAU",
    "authDomain": "encrypted-chat-python.firebaseapp.com",
    "databaseURL": "https://encrypted-chat-python.firebaseio.com",
    "storageBucket": "encrypted-chat-python.appspot.com",
    "projectId": "encrypted-chat-python",
    "messagingSenderId": "779469889144",
    "appId": "1:779469889144:web:41527aa0d5703701d6578d",
    "measurementId": "G-WGLXHL70KQ"
}

# Parameters for currentUser:
'''
currentUser : {
    'kind': '',
    'localId': '',
    'email': '',
    'displayName': '',
    'idToken': '',
    'registered': True,
    'refreshToken': '',
    'expiresIn': '3600',
}
'''

firebase = pyrebase.initialize_app(firebaseConfig)
firebaseDB = firebase.database()
firebaseAuth = firebase.auth()
cipher = _aes.AESCipher('password')

CREATED_BY = ''
CHATROOM_NAME = ''


class Auth:
    currentUser = None
    userID = None

    def create_user(self):

        name = input('\nEnter name: ')
        email = input('Enter your email: ')
        password = input('Enter your password: ')
        # re_password = input('Re-enter password: ')

        # if password != re_password:
        #     raise Exception("passwords do not match")

        try:
            # TODO remove name before pushing
            self.currentUser = firebaseAuth.create_user_with_email_and_password(
                email, password)

            self.userID = self.currentUser["localId"]
            print('Signup Success')

            data = {
                'userId': self.userID,
                'name': name,
                'email': self.currentUser['email'],
            }

            firebaseDB.child('users').child(f"{name}").set(data)

            return self.currentUser

        except Exception as e:
            print(f'Error: {e}')
            self.create_user()
            # exit(0)

    def login_user(self):
        try:
            email = input('\nEnter your email: ')
            password = input('Enter your password: ')

            self.currentUser = firebaseAuth.sign_in_with_email_and_password(
                email, password)

            self.userID = self.currentUser["localId"]

            print('Login Success')

            return self.currentUser

        except Exception as e:
            print(f'Error: {e}')
            self.login_user()
            # exit(0)


user_auth = Auth()


def create_chat_room():
    global CHATROOM_NAME
    length = 0

    chatroom_id = uuid.uuid4()
    print(f'\nChat room ID: {chatroom_id}')

    chatroom_key = input('Enter new password: ')
    encrypted_chatroom_key = cipher.encrypt(chatroom_key)

    all_rooms = firebaseDB.child('chat_rooms').get()
    if all_rooms is not None:
        for room in all_rooms.each():
            length = length + 1
            # if chatroom_id == room.val()['chatroomID']:
            #     print('Chatroom already exists')
            #     create_chat_room()

    data = {
        "chatroomID": str(chatroom_id),
        "encrypted_chatroom_key": encrypted_chatroom_key.hex(),
        "created_userID": user_auth.userID,
        "created_name": user_auth.currentUser['displayName']
    }

    CHATROOM_NAME = f'chatroom_{length + 1}'

    try:
        firebaseDB.child('chat_rooms').child(CHATROOM_NAME).child("details").set(data)

        firebaseDB.child('chat_rooms').child(CHATROOM_NAME).child('attendees').child(user_auth.userID).set(
            {
                'name': user_auth.currentUser['displayName'],
                'joined_at': datetime.now().timestamp(),
            }
        )

        return chatroom_id

    except Exception as e:
        print('create chatroom upload Error:', e)
        create_chat_room()


def join_chat_room():
    global CREATED_BY
    global CHATROOM_NAME
    flag = 0

    def get_password(_room):
        encrypted_chatroom_key = _room.val()['details']['encrypted_chatroom_key']

        chatroom_password = input('\nEnter chatroom password: ')
        # decrypt_key = input('Enter key to decrypt: ')      # password

        decrypted_password = cipher.decrypt(bytes.fromhex(encrypted_chatroom_key))

        if chatroom_password == decrypted_password:
            print('success join')
        else:
            print("Wrong password")
            get_password(_room=_room)

    try:
        chatroom_id = input('\nEnter chatroom ID: ')

        all_rooms = firebaseDB.child('chat_rooms').get()

        for room in all_rooms.each():
            if chatroom_id == room.val()['details']['chatroomID']:
                flag = 1

                CREATED_BY = room.val()['details']['created_name']
                get_password(_room=room)
                CHATROOM_NAME = room.key()

                firebaseDB.child('chat_rooms').child(CHATROOM_NAME).child('attendees').child(
                    user_auth.userID).set(
                    {
                        'name': user_auth.currentUser['displayName'],
                        'joined_at': datetime.now().timestamp(),
                    }
                )

                return chatroom_id

        if flag == 0:
            print("chatroom doesn't exist")
            join_chat_room()

    except Exception as e:
        print(f'Error: {e}')
        join_chat_room()
        # exit(0)
