from encryption.aes_implementation import *

# file_loc_1 = "sample_input/sample_text.txt"

'''
will return an encrypted string and create an encrypted textfile in default directory.
'''
def encrypt_txt(file_loc,passcode="*"):
    with open(file_loc, 'r') as inp_file:
        data = inp_file.read()
    encrypted_text = encrypt(data,passcode)
    with open("encrypted_text.txt", 'wb') as out_file:
        out_file.write(encrypted_text)
    return (encrypted_text)

'''
Will return the decrypted text and create a decrypted textfile in default directory.
'''
def decrypt_txt(file_loc, passcode="*"):
    with open(file_loc, 'rb') as inp_file:
        data = inp_file.read()
    decrypted_text = decrypt(data,passcode)
    with open("decrypted_text.txt",'w') as out_file:
        out_file.write(decrypted_text)

    return (decrypted_text)

'''
will return an encrypted string and rewrite the input file with encrypted file.
'''
def encrypt_txt_ow(file_loc,passcode="*"):
    with open(file_loc, 'r') as inp_file:
        data = inp_file.read()
    encrypted_text = encrypt(data,passcode)
    with open(file_loc, 'wb') as out_file:
        out_file.write(encrypted_text)
    return (encrypted_text)

'''
Will return the decrypted text and create a decrypted textfile in default directory.
'''
def decrypt_txt_ow(file_loc, passcode="*"):
    with open(file_loc, 'rb') as inp_file:
        data = inp_file.read()
    decrypted_text = decrypt(data,passcode)
    with open(file_loc,'w') as out_file:
        out_file.write(decrypted_text)
    return (decrypted_text)

# encrypt_txt_ow(file_loc_1)
# decrypt_txt_ow(file_loc_1)
