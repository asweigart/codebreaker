# Frequency Finder
# http://inventwithpython.com/hacking (BSD Licensed)

import re

# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
englishTrigramFreq = {'THE': 3.51, 'AND': 1.59, 'ING': 1.15, 'HER': 0.82, 'HAT': 0.65, 'HIS': 0.60, 'THA': 0.59, 'ERE': 0.56, 'FOR': 0.56, 'ENT': 0.53, 'ION': 0.51, 'TER': 0.46, 'WAS': 0.46, 'YOU': 0.44, 'ITH': 0.43, 'VER': 0.43, 'ALL': 0.42, 'WIT': 0.40, 'THI': 0.39, 'TIO': 0.38}
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
nonLettersPattern = re.compile('[^A-Z]')


def getLetterCount(message):
    # Returns a dictionary with keys of single letters and values of the
    # count of how many times they appear in the message parameter.
    letterCount = {}
    for letter in LETTERS:
        letterCount[letter] = 0 # intialize each letter to 0

    for letter in message.upper():
        if letter in LETTERS:
            letterCount[letter] += 1

    return letterCount


def getItemAtIndexZero(x):
    return x[0]


def getItemAtIndexOne(x):
    return x[1]


def getFrequencyOrder(message):
    # Returns a string of the alphabet letters arranged in order of most
    # frequently occurring in the message parameter.

    # first, get a dictionary of each letter and its frequency count
    letterToFreq = getLetterCount(message)

    # second, make a dictionary of each frequency count to each letter(s)
    # with that frequency
    freqToLetter = {}
    for letter in LETTERS:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    # third, put each list of letters in reverse "ETAOIN" order, and then
    # convert it to a string
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    # fourth, convert the freqToLetter dictionary to a list of tuple
    # pairs (key, value), then sort them
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)

    # fifth, now that the letters are ordered by frequency, extract all
    # the letters for the final string
    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)


def englishFreqMatchScore(message):
    # Return the number of matches that the string in the message
    # parameter has when its letter frequency is compared to English
    # letter frequency. A "match" is how many of its six most frequent
    # and six least frequent letters is among the six most frequent and
    # six least frequent letters for English.
    freqOrder = getFrequencyOrder(message)

    matchScore = 0
    # Find how many matches for the six most common letters there are.
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1
    # Find how many matches for the six least common letters there are.
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore


def englishTrigramMatch(message, trigramThreshold=2, trigramMatchRange=30):
    # Return True if the string in the message parameter matches the
    # trigram frequency of English.

    # Remove the non-letter characters from message
    message = nonLettersPattern.sub('', message.upper())

    # Count the trigrams in message
    trigrams = {}
    for i in range(len(message) - 2):
        trigram = message[i:i+3]
        if trigram not in trigrams:
            trigrams[trigram] = 1
        else:
            trigrams[trigram] += 1

    # Sort the trigrams by frequency
    topFreqs = list(trigrams.items())
    topFreqs.sort(key=getItemAtIndexOne, reverse=True)
    topFreqLetters = []
    for item in topFreqs:
        topFreqLetters.append(item[0])

    matchScore = 0
    for commonTrig in englishTrigramFreq:
        if commonTrig in topFreqLetters[:trigramMatchRange]:
            matchScore += 1

    return matchScore >= trigramThreshold