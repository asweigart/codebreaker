# Simple Substitution Cipher Breaker
# http://inventwithpython.com/codebreaker (BSD Licensed)

"""
In this program, a "word pattern" is a description of which letters are
repeated in a word. A word pattern is a series of numbers delimited by periods.
The first letter to appear in the word is assigned 0, the second letter 1, and
so on. So the word pattern for 'cucumber' is '0.1.0.1.2.3.4.5' because the
first letter 'c' occurs as the first and third letter in the word 'cucumber'.
So the pattern has '0' as the first and third number.

The pattern for 'abc' or 'cba' is '0.1.2'
The pattern for 'aaa' or 'bbb' is '0.0.0'
The pattern for 'hello' is '0.1.2.2.3'
The pattern for 'advise' or 'closet' is '0.1.2.3.4.5' (they have only unique
letters in the word)

In this program, a "candidate" is a possible English word that a ciphertext
work can decrypt to.
For example, 'cucumber', 'mementos', and 'cocoanut' are candidates for the
ciphertext word 'JHJHWDOV' (because all of them have the pattern
'0.1.0.1.2.3.4.5')

In this program, a "map" or "mapping" is a dictionary where the keys are the
letters in SYMBOLS (e.g. 'A', 'B', 'C', etc) and the values are lists of
letters that could possibly be the correct decryption. If the list is blank,
this means that it is unknown what this letter could decrypt to.
"""

# The import statement for wordPatterns is further down.
import os, sys, simpleSubCipher, re, copy

SYMBOLS = simpleSubCipher.SYMBOLS


def main():
    message = 'SY L NLX SR PYYACAO L YLWJ EISWI UPAR LULSXRJ ISR SXRJSXWJR, IA ESMM RWCTJSXSZA SJ WMPRAMH, LXO TXMARR JIA AQSOAXWA SR PQACEIAMNSXU, IA ESMM CAYTRA JP FAMSAQA SJ. SY, PX JIA PJIAC ILXO, IA SR PYYACAO RPNAJISXU EISWI LYYPCOR L CALRPX YPC LWJSXU SX LWWPCOLXWA JP ISR SXRJSXWJR, IA ESMM LWWABJ SJ AQAX PX JIA RMSUIJARJ AQSOAXWA. JIA PCSUSX PY NHJIR SR AGBMLSXAO SX JISR ELH. -FACJCLXO CTRRAMM'

    nonLettersPattern = re.compile('[^A-Z\s]')
    ciphertext = nonLettersPattern.sub('', message.upper()).split()

    # allCandidates is a dict with keys of a single ciphertext word, and
    # values of the possible word patterns
    # e.g. allCandidates == {'PYYACAO': ['alleged', 'ammeter', ...etc],
    #                        'EISWI': ['aerie', 'aging', 'algol', ...etc],
    #                        'LULSXRJ': ['abalone', 'abashed', ...etc],
    #                        ...etc }
    allCandidates = {}
    for cipherWord in ciphertext:
        pattern = getWordPattern(cipherWord)
        if pattern not in wordPatterns.allPatterns:
            continue
        allCandidates[cipherWord] = copy.copy(wordPatterns.allPatterns[pattern])

        # convert candidate words to uppercase
        for i in range(len(allCandidates[cipherWord])):
            allCandidates[cipherWord][i] = allCandidates[cipherWord][i].upper()

    # determine the possible valid ciphertext translations
    print('Breaking...')
    # Python programs can be stopped at any time by pressing Ctrl-C (on
    # Windows) or Ctrl-D (on Mac and Linux)
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')
    theMap = breakSimpleSub(getNewBlankMapping(), allCandidates)

    # display the results to the user.
    print('Done.')
    print()
    printMapping(ciphertext, theMap)
    print()
    print('Original ciphertext:')
    print(message)
    print()
    print('Broken ciphertext:')
    print(decryptWithMap(message, theMap))
    print()

def getWordPattern(word):
    # Returns a string of the pattern form of the given word.
    # e.g. '0.1.2.3.4.1.2.3.5.6' for 'DUSTBUSTER' or '0.1.2.2.3' for 'DOGGY'
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



def breakSimpleSub(theMap, allCandidates):
    # allCandidate's format:
    #   { 'cipherword1': ['candidate1a', 'candidate1b', ...],
    #     'cipherword2': ['candidate2a', 'candidate2b', ...],
    #     ...}

    for cipherWord in allCandidates.keys():
        # get a new mapping for each ciphertext word
        newMap = getNewBlankMapping()

        # create a map that has all the letters' possible candidate
        # decryptions added to it
        for candidate in allCandidates[cipherWord]:
            newMap = addMappings(newMap, cipherWord, candidate)

        # intersect this new map with the existing map
        theMap = intersectMappings(theMap, newMap)

    # remove any solved letters from the other possible mappings
    theMap = removeSolvedLettersFromMapping(theMap)

    return theMap


def getNewBlankMapping():
    # Returns a dict where the keys are single-character strings of the
    # uppercase letters, and the values are blank lists.
    # E.g. {'A': [], 'B': [], 'C': [], ...etc}
    theMap = {}
    for i in SYMBOLS:
        theMap[i] = []
    return theMap


def addMappings(theMap, cipherWord, candidate):
    # The theMap parameter is a "mapping" data structure that this function
    # modifies. (See the comments at the top of this file.)
    # The cipherWord parameter is a string value of the ciphertext word.
    # The candidate parameter is a possible English word that the cipherWord
    # could decrypt to.

    # This function modifies theMap so that the mappings of the cipherWord's
    # letters to the candidate's letters are added to theMap.

    for i in range(len(cipherWord)):
        if candidate[i] not in theMap[cipherWord[i]]:
            theMap[cipherWord[i]].append(candidate[i])
    return theMap


def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map, and that add only the
    # candidate decryption letters if they exist in both maps.
    result = getNewBlankMapping()
    for i in mapA.keys():

        # An empty list means "any letter is possible". So just copy the other
        # map entirely.
        if mapA[i] == []:
            result[i] = copy.copy(mapB[i])
        elif mapB[i] == []:
            result[i] = copy.copy(mapA[i])

        else:
            for j in mapA[i]:
                if j in mapB[i]:
                    result[i].append(j)
    return result


def removeSolvedLettersFromMapping(theMap):
    # Letters in the mapping that map to only one letter are consider "solved"
    # and can be removed from the other letters.
    # For example, if 'A' maps to possible letters ['M', 'N'], and 'B' maps
    # to ['N'], then we know that 'B' must map to 'N', so we can remove 'N'
    # from the list of what 'A' could map to. So 'A' then maps to ['M'].
    # Note that now that 'A' maps to only one letter, we can remove 'M'
    # from the list of possible mappings for every other letter. (This is why
    # there is a loop that keeps reducing the map.)
    previousSolvedLetters = []
    solvedLetters = None
    while previousSolvedLetters != solvedLetters:
        # This loop will break when solvedLetters is not changed by the
        # reduction process (and is the same as previousSolvedLetters).
        previousSolvedLetters = solvedLetters
        solvedLetters = []

        # solvedLetters will be a list of English letters that have one and
        # only one possible mapping in theMap
        for i in theMap:
            if len(theMap[i]) == 1:
                solvedLetters.append(theMap[i][0])

        # If a letter is solved, than it cannot possibly be a possible
        # decryption letter for a different ciphertext letter, so we should
        # remove it.
        for i in theMap:
            for s in solvedLetters:
                if len(theMap[i]) != 1 and s in theMap[i]:
                    theMap[i].remove(s)

        # With a letter removed, it's possible that we may have reduced other
        # ciphertext letters to one and only one solution, so keep looping
        # until previousSolvedLetters == solvedLetters. At that point, we'll
        # know we can't rmemove any more letters.
    return theMap


def printMapping(ciphertext, theMap):
    # Display a mapping data structure on the screen.
    print('Mapping:')
    print('    ' + ' '.join(list(SYMBOLS)))
    print('    ' + ' '.join('=' * len(SYMBOLS)))

    for i in range(len(SYMBOLS)):
        print('    ', end='')
        foundAnyLetters = False
        for j in SYMBOLS:
            # theMap[j] points to a list of single-character strings that
            # are potential solutions for the ciphertext letter in j.
            if len(theMap[j]) > i:
                foundAnyLetters = True
                print(theMap[j][i] + ' ', end='')
            else:
                print('  ', end='')
        print()
        if foundAnyLetters == False:
            break


def decryptWithMap(ciphertext, theMap):
    # This function will do a simple sub decryption of ciphertext with the
    # information in theMap, instead of a simple sub key.

    # First create a simple sub key from the theMap mapping.
    key = ['x'] * len(SYMBOLS)
    for letter in theMap.keys():
        if len(theMap[letter]) == 1:
            # There is only one possible letter mapping, so add it to the key.
            keyIndex = SYMBOLS.find(theMap[letter][0].upper())
            key[keyIndex] = letter.upper()
        else:
            ciphertext = ciphertext.replace(letter, '_')
    key = ''.join(key)

    # Then decrypt the original ciphertext with this key and return the
    # decryption.
    return simpleSubCipher.decryptMessage(key, ciphertext)


# If the wordPatterns.py file does not exist, create it based on the words
# in our dictionary text file, dictionary.txt.
# (You can download this file from http://inventwithpython.com/dictionary.txt)
if not os.path.exists('wordPatterns.py'):
    import pprint # import the "pretty print" module
    allPatterns = {}

    fp = open('dictionary.txt')
    wordList = fp.readlines()
    fp.close()

    for word in wordList:
        word = word.strip() # get rid of newline at the end of the string
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

# Import our wordPatterns.py file.
import wordPatterns

if __name__ == '__main__':
    main()