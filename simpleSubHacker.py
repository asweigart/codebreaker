# Simple Substitution Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)

"""
In this program, a "word pattern" is a description of which letters are
repeated in a word. A word pattern is numbers delimited by periods.
The first letter to appear in the word is assigned 0, the second letter 1,
and so on. So the word pattern for 'cucumber' is '0.1.0.1.2.3.4.5' because
the first letter 'c' occurs as the first and third letter in the word
'cucumber'. So the pattern has '0' as the first and third number.

The pattern for 'abc' or 'cba' is '0.1.2'
The pattern for 'aaa' or 'bbb' is '0.0.0'
The pattern for 'hello' is '0.1.2.2.3'
The pattern for 'advise' or 'closet' is '0.1.2.3.4.5' (they have only
unique letters in the word)

In this program, a "candidate" is a possible English word that a
ciphertext work can decrypt to.
For example, 'cucumber', 'mementos', and 'cocoanut' are candidates for the
ciphertext word 'JHJHWDOV' (because all of them have the pattern
'0.1.0.1.2.3.4.5')

In this program, a "map" or "mapping" is a dictionary where the keys are
the letters in LETTERS (e.g. 'A', 'B', 'C', etc) and the values are lists
of letters that could possibly be the correct decryption. If the list is
blank, this means that it is unknown what this letter could decrypt to.
"""

import os, simpleSubCipher, re, copy, makeWordPatterns

if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main() # create the wordPatterns.py file
import wordPatterns

LETTERS = simpleSubCipher.LETTERS


def main():
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'

    NONLETTERSPATTERN = re.compile('[^A-Z\s]')
    ciphertext = NONLETTERSPATTERN.sub('', message.upper()).split()

    # allCandidates is a dict with keys of a single ciphertext word, and
    # values of the possible word patterns
    # e.g. allCandidates == {'PYYACAO': ['alleged', 'ammeter', ...etc],
    #                        'EISWI': ['aerie', 'aging', 'algol', ...etc],
    #                        'LULSXRJ': ['abalone', 'abashed', ...etc],
    #                        ...etc }
    allCandidates = {}
    for cipherWord in ciphertext:
        pattern = makeWordPatterns.getWordPattern(cipherWord)
        if pattern not in wordPatterns.allPatterns:
            continue
        allCandidates[cipherWord] = copy.copy(wordPatterns.allPatterns[pattern])

        # convert candidate words to uppercase
        for i in range(len(allCandidates[cipherWord])):
            allCandidates[cipherWord][i] = allCandidates[cipherWord][i].upper()

    # determine the possible valid ciphertext translations
    print('Hacking...')
    # Python programs can be stopped at any time by pressing Ctrl-C (on
    # Windows) or Ctrl-D (on Mac and Linux)
    print('(Press Ctrl-C or Ctrl-D to quit at any time.)')
    theMap = hackSimpleSub(getBlankMapping(), allCandidates)

    # display the results to the user.
    print('Done.')
    print()
    printMapping(theMap)
    print()
    print('Original ciphertext:')
    print(message)
    print()
    print('Hacked message:')
    print(decryptWithMap(message, theMap))
    print()


def hackSimpleSub(theMap, allCandidates):
    # allCandidate's format:
    #   { 'cipherword1': ['candidate1a', 'candidate1b', ...],
    #     'cipherword2': ['candidate2a', 'candidate2b', ...],
    #     ...}

    for cipherWord in allCandidates.keys():
        # get a new mapping for each ciphertext word
        newMap = getBlankMapping()

        # create a map that has all the letters' possible candidate
        # decryptions added to it
        for candidate in allCandidates[cipherWord]:
            newMap = addLettersToMapping(newMap, cipherWord, candidate)

        # intersect this new map with the existing map
        theMap = intersectMappings(theMap, newMap)

    # remove any solved letters from the other possible mappings
    theMap = removeSolvedLettersFromMapping(theMap)

    return theMap


def getBlankMapping():
    # Returns a dict where the keys are single-character strings of the
    # uppercase letters, and the values are blank lists.
    # E.g. {'A': [], 'B': [], 'C': [], ...etc}
    theMap = {}
    for letter in LETTERS:
        theMap[letter] = []
    return theMap


def addLettersToMapping(theMap, cipherWord, candidate):
    # The theMap parameter is a "mapping" data structure that this
    # function modifies. (See the comments at the top of this file.)
    # The cipherWord parameter is a string value of the ciphertext word.
    # The candidate parameter is a possible English word that the
    # cipherWord could decrypt to.

    # This function modifies theMap so that the mappings of the
    # cipherWord's letters to the candidate's letters are added to theMap.

    for i in range(len(cipherWord)):
        if candidate[i] not in theMap[cipherWord[i]]:
            theMap[cipherWord[i]].append(candidate[i])
    return theMap


def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map, and that add only the
    # candidate decryption letters if they exist in both maps.
    intersectedMap = getBlankMapping()
    for letter in mapA.keys():

        # An empty list means "any letter is possible". So just copy the
        # other map entirely.
        if mapA[letter] == []:
            intersectedMap[letter] = copy.copy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMap[letter] = copy.copy(mapA[letter])

        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersectedMap[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMap[letter].append(mappedLetter)
    return intersectedMap


def removeSolvedLettersFromMapping(theMap):
    # Letters in the mapping that map to only one letter are consider
    # "solved" and can be removed from the other letters.
    # For example, if 'A' maps to possible letters ['M', 'N'], and 'B'
    # maps to ['N'], then we know that 'B' must map to 'N', so we can
    # remove 'N' from the list of what 'A' could map to. So 'A' then maps
    # to ['M']. Note that now that 'A' maps to only one letter, we can
    # remove 'M' from the list of possible mappings for every other
    # letter. (This is why there is a loop that keeps reducing the map.)
    previousSolvedLetters = []
    solvedLetters = None
    while previousSolvedLetters != solvedLetters:
        # This loop will break when solvedLetters is not changed by the
        # reduction process (and is the same as previousSolvedLetters).
        previousSolvedLetters = solvedLetters
        solvedLetters = []

        # solvedLetters will be a list of English letters that have one
        # and only one possible mapping in theMap
        for i in theMap:
            if len(theMap[i]) == 1:
                solvedLetters.append(theMap[i][0])

        # If a letter is solved, than it cannot possibly be a possible
        # decryption letter for a different ciphertext letter, so we
        # should remove it.
        for i in theMap:
            for s in solvedLetters:
                if len(theMap[i]) != 1 and s in theMap[i]:
                    theMap[i].remove(s)

        # With a letter removed, it's possible that we may have reduced
        # other ciphertext letters to one and only one solution, so keep
        # looping until previousSolvedLetters == solvedLetters. At that
        # point, we'll know we can't rmemove any more letters.
    return theMap


def printMapping(theMap):
    # Display a mapping data structure on the screen.
    print('Mapping:')
    print('    ' + ' '.join(list(LETTERS)))
    print('    ' + ' '.join('=' * len(LETTERS)))

    for i in range(len(LETTERS)):
        print('    ', end='')
        foundAnyLetters = False
        for j in LETTERS:
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
    key = ['x'] * len(LETTERS)
    for letter in theMap.keys():
        if len(theMap[letter]) == 1:
            # If only one possible letter mapping, add it to the key.
            keyIndex = LETTERS.find(theMap[letter][0].upper())
            key[keyIndex] = letter.upper()
        else:
            ciphertext = ciphertext.replace(letter, '_')
    key = ''.join(key)

    # Then decrypt the original ciphertext with this key and return the
    # decryption.
    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    main()