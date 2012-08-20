# Transposition Cipher Breaker
# http://inventwithpython.com/codebreaker (BSD Licensed)

import math, re, sys, time, os, sys

inputFilename = 'frankenstein.encrypted.txt'
outputFilename = 'frankenstein.decrypted.txt'

dictionaryFile = open('dictionary.txt')
englishWords = {}
for word in dictionaryFile.read().split('\n'):
    englishWords[word] = None
#englishWords = dictionaryFile.read().split('\n') # 507 seconds
dictionaryFile.close()

def main():
    if not os.path.exists(inputFilename):
        print('The file %s does not exist. Quitting...' % (inputFilename))
        sys.exit()

    inputFile = open(inputFilename)
    content = inputFile.read()
    inputFile.close()

    brokenMessage = breakTransposition(content)
    print('Writing broken file to %s:' % (outputFilename))

    outputFile = open(outputFilename, 'w')
    outputFile.write(brokenMessage)
    outputFile.close()



# The decryptMessage() function's code was copy/pasted from
# transpositionDecrypt.py with the comments removed.
def decryptMessage(key, message):
    numOfColumns = math.ceil(len(message) / key)
    numOfRows = key
    numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)

    plaintext = [''] * numOfColumns

    col = 0
    row = 0
    for i in range(len(message)):
        plaintext[col] += message[i]
        col += 1
        if (col == numOfColumns) or (col == numOfColumns - 1 and row >= numOfRows - numOfShadedBoxes):
            col = 0
            row += 1
    return ''.join(plaintext)


# The getEnglishCount() function's code was copy/pasted from transpositionBreaker.py
def getEnglishCount(message):
    message = message.lower()
    message = re.sub('[^a-z\s]', '', message)
    words = message.split()
    matches = 0
    for word in words:
        if word in englishWords:
            matches += 1
    return matches / len(words)


# The isEnglish() function's code was copy/pasted from transpositionBreaker.py
def isEnglish(message, thresholdPercent):
    if englishWords == None:
        loadDictionary('dictionary.txt')
    return (100 * getEnglishCount(message)) >= thresholdPercent


# The breakTransposition() function's code was copy/pasted from
# transpositionBreaker.py and had some modifications made.
def breakTransposition(message):
    print('Breaking...')
    # Python programs can be stopped at any time by pressing Ctrl-C (on
    # Windows) or Ctrl-D (on Mac and Linux)
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')

    for key in range(1, len(message)):
        print('Trying key #%s... ' % (key), end='')
        sys.stdout.flush()

        # We want to track the amount of time it takes to test a single key,
        # so we record the time in startTime.
        startTime = time.time()

        decryptedText = decryptMessage(key, message)
        englishPercentage = round(getEnglishCount(decryptedText) * 100, 2)

        print('Key test time: %s seconds, ' % (round(time.time() - startTime, 3)), end='')
        sys.stdout.flush()

        print('Percent English: %s%%' % (round(getEnglishCount(decryptedText) * 100, 2)))
        if isEnglish(decryptedText, 20):
            print()
            print('Key ' + str(key) + ': ' + decryptedText[:100])
            print()
            print('Enter D for done, or just press Enter to continue:')
            response = input('> ')
            if response.upper().startswith('D'):
                return decryptedText


if __name__ == '__main__':
    main()
