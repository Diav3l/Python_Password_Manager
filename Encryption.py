import hashlib
import secrets
import random


class Encryption:

    """Prompts user for password; hashes and stacks password"""
    def __init__(self):
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_-=|\}]{[\"':;?/>.<, "
        hashed = hashlib.md5(input("Input password: ").encode())
        for i in range(1000000):
            hashed = hashlib.md5(hashed.digest() + hashed.digest())
        random.seed(hashed.digest())
        self.charSet = ''.join(random.sample(alphabet, len(alphabet)))

    def encrypt(self, string: str):
        rotation = secrets.randbelow(len(self.charSet))
        Salt = secrets.randbelow(100)
        encoded = "".join([self.charSet[(self.charSet.find(c) + rotation) % len(self.charSet)] for c in string])
        return encoded + str("{:04d}".format(rotation * Salt)) + str("{:02d}".format(Salt))

    def decrypt(self, string: str):
        rotation = int(string[-6:-2]) // int(string[-2:])
        actual = string[:-6]
        return "".join([self.charSet[(self.charSet.find(c) - rotation) % len(self.charSet)] for c in actual])
