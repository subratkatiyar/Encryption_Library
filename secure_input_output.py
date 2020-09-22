from encryption.aes_implementation import *
# import string
def sinput(prompt = "", passcode = ""):
    secure_variable = encrypt(input(prompt), passcode)
    return (secure_variable)

def sprint(secure_variable, passcode = ""):
    deafult_string = decrypt(secure_variable,passcode)
    return (deafult_string)

# Use case Examplesn
a = sinput("Enter input: ","password")
print(type(a))
print("Encrypted Text is: ",a)
print("Decrypted Text is: ",sprint(a,"password"))
