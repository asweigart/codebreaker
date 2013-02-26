import unittest, subprocess, pyperclip, hashlib, os, sys, io, random, shutil

# You can download pyperclip from:
# http://coffeeghost.net/src/pyperclip.py

# To install Pylint, download the three following files:
# http://pypi.python.org/packages/source/l/logilab-common/logilab-common-0.58.1.tar.gz#md5=77298ab2d8bb8b4af9219791e7cee8ce
# http://pypi.python.org/packages/source/l/logilab-astng/logilab-astng-0.24.0.tar.gz#md5=295bdb2165657ad4b973b3fae1c95f12
# http://pypi.python.org/packages/source/p/pylint/pylint-0.25.2.tar.gz#md5=d878d7688a4f5290dc5b53a836872400
#
# These are the pylint, logilab-astng, and logilab-common modules.
# Install them by running "python setup.py install" (using the Python32 python.exe or some other Python 3 interpreter) from inside the unzipped folders of each of the three modules.
#
# The pylint module needed to be run with "python setup.py install --no-compile" to work (it had some "encoding could not be found" error)
#
# I created a run_tests.bat batch file with this for content:
# @c:\Python32\python.exe c:\Python32\Lib\site-packages\pylint\lint.py --rcfile=pylint.conf %1 %2 %3 %4 %5 %6 %7 %8 %9
#
# This way I could run "run_pylint.bat foo.py" to run pylint on a source code file.
# Be sure to download the pylint.conf config file and have it in the same folderas codebreaker_unit_tests.py


FOX_MESSAGE = "The quick brown fox jumped over the yellow lazy dog.".upper()
ENGLISH_SENTENCES = """I promised her a delicious dinner.
Tony made him some coffee.
That singer granted him his wish.
Those guards offer her some money.
That barber read the children a story.
That pilot told her the shortest way.
They give him a book.
That barber brings her some perfume.
That teacher pays him this salary.
Those librarians left her a ticket.
I told them a joke.
They write her a letter.
Those news announcers saved her a seat.
I read the children a story.
They promise her a delicious dinner.
Ginger tells them many lies.
John showed them a photograph.
I left her a ticket.
I read the children a story.
I teach them English.
I asked him a question.
They gave him a book.
Into the circuitry speculates her therapy.
That news announcer gives him a magazine.
They ordered her a new dress.
They sold him a ticket.
A folded master influences the content apathy.
They have him drive.
Does every drum offer a driven foot?
Can the convict secure the gulf?
They called him a taxi.
How can a roof disappear?
Dick found the book interesting.
When can the subsidiary officer unite the gesture?
They find the box empty.
The remedy originates outside the guide!
Those cashiers heard the girl crying.
They tried to pieces of the underlying Unix Haters mailing list for the older Arpanet; stuff at the disk and whimpers, Gee, are cascading over your recent versions of several dimensions, and little toy machines a generally suggested that that sexual encounters my knowledge of Line.
Rob how to take over to lanning the extra little feature and, the are real time for free space and just those too typical of them. Not something else it.
And so maybe maybe I substitute this a small publishing. Here rarely log in hardware and on the top, of Unix trade shows you think to be much, about how to be loaded, version of acid and have could sided with to. If I When we can be some of a very well, sort; of whom Not is series I wanted who, was not a Null The basic. Thomas or something else could figure give the above would. Annoyed at all the point the end message to control for beta and users log in Unix and retraction, Since only be mov strstr strstr clr strstr mov strstr be: prepared for that packets can to get At one of.
In years, when the various useless. Hmmm; that's right out that Solaris drove them and it works? Aaaiiiiiigghhhhhhh!
Unix internals to simply not written and Bsd on your mailboxes; mail; delivery still waiting for some utilities used punished. This option was an encryption is intolerable on making Life most recently Received have cat process and I've just gone.
To say we do you are native Macintosh any zero. The difference between failures every copy of U so it would have anything which brings the morbidly curious asymmetry that, bring having to do have to another It Already almost useless gibberish to body that's not to put up some when telnetting to wait! Well; deserved day unless you pull the apparently to a server situation evokes a Grand Exalted DNS resolution to happen to me us; here refer to track when that it to use the problem but lofty, political ideals (and now I'll have gotten it seems entirely and portable assembler that either stdout: and a result really a function prototypes must accept any use rehash and converts it appears that are most of any design).
I know! Well reasonable people we can't get some brief has to. It's bitching about sendmail happily hacking with fudge Join the best so you're to assume that I have other than point to recover or even IBM terminal? Just another flame to search for at the executable: after direction. If (you have some fields may have real deadling it's unix box of the and C construct the power maybe not the Smtp mail envelope: was Always must have to bounce in the output: that acts like Tcp gateway machine I read it gives you a couple of The suggestions but some weasle finds its Unix time it from the stdio library then winding up in Or strictly with me back through the file failed to have a complete and it's your cshrc).
With television while finishing production: of the for improving Financial freedom At the sponsors or cordless phone Number: Tel. Now, is A one. Until you has a Moment zu werden. Apr codon sendmail alias database Apr localhost dd this is proud of only son Incest fantasies are ordered all Lists for his servant as our affiliate Marketing executives with an backups so many other literary works. London's most estimate importantly, Your capability and our exclusive turnkey, system Is that Allows you can help Content Id. Td Font size: that. Here's how to Change it works and the web site for this program more value, your account will be accessible for a week after you've this program via E account.
O o; s I am sharing the program Has changed feel there is a part message: in weeks, later Share, in the you would produce and millions of The link; below and movies Cds. The Bank And the search Engine results option.
Simply and Chargebacks CamsCash new home or those X lola run actually exists. Now Have received already you will not guaranteed. Application name address: to healthy! Get started offering a Clue friend: Update adviser Broker, one: Or new Cd. We did not trying to do you; would you want to wait for all There now Click Of great and secrets on A fan second Time. K, trademark of course or all coming all Winning must accept our R Ihr Nosi Team endif if you're the. Best of Our travel with me.""".split('\n')


def checkForText(filename, text):
    fp = open(filename)
    content = fp.read()
    fp.close()

    return text in content

def saveStdout():
    global OLD_STD_OUT

    OLD_STD_OUT = sys.stdout
    o = io.StringIO()
    sys.stdout = o
    return o

def restoreStdout():
    global OLD_STD_OUT
    sys.stdout = OLD_STD_OUT


def getFileContent(filename):
    fo = open(filename)
    content = fo.read()
    fo.close()
    return content


def getFileHash(filename):
    content = getFileContent(filename)
    return hashlib.md5(content.encode('ascii')).hexdigest()


class CodeHackerPyLint(unittest.TestCase):
    def runPylintOnFile(self, filename):
        proc = subprocess.Popen('run_pylint.bat %s"' % (filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')
        self.assertEqual(procOut, '') # no output means success

    def test_reverseCipherPy(self):
        self.runPylintOnFile('reverseCipher.py')

    def test_caesarCipherPy(self):
        self.runPylintOnFile('caesarCipher.py')

    def test_caesarHackerPy(self):
        self.runPylintOnFile('caesarHacker.py')

    def test_transpositionEncryptPy(self):
        self.runPylintOnFile('transpositionEncrypt.py')

    def test_transpositionDecryptPy(self):
        self.runPylintOnFile('transpositionDecrypt.py')

    def test_transpositionFileCipherPy(self):
        self.runPylintOnFile('transpositionFileCipher.py')

    def test_transpositionHackerPy(self):
        self.runPylintOnFile('transpositionHacker.py')

    def test_transpositionFileHackerPy(self):
        self.runPylintOnFile('transpositionFileHacker.py')

    def test_transpositionTestPy(self):
        self.runPylintOnFile('transpositionTest.py')

    def test_detectEnglishPy(self):
        self.runPylintOnFile('detectEnglish.py')

    def test_buggyPy(self):
        self.runPylintOnFile('buggy.py')

    def test_coinFlipsPy(self):
        self.runPylintOnFile('coinFlips.py')

    def test_affineCipherPy(self):
        self.runPylintOnFile('affineCipher.py')

    def test_affineHackerPy(self):
        self.runPylintOnFile('affineHacker.py')

    def test_simpleSubCipherPy(self):
        self.runPylintOnFile('simpleSubCipher.py')

    def test_simpleSubHackerPy(self):
        self.runPylintOnFile('simpleSubHacker.py')

    def test_simpleSubKeywordPy(self):
        self.runPylintOnFile('simpleSubKeyword.py')

    def test_simpleSubDictionaryHackerPy(self):
        self.runPylintOnFile('simpleSubDictionaryHacker.py')

    """
    # The null cipher programs have been cut from the book.
    def test_nullCipherPy(self):
        self.runPylintOnFile('nullCipher.py')

    def test_nullHackerPy(self):
        self.runPylintOnFile('nullHacker.py')
    """

    def test_vigenereCipherPy(self):
        self.runPylintOnFile('vigenereCipher.py')

    def test_vigenereHackerPy(self):
        self.runPylintOnFile('vigenereHacker.py')

    def test_freqAnalysisPy(self):
        self.runPylintOnFile('freqAnalysis.py')

    def test_cryptomathPy(self):
        self.runPylintOnFile('cryptomath.py')

    def test_primeSievePy(self):
        self.runPylintOnFile('primeSieve.py')

    def test_rabinMillerPy(self):
        # make a fake file to run pylint on, so that we can add pylint-ignore messages to that source
        content = getFileContent('rabinMiller.py')
        content = content.replace("for trials in range(5): # try to falsify num's primality 5 times", "for trials in range(5): # try to falsify num's primality 5 times # pylint: disable-msg=W0612") # I know the 'trials' variable is unused, but that's okay.

        fo = open('rabinMiller_unittest_modified.py', 'w')
        fo.write(content)
        fo.close()

        self.runPylintOnFile('rabinMiller_unittest_modified.py')
        os.unlink('rabinMiller_unittest_modified.py')

    def test_makeRsaKeysPy(self):
        self.runPylintOnFile('makeRsaKeys.py')

    def test_rsaCipherPy(self):
        self.runPylintOnFile('rsaCipher.py')

    def test_pyperclipPy(self):
        self.runPylintOnFile('pyperclip.py')


class CodeBreakerUnitTests(unittest.TestCase):
    def test_reverseCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe reverseCipher.py', stdout=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # check that it is encrypting the right string
        self.assertTrue(checkForText('reverseCipher.py', "message = 'Three can keep a secret, if two of them are dead.'"))

        self.assertEqual(procOut, '.daed era meht fo owt fi ,terces a peek nac eerhT\n')


    def test_caesarCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe caesarCipher.py', stdout=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # check that it is encrypting the right string
        self.assertTrue(checkForText('caesarCipher.py', "message = 'This is my secret message.'"))

        # This string is 'This is my secret message.' encrypted with key 13
        self.assertEqual(procOut, 'GUVF VF ZL FRPERG ZRFFNTR.\n')
        self.assertEqual(pyperclip.paste().decode('ascii'), 'GUVF VF ZL FRPERG ZRFFNTR.')


    def test_caesarHackerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe caesarHacker.py', stdout=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # check that it is encrypting the right string
        self.assertTrue(checkForText('caesarHacker.py', "message = 'GUVF VF ZL FRPERG ZRFFNTR.'"))

        # breaking the ciphertext 'GUVF VF ZL FRPERG ZRFFNTR.'
        expectedOutput = """Key #0: GUVF VF ZL FRPERG ZRFFNTR.
Key #1: FTUE UE YK EQODQF YQEEMSQ.
Key #2: ESTD TD XJ DPNCPE XPDDLRP.
Key #3: DRSC SC WI COMBOD WOCCKQO.
Key #4: CQRB RB VH BNLANC VNBBJPN.
Key #5: BPQA QA UG AMKZMB UMAAIOM.
Key #6: AOPZ PZ TF ZLJYLA TLZZHNL.
Key #7: ZNOY OY SE YKIXKZ SKYYGMK.
Key #8: YMNX NX RD XJHWJY RJXXFLJ.
Key #9: XLMW MW QC WIGVIX QIWWEKI.
Key #10: WKLV LV PB VHFUHW PHVVDJH.
Key #11: VJKU KU OA UGETGV OGUUCIG.
Key #12: UIJT JT NZ TFDSFU NFTTBHF.
Key #13: THIS IS MY SECRET MESSAGE.
Key #14: SGHR HR LX RDBQDS LDRRZFD.
Key #15: RFGQ GQ KW QCAPCR KCQQYEC.
Key #16: QEFP FP JV PBZOBQ JBPPXDB.
Key #17: PDEO EO IU OAYNAP IAOOWCA.
Key #18: OCDN DN HT NZXMZO HZNNVBZ.
Key #19: NBCM CM GS MYWLYN GYMMUAY.
Key #20: MABL BL FR LXVKXM FXLLTZX.
Key #21: LZAK AK EQ KWUJWL EWKKSYW.
Key #22: KYZJ ZJ DP JVTIVK DVJJRXV.
Key #23: JXYI YI CO IUSHUJ CUIIQWU.
Key #24: IWXH XH BN HTRGTI BTHHPVT.
Key #25: HVWG WG AM GSQFSH ASGGOUS.
"""
        self.assertEqual(procOut, expectedOutput)


    def test_transpositionEncryptProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionEncrypt.py', stdout=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # encrypting 'Common sense is not so common.' with key 8
        self.assertEqual(procOut, 'Cenoonommstmme oo snnio. s s c|\n')
        self.assertEqual(pyperclip.paste().decode('ascii'), 'Cenoonommstmme oo snnio. s s c')

    def test_transpositionEncryptModule(self):
        import transpositionEncrypt

        self.assertEqual(transpositionEncrypt.encryptMessage(8, 'Common sense is not so common.'), 'Cenoonommstmme oo snnio. s s c')
        self.assertEqual(transpositionEncrypt.encryptMessage(9, 'Common sense is not so common.'), 'Cntoos nmes.m ooi nsc  osnmeom')
        self.assertEqual(transpositionEncrypt.encryptMessage(10, 'Common sense is not so common.'), 'Cssoeom  micoson m nmsooetnn .')
        self.assertEqual(transpositionEncrypt.encryptMessage(100, 'Common sense is not so common.'), 'Common sense is not so common.')

    def test_transpositionDecryptProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionDecrypt.py', stdout=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # decrypting 'Cenoonommstmme oo snnio. s s c' with key 8
        self.assertEqual(procOut, 'Common sense is not so common.|\n')
        self.assertEqual(pyperclip.paste().decode('ascii'), 'Common sense is not so common.')

    def test_transpositionHackerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        # Make sure output is correct
        expectedOutput = """Hacking...
(Press Ctrl-C or Ctrl-D to quit at any time.)
Trying key #1...
Trying key #2...
Trying key #3...
Trying key #4...
Trying key #5...
Trying key #6...
Trying key #7...
Trying key #8...
Trying key #9...
Trying key #10...

Possible encryption hack:
Key 10: Charles Babbage, FRS (26 December 1791 - 18 October 1871) was an English mathematician, philosopher,

Enter D for done, or just press Enter to continue hacking:
> Copying hacked message to clipboard:
Charles Babbage, FRS (26 December 1791 - 18 October 1871) was an English mathematician, philosopher, inventor and mechanical engineer who originated the concept of a programmable computer. Considered a "father of the computer", Babbage is credited with inventing the first mechanical computer that eventually led to more complex designs. Parts of his uncompleted mechanisms are on display in the London Science Museum. In 1991, a perfectly functioning difference engine was constructed from Babbage's original plans. Built to tolerances achievable in the 19th century, the success of the finished engine indicated that Babbage's machine would have worked. Nine years later, the Science Museum completed the printer Babbage had designed for the difference engine.
"""

        expectedClipboard = """Charles Babbage, FRS (26 December 1791 - 18 October 1871) was an English mathematician, philosopher, inventor and mechanical engineer who originated the concept of a programmable computer. Considered a "father of the computer", Babbage is credited with inventing the first mechanical computer that eventually led to more complex designs. Parts of his uncompleted mechanisms are on display in the London Science Museum. In 1991, a perfectly functioning difference engine was constructed from Babbage's original plans. Built to tolerances achievable in the 19th century, the success of the finished engine indicated that Babbage's machine would have worked. Nine years later, the Science Museum completed the printer Babbage had designed for the difference engine."""

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

        # run again, this time skipping that first decrypted output
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('\n'.encode('ascii'))[0].decode('ascii')
        self.assertTrue('Failed to hack encryption.' in procOut)



    def test_frankensteinTextFile(self):
        fp = open('frankenstein.txt')
        content = fp.read()
        fp.close()

        # make sure we still have the original Project Gutenburg text file of Frankenstein:
        self.assertEqual(hashlib.md5(content.encode('ascii')).hexdigest(), '4054e83e00af969dc1b0c27612274a12')

    def test_transpositionFileCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionFileCipher.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        #import pdb; pdb.set_trace()
        if os.path.exists('frankenstein.encrypted.txt'):
            procOut = proc.communicate('C\n'.encode('ascii'))[0].decode('ascii')
            expectedOutputPiece1 = """This will overwrite the file frankenstein.encrypted.txt. (C)ontinue or (Q)uit?
> """
        else:
            procOut = proc.communicate()[0].decode('ascii')
            expectedOutputPiece1 = ''

        expectedOutputPiece1 += """Encrypting...
Encryption time: """
        expectedOutputPiece2 = """seconds
Done encrypting frankenstein.txt (441034 characters).
Encrypted file is frankenstein.encrypted.txt.
"""

        # Make sure output is correct
        self.assertTrue(expectedOutputPiece1 in procOut)
        self.assertTrue(expectedOutputPiece2 in procOut)


    def test_transpositionFileHackerProgram(self):
        if not os.path.exists('frankenstein.encrypted.txt'):
            # Make the encrypted file by running this test:
            self.test_transpositionFileCipherProgram()

        proc = subprocess.Popen('c:\\python32\\python.exe transpositionFileHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedOutputPiece1 = """Hacking...
(Press Ctrl-C or Ctrl-D to quit at any time.)
"""
        expectedOutputPiece2 = """Key 10: Project Gutenberg's Frankenstein, by Mary Wollstonecraft (Godwin) Shelley

This eBook is for the use

Enter D for done, or just press Enter to continue:
> Writing decrypted text to frankenstein.decrypted.txt."""
        self.assertTrue(expectedOutputPiece1 in procOut)
        self.assertTrue(expectedOutputPiece2 in procOut)
        for i in range(1, 11):
            self.assertTrue('Trying key #%s... Test time:' % (i) in procOut)


    def test_transpositionTestProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionTest.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # Technically the seed is set to 42, so the output should be predictable.
        # But I'll just check for the "test passed" string in the output.

        self.assertTrue('Transposition cipher test passed.' in procOut)


    def test_detectEnglishModule(self):
        import detectEnglish, random
        random.seed(42)

        self.assertTrue(detectEnglish.isEnglish(FOX_MESSAGE))
        for sentence in ENGLISH_SENTENCES:
            self.assertTrue(detectEnglish.isEnglish(sentence))

            sentence = list(sentence)
            random.shuffle(sentence)
            sentence = ''.join([word + 'XXX' for word in sentence])
            self.assertFalse(detectEnglish.isEnglish(sentence), 'ERROR! This sentence detected as real English: %s' % (sentence))


    def test_affineCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe affineCipher.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedClipboard = 'fX<*h>}(rTH<Rh()?<?T]TH=T<rh<tT<*_))T?<ISrT))I~TSr<Ii<Ir<*h()?<?T*TI=T<_<4(>_S<ISrh<tT)IT=IS~<r4_r<Ir<R_]<4(>_SEf<0X)_S<k(HIS~'

        self.assertEqual(procOut, 'Key: 2023\nEncrypted text:\nfX<*h>}(rTH<Rh()?<?T]TH=T<rh<tT<*_))T?<ISrT))I~TSr<Ii<Ir<*h()?<?T*TI=T<_<4(>_S<ISrh<tT)IT=IS~<r4_r<Ir<R_]<4(>_SEf<0X)_S<k(HIS~\nFull encrypted text copied to clipboard.\n')
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)


    def test_affineCipherModule(self):
        import affineCipher, cryptomath

        encrypted = affineCipher.encryptMessage(5031, FOX_MESSAGE)
        decrypted = affineCipher.decryptMessage(5031, encrypted)

        self.assertEqual(FOX_MESSAGE, decrypted)
        self.assertEqual(encrypted, 'Hq4{j|F+O{V?a&-{haZ{z|X64_{aQ4?{Hq4{/4$$a&{$"c/{_a=[')

        # Test with many different keys:
        for keyA in range(2, len(affineCipher.SYMBOLS)):
            for keyB in range(1, len(affineCipher.SYMBOLS)):
                if keyA == 1 or keyB == 0 or cryptomath.gcd(keyA, len(affineCipher.SYMBOLS)) != 1:
                    continue
                key = keyA * len(affineCipher.SYMBOLS) + keyB
                enc = affineCipher.encryptMessage(key, FOX_MESSAGE)
                dec = affineCipher.decryptMessage(key, enc)
                self.assertEqual(dec, FOX_MESSAGE)


        # Test with bad keys:
        self.assertRaises(SystemExit, affineCipher.encryptMessage, len(affineCipher.SYMBOLS) * 1 + 23, FOX_MESSAGE)
        self.assertRaises(SystemExit, affineCipher.encryptMessage, len(affineCipher.SYMBOLS) * 5 + 0, FOX_MESSAGE)
        self.assertRaises(SystemExit, affineCipher.encryptMessage, len(affineCipher.SYMBOLS) * 25 + 23, FOX_MESSAGE)
        self.assertRaises(SystemExit, affineCipher.encryptMessage, len(affineCipher.SYMBOLS) * 25 + 23, FOX_MESSAGE)

    def test_affineHackerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe affineHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedOutput = """Tried Key 2181... (lCPD.q<#t`XP?.#cRPR`f`X1`Pt.P6`PD(cc`RP9)
Tried Key 2182... (_6C7!d/ugSKC2!uVECESYSK$SCg!C)SC7zVVSEC,)
Tried Key 2183... (R)6*sW"hZF>6%shI868FLF>vF6Zs6{F6*mIIF86~)
Tried Key 2184... (E{)|fJt[M91)wf[<+)+9?91i9)Mf)n9)|`<<9+)q)
Tried Key 2185... (XwV:FDGLK<IVNFLC;V;<J<IM<VKFV9<V:8CC<;V@)
Tried Key 2186... (y9w[gehml]jwogmd\w\]k]jn]wlgwZ]w[Ydd]\wa)
Tried Key 2187... (;Z9|)'*/.~,91)/&}9}~-~,0~9.)9{~9|z&&~}9#)
Tried Key 2188... (\{Z>JHKPO@MZRJPG?Z?@N@MQ@ZOJZ=@Z><GG@?ZD)
Tried Key 2189... (}={_kilqpan{skqh`{`aoanra{pk{^a{_]hha`{e)
Tried Key 2190... (?^=!-+.32#0=5-3*"="#1#04#=2-= #=!~**#"=')
Tried Key 2191... (` ^BNLOTSDQ^VNTKC^CDRDQUD^SN^AD^B@KKDC^H)
Tried Key 2192... ("A computer would deserve to be called i)

Possible encryption hack:
Key: 2192
Decrypted message: "A computer would deserve to be called intelligent if it could deceive a human into believing that it was human." -Alan Turing

Enter D for done, or just press Enter to continue hacking:"""
        expectedClipboard = '"A computer would deserve to be called intelligent if it could deceive a human into believing that it was human." -Alan Turing'

        self.assertTrue(expectedOutput in procOut)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

        # run again, this time skipping that first decrypted output
        proc = subprocess.Popen('c:\\python32\\python.exe affineHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('\n'.encode('ascii'))[0].decode('ascii')
        self.assertTrue('Failed to hack encryption.' in procOut)


    def test_simpleSubCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubCipher.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedClipboard = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm'
        expectedOutput = 'Using key LFWOAYUISVKMNXPBDCRJTQEGHZ\nThe encrypted message is:\nSy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm\n\nThis message has been copied to the clipboard.\n'

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)


    def test_simpleSubCipherModule(self):
        import simpleSubCipher

        encrypted = simpleSubCipher.encryptMessage('LFWOAYUISVKMNXPBDCRJTQEGHZ', FOX_MESSAGE)
        decrypted = simpleSubCipher.decryptMessage('LFWOAYUISVKMNXPBDCRJTQEGHZ', encrypted)

        encrypted2 = simpleSubCipher.encryptMessage('XPBDCRJTQEGHZLFWOAYUISVKMN', FOX_MESSAGE)

        self.assertEqual(encrypted, 'JIA DTSWK FCPEX YPG VTNBAO PQAC JIA HAMMPE MLZH OPU.')
        self.assertEqual(FOX_MESSAGE, decrypted)
        self.assertNotEqual(encrypted, encrypted2)


    def test_simpleSubHackerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = "Hacking...\nMapping:\n{'A': ['E'],\n 'B': ['Y', 'P', 'B'],\n 'C': ['R'],\n 'D': [],\n 'E': ['W'],\n 'F': ['B', 'P'],\n 'G': ['B', 'Q', 'X', 'P', 'Y'],\n 'H': ['P', 'Y', 'K', 'X', 'B'],\n 'I': ['H'],\n 'J': ['T'],\n 'K': [],\n 'L': ['A'],\n 'M': ['L'],\n 'N': ['M'],\n 'O': ['D'],\n 'P': ['O'],\n 'Q': ['V'],\n 'R': ['S'],\n 'S': ['I'],\n 'T': ['U'],\n 'U': ['G'],\n 'V': [],\n 'W': ['C'],\n 'X': ['N'],\n 'Y': ['F'],\n 'Z': ['Z']}\n\nOriginal ciphertext:\nSy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh. -Facjclxo Ctrramm\n\nCopying hacked message to clipboard:\nIf a man is offered a fact which goes against his instincts, he will scrutinize it closel_, and unless the evidence is overwhelming, he will refuse to _elieve it. If, on the other hand, he is offered something which affords a reason for acting in accordance to his instincts, he will acce_t it even on the slightest evidence. The origin of m_ths is e__lained in this wa_. -_ertrand Russell\n"

        self.assertEqual(procOut, expectedOutput)


    def test_simpleSubKeywordProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubKeyword.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = 'The key used is:\nALPHNUMERICBDFGJKOQSTVWXYZ\nThe encrypted message is:\nYgto pgvno rq lbgwf.\n\nThis message has been copied to the clipboard.\n'
        expectedClipboard = """Ygto pgvno rq lbgwf."""

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    def test_simpleSubKeywordModule(self):
        import simpleSubKeyword

        encrypted = simpleSubKeyword.encryptMessage('hello', FOX_MESSAGE)
        decrypted = simpleSubKeyword.decryptMessage('hello', encrypted)
        encrypted2= simpleSubKeyword.encryptMessage('howdy', FOX_MESSAGE)

        self.assertEqual(FOX_MESSAGE, decrypted)
        self.assertNotEqual(encrypted, encrypted2)

    """
    # The null cipher programs have been cut from the book.
    def test_nullHackerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe nullHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedClipboard = 'When I use a word, it means just what I choose it to mean -- neither more nor less.'

        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)
    """

    def test_simpleSubDictionaryHackerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubDictionaryHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedClipboard = 'CONFIDANTE: ONE ENTRUSTED BY A WITH THE SECRETS OF B CONFIDED TO HERSELF BY C. -AMBROSE BIERCE'

        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    def test_vigenereCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe vigenereCipher.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = 'Encrypted message:\nADIZ AVTZQECI TMZUBB WSA M PMILQEV HALPQAVTAKUOI, LGOUQDAF, KDMKTSVMZTSL, IZR XOEXGHZR KKUSITAAF. VZ WSA TWBHDG UBALMMZHDAD QZ HCE VMHSGOHUQBO OX KAAKULMD GXIWVOS, KRGDURDNY I RCMMSTUGVTAWZ CA TZM OCICWXFG JF "STSCMILPY" OID "UWYDPTSBUCI" WABT HCE LCDWIG EIOVDNW. BGFDNY QE KDDWTK QJNKQPSMEV BA PZ TZM ROOHWZ AT XOEXGHZR KKUSICW IZR VRLQRWXIST UBOEDTUUZNUM. PIMIFO ICMLV EMF DI, LCDWIG OWDYZD XWD HCE YWHSMNEMZH XOVM MBY CQXTSM SUPACG (GUKE) OO BDMFQCLWG BOMK, TZUHVIF\'A OCYETZQOFIFO OSITJM. RCM A LQYS CE OIE VZAV WR VPT 8, LPQ GZCLQAB MEKXABNITTQ TJR YMDAVN FIHOG CJGBHVNSTKGDS. ZM PSQIKMP O IUEJQF JF LMOVIIICQG AOJ JDSVKAVS UZREIZ QDPZMDG, DNUTGRDNY BTS HELPAR JF LPQ PJMTM, MB ZLWKFFJMWKTOIIUIX AVCZQZS OHSB OCPLV NUBY SWBFWIGK NAF OHW MZWBMS UMQCIFM. MTOEJ BTS RAJ PQ KJRCMP OO TZM ZOOIGVMZ KHQAUQVL DINCMALWDM, RHWZQ VZ CJMMHZD GVQ CA TZM RWMSL LQGDGFA RCM A KBAFZD-HZAUMAE KAAKULMD, HCE SKQ. WI 1948 TMZUBB JGQZSY MSF ZSRMSV\'E QJMHCFWIG DINCMALWDM VT EIZQCEKBQF PNADQFNILG, IVZRW PQ ONSAAFSY IF BTS YENMXCKMWVF CA TZM YOICZMEHZR UWYDPTWZE OID TMOOHE AVFSMEKBQR DN EIFVZMSBUQVL TQAZJGQ. PQ KMOLM M DVPWZ AB OHW KTSHIUIX PVSAA AT HOJXTCBEFMEWN, AFL BFZDAKFSY OKKUZGALQZU XHWUUQVL JMMQOIGVE GPCZ IE HCE TMXCPSGD-LVVBGBUBNKQ ZQOXTAWZ, KCIUP ISME XQDGO OTAQFQEV QZ HCE 1960K. BGFDNY\'A TCHOKMJIVLABK FZSMTFSY IF I OFDMAVMZ KRGAQQPTAWZ WI 1952, WZMZ VJMGAQLPAD IOHN WWZQ GOIDT UZGEYIX WI TZM GBDTWL WWIGVWY. VZ AUKQDOEV BDSVTEMZH RILP RSHADM TCMMGVQG (XHWUUQVL UIEHMALQAB) VS SV MZOEJVMHDVW BA DMIKWZ. HPRAVS RDEV QZ 1954, XPSL WHSM TOW ISZKK JQTJRW PUG 42ID TQDHCDSG, RFJM UGMBDDW XAWNOFQZU. VN AVCIZSL LQHZREQZSY TZIF VDS VMMHC WSA EIDCALQ; VDS EWFVZR SVP GJMW WFVZRK JQZDENMP VDS VMMHC WSA MQXIVMZHVL. GV 10 ESKTWUNSM 2009, FGTXCRIFO MB DNLMDBZT UIYDVIYV, NFDTAAT DMIEM YWIIKBQF BOJLAB WRGEZ AVDW IZ CAFAKUOG PMJXWX AHWXCBY GV NSCADN AT OHW JDWOIKP SCQEJVYSIT XWD "HCE SXBOGLAVS KVY ZM ION TJMMHZD." SA AT HAQ 2012 I BFDVSBQ AZMTMD\'G WIDT ION BWNAFZ TZM TCPSW WR ZJRVA IVDCZ EAIGD YZMBO TMZUBB A KBMHPTGZK DVRVWZ WA EFIOHZD.\n\nThe message has been copied to the clipboard.\n'
        expectedClipboard = 'ADIZ AVTZQECI TMZUBB WSA M PMILQEV HALPQAVTAKUOI, LGOUQDAF, KDMKTSVMZTSL, IZR XOEXGHZR KKUSITAAF. VZ WSA TWBHDG UBALMMZHDAD QZ HCE VMHSGOHUQBO OX KAAKULMD GXIWVOS, KRGDURDNY I RCMMSTUGVTAWZ CA TZM OCICWXFG JF "STSCMILPY" OID "UWYDPTSBUCI" WABT HCE LCDWIG EIOVDNW. BGFDNY QE KDDWTK QJNKQPSMEV BA PZ TZM ROOHWZ AT XOEXGHZR KKUSICW IZR VRLQRWXIST UBOEDTUUZNUM. PIMIFO ICMLV EMF DI, LCDWIG OWDYZD XWD HCE YWHSMNEMZH XOVM MBY CQXTSM SUPACG (GUKE) OO BDMFQCLWG BOMK, TZUHVIF\'A OCYETZQOFIFO OSITJM. RCM A LQYS CE OIE VZAV WR VPT 8, LPQ GZCLQAB MEKXABNITTQ TJR YMDAVN FIHOG CJGBHVNSTKGDS. ZM PSQIKMP O IUEJQF JF LMOVIIICQG AOJ JDSVKAVS UZREIZ QDPZMDG, DNUTGRDNY BTS HELPAR JF LPQ PJMTM, MB ZLWKFFJMWKTOIIUIX AVCZQZS OHSB OCPLV NUBY SWBFWIGK NAF OHW MZWBMS UMQCIFM. MTOEJ BTS RAJ PQ KJRCMP OO TZM ZOOIGVMZ KHQAUQVL DINCMALWDM, RHWZQ VZ CJMMHZD GVQ CA TZM RWMSL LQGDGFA RCM A KBAFZD-HZAUMAE KAAKULMD, HCE SKQ. WI 1948 TMZUBB JGQZSY MSF ZSRMSV\'E QJMHCFWIG DINCMALWDM VT EIZQCEKBQF PNADQFNILG, IVZRW PQ ONSAAFSY IF BTS YENMXCKMWVF CA TZM YOICZMEHZR UWYDPTWZE OID TMOOHE AVFSMEKBQR DN EIFVZMSBUQVL TQAZJGQ. PQ KMOLM M DVPWZ AB OHW KTSHIUIX PVSAA AT HOJXTCBEFMEWN, AFL BFZDAKFSY OKKUZGALQZU XHWUUQVL JMMQOIGVE GPCZ IE HCE TMXCPSGD-LVVBGBUBNKQ ZQOXTAWZ, KCIUP ISME XQDGO OTAQFQEV QZ HCE 1960K. BGFDNY\'A TCHOKMJIVLABK FZSMTFSY IF I OFDMAVMZ KRGAQQPTAWZ WI 1952, WZMZ VJMGAQLPAD IOHN WWZQ GOIDT UZGEYIX WI TZM GBDTWL WWIGVWY. VZ AUKQDOEV BDSVTEMZH RILP RSHADM TCMMGVQG (XHWUUQVL UIEHMALQAB) VS SV MZOEJVMHDVW BA DMIKWZ. HPRAVS RDEV QZ 1954, XPSL WHSM TOW ISZKK JQTJRW PUG 42ID TQDHCDSG, RFJM UGMBDDW XAWNOFQZU. VN AVCIZSL LQHZREQZSY TZIF VDS VMMHC WSA EIDCALQ; VDS EWFVZR SVP GJMW WFVZRK JQZDENMP VDS VMMHC WSA MQXIVMZHVL. GV 10 ESKTWUNSM 2009, FGTXCRIFO MB DNLMDBZT UIYDVIYV, NFDTAAT DMIEM YWIIKBQF BOJLAB WRGEZ AVDW IZ CAFAKUOG PMJXWX AHWXCBY GV NSCADN AT OHW JDWOIKP SCQEJVYSIT XWD "HCE SXBOGLAVS KVY ZM ION TJMMHZD." SA AT HAQ 2012 I BFDVSBQ AZMTMD\'G WIDT ION BWNAFZ TZM TCPSW WR ZJRVA IVDCZ EAIGD YZMBO TMZUBB A KBMHPTGZK DVRVWZ WA EFIOHZD.'

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    def test_vigenereCipherModule(self):
        import vigenereCipher

        encrypted = vigenereCipher.encryptMessage('ANTICS', FOX_MESSAGE)
        decrypted = vigenereCipher.decryptMessage('ANTICS', encrypted)

        encrypted2 = vigenereCipher.encryptMessage('WOOF', FOX_MESSAGE)

        self.assertEqual(FOX_MESSAGE, decrypted)
        self.assertNotEqual(encrypted, encrypted2)

    def test_vigenereHackerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe vigenereHacker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedClipboard = """Alan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer scientist. He was highly influential in the development of computer science, providing a formalisation of the concepts of "algorithm" and "computation" with the Turing machine. Turing is widely considered to be the father of computer science and artificial intelligence. During World War II, Turing worked for the Government Code and Cypher School (GCCS) at Bletchley Park, Britain's codebreaking centre. For a time he was head of Hut 8, the section responsible for German naval cryptanalysis. He devised a number of techniques for breaking German ciphers, including the method of the bombe, an electromechanical machine that could find settings for the Enigma machine. After the war he worked at the National Physical Laboratory, where he created one of the first designs for a stored-program computer, the ACE. In 1948 Turing joined Max Newman's Computing Laboratory at Manchester University, where he assisted in the development of the Manchester computers and became interested in mathematical biology. He wrote a paper on the chemical basis of morphogenesis, and predicted oscillating chemical reactions such as the Belousov-Zhabotinsky reaction, which were first observed in the 1960s. Turing's homosexuality resulted in a criminal prosecution in 1952, when homosexual acts were still illegal in the United Kingdom. He accepted treatment with female hormones (chemical castration) as an alternative to prison. Turing died in 1954, just over two weeks before his 42nd birthday, from cyanide poisoning. An inquest determined that his death was suicide; his mother and some others believed his death was accidental. On 10 September 2009, following an Internet campaign, British Prime Minister Gordon Brown made an official public apology on behalf of the British government for "the appalling way he was treated." As of May 2012 a private member's bill was before the House of Lords which would grant Turing a statutory pardon if enacted."""
        expectedOutput = "Kasiski Examination results say the most likely key lengths are: 3 2 6 4 12 8 9 16 5 11 10 15 7 14 13 \n\nAttempting hack with key length 3 (27 possible keys)...\nPossible letters for letter 1 of the key: A L M \nPossible letters for letter 2 of the key: S N O \nPossible letters for letter 3 of the key: V I Z \nAttempting with key: ASV\nAttempting with key: ASI\nAttempting with key: ASZ\nAttempting with key: ANV\nAttempting with key: ANI\nAttempting with key: ANZ\nAttempting with key: AOV\nAttempting with key: AOI\nAttempting with key: AOZ\nAttempting with key: LSV\nAttempting with key: LSI\nAttempting with key: LSZ\nAttempting with key: LNV\nAttempting with key: LNI\nAttempting with key: LNZ\nAttempting with key: LOV\nAttempting with key: LOI\nAttempting with key: LOZ\nAttempting with key: MSV\nAttempting with key: MSI\nAttempting with key: MSZ\nAttempting with key: MNV\nAttempting with key: MNI\nAttempting with key: MNZ\nAttempting with key: MOV\nAttempting with key: MOI\nAttempting with key: MOZ\nAttempting hack with key length 2 (9 possible keys)...\nPossible letters for letter 1 of the key: O A E \nPossible letters for letter 2 of the key: M S I \nAttempting with key: OM\nAttempting with key: OS\nAttempting with key: OI\nAttempting with key: AM\nAttempting with key: AS\nAttempting with key: AI\nAttempting with key: EM\nAttempting with key: ES\nAttempting with key: EI\nAttempting hack with key length 6 (729 possible keys)...\nPossible letters for letter 1 of the key: A E O \nPossible letters for letter 2 of the key: S D G \nPossible letters for letter 3 of the key: I V X \nPossible letters for letter 4 of the key: M Z Q \nPossible letters for letter 5 of the key: O B Z \nPossible letters for letter 6 of the key: V I K \nAttempting with key: ASIMOV\nPossible encryption hack with key ASIMOV:\nAlan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer scientist. He was highly influential in the development of computer science, providing a formalisation of the con\n\nEnter D for done, or just press Enter to continue hacking:\n> Copying hacked message to clipboard:\nAlan Mathison Turing was a British mathematician, logician, cryptanalyst, and computer scientist. He was highly influential in the development of computer science, providing a formalisation of the concepts of \"algorithm\" and \"computation\" with the Turing machine. Turing is widely considered to be the father of computer science and artificial intelligence. During World War II, Turing worked for the Government Code and Cypher School (GCCS) at Bletchley Park, Britain's codebreaking centre. For a time he was head of Hut 8, the section responsible for German naval cryptanalysis. He devised a number of techniques for breaking German ciphers, including the method of the bombe, an electromechanical machine that could find settings for the Enigma machine. After the war he worked at the National Physical Laboratory, where he created one of the first designs for a stored-program computer, the ACE. In 1948 Turing joined Max Newman's Computing Laboratory at Manchester University, where he assisted in the development of the Manchester computers and became interested in mathematical biology. He wrote a paper on the chemical basis of morphogenesis, and predicted oscillating chemical reactions such as the Belousov-Zhabotinsky reaction, which were first observed in the 1960s. Turing's homosexuality resulted in a criminal prosecution in 1952, when homosexual acts were still illegal in the United Kingdom. He accepted treatment with female hormones (chemical castration) as an alternative to prison. Turing died in 1954, just over two weeks before his 42nd birthday, from cyanide poisoning. An inquest determined that his death was suicide; his mother and some others believed his death was accidental. On 10 September 2009, following an Internet campaign, British Prime Minister Gordon Brown made an official public apology on behalf of the British government for \"the appalling way he was treated.\" As of May 2012 a private member's bill was before the House of Lords which would grant Turing a statutory pardon if enacted.\n"

        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)
        self.assertEqual(procOut, expectedOutput)


    def test_primeSieveModule(self):
        import primeSieve

        self.assertTrue(primeSieve.isPrime(2))
        self.assertTrue(primeSieve.isPrime(17))
        self.assertTrue(primeSieve.isPrime(37))
        self.assertFalse(primeSieve.isPrime(20))
        self.assertFalse(primeSieve.isPrime(1))
        self.assertFalse(primeSieve.isPrime(0))
        self.assertFalse(primeSieve.isPrime(-1))

        sieve = primeSieve.primeSieve(1000)
        self.assertTrue(11 in sieve)
        self.assertTrue(16 not in sieve)
        self.assertTrue(17 in sieve)
        self.assertTrue(147 not in sieve)

        for lowPrime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]:
            self.assertTrue(lowPrime in sieve)
            if lowPrime != 2:
                self.assertFalse(lowPrime + 1 in sieve)


    def test_rabinMillerModule(self):
        import rabinMiller, random

        self.assertFalse(rabinMiller.isPrime(1))
        self.assertFalse(rabinMiller.isPrime(0))
        self.assertFalse(rabinMiller.isPrime(-1))
        self.assertFalse(rabinMiller.isPrime(5099806053))
        self.assertTrue(rabinMiller.isPrime(5099806057))

        random.seed(42)
        for i in range(3):
            for keySize in (32, 64, 128, 256, 512, 600, 1024):
                prime = rabinMiller.generateLargePrime(keySize)
                self.assertTrue(rabinMiller.isPrime(prime))

        for lowPrime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997):
            self.assertTrue(rabinMiller.isPrime(lowPrime))

        for i in range(1000):
            a = random.randint(1, 10000)
            b = random.randint(1, 10000)
            self.assertFalse(rabinMiller.isPrime(a * b))

    def test_makeRsaKeysProgram(self):
        # save the original key files so we don't mess them up.
        oldPubHash, oldPrivHash = None, None

        # make sure the old key files (which should be checked into source control) are there.
        self.assertTrue(os.path.exists('al_sweigart_pubkey.txt') and os.path.exists('al_sweigart_privkey.txt'), 'Expected the original key files to be there.')

        oldPubHash = getFileHash('al_sweigart_pubkey.txt')
        shutil.copyfile('al_sweigart_pubkey.txt', 'al_sweigart_pubkey.txt.unittest_bak')
        os.unlink('al_sweigart_pubkey.txt')
        oldPrivHash = getFileHash('al_sweigart_privkey.txt')
        shutil.copyfile('al_sweigart_privkey.txt', 'al_sweigart_privkey.txt.unittest_bak')
        os.unlink('al_sweigart_privkey.txt')

        proc = subprocess.Popen('c:\\python32\\python.exe makeRsaKeys.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        try:
            self.assertTrue(os.path.exists('al_sweigart_pubkey.txt'))
            self.assertTrue(os.path.exists('al_sweigart_privkey.txt'))
            import rsaCipher
            rsaCipher.readKeyFile('al_sweigart_pubkey.txt')
            rsaCipher.readKeyFile('al_sweigart_privkey.txt')

            self.assertTrue('Key files made.' in procOut)
        except:
            raise
        finally:
            # restore the original key files
            shutil.copyfile('al_sweigart_pubkey.txt.unittest_bak', 'al_sweigart_pubkey.txt')
            os.unlink('al_sweigart_pubkey.txt.unittest_bak')
            shutil.copyfile('al_sweigart_privkey.txt.unittest_bak', 'al_sweigart_privkey.txt')
            os.unlink('al_sweigart_privkey.txt.unittest_bak')
            # make sure that the original key files are the same as before.
            self.assertEqual(oldPubHash, getFileHash('al_sweigart_pubkey.txt'))
            self.assertEqual(oldPrivHash, getFileHash('al_sweigart_privkey.txt'))


    def test_makeRsaKeysModule(self):
        import makeRsaKeys

        strio = saveStdout()

        # erase keys if they exist already
        for filename in ('unittest_pubkey.txt', 'unittest_privkey.txt'):
            if os.path.exists(filename):
                os.unlink(filename)

        makeRsaKeys.makeKeyFiles('unittest', 1024)
        self.assertTrue(os.path.exists('unittest_pubkey.txt'))
        self.assertTrue(os.path.exists('unittest_privkey.txt'))
        import rsaCipher
        rsaCipher.readKeyFile('al_sweigart_pubkey.txt')
        rsaCipher.readKeyFile('al_sweigart_privkey.txt')

        # cleanup key files
        for filename in ('unittest_pubkey.txt', 'unittest_privkey.txt'):
            os.unlink(filename)

        for keySize in (32, 64, 128, 256, 512, 600, 1024):
            makeRsaKeys.generateKey(keySize)

        restoreStdout()

    def test_cryptomathModule(self):
        import cryptomath
        random.seed(42)

        # standard set of gcd tests
        self.assertEqual(cryptomath.gcd(543, 526), 1)
        self.assertEqual(cryptomath.gcd(184543, 825), 1)
        self.assertEqual(cryptomath.gcd(184545, 825), 15)
        self.assertEqual(cryptomath.gcd(30594, 8302), 2)

        # create a bunch of things with expected gcds
        for i in range(500):
            a = random.randint(50, 100000)
            b = random.randint(50, 100000)
            self.assertEqual(cryptomath.gcd(a, b*a), a)

        # standard set of mod inverse tests
        self.assertEqual(cryptomath.findModInverse(5, 7), 3)
        self.assertEqual(cryptomath.findModInverse(5, 18), 11)
        self.assertEqual(cryptomath.findModInverse(7, 180), 103)
        self.assertEqual(cryptomath.findModInverse(8, 12), None)
        self.assertEqual(cryptomath.findModInverse(51, 18), None)

        # confirm that relatively prime a & m values have mod inverse of None
        for i in range(500):
            while True:
                a = random.randint(50, 100000)
                m = random.randint(10, 50000)
                if cryptomath.gcd(a, m) != 1:
                    break
            self.assertEqual(cryptomath.findModInverse(a, m), None)
        # confirm that non-relatively prime a & m values do have a mod inverse
        for i in range(500):
            while True:
                a = random.randint(50, 100000)
                m = random.randint(10, 50000)
                if cryptomath.gcd(a, m) == 1:
                    break
            self.assertNotEqual(cryptomath.findModInverse(a, m), None)


    def test_vigenereCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe vigenereCipher.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = 'Encrypted message:\nAdiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif\'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv\'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny\'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd\'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd.\n\nThe message has been copied to the clipboard.\n'
        expectedClipboard = """Adiz Avtzqeci Tmzubb wsa m Pmilqev halpqavtakuoi, lgouqdaf, kdmktsvmztsl, izr xoexghzr kkusitaaf. Vz wsa twbhdg ubalmmzhdad qz hce vmhsgohuqbo ox kaakulmd gxiwvos, krgdurdny i rcmmstugvtawz ca tzm ocicwxfg jf "stscmilpy" oid "uwydptsbuci" wabt hce Lcdwig eiovdnw. Bgfdny qe kddwtk qjnkqpsmev ba pz tzm roohwz at xoexghzr kkusicw izr vrlqrwxist uboedtuuznum. Pimifo Icmlv Emf DI, Lcdwig owdyzd xwd hce Ywhsmnemzh Xovm mby Cqxtsm Supacg (GUKE) oo Bdmfqclwg Bomk, Tzuhvif'a ocyetzqofifo ositjm. Rcm a lqys ce oie vzav wr Vpt 8, lpq gzclqab mekxabnittq tjr Ymdavn fihog cjgbhvnstkgds. Zm psqikmp o iuejqf jf lmoviiicqg aoj jdsvkavs Uzreiz qdpzmdg, dnutgrdny bts helpar jf lpq pjmtm, mb zlwkffjmwktoiiuix avczqzs ohsb ocplv nuby swbfwigk naf ohw Mzwbms umqcifm. Mtoej bts raj pq kjrcmp oo tzm Zooigvmz Khqauqvl Dincmalwdm, rhwzq vz cjmmhzd gvq ca tzm rwmsl lqgdgfa rcm a kbafzd-hzaumae kaakulmd, hce SKQ. Wi 1948 Tmzubb jgqzsy Msf Zsrmsv'e Qjmhcfwig Dincmalwdm vt Eizqcekbqf Pnadqfnilg, ivzrw pq onsaafsy if bts yenmxckmwvf ca tzm Yoiczmehzr uwydptwze oid tmoohe avfsmekbqr dn eifvzmsbuqvl tqazjgq. Pq kmolm m dvpwz ab ohw ktshiuix pvsaa at hojxtcbefmewn, afl bfzdakfsy okkuzgalqzu xhwuuqvl jmmqoigve gpcz ie hce Tmxcpsgd-Lvvbgbubnkq zqoxtawz, kciup isme xqdgo otaqfqev qz hce 1960k. Bgfdny'a tchokmjivlabk fzsmtfsy if i ofdmavmz krgaqqptawz wi 1952, wzmz vjmgaqlpad iohn wwzq goidt uzgeyix wi tzm Gbdtwl Wwigvwy. Vz aukqdoev bdsvtemzh rilp rshadm tcmmgvqg (xhwuuqvl uiehmalqab) vs sv mzoejvmhdvw ba dmikwz. Hpravs rdev qz 1954, xpsl whsm tow iszkk jqtjrw pug 42id tqdhcdsg, rfjm ugmbddw xawnofqzu. Vn avcizsl lqhzreqzsy tzif vds vmmhc wsa eidcalq; vds ewfvzr svp gjmw wfvzrk jqzdenmp vds vmmhc wsa mqxivmzhvl. Gv 10 Esktwunsm 2009, fgtxcrifo mb Dnlmdbzt uiydviyv, Nfdtaat Dmiem Ywiikbqf Bojlab Wrgez avdw iz cafakuog pmjxwx ahwxcby gv nscadn at ohw Jdwoikp scqejvysit xwd "hce sxboglavs kvy zm ion tjmmhzd." Sa at Haq 2012 i bfdvsbq azmtmd'g widt ion bwnafz tzm Tcpsw wr Zjrva ivdcz eaigd yzmbo Tmzubb a kbmhptgzk dvrvwz wa efiohzd."""

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    """
    # The null cipher programs have been cut from the book.
    def test_nullCipherModule(self):
        import nullCipher
        encrypted = nullCipher.encryptMessage('5031', FOX_MESSAGE)
        decrypted = nullCipher.decryptMessage('5031', encrypted)
        self.assertEqual(FOX_MESSAGE, decrypted)
    """
if __name__ == '__main__':
    TEST_ALL = True

    if not TEST_ALL:
        customSuite = unittest.TestSuite()
        #customSuite.addTest(CodeHackerPyLint('test_rabinMillerPy'))
        customSuite.addTest(CodeBreakerUnitTests('test_simpleSubHackerProgram'))
        unittest.TextTestRunner().run(customSuite)
    elif TEST_ALL:
        unittest.main()
