# Simple Substitution Keyword Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

import pyperclip, simpleSubCipher

def main():
    myMessage = r"""Your cover is blown."""
    myKey = 'alphanumeric'
    myMode = 'encrypt' # set to 'encrypt' or 'decrypt'


    print('The key used is:')
    print(makeSimpleSubKey(myKey))

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('The %sed message is:' % (myMode))
    print(translated)

    pyperclip.copy(translated)
    print()
    print('This message has been copied to the clipboard.')


def encryptMessage(key, message):
    key = makeSimpleSubKey(key)
    return simpleSubCipher.encryptMessage(key, message)


def decryptMessage(key, message):
    key = makeSimpleSubKey(key)
    return simpleSubCipher.decryptMessage(key, message)


def makeSimpleSubKey(keyword):
    # create the key from the keyword
    newKey = ''
    keyword = keyword.upper()
    keyAlphabet = list(simpleSubCipher.LETTERS)
    for i in range(len(keyword)):
        if keyword[i] not in newKey:
            newKey += keyword[i]
            keyAlphabet.remove(keyword[i])
    key = newKey + ''.join(keyAlphabet)
    return key


if __name__ == '__main__':
    main()