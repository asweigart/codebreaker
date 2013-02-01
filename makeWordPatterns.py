# Makes the wordPatterns.py File
# http://inventwithpython.com/hacking (BSD Licensed)

# Create wordPatterns.py based on the words in our dictionary
# text file, dictionary.txt. (Download this file from
# http://invpy.com/dictionary.txt)

import pprint


def getWordPattern(word):
    # Returns a string of the pattern form of the given word.
    # e.g. '0.1.2.3.4.1.2.3.5.6' for 'DUSTBUSTER'
    word = word.upper()
    nextNum = 0
    letterNums = {}
    wordPattern = []

    for letter in word:
        if letter not in letterNums:
            letterNums[letter] = str(nextNum)
            nextNum += 1
        wordPattern.append(letterNums[letter])
    return '.'.join(wordPattern)


def main():
    allPatterns = {}

    fp = open('dictionary.txt')
    wordList = fp.read().split('\n')
    fp.close()

    for word in wordList:
        # Get the pattern for each word in wordList.
        pattern = getWordPattern(word)

        if pattern not in allPatterns:
            allPatterns[pattern] = [word]
        else:
            allPatterns[pattern].append(word)

    # This is code that writes code. The wordPatterns.py file contains
    # one very, very large assignment statement.
    fp = open('wordPatterns.py', 'w')
    fp.write('allPatterns = ')
    fp.write(pprint.pformat(allPatterns))
    fp.close()


if __name__ == '__main__':
    main()