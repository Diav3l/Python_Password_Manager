import FileHandler
import Encryption
import hashlib
import os

"""
Password manager that uses variable ROT encryption and alphabet rotation derived 
from md5 hashing and stacking your password 1 million times
"""
__author__ = "Diavel"


def generate(string: str):
    criteria = string.split(':')
    if len(criteria) >= 3 and len(criteria[2]) > 0 and criteria[1].isdigit():
        return Encryption.Encryption.generate(int(criteria[1]), criteria[2] == "True")
    elif len(criteria) >= 2 and len(criteria[1]) > 0 and criteria[1].isdigit():
        return Encryption.Encryption.generate(int(criteria[1]))
    else:
        return Encryption.Encryption.generate()


def add():
    # added newline character because unlike print, input does not add a new line.
    criteria = "Enter username and password is the format (Website, Username, Password) \n" \
               "If password typed is Gen:{int}:{bool} a password will be generated at length\n" \
               "Enter q to return:\n"
    userinput = input(criteria).split(', ')
    if userinput[0].lower() == "q":
        return
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
    user_input = input("enter the index of the entry you want to delete, enter q to return:\n")
    if user_input == 'q' or user_input == 'Q':
        return
    try:
        f.delete(int(user_input))
    except ValueError:
        print("please enter integer")
        delete()


def printall():
    index = 1
    for line in f.print():
        print(str(index) + ": " + Encryptor.decrypt(line))
        index += 1


def verify_login():
    if not os.path.exists(f.filename):
        return True
    elif Encryptor.verify_hash.hexdigest() == Encryptor.decrypt(f.print()[0]).rstrip() and os.path.exists(f.filename):
        return True
    else:
        return False


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
    while True:
        username_pointer = hashlib.sha3_512(input("Username: ").encode()).hexdigest()
        password_hash = hashlib.sha3_512(input("Input password: ").encode())
        Encryptor = Encryption.Encryption(password_hash)
        f = FileHandler.File(username_pointer, Encryptor.encrypt(Encryptor.verify_hash.hexdigest()))
        if not verify_login():
            print("Username or password is incorrect")
            continue
        main()
        print("Goodbye")
        break
