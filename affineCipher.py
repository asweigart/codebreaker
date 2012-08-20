# Affine Cipher
# http://inventwithpython.com/codebreaker (BSD Licensed)
import sys, random, pyperclip

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    message = 'A COMPUTER WOULD DESERVE TO BE CALLED INTELLIGENT IF IT COULD DECEIVE A HUMAN INTO BELIEVING THAT IT WAS HUMAN. -ALAN TURING'
    keyA, keyB = 5, 7
    mode = 'encrypt' # set to 'encrypt' or 'decrypt'

    message = message.upper()

    if keyA == 1:
        sys.exit('The affine cipher becomes incredibly weak when keyA is set to 1. Choose a different key.')
    if keyB == 0:
        sys.exit('The affine cipher becomes incredibly weak when keyB is set to 0. Choose a different key.')
    if gcd(keyA, len(SYMBOLS)) != 1:
        sys.exit('The key (%s) and the size of the alphabet (%s) are not relatively prime. Choose a different key.' % (key, len(SYMBOLS)))

    print('Original text:')
    print(message)

    if mode == 'encrypt':
        translated = encryptMessage(keyA, keyB, message)
    elif mode == 'decrypt':
        translated = decryptMessage(keyA, keyB, message)

    print('%sed text:' % (mode.title()))
    print(translated)
    pyperclip.copy(translated)
    print('%sed text copied to clipboard.' % (mode.title()))


def gcd(a, b):
    # Return the Greatest Common Divisor of a and b.
    while a != 0:
        a, b = b % a, a
    return b


def findModInverse(a, m):
    for b in range(m):
        if (a * b) % m == 1:
            return b
    return None # None is returned only when gcd(a, m) == 1, which is invalid.


def encryptMessage(keyA, keyB, message):
    ciphertext = ''
    for symbol in message:
        symIndex = SYMBOLS.find(symbol)
        if symIndex != -1:
            # encrypt this symbol
            ciphertext += SYMBOLS[(symIndex * keyA + keyB) % len(SYMBOLS)]
        else:
            # just append this symbol unencrypted
            ciphertext += symbol
    return ciphertext


def decryptMessage(keyA, keyB, message):
    plaintext = ''
    modInverseOfKeyA = findModInverse(keyA, len(SYMBOLS))

    for symbol in message:
        symIndex = SYMBOLS.find(symbol)
        if symIndex != -1:
            # decrypt this symbol
            plaintext += SYMBOLS[(symIndex - keyB) * modInverseOfKeyA % len(SYMBOLS)]
        else:
            # just append this symbol unencrypted
            plaintext += symbol
    return plaintext


if __name__ == '__main__':
    main()