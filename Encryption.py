import hashlib
import secrets
import random

__author__ = "Cole J Gordnier"

class Encryption:
    """uses variable ROT encryption and alphabet rotation derived from sha3_512 hashing and stacking the users password """

    def __init__(self, hashedPassword):
        """Generates a unique character list used for encryption based on the given string

        This means that the users password is the encryption and decryption key, therefore it is incredibly important
        that it is safeguarded because a lost password is a lost account and no recovery options are possible.
        """
        # Do not ever modify the below string, it will prevent proper decryption and all data will be lost
        alphabet = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
        for i in range(500000):
            hashedPassword = hashlib.sha3_512(hashedPassword.digest() + hashedPassword.digest())
        random.seed(hashedPassword.digest())
        for i in range(500000):
            hashedPassword = hashlib.sha3_512(hashedPassword.digest() + hashedPassword.digest())
        self.char_set = ''.join(random.sample(alphabet, len(alphabet)))
        self.verify_hash = hashedPassword

    def encrypt(self, string: str) -> str:
        """converts plaintext to ciphertext
        :returns ciphertext: str
        """
        rotation = secrets.randbelow(len(self.char_set) - 1) + 1
        Salt = secrets.randbelow(100)
        encoded = "".join([self.char_set[(self.char_set.find(c) + rotation) % len(self.char_set)] for c in string])
        return encoded + str("{:04d}".format(rotation * Salt)) + str("{:02d}".format(Salt))

    def decrypt(self, string: str) -> str:
        """Converts ciphertext of given plaintext
        :returns plaintext: str
        """
        rotation = int(string[-6:-2]) // int(string[-2:])
        actual = string[:-6]
        return "".join([self.char_set[(self.char_set.find(c) - rotation) % len(self.char_set)] for c in actual])

    @staticmethod
    def generate(length=30, special_characters=True) -> str:
        """Generates a unique password using pythons secrets librairy
        :param length: int, defaults to 30
        :param special_characters: bool, defaults to True
        :return password: str, of requested length and character usage
        """
        if special_characters:
            return str(secrets.token_bytes(length))[1:length+1]
        else:
            return secrets.token_hex(length)[:length]

    @staticmethod
    def stack(hashed_string: hashlib.sha3_512) -> hashlib.sha3_512:
        """Stacks the given string in a sha3_512 hash 1 million times
        :return hashed_string: _Hash
        """
        for i in range(1000000):
            hashed_string = hashlib.sha3_512(hashed_string.digest() + hashed_string.digest())
        return hashed_string
