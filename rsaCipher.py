# RSA Cipher
# http://inventwithpython.com/codebreaker (BSD Licensed)

def main():
    # Runs a test that encrypts a message to a file or decrypts a message
    # from a file.
    filename = 'encrypted_file.txt'
    mode = 'decrypt' # set to 'encrypt' or 'decrypt'

    if mode == 'encrypt':
        message = '"Journalists belong in the gutter because that is where the ruling classes throw their guilty secrets." -Gerald Priestland "The Founding Fathers gave the free press the protection it must have to bare the secrets of government and inform the people." -Hugo Black'
        privKeyFilename = 'al_sweigart_privkey.txt'
        encryptedText = encryptAndWriteToFile(filename, privKeyFilename, message)

        print('Encrypted text:')
        print(encryptedText)

    elif mode == 'decrypt':
        pubKeyFilename = 'al_sweigart_pubkey.txt'
        decryptedText = readFromFileAndDecrypt(filename, pubKeyFilename)

        print('Decrypted text:')
        print(decryptedText)


def getBlocksFromText(message, blockSize=64):
    # Converts a string message to a list of block integers. Each integer
    # represents 64 (or whatever blockSize is set to) string characters.

    messageBytes = message.encode('ascii') # convert the string to bytes
    blockInts = []
    for blockStart in range(0, len(messageBytes), blockSize):
        # Calculate the block integer for this block of text
        blockInt = 0
        for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
            blockInt += int(messageBytes[i]) * (256 ** (i % blockSize))
        blockInts.append(blockInt)
    return blockInts


def getTextFromBlocks(blockInts, messageLength, blockSize=64):
    # Converts a list of block integers to the original message string. The
    # original message length is needed to properly convert the last block
    # integer.
    message = []
    for blockInt in blockInts:
        blockMessage = []
        for i in range(blockSize-1, -1, -1):
            # Decode the message string for the 64 (or whatever blockSize is
            # set to) characters from this block integer.
            charNumber = blockInt // (256 ** i)
            blockInt = blockInt % (256 ** i)
            blockMessage.insert(0, bytes([charNumber]).decode('ascii'))
        message.extend(blockMessage)
    return ''.join(message)


def encryptMessage(message, key):
    # Converts the message string into a list of block integers, and then
    # encrypt each block integer. Be sure to pass the PUBLIC key to encrypt.
    encryptedBlocks = []
    n, e = key
    for block in getBlocksFromText(message):
        # ciphertext = plaintext ^ e mod n
        encryptedBlocks.append(pow(block, e, n))
    return encryptedBlocks


def decryptMessage(encryptedBlocks, messageLength, key):
    # Decrypts a list of encrypted block ints into the original message
    # string. The original message length is required to properly decrypt
    # the last block. Be sure to pass the PRIVATE key to decrypt.
    decryptedBlocks = []
    n, d = key
    for block in encryptedBlocks:
        # plaintext = ciphertext ^ d mod n
        decryptedBlocks.append(pow(block, d, n))
    return getTextFromBlocks(decryptedBlocks, messageLength)


def readKeyFile(keyFilename):
    # Given the filename of a file that contains a public or private key,
    # return the key as a (n,e) or (n,d) tuple value.
    fp = open(keyFilename)
    content = fp.read()
    fp.close()
    key = content.split(',')
    return (int(key[0]), int(key[1]))


def encryptAndWriteToFile(messageFilename, keyFilename, message):
    # Using a key from a key file, encrypt the message and save it to a
    # file. Returns the encrypted message string.
    key = readKeyFile(keyFilename)

    # Encrypt the message
    encryptedBlocks = encryptMessage(message, key)

    # Convert the large int values to one string value.
    for i in range(len(encryptedBlocks)):
        encryptedBlocks[i] = str(encryptedBlocks[i])
    encryptedContent = ','.join(encryptedBlocks)

    # Write out the encrypted string to the output file.
    fp = open(messageFilename, 'w')
    fp.write('%s_%s' % (len(message), encryptedContent))
    fp.close()

    # Also return the encrypted string.
    return encryptedContent


def readFromFileAndDecrypt(messageFilename, keyFilename):
    # Using a key from a key file, read an encrypted message from a file
    # and then decrypt it. Returns the decrypted message string.
    key = readKeyFile(keyFilename)

    # Read in the message length and the encrypted message from the file.
    fp = open(messageFilename)
    content = fp.read()
    messageLength = int(content[:content.index('_')])
    message = content[content.index('_') + 1:]

    # Convert the encrypted message into large int values.
    encryptedBlocks = []
    for block in message.split(','):
        encryptedBlocks.append(int(block))

    # Decrypt the large int values.
    return decryptMessage(encryptedBlocks, messageLength, key)


if __name__ == '__main__':
    main()