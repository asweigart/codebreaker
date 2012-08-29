import unittest, subprocess, pyperclip, hashlib, os

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

def checkForText(filename, text):
    fp = open(filename)
    content = fp.read()
    fp.close()

    return text in content


class CodeBreakerPyLint(unittest.TestCase):
    def runPylintOnFile(self, filename):
        proc = subprocess.Popen('run_pylint.bat %s"' % (filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')
        self.assertEqual(procOut, '') # no output means success

    def test_caesarCipherPy(self):
        self.runPylintOnFile('caesarCipher.py')

    def test_caesarBreakerPy(self):
        self.runPylintOnFile('caesarBreaker.py')

    def test_transpositionEncryptPy(self):
        self.runPylintOnFile('transpositionEncrypt.py')

    def test_transpositionDecryptPy(self):
        self.runPylintOnFile('transpositionDecrypt.py')

    def test_transpositionFileCipherPy(self):
        self.runPylintOnFile('transpositionFileCipher.py')

    def test_transpositionBreakerPy(self):
        self.runPylintOnFile('transpositionBreaker.py')

    def test_transpositionFileBreakerPy(self):
        self.runPylintOnFile('transpositionFileBreaker.py')

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

    def test_affineBreakerPy(self):
        self.runPylintOnFile('affineBreaker.py')

    def test_simpleSubCipherPy(self):
        self.runPylintOnFile('simpleSubCipher.py')

    def test_simpleSubBreakerPy(self):
        self.runPylintOnFile('simpleSubBreaker.py')

    def test_simpleSubKeywordPy(self):
        self.runPylintOnFile('simpleSubKeyword.py')

    def test_simpleSubDictionaryBreakerPy(self):
        self.runPylintOnFile('simpleSubDictionaryBreaker.py')

    def test_nullCipherPy(self):
        self.runPylintOnFile('nullCipher.py')

    def test_nullBreakerPy(self):
        self.runPylintOnFile('nullBreaker.py')

    def test_vigenereCipherPy(self):
        self.runPylintOnFile('vigenereCipher.py')

    def test_vigenereBreakerrPy(self):
        self.runPylintOnFile('vigenereBreaker.py')

    def test_freqFinderPy(self):
        self.runPylintOnFile('freqFinder.py')

    def test_primeSievePy(self):
        self.runPylintOnFile('primeSieve.py')

    def test_rabinMillerPy(self):
        self.runPylintOnFile('rabinMiller.py')

    def test_makeRsaKeysPy(self):
        self.runPylintOnFile('makeRsaKeys.py')

    def test_rsaCipherPy(self):
        self.runPylintOnFile('rsaCipher.py')

    def test_pyperclipPy(self):
        self.runPylintOnFile('pyperclip.py')


class CodeBreakerUnitTests(unittest.TestCase):
    def test_caesarCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe caesarCipher.py', stdout=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # check that it is encrypting the right string
        self.assertTrue(checkForText('caesarCipher.py', "message = 'This is my secret message.'"))

        # This string is 'This is my secret message.' encrypted with key 13
        self.assertEqual(procOut, 'GUVF VF ZL FRPERG ZRFFNTR.\n')
        self.assertEqual(pyperclip.paste().decode('ascii'), 'GUVF VF ZL FRPERG ZRFFNTR.')


    def test_caesarBreakerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe caesarBreaker.py', stdout=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # check that it is encrypting the right string
        self.assertTrue(checkForText('caesarBreaker.py', "message = 'GUVF VF ZL FRPERG ZRFFNTR.'"))

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

    def test_transpositionBreakerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionBreaker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        # Make sure output is correct
        expectedOutput = """Breaking...
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

Possible encryption break:
Key 10: Charles Babbage, FRS (26 December 1791 - 18 October 1871) was an English mathematician, philosopher,

Enter D for done, or just press Enter to continue breaking:
> Copying broken ciphertext to clipboard:
Charles Babbage, FRS (26 December 1791 - 18 October 1871) was an English mathematician, philosopher, inventor and mechanical engineer who originated the concept of a programmable computer. Considered a "father of the computer", Babbage is credited with inventing the first mechanical computer that eventually led to more complex designs. Parts of his uncompleted mechanisms are on display in the London Science Museum. In 1991, a perfectly functioning difference engine was constructed from Babbage's original plans. Built to tolerances achievable in the 19th century, the success of the finished engine indicated that Babbage's machine would have worked. Nine years later, the Science Museum completed the printer Babbage had designed for the difference engine.
"""

        expectedClipboard = """Charles Babbage, FRS (26 December 1791 - 18 October 1871) was an English mathematician, philosopher, inventor and mechanical engineer who originated the concept of a programmable computer. Considered a "father of the computer", Babbage is credited with inventing the first mechanical computer that eventually led to more complex designs. Parts of his uncompleted mechanisms are on display in the London Science Museum. In 1991, a perfectly functioning difference engine was constructed from Babbage's original plans. Built to tolerances achievable in the 19th century, the success of the finished engine indicated that Babbage's machine would have worked. Nine years later, the Science Museum completed the printer Babbage had designed for the difference engine."""

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    def test_frankensteinTextFile(self):
        fp = open('frankenstein.txt')
        content = fp.read()
        fp.close()
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


    def test_transpositionFileBreakerProgram(self):
        if not os.path.exists('frankenstein.encrypted.txt'):
            # Make the encrypted file by running this test:
            self.test_transpositionFileCipherProgram()

        proc = subprocess.Popen('c:\\python32\\python.exe transpositionFileBreaker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedOutputPiece1 = """Breaking...
(Press Ctrl-C or Ctrl-D to quit at any time.)
"""
        expectedOutputPiece2 = """Key 10: Project Gutenberg's Frankenstein, by Mary Wollstonecraft (Godwin) Shelley

This eBook is for the use

Enter D for done, or just press Enter to continue:
> Writing decrypted text to frankenstein.decrypted.txt."""
        self.assertTrue(expectedOutputPiece1 in procOut)
        self.assertTrue(expectedOutputPiece2 in procOut)
        for i in range(1, 11):
            self.assertTrue('Trying key #%s... Key test time:' % (i) in procOut)


    def test_transpositionTestProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe transpositionTest.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        # Technically the seed is set to 42, so the output should be predictable.
        # But I'll just check for the "test passed" string in the output.

        self.assertTrue('Transposition cipher test passed.' in procOut)


    def test_detectEnglishProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe detectEnglish.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = 'Testing the English detection module...\nThe quick brown fox jumped over the yellow lazy dog.\n\tTrue\n\nHello there. lkjjfldsf dsafk alf ewfewlfjl efa\n\tTrue\n\nSumimasen. Kore wa nan desu ka?\n\tFalse\n\n1100010110010111001011110000\n\tFalse\n\n'

        self.assertEqual(procOut, expectedOutput)


    def test_affineCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe affineCipher.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedClipboard = 'H RZPEDYBO NZDKW WBTBOIB YZ MB RHKKBW VUYBKKVLBUY VG VY RZDKW WBRBVIB H QDPHU VUYZ MBKVBIVUL YQHY VY NHT QDPHU. -HKHU YDOVUL'

        self.assertEqual(procOut, 'Encrypted text:\nH RZPEDYBO NZDKW WBTBOIB YZ MB RHKKBW VUYBKKVLBUY VG VY RZDKW WBRBVIB H QDPHU VUYZ MBKVBIVUL YQHY VY NHT QDPHU. -HKHU YDOVUL\nFull encrypted text copied to clipboard.\n')
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    def test_affineCipherModule(self):
        import affineCipher

        encrypted = affineCipher.encryptMessage(5, 23, FOX_MESSAGE)
        decrypted = affineCipher.decryptMessage(5, 23, encrypted)

        self.assertEqual(FOX_MESSAGE, decrypted)
        self.assertEqual(encrypted, 'OGR ZTLHV CEPDK WPI QTFURM PYRE OGR NRAAPD AXSN MPB.')

        # Test with bad keys:
        self.assertRaises(SystemExit, affineCipher.encryptMessage, 1, 23, FOX_MESSAGE)
        self.assertRaises(SystemExit, affineCipher.encryptMessage, 5, 0, FOX_MESSAGE)
        self.assertRaises(SystemExit, affineCipher.encryptMessage, 26, 23, FOX_MESSAGE)
        self.assertRaises(SystemExit, affineCipher.encryptMessage, 26, 23, FOX_MESSAGE)




    def test_affineBreakerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe affineBreaker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedOutput = 'Breaking...\n(Press Ctrl-C or Ctrl-D to quit at any time.)\nTried KeyA 1, KeyB 0... (H RZPEDYBO NZDKW WBTBOIB YZ MB RHKKBW VU)\nTried KeyA 1, KeyB 1... (G QYODCXAN MYCJV VASANHA XY LA QGJJAV UT)\nTried KeyA 1, KeyB 2... (F PXNCBWZM LXBIU UZRZMGZ WX KZ PFIIZU TS)\nTried KeyA 1, KeyB 3... (E OWMBAVYL KWAHT TYQYLFY VW JY OEHHYT SR)\nTried KeyA 1, KeyB 4... (D NVLAZUXK JVZGS SXPXKEX UV IX NDGGXS RQ)\nTried KeyA 1, KeyB 5... (C MUKZYTWJ IUYFR RWOWJDW TU HW MCFFWR QP)\nTried KeyA 1, KeyB 6... (B LTJYXSVI HTXEQ QVNVICV ST GV LBEEVQ PO)\nTried KeyA 1, KeyB 7... (A KSIXWRUH GSWDP PUMUHBU RS FU KADDUP ON)\nTried KeyA 1, KeyB 8... (Z JRHWVQTG FRVCO OTLTGAT QR ET JZCCTO NM)\nTried KeyA 1, KeyB 9... (Y IQGVUPSF EQUBN NSKSFZS PQ DS IYBBSN ML)\nTried KeyA 1, KeyB 10... (X HPFUTORE DPTAM MRJREYR OP CR HXAARM LK)\nTried KeyA 1, KeyB 11... (W GOETSNQD COSZL LQIQDXQ NO BQ GWZZQL KJ)\nTried KeyA 1, KeyB 12... (V FNDSRMPC BNRYK KPHPCWP MN AP FVYYPK JI)\nTried KeyA 1, KeyB 13... (U EMCRQLOB AMQXJ JOGOBVO LM ZO EUXXOJ IH)\nTried KeyA 1, KeyB 14... (T DLBQPKNA ZLPWI INFNAUN KL YN DTWWNI HG)\nTried KeyA 1, KeyB 15... (S CKAPOJMZ YKOVH HMEMZTM JK XM CSVVMH GF)\nTried KeyA 1, KeyB 16... (R BJZONILY XJNUG GLDLYSL IJ WL BRUULG FE)\nTried KeyA 1, KeyB 17... (Q AIYNMHKX WIMTF FKCKXRK HI VK AQTTKF ED)\nTried KeyA 1, KeyB 18... (P ZHXMLGJW VHLSE EJBJWQJ GH UJ ZPSSJE DC)\nTried KeyA 1, KeyB 19... (O YGWLKFIV UGKRD DIAIVPI FG TI YORRID CB)\nTried KeyA 1, KeyB 20... (N XFVKJEHU TFJQC CHZHUOH EF SH XNQQHC BA)\nTried KeyA 1, KeyB 21... (M WEUJIDGT SEIPB BGYGTNG DE RG WMPPGB AZ)\nTried KeyA 1, KeyB 22... (L VDTIHCFS RDHOA AFXFSMF CD QF VLOOFA ZY)\nTried KeyA 1, KeyB 23... (K UCSHGBER QCGNZ ZEWERLE BC PE UKNNEZ YX)\nTried KeyA 1, KeyB 24... (J TBRGFADQ PBFMY YDVDQKD AB OD TJMMDY XW)\nTried KeyA 1, KeyB 25... (I SAQFEZCP OAELX XCUCPJC ZA NC SILLCX WV)\nTried KeyA 3, KeyB 0... (L XRFKBIJW NRBMQ QJPJWUJ IR EJ XLMMJQ HY)\nTried KeyA 3, KeyB 1... (C OIWBSZAN EISDH HAGANLA ZI VA OCDDAH YP)\nTried KeyA 3, KeyB 2... (T FZNSJQRE VZJUY YRXRECR QZ MR FTUURY PG)\nTried KeyA 3, KeyB 3... (K WQEJAHIV MQALP PIOIVTI HQ DI WKLLIP GX)\nTried KeyA 3, KeyB 4... (B NHVARYZM DHRCG GZFZMKZ YH UZ NBCCZG XO)\nTried KeyA 3, KeyB 5... (S EYMRIPQD UYITX XQWQDBQ PY LQ ESTTQX OF)\nTried KeyA 3, KeyB 6... (J VPDIZGHU LPZKO OHNHUSH GP CH VJKKHO FW)\nTried KeyA 3, KeyB 7... (A MGUZQXYL CGQBF FYEYLJY XG TY MABBYF WN)\nTried KeyA 3, KeyB 8... (R DXLQHOPC TXHSW WPVPCAP OX KP DRSSPW NE)\nTried KeyA 3, KeyB 9... (I UOCHYFGT KOYJN NGMGTRG FO BG UIJJGN EV)\nTried KeyA 3, KeyB 10... (Z LFTYPWXK BFPAE EXDXKIX WF SX LZAAXE VM)\nTried KeyA 3, KeyB 11... (Q CWKPGNOB SWGRV VOUOBZO NW JO CQRROV MD)\nTried KeyA 3, KeyB 12... (H TNBGXEFS JNXIM MFLFSQF EN AF THIIFM DU)\nTried KeyA 3, KeyB 13... (Y KESXOVWJ AEOZD DWCWJHW VE RW KYZZWD UL)\nTried KeyA 3, KeyB 14... (P BVJOFMNA RVFQU UNTNAYN MV IN BPQQNU LC)\nTried KeyA 3, KeyB 15... (G SMAFWDER IMWHL LEKERPE DM ZE SGHHEL CT)\nTried KeyA 3, KeyB 16... (X JDRWNUVI ZDNYC CVBVIGV UD QV JXYYVC TK)\nTried KeyA 3, KeyB 17... (O AUINELMZ QUEPT TMSMZXM LU HM AOPPMT KB)\nTried KeyA 3, KeyB 18... (F RLZEVCDQ HLVGK KDJDQOD CL YD RFGGDK BS)\nTried KeyA 3, KeyB 19... (W ICQVMTUH YCMXB BUAUHFU TC PU IWXXUB SJ)\nTried KeyA 3, KeyB 20... (N ZTHMDKLY PTDOS SLRLYWL KT GL ZNOOLS JA)\nTried KeyA 3, KeyB 21... (E QKYDUBCP GKUFJ JCICPNC BK XC QEFFCJ AR)\nTried KeyA 3, KeyB 22... (V HBPULSTG XBLWA ATZTGET SB OT HVWWTA RI)\nTried KeyA 3, KeyB 23... (M YSGLCJKX OSCNR RKQKXVK JS FK YMNNKR IZ)\nTried KeyA 3, KeyB 24... (D PJXCTABO FJTEI IBHBOMB AJ WB PDEEBI ZQ)\nTried KeyA 3, KeyB 25... (U GAOTKRSF WAKVZ ZSYSFDS RA NS GUVVSZ QH)\nTried KeyA 5, KeyB 0... (R TFDGLKVI NFLCU UVJVIMV KF SV TRCCVU ZE)\nTried KeyA 5, KeyB 1... (W YKILQPAN SKQHZ ZAOANRA PK XA YWHHAZ EJ)\nTried KeyA 5, KeyB 2... (B DPNQVUFS XPVME EFTFSWF UP CF DBMMFE JO)\nTried KeyA 5, KeyB 3... (G IUSVAZKX CUARJ JKYKXBK ZU HK IGRRKJ OT)\nTried KeyA 5, KeyB 4... (L NZXAFEPC HZFWO OPDPCGP EZ MP NLWWPO TY)\nTried KeyA 5, KeyB 5... (Q SECFKJUH MEKBT TUIUHLU JE RU SQBBUT YD)\nTried KeyA 5, KeyB 6... (V XJHKPOZM RJPGY YZNZMQZ OJ WZ XVGGZY DI)\nTried KeyA 5, KeyB 7... (A COMPUTER WOULD DESERVE TO BE CALLED IN)\n\nPossible encryption break:\nKeyA: 5, KeyB: 7\nDecrypted message: A COMPUTER WOULD DESERVE TO BE CALLED INTELLIGENT IF IT COULD DECEIVE A HUMAN INTO BELIEVING THAT IT WAS HUMAN. -ALAN TURING\n\nEnter D for done, or just press Enter to continue breaking:\n> Copying broken ciphertext to clipboard:\nA COMPUTER WOULD DESERVE TO BE CALLED INTELLIGENT IF IT COULD DECEIVE A HUMAN INTO BELIEVING THAT IT WAS HUMAN. -ALAN TURING\n'
        expectedClipboard = 'A COMPUTER WOULD DESERVE TO BE CALLED INTELLIGENT IF IT COULD DECEIVE A HUMAN INTO BELIEVING THAT IT WAS HUMAN. -ALAN TURING'

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)


    def test_simpleSubCipherProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubCipher.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedClipboard = 'SY L NLX SR PYYACAO L YLWJ EISWI UPAR LULSXRJ ISR SXRJSXWJR, IA ESMM RWCTJSXSZA SJ WMPRAMH, LXO TXMARR JIA AQSOAXWA SR PQACEIAMNSXU, IA ESMM CAYTRA JP FAMSAQA SJ. SY, PX JIA PJIAC ILXO, IA SR PYYACAO RPNAJISXU EISWI LYYPCOR L CALRPX YPC LWJSXU SX LWWPCOLXWA JP ISR SXRJSXWJR, IA ESMM LWWABJ SJ AQAX PX JIA RMSUIJARJ AQSOAXWA. JIA PCSUSX PY NHJIR SR AGBMLSXAO SX JISR ELH. -FACJCLXO CTRRAMM'

        expectedOutput = 'The encrypted message is:\nSY L NLX SR PYYACAO L YLWJ EISWI UPAR LULSXRJ ISR SXRJSXWJR, IA ESMM RWCTJSXSZA SJ WMPRAMH, LXO TXMARR JIA AQSOAXWA SR PQACEIAMNSXU, IA ESMM CAYTRA JP FAMSAQA SJ. SY, PX JIA PJIAC ILXO, IA SR PYYACAO RPNAJISXU EISWI LYYPCOR L CALRPX YPC LWJSXU SX LWWPCOLXWA JP ISR SXRJSXWJR, IA ESMM LWWABJ SJ AQAX PX JIA RMSUIJARJ AQSOAXWA. JIA PCSUSX PY NHJIR SR AGBMLSXAO SX JISR ELH. -FACJCLXO CTRRAMM\n\nThis message has been copied to the clipboard.\n'

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


    def test_simpleSubBreakerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubBreaker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = 'Breaking...\n(Press Ctrl-C or Ctrl-D to quit at any time.)\nDone.\n\nMapping:\n    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z\n    = = = = = = = = = = = = = = = = = = = = = = = = = =\n    E B R   K B B B H T   A L M D O V S I U G   C N F Z \n      W     W P Q K                                     \n      P         X P                                     \n                Y W                                     \n                P X                                     \n                W Y                                     \n                                                        \n\nOriginal ciphertext:\nSY L NLX SR PYYACAO L YLWJ EISWI UPAR LULSXRJ ISR SXRJSXWJR, IA ESMM RWCTJSXSZA SJ WMPRAMH, LXO TXMARR JIA AQSOAXWA SR PQACEIAMNSXU, IA ESMM CAYTRA JP FAMSAQA SJ. SY, PX JIA PJIAC ILXO, IA SR PYYACAO RPNAJISXU EISWI LYYPCOR L CALRPX YPC LWJSXU SX LWWPCOLXWA JP ISR SXRJSXWJR, IA ESMM LWWABJ SJ AQAX PX JIA RMSUIJARJ AQSOAXWA. JIA PCSUSX PY NHJIR SR AGBMLSXAO SX JISR ELH. -FACJCLXO CTRRAMM\n\nBroken ciphertext:\nIF A MAN IS OFFERED A FACT _HICH GOES AGAINST HIS INSTINCTS, HE _ILL SCRUTINIZE IT CLOSEL_, AND UNLESS THE EVIDENCE IS OVER_HELMING, HE _ILL REFUSE TO _ELIEVE IT. IF, ON THE OTHER HAND, HE IS OFFERED SOMETHING _HICH AFFORDS A REASON FOR ACTING IN ACCORDANCE TO HIS INSTINCTS, HE _ILL ACCE_T IT EVEN ON THE SLIGHTEST EVIDENCE. THE ORIGIN OF M_THS IS E__LAINED IN THIS _A_. -_ERTRAND RUSSELL\n\n'

        self.assertEqual(procOut, expectedOutput)


    def test_simpleSubKeywordProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubKeyword.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = 'The key used is:\nALPHNUMERICBDFGJKOQSTVWXYZ\nThe encrypted message is:\nYGTO PGVNO RQ LBGWF.\n\nThis message has been copied to the clipboard.\n'
        expectedClipboard = """YGTO PGVNO RQ LBGWF."""

        self.assertEqual(procOut, expectedOutput)
        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    def test_simpleSubKeywordModule(self):
        import simpleSubKeyword

        encrypted = simpleSubKeyword.encryptMessage('hello', FOX_MESSAGE)
        decrypted = simpleSubKeyword.decryptMessage('hello', encrypted)
        encrypted2= simpleSubKeyword.encryptMessage('howdy', FOX_MESSAGE)

        self.assertEqual(FOX_MESSAGE, decrypted)
        self.assertNotEqual(encrypted, encrypted2)

    def test_nullBreakerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe nullBreaker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedClipboard = 'When I use a word, it means just what I choose it to mean -- neither more nor less.'

        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)

    def test_simpleSubDictionaryBreakerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe simpleSubDictionaryBreaker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
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

    def test_vigenereBreakerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe vigenereBreaker.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate('D\n'.encode('ascii'))[0].decode('ascii')

        expectedClipboard = """ALAN MATHISON TURING WAS A BRITISH MATHEMATICIAN, LOGICIAN, CRYPTANALYST, AND COMPUTER SCIENTIST. HE WAS HIGHLY INFLUENTIAL IN THE DEVELOPMENT OF COMPUTER SCIENCE, PROVIDING A FORMALISATION OF THE CONCEPTS OF "ALGORITHM" AND "COMPUTATION" WITH THE TURING MACHINE. TURING IS WIDELY CONSIDERED TO BE THE FATHER OF COMPUTER SCIENCE AND ARTIFICIAL INTELLIGENCE. DURING WORLD WAR II, TURING WORKED FOR THE GOVERNMENT CODE AND CYPHER SCHOOL (GCCS) AT BLETCHLEY PARK, BRITAIN'S CODEBREAKING CENTRE. FOR A TIME HE WAS HEAD OF HUT 8, THE SECTION RESPONSIBLE FOR GERMAN NAVAL CRYPTANALYSIS. HE DEVISED A NUMBER OF TECHNIQUES FOR BREAKING GERMAN CIPHERS, INCLUDING THE METHOD OF THE BOMBE, AN ELECTROMECHANICAL MACHINE THAT COULD FIND SETTINGS FOR THE ENIGMA MACHINE. AFTER THE WAR HE WORKED AT THE NATIONAL PHYSICAL LABORATORY, WHERE HE CREATED ONE OF THE FIRST DESIGNS FOR A STORED-PROGRAM COMPUTER, THE ACE. IN 1948 TURING JOINED MAX NEWMAN'S COMPUTING LABORATORY AT MANCHESTER UNIVERSITY, WHERE HE ASSISTED IN THE DEVELOPMENT OF THE MANCHESTER COMPUTERS AND BECAME INTERESTED IN MATHEMATICAL BIOLOGY. HE WROTE A PAPER ON THE CHEMICAL BASIS OF MORPHOGENESIS, AND PREDICTED OSCILLATING CHEMICAL REACTIONS SUCH AS THE BELOUSOV-ZHABOTINSKY REACTION, WHICH WERE FIRST OBSERVED IN THE 1960S. TURING'S HOMOSEXUALITY RESULTED IN A CRIMINAL PROSECUTION IN 1952, WHEN HOMOSEXUAL ACTS WERE STILL ILLEGAL IN THE UNITED KINGDOM. HE ACCEPTED TREATMENT WITH FEMALE HORMONES (CHEMICAL CASTRATION) AS AN ALTERNATIVE TO PRISON. TURING DIED IN 1954, JUST OVER TWO WEEKS BEFORE HIS 42ND BIRTHDAY, FROM CYANIDE POISONING. AN INQUEST DETERMINED THAT HIS DEATH WAS SUICIDE; HIS MOTHER AND SOME OTHERS BELIEVED HIS DEATH WAS ACCIDENTAL. ON 10 SEPTEMBER 2009, FOLLOWING AN INTERNET CAMPAIGN, BRITISH PRIME MINISTER GORDON BROWN MADE AN OFFICIAL PUBLIC APOLOGY ON BEHALF OF THE BRITISH GOVERNMENT FOR "THE APPALLING WAY HE WAS TREATED." AS OF MAY 2012 A PRIVATE MEMBER'S BILL WAS BEFORE THE HOUSE OF LORDS WHICH WOULD GRANT TURING A STATUTORY PARDON IF ENACTED."""
        expectedOutput = 'Determining most likely key lengths with Kasiski Examination...\nKasiski Examination results say the most likely key lengths are: 3 2 6 4 12 \n\nPossible letters for letter 1 of the key: A L M \nPossible letters for letter 2 of the key: S N O \nPossible letters for letter 3 of the key: V I Z \nAttempting with key: ASV\nAttempting with key: ASI\nAttempting with key: ASZ\nAttempting with key: ANV\nAttempting with key: ANI\nAttempting with key: ANZ\nAttempting with key: AOV\nAttempting with key: AOI\nAttempting with key: AOZ\nAttempting with key: LSV\nAttempting with key: LSI\nAttempting with key: LSZ\nAttempting with key: LNV\nAttempting with key: LNI\nAttempting with key: LNZ\nAttempting with key: LOV\nAttempting with key: LOI\nAttempting with key: LOZ\nAttempting with key: MSV\nAttempting with key: MSI\nAttempting with key: MSZ\nAttempting with key: MNV\nAttempting with key: MNI\nAttempting with key: MNZ\nAttempting with key: MOV\nAttempting with key: MOI\nAttempting with key: MOZ\nPossible letters for letter 1 of the key: O A E \nPossible letters for letter 2 of the key: M S I \nAttempting with key: OM\nAttempting with key: OS\nAttempting with key: OI\nAttempting with key: AM\nAttempting with key: AS\nAttempting with key: AI\nAttempting with key: EM\nAttempting with key: ES\nAttempting with key: EI\nPossible letters for letter 1 of the key: A E O \nPossible letters for letter 2 of the key: S D G \nPossible letters for letter 3 of the key: I V X \nPossible letters for letter 4 of the key: M Z Q \nPossible letters for letter 5 of the key: O B Z \nPossible letters for letter 6 of the key: V I K \nAttempting with key: ASIMOV\n\nPossible encryption break:\nKey ASIMOV: ALAN MATHISON TURING WAS A BRITISH MATHEMATICIAN, LOGICIAN, CRYPTANALYST, AND COMPUTER SCIENTIST. HE WAS HIGHLY INFLUENTIAL IN THE DEVELOPMENT OF COMPUTER SCIENCE, PROVIDING A FORMALISATION OF THE CON\n\nEnter D for done, or just press Enter to continue breaking:\n> Copying broken ciphertext to clipboard:\nALAN MATHISON TURING WAS A BRITISH MATHEMATICIAN, LOGICIAN, CRYPTANALYST, AND COMPUTER SCIENTIST. HE WAS HIGHLY INFLUENTIAL IN THE DEVELOPMENT OF COMPUTER SCIENCE, PROVIDING A FORMALISATION OF THE CONCEPTS OF "ALGORITHM" AND "COMPUTATION" WITH THE TURING MACHINE. TURING IS WIDELY CONSIDERED TO BE THE FATHER OF COMPUTER SCIENCE AND ARTIFICIAL INTELLIGENCE. DURING WORLD WAR II, TURING WORKED FOR THE GOVERNMENT CODE AND CYPHER SCHOOL (GCCS) AT BLETCHLEY PARK, BRITAIN\'S CODEBREAKING CENTRE. FOR A TIME HE WAS HEAD OF HUT 8, THE SECTION RESPONSIBLE FOR GERMAN NAVAL CRYPTANALYSIS. HE DEVISED A NUMBER OF TECHNIQUES FOR BREAKING GERMAN CIPHERS, INCLUDING THE METHOD OF THE BOMBE, AN ELECTROMECHANICAL MACHINE THAT COULD FIND SETTINGS FOR THE ENIGMA MACHINE. AFTER THE WAR HE WORKED AT THE NATIONAL PHYSICAL LABORATORY, WHERE HE CREATED ONE OF THE FIRST DESIGNS FOR A STORED-PROGRAM COMPUTER, THE ACE. IN 1948 TURING JOINED MAX NEWMAN\'S COMPUTING LABORATORY AT MANCHESTER UNIVERSITY, WHERE HE ASSISTED IN THE DEVELOPMENT OF THE MANCHESTER COMPUTERS AND BECAME INTERESTED IN MATHEMATICAL BIOLOGY. HE WROTE A PAPER ON THE CHEMICAL BASIS OF MORPHOGENESIS, AND PREDICTED OSCILLATING CHEMICAL REACTIONS SUCH AS THE BELOUSOV-ZHABOTINSKY REACTION, WHICH WERE FIRST OBSERVED IN THE 1960S. TURING\'S HOMOSEXUALITY RESULTED IN A CRIMINAL PROSECUTION IN 1952, WHEN HOMOSEXUAL ACTS WERE STILL ILLEGAL IN THE UNITED KINGDOM. HE ACCEPTED TREATMENT WITH FEMALE HORMONES (CHEMICAL CASTRATION) AS AN ALTERNATIVE TO PRISON. TURING DIED IN 1954, JUST OVER TWO WEEKS BEFORE HIS 42ND BIRTHDAY, FROM CYANIDE POISONING. AN INQUEST DETERMINED THAT HIS DEATH WAS SUICIDE; HIS MOTHER AND SOME OTHERS BELIEVED HIS DEATH WAS ACCIDENTAL. ON 10 SEPTEMBER 2009, FOLLOWING AN INTERNET CAMPAIGN, BRITISH PRIME MINISTER GORDON BROWN MADE AN OFFICIAL PUBLIC APOLOGY ON BEHALF OF THE BRITISH GOVERNMENT FOR "THE APPALLING WAY HE WAS TREATED." AS OF MAY 2012 A PRIVATE MEMBER\'S BILL WAS BEFORE THE HOUSE OF LORDS WHICH WOULD GRANT TURING A STATUTORY PARDON IF ENACTED.\n'

        self.assertEqual(pyperclip.paste().decode('ascii'), expectedClipboard)
        self.assertEqual(procOut, expectedOutput)


    def test_freqFinderProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe freqFinder.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = '12\nShakespeare\'s Sonnet #29\nWHEN, IN DISGRACE WITH FORTUNE AND MEN\'S EYES,\nI ALL ALONE BEWEEP MY OUTCAST STATE,\nAND TROUBLE DEAF HEAVEN WITH MY BOOTLESS CRIES,\nAND LOOK UPON MYSELF AND CURSE MY FATE,\nWISHING ME LIKE TO ONE MORE RICH IN HOPE,\nFEATURED LIKE HIM, LIKE HIM WITH FRIENDS POSSESSED,\nDESIRING THIS MAN\'S ART, AND THAT MAN\'S SCOPE,\nWITH WHAT I MOST ENJOY CONTENTED LEAST,\nYET IN THESE THOUGHTS MYSELF ALMOST DESPISING,\nHAPLY I THINK ON THEE, AND THEN MY STATE,\nLIKE TO THE LARK AT BREAK OF DAY ARISING\nFROM SULLEN EARTH, SINGS HYMNS AT HEAVEN\'S GATE\n\nFOR THY SWEET LOVE REMEMBERED SUCH WEALTH BRINGS,\nTHAT THEN I SCORN TO CHANGE MY STATE WITH KINGS.\n\nLetter Frequencies of Sonnet #29:\n{\'A\': 37, \'C\': 10, \'B\': 6, \'E\': 66, \'D\': 16, \'G\': 11, \'F\': 10, \'I\': 35, \'H\': 32, \'K\': 9, \'J\': 1, \'M\': 20, \'L\': 20, \'O\': 28, \'N\': 38, \'Q\': 0, \'P\': 7, \'S\': 42, \'R\': 21, \'U\': 9, \'T\': 49, \'W\': 11, \'V\': 3, \'Y\': 14, \'X\': 0, \'Z\': 0}\n\nFrequency score of Sonnet #29:\n10\n\nFrequency score of Scrambled Sonnet #29:\n10\n\nFrequency score of Lorem Ipsum text:\n4\n\nFrequency score of alphabet:\n0\n\nFrequency score of alphabet x 100:\n0\n\nFrequency score of "AAAAAAAAAAAAAAAH":\n1\n\nFrequency score of "VDIUFRFDSFEWAFDSAFLKHFDSALKFA":\n1\n\n'

        self.assertEqual(procOut, expectedOutput)


    def test_primeSieveProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe primeSieve.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = '  2 is prime: True\n  5 is prime: True\n 11 is prime: True\n 16 is prime: False\n 17 is prime: True\n101 is prime: True\n126 is prime: False\n147 is prime: False\n\n  2 is prime: True\n  5 is prime: True\n 11 is prime: True\n 16 is prime: False\n 17 is prime: True\n101 is prime: True\n126 is prime: False\n147 is prime: False\n\nTesting if both functions are consistent with each other...\nTest Passed: Both functions are consistent with each other.\n'
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


    def test_rabinMillerProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe rabinMiller.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        expectedOutput = 'Example prime testing:\n2 is prime: True\n3 is prime: True\n5 is prime: True\n10 is prime: False\n100 is prime: False\n101 is prime: True\n5099806053 is prime: False\n5099806057 is prime: True\n'
        self.assertEqual(procOut, expectedOutput)

    def test_rabinMillerModule(self):
        import rabinMiller, random

        self.assertTrue(rabinMiller.isPrime(2))
        self.assertTrue(rabinMiller.isPrime(17))
        self.assertTrue(rabinMiller.isPrime(37))
        self.assertFalse(rabinMiller.isPrime(20))
        self.assertFalse(rabinMiller.isPrime(1))
        self.assertFalse(rabinMiller.isPrime(0))
        self.assertFalse(rabinMiller.isPrime(-1))
        self.assertFalse(rabinMiller.isPrime(5099806053))
        self.assertTrue(rabinMiller.isPrime(5099806057))

        random.seed(42)
        for keySize in (32, 64, 128, 256, 512, 600, 1024):
            prime = rabinMiller.generateLargePrime(keySize)
            self.assertTrue(rabinMiller.isPrime(prime))

    def test_makeRsaKeysProgram(self):
        proc = subprocess.Popen('c:\\python32\\python.exe makeRsaKeys.py', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        procOut = proc.communicate()[0].decode('ascii')

        self.assertTrue('Key files made.' in procOut)

    def test_makeRsaKeysModule(self):
        import makeRsaKeys, os

        makeRsaKeys.SILENT_MODE = True

        # erase keys if they exist already
        for filename in ('unittest_pubkey.txt', 'unittest_privkey.txt'):
            if os.path.exists(filename):
                os.unlink(filename)

        makeRsaKeys.makeKeyFiles('unittest')
        self.assertTrue(os.path.exists('unittest_pubkey.txt'))
        self.assertTrue(os.path.exists('unittest_privkey.txt'))
        # Testing the format of the key files can be done with rsaCipher.readKeyFile() later

        # cleanup key files
        for filename in ('unittest_pubkey.txt', 'unittest_privkey.txt'):
            os.unlink(filename)

        for keySize in (32, 64, 128, 256, 512, 600, 1024):
            makeRsaKeys.generateKey(keySize)

    def test_cryptomathModule(self):
        import cryptomath, random
        random.seed(42)

        self.assertEqual(cryptomath.gcd(543, 526), 1)
        self.assertEqual(cryptomath.gcd(184543, 825), 1)
        self.assertEqual(cryptomath.gcd(184545, 825), 15)
        self.assertEqual(cryptomath.gcd(30594, 8302), 2)

        # create a bunch of things with expected gcds
        for i in range(500):
            a = random.randint(50, 100000)
            b = random.randint(50, 100000)
            self.assertEqual(cryptomath.gcd(a, b*a), a)

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



if __name__ == '__main__':
    TEST_ALL = False

    if not TEST_ALL:
        customSuite = unittest.TestSuite()
        customSuite.addTest(CodeBreakerUnitTests('test_cryptomathModule'))
        unittest.TextTestRunner().run(customSuite)
    elif TEST_ALL:
        unittest.main()

