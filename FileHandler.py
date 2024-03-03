import os


class File:

    """Creates file if it does not exist and add the users verify_hash at the top of the file"""
    def __init__(self, pointer: str, verify_hash:str):
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

    """adds entry to the bottom of the file"""
    def append_file(self, passwordEntry: str):
        with open(self.filename, 'a') as f:
            f.write(passwordEntry + "\n")

    """Replaces content of file with contents of given array"""
    def write_file(self, strings: list[str]):
        string = ''
        for line in strings:
            string += line+"\n"
        with open(self.filename, 'w') as f:
            f.write(string)

    """Return every entry in file as array"""
    def print(self):
        array = []
        with open(self.filename, 'r') as f:
            for line in f:
                array.append(line.rstrip())
        return array

    """Removes object from index"""
    def delete(self, line_to_remove: int):
        array = self.print()
        try:
            array.pop(line_to_remove-1)
        except IndexError:
            print("line is empty")
            return
        with open(self.filename, 'w') as f:
            for line in array:
                f.write(line+"\n")
