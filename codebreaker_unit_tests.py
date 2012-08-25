import unittest, subprocess, pyperclip

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

    #def test_nullBreakerPy(self):
    #    self.runPylintOnFile('nullBreaker.py')

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
        correctString = """Key #0: GUVF VF ZL FRPERG ZRFFNTR.
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
        self.assertEqual(procOut, correctString)


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





if __name__ == '__main__':
    unittest.main()
