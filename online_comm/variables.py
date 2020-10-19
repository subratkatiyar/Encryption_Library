# from fireDatabase import Auth, Chatroom
# from firebaseChats import FirebaseChats
# import pyrebase
# import aes_implementation as _aes
#
# # main.py
# current_user = None
# user_auth = Auth()
# chatroom_obj = Chatroom(current_user)
#
# # firebaseChats.py
# chatsObj = FirebaseChats()
#
# # fireDatabase.py
# # After storageBucket are not necessary
# firebaseConfig = {
#     "apiKey": "AIzaSyDJt212WpCmneIEZoy4lICFahAJF1vVPAU",
#     "authDomain": "encrypted-chat-python.firebaseapp.com",
#     "databaseURL": "https://encrypted-chat-python.firebaseio.com",
#     "storageBucket": "encrypted-chat-python.appspot.com",
#     "projectId": "encrypted-chat-python",
#     "messagingSenderId": "779469889144",
#     "appId": "1:779469889144:web:41527aa0d5703701d6578d",
#     "measurementId": "G-WGLXHL70KQ"
# }
#
# firebase = pyrebase.initialize_app(firebaseConfig)
# firebaseDB = firebase.database()
# firebaseAuth = firebase.auth()
# cipher = _aes.AESCipher('password')
#
# # Parameters for currentUser:
# '''
# currentUser : {
#     'kind': '',
#     'localId': '',
#     'email': '',
#     'displayName': '',
#     'idToken': '',
#     'registered': True,
#     'refreshToken': '',
#     'expiresIn': '3600',
# }
# '''
