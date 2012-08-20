# Affine Cipher Breaker
# http://inventwithpython.com/codebreaker (BSD Licensed)
import pyperclip, affineCipher, detectEnglish

def main():
    myMessage = 'H RZPEDYBO NZDKW WBTBOIB YZ MB RHKKBW VUYBKKVLBUY VG VY RZDKW WBRBVIB H QDPHU VUYZ MBKVBIVUL YQHY VY NHT QDPHU. -HKHU YDOVUL'

    brokenCiphertext = breakAffine(myMessage.upper())

    if brokenCiphertext != None:
        # The plaintext is displayed on the screen. For the convenience of
        # the user, we copy the text of the code to the clipboard.
        print('Copying broken ciphertext to clipboard:')
        print(brokenCiphertext[:1000])
        pyperclip.copy(brokenCiphertext)
    else:
        print('Could not break this ciphertext.')


def breakAffine(message):
    print('Breaking...')

    # Python programs can be stopped at any time by pressing Ctrl-C (on
    # Windows) or Ctrl-D (on Mac and Linux)
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')

    # brute force by looping through every possible key
    for keyA in range(len(affineCipher.SYMBOLS)):
        if affineCipher.gcd(keyA, len(affineCipher.SYMBOLS)) != 1:
            continue

        for keyB in range(len(affineCipher.SYMBOLS)):
            decryptedText = affineCipher.decryptMessage(keyA, keyB, message)
            print('Tried KeyA %s, KeyB %s... (%s)' % (keyA, keyB, decryptedText[:40]))

            if detectEnglish.isEnglish(decryptedText):
                # Check with the user if the decrypted key has been found.
                print()
                print('Possible encryption break:')
                print('KeyA: %s, KeyB: %s' % (keyA, keyB))
                print('Decrypted message: ' + decryptedText[:100])
                print()
                print('Enter D for done, or just press Enter to continue breaking:')
                response = input('> ')

                if response.upper().startswith('D'):
                    return decryptedText
    return None

if __name__ == '__main__':
    main()