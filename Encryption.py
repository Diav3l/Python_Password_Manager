import hashlib
import secrets
import random


class Encryption:
    """uses variable ROT encryption and alphabet rotation derived from sha3_512 hashing and stacking the users password """

    def __init__(self, hashedPassword):
        """Generates a unique character list based on the given string"""
        # Do not ever modify the below string, it will prevent proper decryption and all data will be lost
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_-=|\}]{[\"':;?/>.<, "
        for i in range(500000):
            hashedPassword = hashlib.sha3_512(hashedPassword.digest() + hashedPassword.digest())
        random.seed(hashedPassword.digest())
        for i in range(500000):
            hashedPassword = hashlib.sha3_512(hashedPassword.digest() + hashedPassword.digest())
        self.charSet = ''.join(random.sample(alphabet, len(alphabet)))
        self.verify_hash = hashedPassword

    def encrypt(self, string: str) -> str:
        """:returns ciphertext of given plaintext"""
        rotation = secrets.randbelow(len(self.charSet))
        Salt = secrets.randbelow(100)
        encoded = "".join([self.charSet[(self.charSet.find(c) + rotation) % len(self.charSet)] for c in string])
        return encoded + str("{:04d}".format(rotation * Salt)) + str("{:02d}".format(Salt))

    def decrypt(self, string: str) -> str:
        """:returns plaintext of given ciphertext"""
        rotation = int(string[-6:-2]) // int(string[-2:])
        actual = string[:-6]
        return "".join([self.charSet[(self.charSet.find(c) - rotation) % len(self.charSet)] for c in actual])

    @staticmethod
    def generate(length=30, special_characters=True) -> str:
        """:returns a unique password of chosen length"""
        if special_characters:
            return str(secrets.token_bytes(length))[1:length+1]
        else:
            return secrets.token_hex(length)[:length]

    @staticmethod
    def stack(string):
        for i in range(1000000):
            string = hashlib.sha3_512(string.digest() + string.digest())
        return string
