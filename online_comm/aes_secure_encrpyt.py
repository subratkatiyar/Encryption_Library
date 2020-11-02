from aes_implementation import cipher

'''
Any file that can be opened by with command in pyhton can now be encrypte.
Working checked on:-
-> .txt file
-> .csv file

~~~~~~~~~~~~~~~~~~~~~
will return an encrypted file and create an encrypted file in default directory.
'''


def encrypt_file(file_loc, passcode="*"):
    with open(file_loc, 'r') as inp_file:
        data = inp_file.read()
    encrypted_text = cipher.encrypt(data, passcode)
    file_loc = file_loc + ".encrypted"
    print(file_loc)
    with open(file_loc, 'wb') as out_file:
        out_file.write(encrypted_text)
    return encrypted_text


'''
Will return the decrypted file and create a decrypted file in default directory.
'''


def decrypt_file(file_loc, passcode="*"):
    if file_loc.endswith(".encrypted"):
        with open(file_loc, 'rb') as inp_file:
            data = inp_file.read()
        decrypted_text = cipher.decrypt(data, passcode)
        file_loc = file_loc.replace(".encrypted", "")
        with open(file_loc, 'w') as out_file:
            out_file.write(decrypted_text)
        return decrypted_text
    else:
        print("Wrong file")
        return "Input file not of correct format"

# Not necessary code below. Donot look.

# '''
# will return an encrypted string and rewrite the input file with encrypted file.
# '''
# def encrypt_txt_ow(file_loc,passcode="*"):
#     with open(file_loc, 'r') as inp_file:
#         data = inp_file.read()
#     encrypted_text = encrypt(data,passcode)
#     with open(file_loc, 'wb') as out_file:
#         out_file.write(encrypted_text)
#     return (encrypted_text)
#
# '''
# Will return the decrypted text and create a decrypted textfile in default directory.
# '''
# def decrypt_txt_ow(file_loc, passcode="*"):
#     with open(file_loc, 'rb') as inp_file:
#         data = inp_file.read()
#     decrypted_text = decrypt(data,passcode)
#     with open(file_loc,'w') as out_file:
#         out_file.write(decrypted_text)
#     return (decrypted_text)
