import string, pprint, sys

def getWordPattern(word):
    word = word.upper()
    nextNum = 0
    letterNums = {}
    wordPattern = []

    for letter in word:
        if letter in letterNums:
            wordPattern.append(str(letterNums[letter]))
        else:
            wordPattern.append(str(nextNum))
            letterNums[letter] = nextNum
            nextNum += 1
    return '.'.join(wordPattern)

def main():

    allPatterns = {}
    print('Calculating patterns...')

    fp = open('wiktionary.txt')
    content = fp.readlines()
    fp.close()

    counter = 0
    for line in content:
        line = line.strip()
        pattern = getWordPattern(line)

        if pattern not in allPatterns:
            allPatterns[pattern] = [line]
        else:
            allPatterns[pattern].append(line)
        counter = counter + 1

    print('%s words found in the dictionary.' % counter)
    print('Writing dictionary_patterns.py file...')
    fp = open('dictionary_patterns.py', 'w')
    fp.write('allPatterns = ')
    fp.write(pprint.pformat(allPatterns))
    fp.close()
    print('Done.')


if __name__ == '__main__':
    main()
