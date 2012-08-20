# Caesar Cipher
# http://inventwithpython.com/codebreaker (BSD Licensed)

# the string to be encrypted/decrypted
message = 'This is my secret message.'

# the encryption/decryption key
key = 13

# tells the program to encrypt of decrypt
mode = 'encrypt' # set to 'encrypt' or 'decrypt'

# every possible symbol that can be encrypted
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# stores the encrypted/decrypted form of the message
translated = ''

# capitalize the string in message
message = message.upper()

# run the encryption/decryption code on each symbol in the message string
for symbol in message:
    # get the number of the symbol
    num = SYMBOLS.find(symbol)

    # -1 means the symbol in the message was not found in SYMBOLS
    if num != -1:
        # get the encrypted (or decrypted) number for this symbol
        if mode == 'encrypt':
           num = num + key
        elif mode == 'decrypt':
           num = num - key

        # handle the wrap around if num is larger than the length of SYMBOLS
        # or less than 0
        if num >= len(SYMBOLS):
            num = num - len(SYMBOLS)
        elif num < 0:
            num = num + len(SYMBOLS)

        # add encrypted/decrypted number's symbol at the end of translated
        translated = translated + SYMBOLS[num]

    else:
        # just add the symbol without encrypting/decrypting
        translated = translated + symbol

# print the encrypted/decrypted string to the screen
print(translated)
