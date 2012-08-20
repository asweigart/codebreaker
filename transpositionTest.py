# Transposition Cipher Test
# http://inventwithpython.com/codebreaker (BSD Licensed)

import transpositionEncrypt, transpositionDecrypt, random, sys

random.seed(0) # set the random "seed"

for i in range(1, 21): # run 20 tests
    # Generate random messages to test.
    message = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' * random.randint(4, 40)
    message = list(message)
    random.shuffle(message)
    message = ''.join(message)

    print('Test #%s: "%s..."' % (i, message[:50]))

    # Check all possible keys for each message.
    for key in range(1, len(message)):
        encrypted = transpositionEncrypt.encryptMessage(key, message)
        decrypted = transpositionDecrypt.decryptMessage(key, encrypted)

        # If the decryption doesn't match the original message, display
        # an error message and quit.
        if message != decrypted:
            print('Mismatch with key %s and message %s.' % (key, message))
            print(decrypted)
            sys.exit()

print('Transposition cipher test passed.')
