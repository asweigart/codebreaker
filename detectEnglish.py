# Detect English module
# http://inventwithpython.com/codebreaker (BSD Licensed)

# To use, run:
#   import detectEnglish
#   detectEnglish.isEnglish(someString) # returns True or False
# (There must be a "dictionary.txt" file in this directory with all English
# words in it, one word per line.)
import re

nonLettersOrSpacePattern = re.compile('[^A-Z\s]')
nonLettersPattern = re.compile('[^A-Z]')
LETTTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def loadDictionary(dictionaryFilename):
    dictionaryFile = open(dictionaryFilename)
    englishWords = {}
    for word in dictionaryFile.read().split('\n'):
        englishWords[word] = None
    dictionaryFile.close()
    return englishWords

ENGLISH_WORDS = loadDictionary('dictionary.txt')


def getEnglishCount(message):
    message = message.upper()
    message = re.sub('[^A-Z\s]', '', message)
    words = message.split()

    if not words:
        return False # no words at all, so return False

    matches = 0
    for word in words:
        if word in ENGLISH_WORDS:
            matches += 1
    return matches / len(words)


def isEnglish(message, wordPercentage=20, letterPercentage=67):
    # By default, 20% of the words must exist in the dictionary file, and
    # 67% of all the characters in the message must be letters (not
    # punctuation, spaces, or numbers).
    wordPercentage /= 100
    letterPercentage /= 100

    # Get the percentage of recognized English words.
    englishWords = getEnglishCount(message)

    # Get the number of letters in the message.
    numLetters = 0
    for symbol in message.upper():
        if symbol in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            numLetters += 1

    return (englishWords >= wordPercentage) and (numLetters / len(message) >= letterPercentage)