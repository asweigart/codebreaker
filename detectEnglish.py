# Detect English module
# http://inventwithpython.com/codebreaker (BSD Licensed)

# To use, run:
#   import detectEnglish
#   detectEnglish.isEnglish(someString) # returns True or False
# (There must be a "dictionary.txt" file in this directory with all English
# words in it, one word per line.)
import re

dictionaryFile = open('dictionary.txt')
ENGLISH_WORDS = {}
for word in dictionaryFile.read().upper().split('\n'):
    ENGLISH_WORDS[word] = None
dictionaryFile.close()

nonLettersOrSpacePattern = re.compile('[^A-Z\s]')
nonLettersPattern = re.compile('[^A-Z]')
LETTTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    print('Testing the English detection module...')
    messages = ['The quick brown fox jumped over the yellow lazy dog.',
                'Hello there. lkjjfldsf dsafk alf ewfewlfjl efa',
                'Sumimasen. Kore wa nan desu ka?',
                '1100010110010111001011110000']
    for m in messages:
        print('%s\n\t%s\n' % (m, isEnglish(m)))


def getEnglishCount(message):
    # Returns the amount of words in message that appear in the dictionary.

    message = message.upper()

    # Use a "regular expression" to get rid of non-letters or spaces from the message.
    message = nonLettersOrSpacePattern.sub('', message)

    words = message.split()

    if not words:
        return False # after removing non-letters, message was blank

    # Go through each word and see how many are english words.
    matches = 0
    for word in words:
        # If the word exists in ENGLISH_WORDS, then increment the number of
        # matches by 1.
        if word in ENGLISH_WORDS:
            matches += 1

    # Return the fraction of matching words out of total words.
    return (matches / len(words))

def isEnglish(message, wordPercentage=20):
    # By default, 20% of the words must be recognized as English words that
    # exist in the dictionary file.
    wordPercentage /= 100


    # Get the percentage of recognized English words.
    englishWords = getEnglishCount(message)

    # Get the number of letters in the message.
    numLetters = len(nonLettersPattern.sub('', message.upper()))

    return (englishWords >= wordPercentage)

if __name__ == '__main__':
    main()