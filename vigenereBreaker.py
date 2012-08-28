# Vigenere Cipher Breaker
# http://inventwithpython.com/codebreaker (BSD Licensed)

import copy, math, itertools, re
import vigenereCipher, pyperclip, freqFinder, detectEnglish
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

MAX_KEY_LENGTH = 16
NUM_MOST_FREQ_LETTERS = 3
SILENT_MODE = False
FACTOR_CACHE = {} # a dictionary that stores lists of factors

nonLettersPattern = re.compile('[^A-Z]')

def main():
    # Instead of typing this ciphertext out, you can copy & paste it
    # from http://inventwithpython.com/vigenereBreaker.py
    ciphertext = """ADIZ AVTZQECI TMZUBB WSA M PMILQEV HALPQAVTAKUOI, LGOUQDAF, KDMKTSVMZTSL, IZR XOEXGHZR KKUSITAAF. VZ WSA TWBHDG UBALMMZHDAD QZ HCE VMHSGOHUQBO OX KAAKULMD GXIWVOS, KRGDURDNY I RCMMSTUGVTAWZ CA TZM OCICWXFG JF "STSCMILPY" OID "UWYDPTSBUCI" WABT HCE LCDWIG EIOVDNW. BGFDNY QE KDDWTK QJNKQPSMEV BA PZ TZM ROOHWZ AT XOEXGHZR KKUSICW IZR VRLQRWXIST UBOEDTUUZNUM. PIMIFO ICMLV EMF DI, LCDWIG OWDYZD XWD HCE YWHSMNEMZH XOVM MBY CQXTSM SUPACG (GUKE) OO BDMFQCLWG BOMK, TZUHVIF'A OCYETZQOFIFO OSITJM. RCM A LQYS CE OIE VZAV WR VPT 8, LPQ GZCLQAB MEKXABNITTQ TJR YMDAVN FIHOG CJGBHVNSTKGDS. ZM PSQIKMP O IUEJQF JF LMOVIIICQG AOJ JDSVKAVS UZREIZ QDPZMDG, DNUTGRDNY BTS HELPAR JF LPQ PJMTM, MB ZLWKFFJMWKTOIIUIX AVCZQZS OHSB OCPLV NUBY SWBFWIGK NAF OHW MZWBMS UMQCIFM. MTOEJ BTS RAJ PQ KJRCMP OO TZM ZOOIGVMZ KHQAUQVL DINCMALWDM, RHWZQ VZ CJMMHZD GVQ CA TZM RWMSL LQGDGFA RCM A KBAFZD-HZAUMAE KAAKULMD, HCE SKQ. WI 1948 TMZUBB JGQZSY MSF ZSRMSV'E QJMHCFWIG DINCMALWDM VT EIZQCEKBQF PNADQFNILG, IVZRW PQ ONSAAFSY IF BTS YENMXCKMWVF CA TZM YOICZMEHZR UWYDPTWZE OID TMOOHE AVFSMEKBQR DN EIFVZMSBUQVL TQAZJGQ. PQ KMOLM M DVPWZ AB OHW KTSHIUIX PVSAA AT HOJXTCBEFMEWN, AFL BFZDAKFSY OKKUZGALQZU XHWUUQVL JMMQOIGVE GPCZ IE HCE TMXCPSGD-LVVBGBUBNKQ ZQOXTAWZ, KCIUP ISME XQDGO OTAQFQEV QZ HCE 1960K. BGFDNY'A TCHOKMJIVLABK FZSMTFSY IF I OFDMAVMZ KRGAQQPTAWZ WI 1952, WZMZ VJMGAQLPAD IOHN WWZQ GOIDT UZGEYIX WI TZM GBDTWL WWIGVWY. VZ AUKQDOEV BDSVTEMZH RILP RSHADM TCMMGVQG (XHWUUQVL UIEHMALQAB) VS SV MZOEJVMHDVW BA DMIKWZ. HPRAVS RDEV QZ 1954, XPSL WHSM TOW ISZKK JQTJRW PUG 42ID TQDHCDSG, RFJM UGMBDDW XAWNOFQZU. VN AVCIZSL LQHZREQZSY TZIF VDS VMMHC WSA EIDCALQ; VDS EWFVZR SVP GJMW WFVZRK JQZDENMP VDS VMMHC WSA MQXIVMZHVL. GV 10 ESKTWUNSM 2009, FGTXCRIFO MB DNLMDBZT UIYDVIYV, NFDTAAT DMIEM YWIIKBQF BOJLAB WRGEZ AVDW IZ CAFAKUOG PMJXWX AHWXCBY GV NSCADN AT OHW JDWOIKP SCQEJVYSIT XWD "HCE SXBOGLAVS KVY ZM ION TJMMHZD." SA AT HAQ 2012 I BFDVSBQ AZMTMD'G WIDT ION BWNAFZ TZM TCPSW WR ZJRVA IVDCZ EAIGD YZMBO TMZUBB A KBMHPTGZK DVRVWZ WA EFIOHZD."""
    brokenCiphertext = breakVigenere(ciphertext)

    if brokenCiphertext != None:
        print('Copying broken ciphertext to clipboard:')
        print(brokenCiphertext)
        pyperclip.copy(brokenCiphertext)
    else:
        print('Failed to break encryption.')



def findRepeatSequences(ciphertext):
    # Goes through the ciphertext and finds any 3 to 5 letter sequences that
    # are repeated. Returns a dict with the keys of the sequence and value
    # of a list of spacings (the number of letters between the repeats.)

    # Take out all of the non-letter characters from the ciphertext string.
    letterList = [] # start with a blank list
    for letter in ciphertext:
        if letter.isalpha():
            letterList.append(letter) # only add letters to the list
    ciphertext = ''.join(letterList) # create one string from the list

    # Compile a list of seqLen-letter sequences found in the ciphertext.
    seqSpacings = {}
    for seqLen in range(3, 5):
        for seqStart in range(len(ciphertext) - seqLen):
            # Determine what the sequence is, and store it in seq
            seq = ciphertext[seqStart:seqStart+seqLen]

            # Look for this sequence in the rest of the ciphertext
            for i in range(seqStart + seqLen, len(ciphertext) - seqLen):
                if ciphertext[i:i + seqLen] == seq:
                    # Found a repeated sequence.
                    if seq not in seqSpacings:
                        # First time a repeat was found, create a blank list
                        # for it in seqSpacings.
                        seqSpacings[seq] = []

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence.
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getFactors(num):
    # Returns a list of factors of num.
    # For example, getFactors(28) returns [2, 14, 4, 7]

    # If we've calculated the factors before, they will be in FACTOR_CACHE.
    # In that case, just return a copy of the list of factors.
    if num in FACTOR_CACHE:
        return copy.copy(FACTOR_CACHE[num])

    factors = [] # the list of factors found

    # When finding factors, you only need to check the integers up to the
    # square root of the number.
    for i in range(2, int(math.sqrt(num))): # skip the factors 1 and num
        if num % i == 0:
            factors.append(i)
            factors.append(int(num / i))

    FACTOR_CACHE[num] = factors # add thist list to FACTOR_CACHE

    return copy.copy(factors) # return a copy of this list of factors


def getMostCommonFactors(seqFactors):
    # First, get a count of many times a factor occurs in seqFactors
    factorCounts = {} # key is a factor, value is the number of times it occurs
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Second, put the factor and its count into a tuple, and make a list of these tuples so we can sort them.
    factorsByCount = []
    for factor in factorCounts:
        if factor < MAX_KEY_LENGTH: # also, don't include factors larger than MAX_KEY_LENGTH
            factorsByCount.append( (factor, factorCounts[factor]) )
    factorsByCount.sort(key=lambda x: x[1], reverse=True) # sort the list by the factor count

    # Third, go through the factorsByCount list and cut off the list after you find a factor that is not within 50% of the size of the previous factor count.
    markCount = factorsByCount[0][1]
    for i in range(1, len(factorsByCount)):
        if markCount * 0.5 > factorsByCount[i][1]:
            factorsByCount = factorsByCount[:i] # set factorsByCount to the factors in the list up to i (and cutting off the rest)
            break

    # The factors are more likely to be the true key length, so sort them by factor:
    #factorsByCount.sort(key=lambda x: x[0])

    return factorsByCount


def getNthLetter(nth, keyLength, message):
    # Returns every Nth letter for each keyLength set of letters in text.
    # E.g. getNthLetter(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthLetter(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthLetter(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthLetter(1, 5, 'ABCABCABC') returns 'AC'

    # Use a "regular expression" to get rid of non-letters from the message.
    message = nonLettersPattern.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def breakVigenere(ciphertext):
    # First, we need to do Kasiski Examination to figure out what the length of the ciphertext's encryption key is.
    if not SILENT_MODE:
        print('Determining most likely key lengths with Kasiski Examination...')

    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        print('Kasiski Examination results say the most likely key lengths are: ', end='')
        for keyLength in allLikelyKeyLengths:
            print('%s ' % (keyLength), end='')
        print()
        print()

    for keyLength in allLikelyKeyLengths:
        #print('Attempting break with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        brokenCiphertext = attemptBreakWithKeyLength(ciphertext, keyLength)
        if brokenCiphertext != None:
            break

    # If none of the key lengths we found using Kasiski Examination worked, start brute forcing through key lengths.
    if brokenCiphertext == None:
        if not SILENT_MODE:
            print('Unable to break message with likely key length(s). Brute forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            if keyLength not in allLikelyKeyLengths: # don't re-check key lengths we've already tried from Kasiski Examination
                if not SILENT_MODE:
                    print('Attempting break with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                brokenCiphertext = attemptBreakWithKeyLength(ciphertext, keyLength)
                if brokenCiphertext != None:
                    break

    return brokenCiphertext


def kasiskiExamination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occurr multiple times in the ciphertext.
    # repeatedSeqs has a value like: {'EXG': [192], 'NAF': [339, 972, 633], ... }
    repeatedSeqs = findRepeatSequences(ciphertext)

    # seqFactors keys are sequences, values are list of factors of the spacings.
    # seqFactos has a value like: {'GFD': [2, 3, 4, 6, 9, 12, 18, 23, 36, 46, 69, 92, 138, 207, 276, 414], 'ALW': [2, 3, 4, 6, ...], ...}
    seqFactors = {}
    for seq in repeatedSeqs:
        seqFactors[seq] = []
        for spacing in repeatedSeqs[seq]:
            seqFactors[seq].extend(getFactors(spacing))

    # factorsByCount is a list of tuples: (factor, factorCount)
    # factorsByCount has a value like: [(3, 497), (2, 487), (6, 453), (4, 284), (12, 260)]
    factorsByCount = getMostCommonFactors(seqFactors)

    # Now we extract the factor counts from factorsByCount and put them in variables named allLikelyKeyLengths and allLikelyKeyLengthsStr so that they are easier to use later.
    allLikelyKeyLengths = []
    for i in range(len(factorsByCount)):
        allLikelyKeyLengths.append(factorsByCount[i][0])

    return allLikelyKeyLengths


def attemptBreakWithKeyLength(ciphertext, mostLikelyKeyLength):
    # Determine the most likely letters for each letter in the key.

    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores list.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthLetter(nth, mostLikelyKeyLength, ciphertext)

        # freqScores is a list of tuples (<letter>, <eng. freq. match score>)
        # This list is sorted by match score (a lower score means a better
        # match. See the englishFreqMatch() comments in freqFinder).
        freqScores = []
        for possibleKey in LETTERS:
            translated = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            freqScores.append((possibleKey, freqFinder.englishFreqMatch(translated)))

        # Each value in freqScores is a tuple (<letter>, <match score>). Since
        # we want to sort by match score, we need to pass a "lambda" function
        # to sort()'s "key" parameter to look at the value at the [1] index.
        freqScores.sort(key=lambda x: x[1], reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            # use i+1, because otherwise the "first" letter is called the "0th" letter
            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()

    # Try every combination of the most likely letters for each position
    # in the key.
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):
        # Create a possible key from the letters in allFreqScores
        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))

        decryptedText = vigenereCipher.decryptMessage(possibleKey, ciphertext)

        if freqFinder.englishTrigramMatch(decryptedText):
            if detectEnglish.isEnglish(decryptedText):
                # Check with the user to see if the decrypted key has been found.
                print()
                print('Possible encryption break:')
                print('Key ' + str(possibleKey) + ': ' + decryptedText[:200])
                print()
                print('Enter D for done, or just press Enter to continue breaking:')
                response = input('> ')

                if response.strip().upper().startswith('D'):
                    return decryptedText

    # No English-looking decryption found with any of the possible keys,
    # so return None.
    return None


# If vigenereBreaker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()