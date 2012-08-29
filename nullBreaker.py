# Null Cipher Breaker
# http://inventwithpython.com/codebreaker (BSD Licensed)

import nullCipher, pyperclip, detectEnglish, itertools

# There are two settings our breaking program needs to limit the range of the possible keys it checks.
# MAX_KEY_NUMBER is the range of numbers it checks for each number in the key. A MAX_KEY_NUMBER value of 9 means it will check the numbers 0 through 9.
# MAX_KEY_LENGTH is the largest amount of numbers in the key. A MAX_KEY_LENGTH value of 5 means that the key could be something like '1 2 3 4 5' or '1 1 1 1 1' or '1 2 3 4', but not '1 2 3 4 5 6'
# If these numbers are too large, then breaking the code will take a long time. If these numbers are too small, then the breaking program won't be able to break the encryption.
MAX_KEY_NUMBER = 9
MAX_KEY_LENGTH = 5

SILENT_MODE = False

myMessage = """y\ZWh,De,. n #{ItZ9 uL<sl6!e 2&a"\B w{Eo;l#rdvK,9\s i.Xt?WC mQ-ef>yanpushOz j9lu_H4stsd .Bawhmua_ogt <`I#w$ ctoh({'oo={sINUe 84i%G3t NLt2#Wo 7Zm*<^eacUnuG6 -=g-f:! nxQe$Qmit&Ah0#ner:O Gt!moc;rXGUe q/nKrgor"\ 9 \lecBs|10s.9i"""
#                 Wh  e   n   I    u  s   e   a    w  o   rd  ,    i  t    m  e   an  s    j  u   st      wh  a   t   I    c  h   oo  s   e   i   t   t   o   m   ea  n    -  -    n  e   it  h   er      mo  r   e   n   or      le  s   s.

def main():
    # As a convenience to the user, we will calculate the number of keys that the current MAX_KEY_LENGTH and MAX_KEY_NUMBER settings will cause the breaker program to go through.
    possibleKeys = 0 # start the number of keys at 0.
    for i in range(1, MAX_KEY_LENGTH + 1):
        # In order to find the total number of possible keys, we need to add the total number of keys of 1 number, of 2 numbers, of 3 numbers, and so on up to MAX_KEY_LENGTH numbers.
        # To find the number of keys with i numbers in them, we multiply the range of numbers (that is, MAX_KEY_NUMBER) by itself i times. That is, we find MAX_KEY_NUMBER to the ith power.
        possibleKeys += MAX_KEY_NUMBER ** i

    # After exiting the loop, the value in possibleKeys is the total number of keys for MAX_KEY_NUMBER and MAX_KEY_RANGE. We then print this data to the user.
    print('Max key number: %s' % MAX_KEY_NUMBER)
    print('Max key length: %s' % MAX_KEY_LENGTH)
    print('Possible keys to try: %s' % (possibleKeys))
    print()

    # Python programs can be stopped at any time by pressing Ctrl-C (on Windows) or Ctrl-D (on Mac and Linux)
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')
    print('Breaking...')

    # The breakNull() function will have all the encryption breaking code in it, and return the original plaintext.
    brokenMessage = breakNull(myMessage)

    if brokenMessage != None:
        # The plaintext is displayed on the screen. For the convenience of the user, we copy the text of the code to the clipboard.
        print('Copying broken message to clipboard:')
        print(brokenMessage)
        pyperclip.copy(brokenMessage)
    else:
        print('Failed to break encryption.')


def breakNull(ciphertext):
    # The program needs to try keys of length 1 (such as '5'), of length 2 (such as '5 5'), and so on up to length MAX_KEY_LENGTH.
    # This is because the key '1 0' will decrypt differently than '1 0 0'.
    for keyLength in range(1, MAX_KEY_LENGTH + 1):
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
                print('Possible encryption break:')
                print('Key: %s' % (key))
                print('Decrypted message: ' + decryptedText[:200])
                print()
                print('Enter D for done, or just press Enter to continue breaking:')
                response = input('> ')

                if response.strip().upper().startswith('D'):
                    return decryptedText
    return None # failed to break encryption


if __name__ == '__main__':
    main()