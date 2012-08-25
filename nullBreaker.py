# Null Cipher Breaker, http://inventwithpython.com/codebreaker (BSD Licensed)
import copy, time, nullCipher, pyperclip, transpositionBreaker

# There are two settings our breaking program needs to limit the range of the possible keys it checks.
# MAX_KEY_NUMBER is the range of numbers it checks for each number in the key. A MAX_KEY_NUMBER value of 9 means it will check the numbers 0 through 9.
# MAX_KEY_LENGTH is the largest amount of numbers in the key. A MAX_KEY_LENGTH value of 5 means that the key could be something like '1 2 3 4 5' or '1 1 1 1 1' or '1 2 3 4', but not '1 2 3 4 5 6'
# If these numbers are too large, then breaking the code will take a long time. If these numbers are too small, then the breaking program won't be able to break the encryption.
MAX_KEY_NUMBER = 9
MAX_KEY_LENGTH = 5

myMessage = 'kWhhbe#n n>IP uTksEe b<aZ wXCo(rdq7,( iActy moveeanggsU jCku2stmT dwhlvaPt FZIx czyhtoo(&sxe SUi6t Ylt#o 3kmCeaU5nb -rR-b nbLegitOTh6eroN Jmogzr2e Lgnpor/0 GleOjs.s.'
              #W h e n   I  u  s e   a  w  o rd  ,  i  t  m  eans just what I choose it to mean -- neither more nor less.

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
    for trialKeyLength in range(1, MAX_KEY_LENGTH + 1):
        # We will be using the "list of int values" for of keys. The string form like '4 2 3' that we use in the original encryption program is used just because it makes it easier to type for the user.
        # We use list replication (multiplying a list value by an int value) to get the starting key.
        trialKey = [0] * trialKeyLength

        trialKey = getNextKey(trialKey)

        while trialKey != [0] * trialKeyLength:
            decryptedText = nullCipher.decryptMessage(ciphertext, trialKey)
            percentEnglish = round(transpositionBreaker.getEnglishCount(decryptedText) * 100, 2)
            if percentEnglish > 0:
                print('Key %s decrypts to %s%% English.' % (trialKey, percentEnglish))
            if percentEnglish >= 25:
                print()
                print('Possible encryption break:')
                print('Key ' + str(trialKey) + ': ' + decryptedText[:100])
                print()
                print('Enter D for done, or just press Enter to continue breaking:')
                response = input('> ')

                if response.strip().upper().startswith('D'):
                    return decryptedText
            trialKey = getNextKey(trialKey)
    print('Failed to break encryption.')
    return None


if __name__ == '__main__':
    main()