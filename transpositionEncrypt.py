# Transposition Cipher Encryption
# http://inventwithpython.com/codebreaker (BSD Licensed)

import math, pyperclip

def main():
    myMessage = 'Common sense is not so common.'
    myKey = 8

    translated = encryptMessage(myKey, myMessage)

    # Print the (encrypted) string in translated to the screen, with
    # a | (called "pipe" character) after it in case there are spaces at the
    # end of the encrypted message.
    print(translated + '|')

    # Copy the (encrypted) string in translated to the clipboard.
    pyperclip.copy(translated)


def encryptMessage(key, message):
    # Each string in ciphertext represents a column in the transposition grid.
    ciphertext = [''] * key

    # Loop through each column in ciphertext.
    for col in range(key):
        pointer = col

        # Keep looping until pointer goes past the length of the message.
        while pointer < len(message):
            # Place the character at pointer in message at the end of the
            # current column in the ciphertext list.
            ciphertext[col] += message[pointer]

            # move pointer over
            pointer += key

    # Convert the ciphertext list into a single string value and return it.
    return ''.join(ciphertext)

# If transpositionEncrypt.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()
