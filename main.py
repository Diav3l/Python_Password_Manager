import FileHandler
import Encryption
import hashlib
import os

"""
Password manager that uses variable ROT encryption and alphabet rotation derived 
from md5 hashing and stacking your password 1 million times
"""
__author__ = "Diavel"


def generate(string: str) -> str:
    criteria = string.split(':')
    if len(criteria) >= 3 and len(criteria[2]) > 0 and criteria[1].isdigit():
        return Encryption.Encryption.generate(int(criteria[1]), criteria[2] == "True")
    elif len(criteria) >= 2 and len(criteria[1]) > 0 and criteria[1].isdigit():
        return Encryption.Encryption.generate(int(criteria[1]))
    else:
        return Encryption.Encryption.generate()


def add() -> None:
    # added newline character because unlike to_array, input does not add a new line.
    criteria = "Enter username and password is the format (Website, Username, Password) \n" \
               "If password typed is Gen:{int}:{bool} a password will be generated at length\n" \
               "Enter q to return:\n"
    userinput = input(criteria).split(', ')
    if userinput[0].lower() == "q":
        return
    if len(userinput) < 3 or len(userinput[2]) <= 0:
        print("Please enter info as (Website, Username, Password)")
        add()  # reruns the add function if the length is wrong
        return
    else:
        if userinput[2].__contains__("Gen"):
            userinput[2] = generate(userinput[2])
        f.append_file(Encryptor.encrypt(userinput[0].lower() + ", " + userinput[1] + ", " + userinput[2]))


def delete() -> None:
    if not f.to_array():
        print("File is empty")
        return
    user_input = input("enter the index of the entry you want to delete_line, enter q to return:\n")
    if user_input == 'q' or user_input == 'Q':
        return
    elif user_input == "1":
        print("Cannot delete_line verify hash")
        return
    try:
        f.delete_line(int(user_input))
    except ValueError:
        print("please enter integer")
        delete()


def printall() -> None:
    index = 1
    for line in f.to_array():
        print(str(index) + ": " + Encryptor.decrypt(line))
        index += 1


def verify_login() -> bool:
    if not os.path.exists(f.filename):
        return True
    elif Encryptor.verify_hash.hexdigest() == Encryptor.decrypt(f.to_array()[0]).rstrip() and os.path.exists(f.filename):
        return True
    else:
        return False


def change_password() -> None:
    old_password_hash = Encryption.Encryption.stack(hashlib.sha3_512(input("Old Password: ").encode())).hexdigest()
    if not old_password_hash == Encryptor.decrypt(f.to_array()[0]).rstrip():
        print("Old password is incorrect")
        change_password()
        return
    new = hashlib.sha3_512(input("New Password: ").encode())
    confirm_new = hashlib.sha3_512(input("Confirm New Password: ").encode())
    if not new.hexdigest() == confirm_new.hexdigest():
        print("new passwords do not match")
        change_password()
        return
    encrypted_file = f.to_array()
    plaintext = []
    for line in encrypted_file:
        plaintext.append(Encryptor.decrypt(line))
    plaintext[0] = Encryption.Encryption.stack(new).hexdigest()
    ciphertext = []
    temp_encryptor = Encryption.Encryption(new)
    for line in plaintext:
        ciphertext.append(temp_encryptor.encrypt(line))
    f.write_file(ciphertext)
    del plaintext


def main():
    menu = "Add entry................a\n" \
            "Print all entries........p\n" \
            "Delete password entry....d\n" \
            "Change password..........c\n" \
            "Generate noise files.....g\n" \
            "Quit and close program...q\n:"
    while True:
        match input(menu).lower():
            case "a":
                add()
            case "d":
                delete()
            case "p":
                printall()
            case "q":
                break
            case "c":
                change_password()
                break
            case "g":
                Encryption.Encryption.generate_noise(int(input("Number of Files: ")))
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
