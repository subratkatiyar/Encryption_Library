from fireDatabase import user_auth, create_chat_room, join_chat_room
from firebaseChats import FirebaseChats

current_user = None
chatsObj = FirebaseChats()


# User Authentication (Login/Signup)
def authenticate_user():
    global current_user

    authentication = int(input("1. Signup\n2. Login\n"))
    # user_auth = firebaseUser

    try:
        if authentication == 1:
            current_user = user_auth.create_user()
        else:
            current_user = user_auth.login_user()

    except Exception as err:
        print(f'Error: {err}')
        authenticate_user()


# After authentication
def join_chatroom():
    print('\n\n1. Create chat room \n2. Join chat room')
    chat_type = int(input())

    try:
        if chat_type == 1:
            create_chat_room()

        else:
            join_chat_room()

        print('\nEnter q/Q to quit anytime')
        while True:
            chatsObj.send_chat()
            chatsObj.receive_chat()

    except Exception as e:
        print(f'Main Error: {e}')


authenticate_user()
join_chatroom()
