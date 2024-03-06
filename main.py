import FileHandler
import Encryption
import hashlib
import os

__author__ = "Cole J Gordnier"


def generate_password(string: str) -> str:
    """Handles user input to create a unique password given user criteria
    :returns str
    """
    criteria = string.split(':')
    if len(criteria) >= 3 and len(criteria[2]) > 0 and criteria[1].isdigit():
        return Encryption.Encryption.generate(int(criteria[1]), criteria[2] == "True")
    elif len(criteria) >= 2 and len(criteria[1]) > 0 and criteria[1].isdigit():
        return Encryption.Encryption.generate(int(criteria[1]))
    else:
        return Encryption.Encryption.generate()

def update_noise():
    """This method creates noise files with the same date and time as user files

    This method is a security measure that stops attackers from identifying the file that contains the users passwords.
    This file updates the datetime modified attribute of all files to be exactly the same, while the datetime created
    cannot be change noise files are created at the same time as user files, so they should already be identical.
    This prevents someone with access to the source files from identifying user created files.
    """
    import time
    for file in os.listdir("UserData"):
        file = os.path.join("UserData",file)
        os.utime(file,(time.time(),time.time()))



def add_entry() -> None:
    """Encrypts and adds new entry to users file"""
    criteria = "Enter username and password is the format (Website, Username, Password) \n" \
               "If password typed is Gen:{int}:{bool} a password will be generated at length\n" \
               "Enter q to return\n:"
    userinput = input(criteria).split(', ')
    if userinput[0].lower() == "q":
        return
    if len(userinput) < 3 or len(userinput[2]) <= 0:
        print("Please enter info as (Website, Username, Password)")
        add_entry()
        return
    else:
        if userinput[2].__contains__("Gen"):
            userinput[2] = generate_password(userinput[2])
        f.append_file(Encryptor.encrypt(userinput[0].lower() + ", " + userinput[1] + ", " + userinput[2]))


def delete_entry() -> None:
    """Deletes line from user file"""
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
        delete_entry()


def print_all_entries() -> None:
    """Decrypts and prints all user entries to the console"""
    index = 1
    for line in f.to_array():
        print(str(index) + ": " + Encryptor.decrypt(line))
        index += 1


def verify_login() -> bool:
    """Verifies that user provided the correct password"""
    if not os.path.exists(f.filename):
        return True
    elif Encryptor.verify_hash.hexdigest() == Encryptor.decrypt(f.to_array()[0]).rstrip() and os.path.exists(f.filename):
        return True
    else:
        return False


def change_password() -> None:
    """Changes the users password for encryption and decryption

    This method requires that the whole file be decrypted with the old key and re-encrypted with the new key.
    This means that for a very short amount of time the users file exists as plaintext in RAM, the variable containing
    the plaintext entries is deleted at the end of the method, and the user is logged out
    """
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

def delete_account():
    """Deletes account file"""
    pass


def main():
    menu = "Add entry................a\n" \
            "Print all entries........p\n" \
            "Delete password entry....d\n" \
            "Change password..........c\n" \
            "Quit and close program...q\n" \
            "Delete account.....delete\n:"
    while True:
        update_noise()
        match input(menu).lower():
            case "a":
                add_entry()
            case "d":
                delete_entry()
            case "p":
                print_all_entries()
            case "q":
                break
            case "c":
                change_password()
                break
            case "DELETE":
                print("not yet implemented")
            case _:
                print("Invalid input")
    update_noise()


if __name__ == "__main__":
    while True:
        username_pointer = hashlib.sha3_512(input("Username: ").encode()).hexdigest()
        password_hash = hashlib.sha3_512(input("Input password: ").encode())
        Encryptor = Encryption.Encryption(password_hash)
        f = FileHandler.File(username_pointer, Encryptor.encrypt(Encryptor.verify_hash.hexdigest()), True)
        if not verify_login():
            print("Username or password is incorrect")
            continue
        main()
        print("Goodbye")
        break
