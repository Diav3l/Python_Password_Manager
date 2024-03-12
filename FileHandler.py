import os


class File:
    """File handler class"""


    def __init__(self, pointer: str, verify_hash: str, user_file = False):
        """Creates file if it does not exist and add the users verify_hash at the top of the file

        This is used to create all files. If instantiation is tagged as a user file it creates noise files around the
        user file so that the user file is guaranteed to share a creation time with noise files. This prevents easy
        identification of user files. A random number of noise files are created on each side of the user file. This
        means that even after a user deletes their file the noise files still appear the same as user info, and
        contribute to security.

        :param pointer: str, is the filename
        :param verify_hash: str, is the first line of file
        :param user_file = False, if True creates noise file
        """
        if user_file:
            # see users manual for explanation *
            import Encryption
            import secrets
        self.filename = "UserData/"+pointer+".txt"
        if not os.path.isdir("UserData"):
            os.mkdir("UserData")
        if not os.path.exists(self.filename):
            if user_file:
                Encryption.Encryption.generate_noise(secrets.randbelow(11)+40)
            with open(self.filename, 'w') as f:
                f.write(verify_hash+"\n")
            if user_file:
                Encryption.Encryption.generate_noise(secrets.randbelow(11)+40)

    def append_file(self, passwordEntry: str) -> None:
        """Adds entry to the bottom of the file
        :param passwordEntry: str
        """
        with open(self.filename, 'a') as f:
            f.write(passwordEntry + "\n")

    def write_file(self, strings: list[str]) -> None:
        """Replaces content of file with contents of given array
        :param strings: list[str]
        """
        string = ''
        for line in strings:
            string += line+"\n"
        with open(self.filename, 'w') as f:
            f.write(string)

    def to_array(self) -> list[str]:
        """Copies the entire file to an array
        :return list[str] of every line in the file, removes new line characters
        """
        array = []
        with open(self.filename, 'r') as f:
            for line in f:
                array.append(line.rstrip())
        return array

    def delete_line(self, line_to_remove: int) -> None:
        """Deletes given line in range [1,∞)
        :param line_to_remove: int
        """
        array = self.to_array()
        try:
            array.pop(line_to_remove-1)
        except IndexError:
            print("line is empty")
            return
        with open(self.filename, 'w') as f:
            for line in array:
                f.write(line+"\n")

    def delete_file(self) -> None:
        """Deletes the users file"""
        os.remove(self.filename)

