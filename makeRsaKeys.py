# RSA Key Generator
# http://inventwithpython.com/codebreaker (BSD Licensed)

import random, sys, os, rabinMiller, cryptomath

OVERWRITE_MODE = True # CAREFUL! If True, you may overwrite your old keys!
SILENT_MODE = False
DEFAULT_KEY_SIZE = 1024

def main():
    # create a public/private keypair with 1024 bit keys
    print('Making key files...')
    makeKeyFiles('al_sweigart', 1024)
    print('Key files made.')


def makeKeyFiles(name, keySize=DEFAULT_KEY_SIZE):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    # name parameter) with the the n,e and d,e integers written in them,
    # delimited by a comma.

    # Our safety check will prevent us from overwriting our old key files:
    if not OVERWRITE_MODE and (os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name))):
        sys.exit('WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or set OVERWRITE_MODE to True and re-run this program.' % (name, name))

    publicKey, privateKey = generateKey(keySize)

    if not SILENT_MODE:
        print()
        print('The public key is a %s and %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
        print()
        print('Writing public key to file %s_pubkey.txt...' % (name))
    fp = open('%s_pubkey.txt' % (name), 'w')
    fp.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fp.close()

    if not SILENT_MODE:
        print()
        print('The private key is a %s and %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
        print()
        print('Writing private key to file %s_privkey.txt...' % (name))
    fp = open('%s_privkey.txt' % (name), 'w')
    fp.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fp.close()


def generateKey(keySize=DEFAULT_KEY_SIZE):
    # Creates a public/private key pair with keys that are keySize bits in
    # size. This function may take a while to run.

    # Step 1: Create two prime numbers, p and q.
    if not SILENT_MODE:
        print('Generating p prime...')
    p = rabinMiller.generateLargePrime(keySize)
    if not SILENT_MODE:
        print('Generating q prime...')
    q = rabinMiller.generateLargePrime(keySize)

    # Step 2: Create a number e.
    if not SILENT_MODE:
        print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Come up with an e that is relatively prime to (p-1)*(q-1)
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if cryptomath.gcd(e, (p - 1) * (q - 1)) == 1:
            break
    n = p * q

    # Step 3: Get the mod inverse of e.
    if not SILENT_MODE:
        print('Calculating d that is mod inverse of e...')
    d = cryptomath.findModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    if not SILENT_MODE:
        print('Public key:')
        print(publicKey)
        print('Private key:')
        print(privateKey)

    return (publicKey, privateKey)



# If makeRsaKeys.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()