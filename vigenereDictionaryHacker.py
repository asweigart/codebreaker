# Vigenere Cipher Dictionary Hacker
# http://inventwithpython.com/codebreaker (BSD Licensed)

import detectEnglish, vigenereCipher

def main():
    ciphertext = ''

    fp = open('dictionary.txt')
    for word in fp.readline():
        word = word.upper().strip() # remove the newline at the end
        plaintext = vigenereCipher.decryptMessage(ciphertext, word)
        if detectEnglish.isEnglish(plaintext):
            # Check with the user to see if the decrypted key has been found.
            print()
            print('Possible encryption break:')
            print('Key ' + str(possibleKey) + ': ' + decryptedText[:100])
            print()
            print('Enter D for done, or just press Enter to continue breaking:')
            response = input('> ')

            if response.upper().startswith('D'):
                return decryptedText

    fp.close()



if __name__ == '__main__':
    main()