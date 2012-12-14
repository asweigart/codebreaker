# Null Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)

import nullCipher, pyperclip, detectEnglish, itertools

# There are two settings our hacking program needs to limit the range of
# the possible keys it checks.
# MAX_KEY_NUMBER is the range of numbers it checks for each number in the
# key. A MAX_KEY_NUMBER value of 9 means it will check 0 through 9.
# MAX_KEY_DIGITS is the largest amount of numbers in the key. A value of 5
# means that the key could be something like '1 2 3 4 5' or '1 1 1 1 1' or
# '1 2 3 4', but not '1 2 3 4 5 6'
# If these numbers are too large, then hacking the code will take a long
# time. If these numbers are too small, then the hacking program won't be
# able to hack the encryption.

MAX_KEY_NUMBER = 9
MAX_KEY_DIGITS = 5

SILENT_MODE = False

# This can be copy/pasted from http://invpy.com/nullHacker.py
myMessage = """sn Wht eetan mnIeu  uedswsae aiaeh  wh ohh rdrh,  h ihotote muoeh  annesets jtwunetst - e-rwhe am jt   Inoo c,nh   oossssace oai o t oWth.no   miiteaton r  -s -ou  nwse. nito hwiieroe s imoiorot e o nsesorer  anletesmt s.ah"""


def main():
    # Calculate the number of keys that the current MAX_KEY_DIGITS and
    # MAX_KEY_NUMBER values will cause the hacker program to go through.
    possibleKeys = 0 # start the number of keys at 0.
    for i in range(1, MAX_KEY_DIGITS + 1):
        # To find the total number of possible keys, add the total number
        # of keys for 1-digit keys, 2-digit keys, and so on up to
        # MAX_KEY_DIGITS-digit keys.
        # To find the number of keys with i digits in them, multiply the
        # range of numbers (that is, MAX_KEY_NUMBER) by itself i times.
        # That is, we find MAX_KEY_NUMBER to the ith power.
        possibleKeys += MAX_KEY_NUMBER ** i

    # After exiting the loop, the value in possibleKeys is the total number
    # of keys for MAX_KEY_NUMBER and MAX_KEY_RANGE.
    print('Max key number: %s' % MAX_KEY_NUMBER)
    print('Max key length: %s' % MAX_KEY_DIGITS)
    print('Possible keys to try: %s' % (possibleKeys))
    print()

    # Python programs can be stopped at any time by pressing Ctrl-C (on
    # Windows) or Ctrl-D (on Mac and Linux)
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')
    print('Hacking...')

    brokenMessage = hackNull(myMessage)

    if brokenMessage != None:
        print('Copying broken message to clipboard:')
        print(brokenMessage)
        pyperclip.copy(brokenMessage)
    else:
        print('Failed to hack encryption.')


def hackNull(ciphertext):
    # The program needs to try keys of length 1 (such as '5'), of length 2
    # (such as '5 3'), and so on up to length MAX_KEY_DIGITS.
    for keyLength in range(1, MAX_KEY_DIGITS + 1):
        for keyParts in itertools.product(range(MAX_KEY_NUMBER + 1), repeat=keyLength):
            key = []
            for digit in keyParts:
                key.append(str(digit))
            key = ''.join(key)

            decryptedText = nullCipher.decryptMessage(key, ciphertext)

            if not SILENT_MODE:
                print('Key %s: %s' % (key, decryptedText[:40]))

            if detectEnglish.isEnglish(decryptedText):
                print()
                print('Possible encryption hack:')
                print('Key: %s' % (key))
                print('Decrypted message: ' + decryptedText[:200])
                print()
                print('Enter D for done, or just press Enter to continue hacking:')
                response = input('> ')

                if response.strip().upper().startswith('D'):
                    return decryptedText
    return None # failed to hack encryption


if __name__ == '__main__':
    main()