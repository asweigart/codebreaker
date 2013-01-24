# Vigenere Cipher Hacker
# http://inventwithpython.com/hacking (BSD Licensed)

import copy, math, itertools, re
import vigenereCipher, pyperclip, freqAnalysis, detectEnglish
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

MAX_KEY_LENGTH = 16
NUM_MOST_FREQ_LETTERS = 3
SILENT_MODE = False
FACTOR_CACHE = {} # a dictionary that stores lists of factors

nonLettersPattern = re.compile('[^A-Z]')


def main():
    # Instead of typing this ciphertext out, you can copy & paste it
    # from http://invpy.com/vigenereHacker.py
    ciphertext = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""
    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')


def findRepeatSequences(ciphertext):
    # Goes through the ciphertext and finds any 3 to 5 letter sequences
    # that are repeated. Returns a dict with the keys of the sequence and
    # value of a list of spacings (number of letters between the repeats.)

    # Take out all of the non-letter characters from the ciphertext.
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
                        # First time a repeat was found, create a blank
                        # list for it in seqSpacings.
                        seqSpacings[seq] = []

                    # Append the spacing distance between the repeated
                    # sequence and the original sequence.
                    seqSpacings[seq].append(i - seqStart)
    return seqSpacings


def getFactors(num):
    # Returns a list of factors of num.
    # For example, getFactors(28) returns [2, 14, 4, 7]

    # If we've calculated the factors before, they'll be in FACTOR_CACHE.
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
    factorCounts = {} # key is a factor, value is how often if occurs
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1

    # Second, put the factor and its count into a tuple, and make a list
    # of these tuples so we can sort them.
    factorsByCount = []
    for factor in factorCounts:
        # exclude factors larger than MAX_KEY_LENGTH
        if factor < MAX_KEY_LENGTH:
            factorsByCount.append( (factor, factorCounts[factor]) )

    # sort the list by the factor count
    factorsByCount.sort(key=freqAnalysis.getItemAtIndexOne, reverse=True)

    # Third, go through the factorsByCount list and cut off the list
    # after you find a factor that is not within 50% of the size of the
    # previous factor count.
    markCount = factorsByCount[0][1]
    for i in range(1, len(factorsByCount)):
        if markCount * 0.5 > factorsByCount[i][1]:
            # set factorsByCount to thelist up to i (and cut the rest)
            factorsByCount = factorsByCount[:i]
            break

    return factorsByCount


def kasiskiExamination(ciphertext):
    # Find out the sequences of 3 to 5 letters that occurr multiple times
    # in the ciphertext. repeatedSeqs has a value like:
    # {'EXG': [192], 'NAF': [339, 972, 633], ... }
    repeatedSeqs = findRepeatSequences(ciphertext)

    # seqFactors keys are sequences, values are list of factors of the
    # spacings. seqFactos has a value like: {'GFD': [2, 3, 4, 6, 9, 12,
    # 18, 23, 36, 46, 69, 92, 138, 207], 'ALW': [2, 3, 4, 6, ...], ...}
    seqFactors = {}
    for seq in repeatedSeqs:
        seqFactors[seq] = []
        for spacing in repeatedSeqs[seq]:
            seqFactors[seq].extend(getFactors(spacing))

    # factorsByCount is a list of tuples: (factor, factorCount)
    # factorsByCount has a value like: [(3, 497), (2, 487), (6, 453), ...]
    factorsByCount = getMostCommonFactors(seqFactors)

    # Now we extract the factor counts from factorsByCount and put them
    # in variables named allLikelyKeyLengths and allLikelyKeyLengthsStr
    # so that they are easier to use later.
    allLikelyKeyLengths = []
    for i in range(len(factorsByCount)):
        allLikelyKeyLengths.append(factorsByCount[i][0])

    return allLikelyKeyLengths


def getNthLetter(nth, keyLength, message):
    # Returns every Nth letter for each keyLength set of letters in text.
    # E.g. getNthLetter(1, 3, 'ABCABCABC') returns 'AAA'
    #      getNthLetter(2, 3, 'ABCABCABC') returns 'BBB'
    #      getNthLetter(3, 3, 'ABCABCABC') returns 'CCC'
    #      getNthLetter(1, 5, 'ABCABCABC') returns 'AC'

    # Use a "regular expression" remove non-letters from the message.
    message = nonLettersPattern.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLength
    return ''.join(letters)


def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # Determine the most likely letters for each letter in the key.

    # allFreqScores is a list of mostLikelyKeyLength number of lists.
    # These inner lists are the freqScores list.
    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthLetter(nth, mostLikelyKeyLength, ciphertext)

        # freqScores is a list of tuples like:
        # [(<letter>, <Eng. Freq. match score>), ... ]
        # This list is sorted by match score (a lower score means a better
        # match. See the englishFreqMatchScore() comments in freqAnalysis).
        freqScores = []
        for possibleKey in LETTERS:
            translated = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            freqScores.append((possibleKey, freqAnalysis.englishFreqMatchScore(translated)))

        # Sort by match score
        freqScores.sort(key=freqAnalysis.getItemAtIndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):
            # use i+1 so the first letter is not called the "0th" letter
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

        if freqAnalysis.englishTrigramMatch(decryptedText):
            if detectEnglish.isEnglish(decryptedText):
                # Check with the user to see if the key has been found.
                print()
                print('Possible encryption hack:')
                print('Key ' + str(possibleKey) + ': ' + decryptedText[:200])
                print()
                print('Enter D for done, or just press Enter to continue hacking:')
                response = input('> ')

                if response.strip().upper().startswith('D'):
                    return decryptedText

    # No English-looking decryption found with any of the possible keys,
    # so return None.
    return None


def hackVigenere(ciphertext):
    # First, we need to do Kasiski Examination to figure out what the
    # length of the ciphertext's encryption key is.
    if not SILENT_MODE:
        print('Determining most likely key lengths with Kasiski Examination...')

    allLikelyKeyLengths = kasiskiExamination(ciphertext.upper())
    if not SILENT_MODE:
        print('Kasiski Examination results say the most likely key lengths are: ', end='')
        for keyLength in allLikelyKeyLengths:
            print('%s ' % (keyLength), end='')
        print()
        print()

    for keyLength in allLikelyKeyLengths:
        print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext.upper(), keyLength)
        if hackedMessage != None:
            break

    # If none of the key lengths we found using Kasiski Examination
    # worked, start brute forcing through key lengths.
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # don't re-check key lengths already tried from Kasiski
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext.upper(), keyLength)
                if hackedMessage != None:
                    break

    if hackedMessage != None:
        # Set the broken ciphertext to the original casing.
        origCase = []
        for i in range(len(ciphertext)):
            if ciphertext[i].isupper():
                origCase.append(hackedMessage[i].upper())
            else:
                origCase.append(hackedMessage[i].lower())
        hackedMessage = ''.join(origCase)

    return hackedMessage


# If vigenereHacker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()