# Null Cipher
# http://inventwithpython.com/codebreaker (BSD Licensed)

import random, pyperclip

myMessage = 'When I use a word, it means just what I choose it to mean -- neither more nor less.'
myKey = '302'
mode = 'encrypt' # set to 'encrypt' or 'decrypt'

# The nulls will be randomly selected from this list of characters.
# Don't forget the space character at the start!
SYMBOLS = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

def main():
    if mode == 'encrypt':
        translated = encryptMessage(myMessage, myKey)
    elif mode == 'decrypt':
        translated = decryptMessage(myMessage, myKey)

    print('%sed message: ' % (mode.title()) + translated)
    print('The message has been copied to the clipboard.')
    pyperclip.copy(translated)


def encryptMessage(message, key):
    # The expression int(key[keyIndex]) will be used to decide how many
    # nulls should be inserted. For example, if key is the value '102' and
    # keyIndex is 0, then 1 null character will be inserted into the
    # ciphertext.
    keyIndex = 0

    ciphertext = '' # will contain the encrypted string
    for symbol in message:
        for dummy in range(int(key[keyIndex])):
            # A randomly-selected null symbol is appended to the end
            # of the ciphertext.
            ciphertext += random.choice(SYMBOLS)

        # Increment keyIndex so that on the next iteration, we use a
        # number of nulls specified by the next character in key.
        keyIndex += 1
        if keyIndex == len(key):
            # If keyIndex is past the last index of key (which is
            # len(key) - 1), then reset keyIndex back to 0.
            keyIndex = 0

        # Add the real symbol after adding the nulls.
        ciphertext += symbol

    # Add some more nulls after adding the last symbol. This way, a code
    # breaker cannot assume that the last symbol in the ciphertext is
    # always a part of the original message.
    for dummy in range(int(key[keyIndex])):
        ciphertext += random.choice(SYMBOLS)

    return ciphertext


def decryptMessage(message, key):
    # The value inside messageIndex will refer to the index we are
    # currently looking at in message.
    messageIndex = 0
    keyIndex = 0

    plaintext = '' # will contain the decrypted string

    while True:
        # The expression int(key[keyIndex]) will give us the int value of
        # how many nulls to skip over. We will move the value in
        # messageIndex by this amount.
        messageIndex += int(key[keyIndex])

        # If messageIndex is not past the last index in the message string
        # (the last index is len(message) - 1) then we are done decrypting
        # and should break out of the loop.
        if messageIndex >= len(message):
            break

        # Increment keyIndex so that on the next iteration, we
        # use a number of nulls specified by the next character in key.
        keyIndex += 1
        if keyIndex == len(key):
            keyIndex = 0

        # Append the symbol at messageIndex to the plaintext variable.
        plaintext += message[messageIndex]
        messageIndex += 1

    return plaintext


if __name__ == '__main__':
    main()