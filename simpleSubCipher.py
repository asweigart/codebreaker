# Simple Substitution Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import pyperclip, sys, random


LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    myMessage = 'If a man is offered a fact which goes against his instincts, he will scrutinize it closely, and unless the evidence is overwhelming, he will refuse to believe it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will accept it even on the slightest evidence. The origin of myths is explained in this way. -Bertrand Russell'
    myKey = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    myMode = 'encrypt' # set to 'encrypt' or 'decrypt'

    checkValidKey(myKey)

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)
    print('Using key %s' % (myKey))
    print('The %sed message is:' % (myMode))
    print(translated)
    pyperclip.copy(translated)
    print()
    print('This message has been copied to the clipboard.')


def checkValidKey(key):
    keyList = list(set(key))
    lettersList = list(LETTERS)
    keyList.sort()
    lettersList.sort()
    if keyList != lettersList or len(set(key)) != len(key):
        sys.exit('There is an error in the key or symbol set.')


def translateMessage(key, message, mode):
    translated = ''
    CHARS_A = LETTERS
    CHARS_B = key
    if mode == 'decrypt':
        # For decrypting, we can use the same code as encrypting. We
        # just need to swap where the key and LETTERS strings are used.
        CHARS_A, CHARS_B = CHARS_B, CHARS_A

    # loop through each symbol in the message
    for symbol in message:
        if symbol.upper() in CHARS_A:
            # encrypt/decrypt the symbol
            symIndex = CHARS_A.find(symbol.upper())
            if symbol.isupper():
                translated += CHARS_B[symIndex].upper()
            else:
                translated += CHARS_B[symIndex].lower()
        else:
            # symbol is not in LETTERS, just add it
            translated += symbol

    return translated


def encryptMessage(key, message):
    return translateMessage(key, message, 'encrypt')


def decryptMessage(key, message):
    return translateMessage(key, message, 'decrypt')


def getRandomKey():
    key = list(LETTERS)
    random.shuffle(key)
    return ''.join(key)


if __name__ == '__main__':
    main()