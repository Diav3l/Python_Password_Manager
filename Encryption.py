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
    def stack(hashed_string: hashlib.sha3_512) -> hashlib.sha3_512:
        """:returns hash_string stacked 1 million times"""
        for i in range(1000000):
            hashed_string = hashlib.sha3_512(hashed_string.digest() + hashed_string.digest())
        return hashed_string

    @staticmethod
    def generate_noise(number_of_files: int):
        """Creates files of random length with noise that looks the same as actual user data"""
        import FileHandler
        alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_-=|\}]{[\"':;?/>.<, "
        i = len(alphabet)
        for file_iterator in range(number_of_files):
            random.seed(secrets.token_hex())
            shuffled = ''.join(random.sample(alphabet, len(alphabet)))
            false_rotation = secrets.randbelow(i)
            false_salt = secrets.randbelow(100)
            false_salt = str("{:04d}".format(false_rotation * false_salt)) + str("{:02d}".format(false_salt))
            false_title = hashlib.sha3_512(secrets.token_hex().encode()).hexdigest()
            false_header = "".join([shuffled[(shuffled.find(c) + secrets.randbelow(i)) % i] for c in false_title])
            f = FileHandler.File(false_title, false_header+false_salt)
            for line_iterator in range(random.randrange(1, 100)):
                length = random.randrange(40, 60)
                line = Encryption.generate(length, False)
                line = "".join([shuffled[(shuffled.find(c) + secrets.randbelow(i)) % i] for c in line])
                false_rotation = secrets.randbelow(i)
                false_salt = secrets.randbelow(100)
                false_salt = str("{:04d}".format(false_rotation * false_salt)) + str("{:02d}".format(false_salt))
                f.append_file(line+false_salt)
