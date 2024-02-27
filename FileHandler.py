class File:

    """Creates file if it does not exist"""
    def __init__(self, pointer: str):
        self.filename = "UserData/"+pointer+".txt"
        """
        this is in a try except because the 'x' argument throws an error if the file exists.
        But if the file exists no actions need to be taken. 
        This is one of the only times in python except pass is acceptable.
        """
        try:
            open(self.filename, 'x')
        except FileExistsError:
            pass

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
    def delete(self, lineToRemove: int):
        array = self.print()
        try:
            array.pop(lineToRemove-1)
        except IndexError:
            print("line is empty")
            return
        with open(self.filename, 'w') as f:
            for line in array:
                f.write(line+"\n")
