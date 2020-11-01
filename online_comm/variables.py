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
    threadFlag = False
    firebaseReceive_thread = None
    getAttendees_thread = None
    localRcv_thread = None

    userExpiryTimeLeft = 0.0
    current_status = 'ONLINE'

    # text variables
    storeEmail = None
    storeUserID = None
    storeName = None
    #

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
