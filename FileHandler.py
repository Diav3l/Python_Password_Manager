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
            open(self.filename, 'x')

    """adds entry to the bottom of the file"""
    def appendFile(self, passwordEntry):
        with open(self.filename, 'a') as f:
            f.write(passwordEntry + "\n")

    """Return every entry in file as array"""
    def print(self):
        array = []
        with open(self.filename, 'r') as f:
            for line in f:
                array.append(line.rstrip())
        return array

    """Removes object from index"""
    def delete(self, line_to_remove: int):
        if line_to_remove == 1:
            print("Cannot delete verify hash")
            return
        array = self.print()
        try:
            array.pop(line_to_remove-1)
        except IndexError:
            print("line is empty")
            return
        with open(self.filename, 'w') as f:
            for line in array:
                f.write(line+"\n")
