import os


class File:
    """File handler class, takes file name and first line of file arguments"""


    def __init__(self, pointer: str, verify_hash: str):
        """Creates file if it does not exist and add the users verify_hash at the top of the file"""
        self.filename = "UserData/"+pointer+".txt"
        try:
            open(self.filename, 'x')
            with open(self.filename, 'w') as f:
                f.write(verify_hash+"\n")
        except FileExistsError:
            pass
        except FileNotFoundError:
            os.mkdir("UserData")
            with open(self.filename, 'w') as f:
                f.write(verify_hash+"\n")


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

    def print(self) -> list[str]:
        """:returns every entry in file as array"""
        array = []
        with open(self.filename, 'r') as f:
            for line in f:
                array.append(line.rstrip())
        return array

    def delete(self, line_to_remove: int) -> None:
        """Deletes line with given number [1,∞)"""
        array = self.print()
        try:
            array.pop(line_to_remove-1)
        except IndexError:
            print("line is empty")
            return
        with open(self.filename, 'w') as f:
            for line in array:
                f.write(line+"\n")
