# Prime Number Sieve
# http://inventwithpython.com/codebreaker (BSD Licensed)
import math

def main():
    print('  2 is prime: %s' % (isPrime(2)))
    print('  5 is prime: %s' % (isPrime(5)))
    print(' 11 is prime: %s' % (isPrime(11)))
    print(' 16 is prime: %s' % (isPrime(16)))
    print(' 17 is prime: %s' % (isPrime(17)))
    print('101 is prime: %s' % (isPrime(101)))
    print('126 is prime: %s' % (isPrime(126)))
    print('147 is prime: %s' % (isPrime(147)))
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
    print()
    testPrimeFunctions()


def isPrime(num):
    # Returns True if num is a prime number, otherwise False.

    # Note: Generally, isPrime() is slower than primeSieve()

    # all numbers less than 2 are not prime
    if num < 2:
        return False

    # see if num is divisible by any number up to the square root of num
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


def primeSieve(sieveSize):
    # Returns a list of prime numbers calculated using
    # the Sieve of Eratosthenes algorithm.

    sieve = [True] * sieveSize
    sieve[0] = False # zero and one are not prime numbers
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


def testPrimeFunctions():
    TEST_SIZE = 50000
    sievePrimes = primeSieve(TEST_SIZE)

    print('Testing if both functions are consistent with each other...')
    allCorrect = True
    for i in range(TEST_SIZE):
        if (i in sievePrimes and not isPrime(i)) or (i not in sievePrimes and isPrime(i)):
            print('The two functions disagree if %s is prime.' % (i))
            allCorrect = False

    if allCorrect:
        print('Test Passed: Both functions are consistent with each other.')
    else:
        print('ERROR! Both functions are not consistent with each other.')


if __name__ == '__main__':
    main()