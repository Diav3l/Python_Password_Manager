import os
import Encryption


class File:
    """File handler class, takes file name and first line of file arguments"""


    def __init__(self, pointer: str, verify_hash: str, user_file = False):
        """Creates file if it does not exist and add the users verify_hash at the top of the file

        :param pointer: str, is the filename
        :param verify_hash: str, is the first line of file
        :param user_file = False, if True creates noise file
        """
        self.filename = "UserData/"+pointer+".txt"
        if not os.path.isdir("UserData"):
            os.mkdir("UserData")
        if not os.path.exists(self.filename):
            if user_file:
                Encryption.Encryption.generate_noise(50)
            with open(self.filename, 'w') as f:
                f.write(verify_hash+"\n")
            if user_file:
                Encryption.Encryption.generate_noise(50)

    def append_file(self, passwordEntry: str) -> None:
        """Adds entry to the bottom of the file"""
        with open(self.filename, 'a') as f:
            f.write(passwordEntry + "\n")

    def write_file(self, strings: list[str]) -> None:
        """Replaces content of file with contents of given array"""
        string = ''
        for line in strings:
            string += line+"\n"
        with open(self.filename, 'w') as f:
            f.write(string)

    def to_array(self) -> list[str]:
        """:returns every entry in file as array"""
        array = []
        with open(self.filename, 'r') as f:
            for line in f:
                array.append(line.rstrip())
        return array

    def delete_line(self, line_to_remove: int) -> None:
        """Deletes given line in range [1,∞)"""
        array = self.to_array()
        try:
            array.pop(line_to_remove-1)
        except IndexError:
            print("line is empty")
            return
        with open(self.filename, 'w') as f:
            for line in array:
                f.write(line+"\n")
