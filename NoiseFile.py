import FileHandler
from Encryption import Encryption
import secrets
import random
import hashlib
class NoiseFile:
    """Class that is used to generate noise files

    This class is standalone to prevent circular imports of Encryption and File"""
    @staticmethod
    def generate_noise_file(number_of_files =secrets.randbelow(11) + 40) -> None:
        """Creates files of random length with noise that looks the same as actual user data
        :param number_of_files: int, default secrets.randbelow(11)+40
        """

        alphabet = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ """
        for file_iterator in range(number_of_files):
            random.seed(secrets.token_hex())
            shuffled = ''.join(random.sample(alphabet, len(alphabet)))
            false_rotation = secrets.randbelow(94) + 1
            false_salt = secrets.randbelow(100)
            false_salt = str("{:04d}".format(false_rotation * false_salt)) + str("{:02d}".format(false_salt))
            false_title = hashlib.sha3_512(secrets.token_hex().encode()).hexdigest()
            false_header = "".join([shuffled[(shuffled.find(c) + false_rotation) % 95] for c in false_title])
            f = FileHandler.File(false_title, false_header + false_salt)
            for line_iterator in range(random.randrange(1, 100)):
                website = "http://" + Encryption.generate(random.randrange(11, 23), False) + ".com"
                username = Encryption.generate(random.randrange(5, 15), False)
                password = Encryption.generate(random.randrange(8, 20), False)
                line = website + ", " + username + ", " + password
                false_rotation = secrets.randbelow(94) + 1
                false_salt = secrets.randbelow(100)
                encoded = "".join([alphabet[(alphabet.find(c) + false_rotation) % 95] for c in line])
                false_salt = str("{:04d}".format(false_rotation * false_salt)) + str("{:02d}".format(false_salt))
                f.append_file(encoded + false_salt)