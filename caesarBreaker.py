# Caesar Cipher Breaker
# http://inventwithpython.com/codebreaker (BSD Licensed)

message = 'GUVF VF ZL FRPERG ZRFFNTR.'
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# loop through every possible key
for key in range(len(SYMBOLS)):

    # It is important to set translated to the blank string so that the
    # previous iteration's value for translated is cleared.
    translated = ''

    # The rest of the program is the same as the original Caesar program:

    # run the encryption/decryption code on each symbol in the message string
    for symbol in message:
        # get the number of the symbol
        num = SYMBOLS.find(symbol)

        # -1 means the symbol in the message was not found in SYMBOLS
        if num != -1:

            num = num - key

            # handle the wrap around if num is 26 or larger of less than 0
            if num < 0:
                num = num + len(SYMBOLS)

            # add encrypted/decrypted number's symbol at the end of translated
            translated = translated + SYMBOLS[num]

        else:
            # just add the symbol without encrypting/decrypting
            translated = translated + symbol

    # display the current key being tested, along with its decryption
    print('Key #%s: %s' % (key, translated))
