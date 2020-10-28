"""
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
"""


class Variables:
    # current_user = None
    threadFlag = False
    receive_thread = None
    storeEmail = None
    storeUserID = None
    storeName = None
    current_user = {
        'kind': '',
        'localId': '',
        'email': '',
        'displayName': '',
        'idToken': '',
        'registered': False,
        'refreshToken': '',
        'expiresIn': '3600',
    }
    chatroomData = {
        "chatroomID": '',
        "encrypted_chatroom_key": '',  # ! Only created chatroom
        "created_userID": '',
        "created_name": ''
    }
    userData = {
        'userId': '',
        'name': '',
        'email': '',
        'profileIndex': -1
    }
