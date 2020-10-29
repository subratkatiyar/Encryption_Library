from datetime import datetime
from random import randint

import pyrebase

import aes_implementation as _aes
from variables import Variables
from master_key import master_key

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

firebase = pyrebase.initialize_app(firebaseConfig)
firebaseDB = firebase.database()
firebaseAuth = firebase.auth()
cipher = _aes.AESCipher(master_key)


class Auth:
    currentUser = None
    userID = None
    CREATED_BY = ''
    CHATROOM_ID = 'chatroom_0'

    def create_user(self, email, password, name):
        # TODO remove name before pushing
        self.currentUser = firebaseAuth.create_user_with_email_and_password(email, password, name)

        self.userID = self.currentUser["localId"]
        print('Signup Success')

        data = {
            'userId': self.userID,
            'name': name,
            'email': self.currentUser['email'],
            'profileIndex': randint(1, 7)
        }

        Variables.userData = data

        firebaseDB.child('users').child(f"{email}").set(data)

        return self.currentUser

    def login_user(self, email, password):
        self.currentUser = firebaseAuth.sign_in_with_email_and_password(email, password)
        self.userID = self.currentUser["localId"]

        Variables.userData = firebaseDB.child('users').child(self.currentUser['displayName']).get().val()

        print('Login Success')

        return self.currentUser


user_auth = Auth()


def create_chat_room(chatroom_id='', chatroom_key=''):
    length = 0

    encrypted_chatroom_key = cipher.encrypt(chatroom_key)

    all_rooms = firebaseDB.child('chat_rooms').get()
    if all_rooms is not None:
        for room in all_rooms.each():
            length = length + 1
            if chatroom_id == room.val()['details']['chatroomID']:
                raise Exception('CHATROOM_EXISTS')

    data = {
        "chatroomID": chatroom_id,
        "encrypted_chatroom_key": encrypted_chatroom_key.hex(),
        "created_userID": user_auth.userID,
        "created_name": user_auth.currentUser['displayName']
    }

    user_auth.CHATROOM_ID = f'chatroom_{length}'

    try:
        firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child("details").set(data)

        firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('chats').child('temp').set(
            {
                'msg': "",
                'user': "dummy",
            }
        )

        firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('attendees').child(user_auth.userID).set(
            {
                'name': user_auth.currentUser['displayName'],
                'email': user_auth.currentUser['email'],
                'joined_at': datetime.now().timestamp(),
                'status': 'online'
            }
        )

        return data

    except Exception:
        raise Exception('ERROR_UPLOAD_DATA')


def join_chat_room(chatroom_id, chatroom_password):
    flag = 0

    # Function
    def get_password(_room):
        encrypted_chatroom_key = _room.val()['details']['encrypted_chatroom_key']
        decrypted_password = cipher.decrypt(bytes.fromhex(encrypted_chatroom_key))

        if chatroom_password == decrypted_password:
            print('success join')
        else:
            raise Exception('INVALID_CHATROOM_PASSWORD')

    # End Function

    all_rooms = firebaseDB.child('chat_rooms').get()

    for room in all_rooms.each():
        if chatroom_id == room.val()['details']['chatroomID']:
            flag = 1
            print(flag)

            user_auth.CREATED_BY = room.val()['details']['created_name']
            get_password(_room=room)
            user_auth.CHATROOM_ID = f"{room.key()}"

            try:
                firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('attendees').child(
                    user_auth.userID).set(
                    {
                        'name': user_auth.currentUser['displayName'],
                        'email': user_auth.currentUser['email'],
                        'joined_at': datetime.now().timestamp(),
                        'status': 'online'
                    }
                )

                firebaseDB.child('chat_rooms').child(user_auth.CHATROOM_ID).child('chats').child('temp').set(
                    {
                        'msg': "",
                        'user': "dummy",
                    }
                )

                data = {
                    'chatroomID': user_auth.CHATROOM_ID,
                    'created_name': user_auth.CREATED_BY,
                    'created_userID': room.val()['details']['created_userID']
                }
                return data
            except Exception:
                raise Exception('ERROR_JOINING_CHATROOM')

    if flag == 0:
        raise Exception('CHATROOM_NOT_EXIST')
