import math

# isPrime is about 15 times slower than primeSieve

# have them manually check off a sieve on paper

def isPrime(num):
    # all numbers less than 2 are not prime
    if num < 2:
        return False

    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

print('  2 is prime: %s' % (isPrime(2)))
print('  5 is prime: %s' % (isPrime(5)))
print(' 11 is prime: %s' % (isPrime(11)))
print(' 16 is prime: %s' % (isPrime(16)))
print(' 17 is prime: %s' % (isPrime(17)))
print('101 is prime: %s' % (isPrime(101)))
print('126 is prime: %s' % (isPrime(126)))
print('147 is prime: %s' % (isPrime(147)))



def primeSieve(sieveSize):
    # create a sieve where all numbers are marked as primes
    sieve = [True] * sieveSize

    # zero and one are not prime numbers
    sieve[0] = False
    sieve[1] = False

    # create the sieve
    for i in range(2, int(math.sqrt(sieveSize)) + 1):
        pointer = i * 2
        while pointer < sieveSize:
            sieve[pointer] = False
            pointer += i

    # compile the list of primes
    primes = []
    for i in range(sieveSize):
        if sieve[i] == True:
            primes.append(i)

    return primes

print()
primes = primeSieve(1000)
print('  2 is prime: %s' % (2 in primes))
print('  5 is prime: %s' % (5 in primes))
print(' 11 is prime: %s' % (11 in primes))
print(' 16 is prime: %s' % (16 in primes))
print(' 17 is prime: %s' % (17 in primes))
print('101 is prime: %s' % (101 in primes))
print('126 is prime: %s' % (126 in primes))
print('147 is prime: %s' % (147 in primes))


import pyperclip
pyperclip.copy(str(primeSieve(1000)))



def testPrimeFunctions():
    sievePrimes = primeSieve(10000)

    allCorrect = True
    for i in range(10000):
        if (i in sievePrimes and not isPrime(i)) or (i not in sievePrimes and isPrime(i)):
            print('The two functions disagree if %s is prime.' % (i))
            allCorrect = False

    if allCorrect:
        print('The two functions are consistent.')
    else:
        print('ERROR! The two functions are not consistent.')

print()
testPrimeFunctions()