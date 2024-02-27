import hashlib
import secrets
import random
"""Class that uses variable ROT encryption and alphabet rotation derived 
from md5 hashing and stacking your password 1 million times"""


class Encryption:

    """Prompts user for password; hashes and stacks password"""
    def __init__(self, hashedPassword):
        # Do not ever modify this string, it will prevent proper decryption and all data will be lost
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_-=|\}]{[\"':;?/>.<, "
        for i in range(1000000):
            hashedPassword = hashlib.md5(hashedPassword.digest() + hashedPassword.digest())
        random.seed(hashedPassword.digest())
        self.charSet = ''.join(random.sample(alphabet, len(alphabet)))

    """Encrypts the provided plaintext string to str(ciphertext)"""
    def encrypt(self, string: str):
        rotation = secrets.randbelow(len(self.charSet))
        Salt = secrets.randbelow(100)
        encoded = "".join([self.charSet[(self.charSet.find(c) + rotation) % len(self.charSet)] for c in string])
        return encoded + str("{:04d}".format(rotation * Salt)) + str("{:02d}".format(Salt))

    """Converts ciphertext back into plaintext"""
    def decrypt(self, string: str):
        rotation = int(string[-6:-2]) // int(string[-2:])
        actual = string[:-6]
        return "".join([self.charSet[(self.charSet.find(c) - rotation) % len(self.charSet)] for c in actual])

    """generates a unique password of chosen length"""
    @staticmethod
    def generate(length=30, special_characters=True):
        if special_characters:
            return str(secrets.token_bytes(length))[2:length+2]
        else:
            return secrets.token_hex(length)[:length]
