# Simple Substitution Cipher, http://inventwithpython.com/codebreaker (BSD Licensed)
import pyperclip, sys, random


SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    myMessage = 'IF A MAN IS OFFERED A FACT WHICH GOES AGAINST HIS INSTINCTS, HE WILL SCRUTINIZE IT CLOSELY, AND UNLESS THE EVIDENCE IS OVERWHELMING, HE WILL REFUSE TO BELIEVE IT. IF, ON THE OTHER HAND, HE IS OFFERED SOMETHING WHICH AFFORDS A REASON FOR ACTING IN ACCORDANCE TO HIS INSTINCTS, HE WILL ACCEPT IT EVEN ON THE SLIGHTEST EVIDENCE. THE ORIGIN OF MYTHS IS EXPLAINED IN THIS WAY. -BERTRAND RUSSELL'
    #myMessage = 'eccentric assault'.upper()
    myMessage = 'SY L NLX SR PYYACAO L YLWJ EISWI UPAR LULSXRJ ISR SXRJSXWJR, IA ESMM RWCTJSXSZA SJ WMPRAMH, LXO TXMARR JIA AQSOAXWA SR PQACEIAMNSXU, IA ESMM CAYTRA JP FAMSAQA SJ. SY, PX JIA PJIAC ILXO, IA SR PYYACAO RPNAJISXU EISWI LYYPCOR L CALRPX YPC LWJSXU SX LWWPCOLXWA JP ISR SXRJSXWJR, IA ESMM LWWABJ SJ AQAX PX JIA RMSUIJARJ AQSOAXWA. JIA PCSUSX PY NHJIR SR AGBMLSXAO SX JISR ELH. -FACJCLXO CTRRAMM'
    myKey = 'LFWOAYUISVKMNXPBDCRJTQEGHZ'
    myMode = 'decrypt' # set to 'encrypt' or 'decrypt'

    if len(myKey) != len(SYMBOLS):
        sys.exit('The key must have the same number of symbols as the symbol set.')
    if len(set(myKey)) != len(myKey):
        sys.exit('The key cannot have duplicate symbols in it.')
    if len(set(SYMBOLS)) != len(SYMBOLS):
        sys.exit('The symbol set cannot have missing or duplicate symbols in it.')

    if myMode == 'encrypt':
        translated = encryptMessage(myKey, myMessage)
    elif myMode == 'decrypt':
        translated = decryptMessage(myKey, myMessage)

    print('The %sed message is:' % (myMode))
    print(translated)

    pyperclip.copy(translated)
    print()
    print('This message has been copied to the clipboard.')


def encryptMessage(key, message, decrypting=False):
    translated = ''

    SET_A = SYMBOLS
    SET_B = key
    if decrypting:
        # For decrypting, we can use the same code as encrypting. We just need to swap where the key and SYMBOLS strings are used.
        SET_A, SET_B = SET_B, SET_A


    # loop through each symbol in the message
    for symbol in message:
        symIndex = SET_A.find(symbol)

        if symIndex != -1: # found in SYMBOLS
            translated += SET_B[symIndex]
        else: # not found
            translated += symbol # do not encrypt/decrypt this symbol

    return translated


def decryptMessage(key, message):
    # Decrypting uses a lot of the same code as encrypting, so we can just wrap the encryptMessage() function (and pass True for the decrypting parameter).
    return encryptMessage(key, message, True)


def getRandomKey():
    key = list(SYMBOLS)
    random.shuffle(key)
    return ''.join(key)


if __name__ == '__main__':
    main()