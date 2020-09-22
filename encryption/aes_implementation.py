'''
AES uses 16, 24 or 32 bytes.
1.Electronic Code Block.
~~~~~~~~~~~~~~~~~~~~~~
Main problem faced in this implementaion is similar text will have similar
cypher text.

2.Cypher Block Chaining Mode.
~~~~~~~~~~~~~~~~~~~~~~~~~~~
--> Break input into 16 bits.
--> If not 16 bits add a random sequence of chars to make 16 bits.

Step-1 : Pairing.
    If number of characters are in the input is not divisible by 16,
    a fixed string is appended to the string.
    Example:
        a = "Test Input"
        len(a) will be 10. So, its not 16.

        Code, to fix this.
        fixed_string = a + (16-len(msg)%16) * "*"
        Output:
            Test Input******

'''

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
'''
In AES, the password can only be of 16, 24 or 32 bytes.
So, we will use the SHA 256 to hash the key into a 32 byte value.
'''
password = input("Enter Password")
hash_obj = SHA256.new(password.encode('utf-8'))
hkey = hash_obj.digest()

# hkey will be of 32 length.
def encrypt(info):
    msg = info
    BLOCK_SIZE = 16
    PAD = '*'
    padding = lambda x:x+ (BLOCK_SIZE-len(x)%BLOCK_SIZE) * PAD
    cipher = AES.new(hkey, AES.MODE_ECB)
    result = cipher.encrypt(padding(msg).encode('utf-8'))
    return result

def decrypt(info):
    msg = info
    PAD = '*'
    decipher = AES.new(hkey,AES.MODE_ECB)
    decipher_text = decipher.decrypt(msg).decode('utf-8')
    pad_index = decipher_text.find(PAD)
    result = decipher_text[:pad_index]
    return result
# Encrypting my name.
print("Encrypted Text",encrypt("Subrat***"))
# Decrypting my name
print("Decrypted Text",decrypt(encrypt("Subrat***")))
