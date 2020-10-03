import pyrebase
import uuid
from aes_implementation import encrypt, decrypt

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
currentUser = None
userID = None


def create_user():
    global currentUser
    global userID

    name = input('\nEnter name: ')
    email = input('Enter your email: ')
    password = input('Enter your password: ')
    # re_password = input('Re-enter password: ')

    # if password != re_password:
    #     raise Exception("passwords do not match")

    try:
        currentUser = firebaseAuth.create_user_with_email_and_password(
            email, password, name)

        userID = currentUser["localId"]
        print('Signup Success')

        data = {
            'userId': userID,
            'name': name,
            'email': currentUser['email'],
        }

        firebaseDB.child('users').child(f"{userID}").set(data)

    except Exception as e:
        print(f'Error: {e}')
        # exit(0)


def login_user():
    global currentUser
    global userID

    try:
        # email = input('\nEnter your email: ')
        # password = input('Enter your password: ')

        currentUser = firebaseAuth.sign_in_with_email_and_password(
            'subrat@gmail.com', 'subrat123')

        userID = currentUser["localId"]

        print('Login Success')

    except Exception as e:
        print(f'Error: {e}')
        # exit(0)


# User Authentication (Login/Signup)
authentication = int(input("1. Signup\n2. Login\n"))

try:
    if authentication == 1:
        create_user()
    else:
        login_user()
except Exception as e:
    print(f'Error: {e}')
    # exit(0)


# Chat room functions
def createChatRoom():

    chatroomID = uuid.uuid4()
    print(f'\nChat room ID: {chatroomID}')

    key = input('Enter new key: ')
    encrypted_key = encrypt(key, 'password')
    print(f'Encrypted key: {encrypted_key}')

    # all_rooms = firebaseDB.child('chat_rooms').get()
    # for room in all_rooms.each():
    #     if chatroomID == room.value().get('chatroomID'):
    #         raise Exception('Chatroom already exists')
    #         exit(0)

    data = {
        "chatroomID": str(chatroomID),
        "encrypted_key": str(encrypted_key),
    }

    # user_ID = currentUser["userId"]
    firebaseDB.child('chat_rooms').child(f"{userID}").set(data)

    print(f'\nChat room created with ID: {chatroomID}')


def joinChatRoom():

    try:
        chatroomID = input('\nEnter chatroom ID: ')

        all_rooms = firebaseDB.child('chat_rooms').get()
        # INPUT
        # 0af1be5c-df9e-4902-af42-73f31a163f7e
        # b"\xa1+\x0e]\xdf7as\xad\xc5H\xfa'&b\xad" to string

        # OUTPUT
        # {'chatroomID': '0af1be5c-df9e-4902-af42-73f31a163f7e',
        # 'encrypted_key': 'b"\\xa1+\\x0e]\\xdf7as\\xad\\xc5H\\xfa\'&b\\xad"'}

        for room in all_rooms.each():
            if chatroomID == room.val()['chatroomID']:
                # As we use ECB we have same encrypted key for the same text
                # But use CBC and first decrypt both the keys and then kompare
                key = input('Enter key to join: ')

                if key == room.val()['encrypted_key']:
                    print('success')
                    break
                else:
                    print("Wrong key")
            else:
                print("chatroom doesn't exist")

    except Exception as e:
        print(f'Error: {e}')
        # exit(0)


# After authenthication
print('1. Create chat room \n2. Join chat room')
chat_type = int(input())

try:
    if chat_type == 1:
        createChatRoom()
    else:
        joinChatRoom()

except Exception as e:
    print(f'Error: {e}')
    # exit(0)
