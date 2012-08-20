# RSA Key Generator
# http://inventwithpython.com/codebreaker (BSD Licensed)

import random
import rabinMiller

SILENT_MODE = False

def main():
    # create a public/private keypair with 1024 bit keys
    print('Making key files...')
    makeKeyFiles('al_sweigart', 1024)
    print('Key files made.')


def makeKeyFiles(name, keysize=1024):
    # Creates two files 'x_pubkey.txt' and 'x_privkey.txt' (where x is the
    # name parameter) with the the n,e and d,e integers written in them,
    # delimited by a comma.

    publicKey, privateKey = generateKey(keysize)

    if not SILENT_MODE:
        print()
        print('The public key is a %s and %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
        print()
        print('Writing public key to file %s_pubkey.txt...' % (name))
    fp = open('%s_pubkey.txt' % (name), 'w')
    fp.write('%s,%s' % (publicKey[0], publicKey[1]))
    fp.close()

    if not SILENT_MODE:
        print()
        print('The private key is a %s and %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
        print()
        print('Writing private key to file %s_privkey.txt...' % (name))
    fp = open('%s_privkey.txt' % (name), 'w')
    fp.write('%s,%s' % (privateKey[0], privateKey[1]))
    fp.close()


def generateKey(keysize=1024):
    # Creates a public/private key pair with keys that are keysize bits in
    # size. This function may take a while to run.

    # Step 1: Create two prime numbers, p and q.
    if not SILENT_MODE:
        print('Generating p prime...')
    p = rabinMiller.generateLargePrime(keysize)
    if not SILENT_MODE:
        print('Generating q prime...')
    q = rabinMiller.generateLargePrime(keysize)

    # Step 2: Create a number e.
    if not SILENT_MODE:
        print('Generating e that is relatively prime to (p-1)*(q-1)...')
    while True:
        # Come up with an e that is relatively prime to (p-1)*(q-1)
        e = random.randrange(2 ** (keysize - 1), 2 ** (keysize))
        if gcd(e, (p - 1) * (q - 1)) == 1:
            break
    n = p * q

    # Step 3: Get the mod inverse of e.
    if not SILENT_MODE:
        print('Calculating d that is mod inverse of e...')
    d = getModInverse(e, (p - 1) * (q - 1))

    publicKey = (n, e)
    privateKey = (n, d)

    if not SILENT_MODE:
        print('Public key:')
        print(publicKey)
        print('Private key:')
        print(privateKey)

    return (publicKey, privateKey)


def gcd(a, b):
    # Return the Greatest Common Divisor of a and b.
    while a != 0:
        a, b = b % a, a
    return b


def getModInverse(a, m):
    # Returns the modular inverse of a % m, which is
    # the number x such that a*x % m = 1

    # Calculate using the Extended Euclidean Algorithm:
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3 # // is the integer division operator
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m


if __name__ == '__main__':
    main()