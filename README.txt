    This program uses a number of methods to protect user information theses include: using the users password to
scramble the character list used for ROT encryption,stacking the users password, Varying the rotation on ROT encryption
for each entry, naming the users file a hash of their username, and creating random noise files with the users file.

    ROT encryption is a symmetrical encryption process that simply moves each character on a string over a set number of
places along an alphabet string. Using the users password as a seed to scramble this string effectively prevents user
data from being decrypted without the password. Stacking the users password in a SHA3_512 hash lengthens the time taken
to process a password. The reason this is useful is it helps protect from a brute force attempt. Password strength or
entropy is measured with the equation L^S L= length of the password and S = the possible characters. Brute force time
required is password entropy multiplied by the time taken to process a single password. If it takes the user one second
to log in they won't notice, but it makes it incredibly difficult to brute force. The time taken to crack a password that
has 10 characters and uses special characters and capitals if it takes 1 second per attempt is (94^10)*1s = 1.7E12 years.
which is functionally impossible to brute force on modern computers.

    Naming the user file a hash of the username and creating noise files at the same time as user files prevents user
files from being easily identified by an attacker, and the update_noise method in main means that all files in the
UserData directory have the same time modified and the users actual file shares creation time with other files.
All of which have hashed names and a random number of lines.