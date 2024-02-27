import FileHandler
import Encryption

"""
Password manager that uses variable ROT encryption and alphabet rotation derived 
from md5 hashing and stacking your password 1 million times
"""
__author__ = "Diavel"


def generate(string: str):
    criteria = string.split(':')
    if len(criteria) <= 2:
        return Encryption.Encryption.generate(int(criteria[1]))
    else:
        return Encryption.Encryption.generate(int(criteria[1]), criteria[2] == "True")


def add():
    # added newline character because unlike print, input does not add a new line.
    criteria = "Enter username and password is the format (Website, Username, Password) \n" \
               "if password typed is Gen:{int}:{bool} a password will be generated at length:\n"
    userinput = input(criteria).split(', ')
    if len(userinput) < 3 or len(userinput[2]) <= 0:
        print("Please enter info as (Website, Username, Password)")
        add()  # reruns the add function if the length is wrong
    else:
        if userinput[2].__contains__("Gen"):
            userinput[2] = generate(userinput[2])
        string = userinput[0].lower() + ", " + userinput[1] + ", " + userinput[2]
        f.appendFile(Encryptor.encrypt(string))


def delete():
    if not f.print():
        print("File is empty")
        return
    f.delete(int(input("enter the index of the entry you want to delete:\n")))


def printall():
    index = 1
    for line in f.print():
        print(str(index) + ": " + Encryptor.decrypt(line))
        index += 1


def main():
    while True:
        match input("Add, print, delete, or quit (a/p/d/q): ").lower():
            case "a":
                add()
            case "d":
                delete()
            case "p":
                printall()
            case "q":
                break
            case _:
                print("Invalid input")


if __name__ == "__main__":
    f = FileHandler.File()
    Encryptor = Encryption.Encryption()
    main()
