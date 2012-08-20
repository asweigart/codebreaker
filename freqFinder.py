# Frequency Finder
# http://inventwithpython.com/codebreaker (BSD Licensed)

# frequency taken from http://en.wikipedia.org/wiki/Letter_frequency
englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
englishTrigramFreq = {'THE': 3.508232, 'AND': 1.593878, 'ING': 1.147042, 'HER': 0.822444, 'HAT': 0.650715, 'HIS': 0.596748, 'THA': 0.593593, 'ERE': 0.560594, 'FOR': 0.555372, 'ENT': 0.530771, 'ION': 0.506454, 'TER': 0.461099, 'WAS': 0.460487, 'YOU': 0.437213, 'ITH': 0.43125, 'VER': 0.430732, 'ALL': 0.422758, 'WIT': 0.39729, 'THI': 0.394796, 'TIO': 0.378058}
englishFreqOrder = ('E', 'T', 'A', 'O', 'I', 'N', 'S', 'H', 'R', 'D', 'L', 'C', 'U', 'M', 'W', 'F', 'G', 'Y', 'P', 'B', 'V', 'K', 'J', 'X', 'Q', 'Z')
ETAOIN = ''.join(englishFreqOrder)
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

TRIGRAM_THRESHOLD = 2
TRIGRAM_MATCH_RANGE = 30

def getLetterCount(message):
    letterToCount = {}
    for letter in LETTERS:
        letterToCount[letter] = 0 # intialize each letter to 0

    for letter in message:
        if letter in LETTERS:
            letterToCount[letter] += 1

    return letterToCount

def getLetterFreq(message):
    counts = getLetterCount(message)
    totalCount = 0
    for letter in counts:
        totalCount += counts[letter]

    letterToFreq = {}
    for letter in counts:
        letterToFreq[letter] = round(counts[letter] * 100 / totalCount, 2)
    return letterToFreq

def _getFrequencyOrder(message):
    message = message.upper()
    # first, get a dictionary of each letter and its frequency count from the message
    letterToFreq = getLetterCount(message)

    # second, make a dictionary of each frequency count to each letter(s) with that frequency
    freqToLetter = {}
    for letter in LETTERS:
        freqToLetter[letterToFreq[letter]] = [] # intialize to a blank list

    for letter in LETTERS:
        freqToLetter[letterToFreq[letter]].append(letter)

    # third, put each list of letters in reverse "ETAOIN" order, and then convert it to a string
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=lambda x: ETAOIN.find(x), reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    # fourth, convert the freqToLetter dictionary to a list of tuple pairs (key, value), then sort them
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=lambda x: x[0], reverse=True)

    # fifth, now that the letters are ordered by frequency, extract all the letters for the final string
    freqOrder = ''
    for freqPair in freqPairs:
        freqOrder += freqPair[1]

    return freqOrder


def _englishFreqMatch(message):
    message = message.upper()
    freq = getLetterCount(message)

    total = 0
    freqPercentage = {}
    for letter in freq:
        total += freq[letter]
    for letter in freq:
        freqPercentage[letter] = freq[letter] / total

    offScore = 0.0 # the lower the offScore, the better the match
    for letter in LETTERS:
        offScore += (englishLetterFreq[letter] - freqPercentage[letter]) ** 2
    return round(offScore, 3)

def englishFreqMatch(message):
    freqOrder = _getFrequencyOrder(message)

    matches = 0
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matches += 1
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matches += 1

    return matches


def englishTrigramMatch(message):
    message = message.upper()

    # Create a string of only hte letter characters
    lettersOnly = []
    for character in message:
        if character in LETTERS:
            lettersOnly.append(character)
    message = ''.join(lettersOnly)

    total = 0
    trigrams = {}
    for i in range(len(message) - 2):
        trigram = message[i:i+3]
        if trigram in trigrams:
            trigrams[trigram] += 1
        else:
            trigrams[trigram] = 1
        total +=1

    topFreqs = list(trigrams.items())
    topFreqs.sort(key=lambda x: x[1], reverse=True)
    topFreqs = [x[0] for x in topFreqs]

    trigramFreqs = {}
    for trigram in trigrams:
        trigramFreqs[trigram] = trigrams[trigram] / total * 100

    matches = 0
    for commonTrig in englishTrigramFreq:
        if commonTrig in topFreqs[:TRIGRAM_MATCH_RANGE]:
            matches += 1

    return matches >= TRIGRAM_THRESHOLD


def main():
    import random

    sonnet = """WHEN, IN DISGRACE WITH FORTUNE AND MEN'S EYES,
I ALL ALONE BEWEEP MY OUTCAST STATE,
AND TROUBLE DEAF HEAVEN WITH MY BOOTLESS CRIES,
AND LOOK UPON MYSELF AND CURSE MY FATE,
WISHING ME LIKE TO ONE MORE RICH IN HOPE,
FEATURED LIKE HIM, LIKE HIM WITH FRIENDS POSSESSED,
DESIRING THIS MAN'S ART, AND THAT MAN'S SCOPE,
WITH WHAT I MOST ENJOY CONTENTED LEAST,
YET IN THESE THOUGHTS MYSELF ALMOST DESPISING,
HAPLY I THINK ON THEE, AND THEN MY STATE,
LIKE TO THE LARK AT BREAK OF DAY ARISING
FROM SULLEN EARTH, SINGS HYMNS AT HEAVEN'S GATE
FOR THY SWEET LOVE REMEMBERED SUCH WEALTH BRINGS,
THAT THEN I SCORN TO CHANGE MY STATE WITH KINGS."""

    loremIpsum = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam porta varius ante eget tincidunt. Pellentesque placerat, turpis nec elementum consectetur, enim nulla molestie velit, quis semper erat lacus quis metus.'.upper()

    print(englishFreqMatch("""Originally conceived to follow the UK Prestel specifications, and developed on contract by IBM Germany, Btx added a number of additional features before launch, including some inspired by the French Minitel service, to create a new display standard of its own, which in 1981 was designated the CEPT1 profile. In 1995 an enhanced backward-compatible standard called Kernel for Intelligent Communication Terminals (KIT) was announced, but this never really gained acceptance. CEPT permits the transmission of graphical pages with a resolution of 480 by 250 pixels, where 32 out of a palette of 4096 colors could be shown at the same time. This corresponds to the technical possibilities of the early 1980s."""))

    print('Shakespeare\'s Sonnet #29')
    print(sonnet)
    print()

    print('Letter Frequencies of Sonnet #29:')
    print(getLetterCount(sonnet))
    print()

    print('Frequency score of Sonnet #29:')
    print(englishFreqMatch(sonnet))
    print()

    # Scrambling Sonnet #29
    scrambled = list(sonnet)
    random.shuffle(scrambled)
    scrambled = ''.join(scrambled)

    print('Frequency score of Scrambled Sonnet #29:')
    print(englishFreqMatch(scrambled))
    print()

    print('Frequency score of Lorem Ipsum text:')
    print(englishFreqMatch(loremIpsum))
    print()

    print('Frequency score of alphabet:')
    print(englishFreqMatch(LETTERS))
    print()

    print('Frequency score of alphabet x 100:')
    print(englishFreqMatch(LETTERS * 100))
    print()

    print('Frequency score of "AAAAAAAAAAAAAAAH":')
    print(englishFreqMatch("AAAAAAAAAAAAAAAH"))
    print()

    print('Frequency score of "VDIUFRFDSFEWAFDSAFLKHFDSALKFA":')
    print(englishFreqMatch("VDIUFRFDSFEWAFDSAFLKHFDSALKFA"))
    print()

if __name__ == '__main__':
    main()
