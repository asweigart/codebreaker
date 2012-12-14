# Null Cipher
# http://inventwithpython.com/hacking (BSD Licensed)
import random, pyperclip

myMessage = """When I use a word, it means just what I choose it to mean -- neither more nor less."""
myKey = '302'
mode = 'encrypt' # set to 'encrypt' or 'decrypt'


def main():
    if mode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif mode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('%sed message: ' % (mode.title()) + translated)
    print('The message has been copied to the clipboard.')
    pyperclip.copy(translated)


def encryptMessage(key, message):
    # The expression int(key[keyIndex]) will be used to decide how many
    # nulls should be inserted. For example, if key is the value '570'
    # and keyIndex is 0, then 5 null characters will be inserted into
    # the ciphertext.
    keyIndex = 0

    ciphertext = '' # will contain the encrypted string
    for symbol in list(message) + [None]:
        for dummy in range(int(key[keyIndex])):
            # Add a null.
            ciphertext += random.choice(myMessage)

        if symbol == None:
            break # the None value marks the end

        # Increment keyIndex so that on the next iteration, we use a
        # number of nulls specified by the next character in key.
        keyIndex += 1
        if keyIndex == len(key):
            # keyIndex is past the end, so reset it back to 0.
            keyIndex = 0

        # Add the real symbol after adding the nulls.
        ciphertext += symbol
    return ciphertext


def decryptMessage(key, message):
    # The value inside messageIndex will refer to the index we are
    # currently looking at in message.
    messageIndex = 0
    keyIndex = 0

    plaintext = '' # will contain the decrypted string

    while True:
        # The expression int(key[keyIndex]) will give us the int value of
        # how many nulls to skip over. We will increment the value in
        # messageIndex by this amount.
        messageIndex += int(key[keyIndex])

        if messageIndex >= len(message):
            # When messageIndex is past the last index, we are done.
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