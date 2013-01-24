# Simple Substitution Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)

"""
In this program, a "word pattern" is a description of which letters are
repeated in a word. A word pattern is numbers delimited by periods.
The first letter to appear in the word is assigned 0, the second letter 1,
and so on. So the word pattern for 'cucumber' is '0.1.0.1.2.3.4.5' because
the first letter 'c' occurs as the first and third letter in the word
'cucumber'. So the pattern has '0' as the first and third number. The 'u'
occurs as the second and fourth letter, so '1' is used for the second and
fourth number.
The numbers are delimited by periods to separate them.

The word pattern for 'abc' or 'cba' is '0.1.2'
The word pattern for 'aaa' or 'bbb' is '0.0.0'
The word pattern for 'hello' is '0.1.2.2.3'
The word pattern for 'advise' or 'closet' is '0.1.2.3.4.5' (they have only
unique letters in the word)

In this program, a "candidate" is a possible English word that a
ciphertext work can decrypt to.
For example, 'cucumber', 'mementos', and 'cocoanut' are candidates for the
ciphertext word 'JHJHWDOV' (because all of these words have the pattern
'0.1.0.1.2.3.4.5')

In this program, a "map" or "letter mapping" is a dictionary where the
keys are single-letter strings (e.g. 'A', 'B', 'C', etc) and the values
are lists of single-letter strings that could possibly be the correct
decryption for the letter in the key. If the list is blank, this means
that it is unknown what this letter could decrypt to.
"""

import os, re, copy, pprint, pyperclip, simpleSubCipher, makeWordPatterns

if not os.path.exists('wordPatterns.py'):
    makeWordPatterns.main() # create the wordPatterns.py file
import wordPatterns

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersOrSpacePattern = re.compile('[^A-Z\s]')

def main():
    message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'

    # Determine the possible valid ciphertext translations.
    print('Hacking...')
    letterMapping = hackSimpleSub(message)

    # Display the results to the user.
    print('Mapping:')
    pprint.pprint(letterMapping)
    print()
    print('Original ciphertext:')
    print(message)
    print()
    print('Copying hacked message to clipboard:')
    hackedMessage = decryptWithLetterMapping(message, letterMapping)
    pyperclip.copy(hackedMessage)
    print(hackedMessage)


def getBlankMapping():
    # Returns a dict where the keys are uppercase single-letter strings
    # and the values are blank lists.
    # E.g. {'A': [], 'B': [], 'C': [], ...etc}
    #
    # We will call the single-letter strings in the keys "cipher letters"
    # and the single-letter strings in the value's list "possible
    # decryption letters".
    letterMapping = {}
    for letter in LETTERS:
        letterMapping[letter] = []
    return letterMapping


def addLettersToMapping(letterMapping, cipherWord, candidate):
    # The letterMapping parameter is a "letter mapping" data structure
    # that this function modifies.
    # The cipherWord parameter is a string value of the ciphertext word.
    # The candidate parameter is a possible English word that the
    # cipherWord could decrypt to.

    # This function adds the letters of the candidate as possible new
    # decryptions for the letters of the cipher word to the letter mapping
    # data structure.

    letterMapping = copy.deepcopy(letterMapping)
    for i in range(len(cipherWord)):
        if candidate[i] not in letterMapping[cipherWord[i]]:
            letterMapping[cipherWord[i]].append(candidate[i])
    return letterMapping


def intersectMappings(mapA, mapB):
    # To intersect two maps, create a blank map, and that add only the
    # possible decryption letters if they exist in BOTH maps.
    intersectedMapping = getBlankMapping()
    for letter in LETTERS:

        # An empty list means "any letter is possible". In this case just
        # copy the other map entirely.
        if mapA[letter] == []:
            intersectedMapping[letter] = copy.copy(mapB[letter])
        elif mapB[letter] == []:
            intersectedMapping[letter] = copy.copy(mapA[letter])

        else:
            # If a letter in mapA[letter] exists in mapB[letter], add
            # that letter to intersectedMapping[letter].
            for mappedLetter in mapA[letter]:
                if mappedLetter in mapB[letter]:
                    intersectedMapping[letter].append(mappedLetter)
    return intersectedMapping


def removeSolvedLettersFromMapping(letterMapping):
    # Cipher letters in the mapping that map to only one letter are
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
        # reduction process inside this loop (meaning it is the same
        # as previousSolvedLetters).
        previousSolvedLetters = solvedLetters
        solvedLetters = []

        # solvedLetters will be a list of English letters that have one
        # and only one possible mapping in letterMapping
        for letter in LETTERS:
            if len(letterMapping[letter]) == 1:
                solvedLetters.append(letterMapping[letter][0])

        # If a letter is solved, than it cannot possibly be a possible
        # decryption letter for a different ciphertext letter, so we
        # should remove it.
        for letter in LETTERS:
            for s in solvedLetters:
                if len(letterMapping[letter]) != 1 and s in letterMapping[letter]:
                    letterMapping[letter].remove(s)

        # With a letter removed, it's possible that we may have reduced
        # other ciphertext letters to one and only one solution, so keep
        # looping until previousSolvedLetters == solvedLetters. At that
        # point, we'll know we can't remove any more letters.
    return letterMapping


def hackSimpleSub(message):
    letterMapping = getBlankMapping()

    # allCandidates is a dict with keys of a single ciphertext word, and
    # values of the possible word patterns.
    # e.g. allCandidates == {'PYYACAO': ['alleged', 'ammeter', ...etc],
    #                        'EISWI': ['aerie', 'aging', 'algol', ...etc],
    #                        'LULSXRJ': ['abalone', 'abashed', ...etc],
    #                        ...etc }
    allCandidates = {}
    message = nonLettersOrSpacePattern.sub('', message.upper()).split()
    for cipherWord in message:
        if cipherWord in allCandidates:
            continue # we've already done this word, so continue
        pattern = makeWordPatterns.getWordPattern(cipherWord)
        if pattern not in wordPatterns.allPatterns:
            continue
        allCandidates[cipherWord] = copy.copy(wordPatterns.allPatterns[pattern])

    for cipherWord in allCandidates.keys():
        # Get a new mapping for each ciphertext word.
        newMap = getBlankMapping()

        # Create a map that has all the letters' possible candidate
        # decryptions.
        for candidate in allCandidates[cipherWord]:
            newMap = addLettersToMapping(newMap, cipherWord, candidate)

        # Intersect this new map with the existing map.
        letterMapping = intersectMappings(letterMapping, newMap)

    # Remove any solved letters from the other possible mappings.
    letterMapping = removeSolvedLettersFromMapping(letterMapping)

    return letterMapping


def decryptWithLetterMapping(ciphertext, letterMapping):
    # Return a string of the ciphertext decrypted with the letter mapping,
    # with any ambiguous decrypted letters replaced with a _ underscore.

    # First create a simple sub key from the letterMapping mapping.
    key = ['x'] * len(LETTERS)
    for letter in LETTERS:
        if len(letterMapping[letter]) == 1:
            # If only one possible letter mapping, add it to the key.
            keyIndex = LETTERS.find(letterMapping[letter][0])
            key[keyIndex] = letter
        else:
            ciphertext = ciphertext.replace(letter.lower(), '_')
            ciphertext = ciphertext.replace(letter.upper(), '_')
    key = ''.join(key)

    # With the key we've created, decrypt the message.
    return simpleSubCipher.decryptMessage(key, ciphertext)


if __name__ == '__main__':
    main()