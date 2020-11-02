"""
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

"""

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

'''
In AES, the password can only be of 16, 24 or 32 bytes.
So, we will use the SHA 256 to hash the key into a 32 byte value.
'''
# password = input("Enter Password")
# hash_obj = SHA256.new(password.encode('utf-8'))
# hkey = hash_obj.digest()

# Using a default password.


# hkey will be of 32 length.

BLOCK_SIZE = 16
PAD = '*'


def padding(x): return x + (BLOCK_SIZE - len(x) % BLOCK_SIZE) * PAD


# def unpad(s): return s[0:-ord(s[-1:])]


class AESCipher:

    def __init__(self, key='*'):
        self.key = key.encode('utf-8')
        # super().__init__()

    def encrypt(self, info):
        msg = padding(info)

        # password = passcode
        hash_obj = SHA256.new(self.key)
        hkey = hash_obj.digest()

        iv = Random.new().read(AES.block_size)
        aes_mode = AES.new(hkey, AES.MODE_CBC, iv)
        result = aes_mode.encrypt(msg.encode('utf-8'))

        # return base64.b64encode(result)
        return iv + result

    def decrypt(self, info):
        # msg = base64.b64decode(info)
        iv = info[:16]
        msg = info[16:]

        # password = passcode
        hash_obj = SHA256.new(self.key)
        hkey = hash_obj.digest()

        decipher = AES.new(hkey, AES.MODE_CBC, iv)
        decipher_text = decipher.decrypt(msg).decode('utf-8')

        pad_index = decipher_text.find(PAD)
        result = decipher_text[:pad_index]

        return result

# 7335f85d-05cf-486c-b323-30fd3e1637cd
# key to encrypt master key


cipher = AESCipher('password')
