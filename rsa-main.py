# python3

## Libraries
import sys, threading
import random
import utils

sys.setrecursionlimit(10**7)
threading.stack_size(2**27)


## Supporting Mathematical Functions
def ConvertToInt(message_str):
  res = 0
  for i in range(len(message_str)):
    res = res * 256 + ord(message_str[i])
  return res

def ConvertToStr(n):
    res = ""
    while n > 0:
        res += chr(n % 256)
        n //= 256
    return res[::-1]

def PowMod(a, n, mod):
    if n == 0:
        return 1 % mod
    elif n == 1:
        return a % mod
    else:
        b = PowMod(a, n // 2, mod)
        b = b * b % mod
        if n % 2 == 0:
          return b
        else:
          return b * a % mod

def ExtendedEuclid(a, b):
    if b == 0:
        return (1, 0)
    (x, y) = ExtendedEuclid(b, a % b)
    k = a // b
    return (y, x - k * y)

def InvertModulo(a, n):
    (b, x) = ExtendedEuclid(a, n)
    if b < 0:
        b = (b % n + n) % n
    return b

def GCD(a, b):
  if b == 0:
    return a
  return GCD(b, a % b)

def IntSqrt(n):
  low = 1
  high = n
  iterations = 0
  while low < high and iterations < 5000:
    iterations += 1
    mid = (low + high + 1) // 2
    if mid * mid <= n:
      low = mid
    else:
      high = mid - 1
  return low

def ChineseRemainderTheorem(n1, r1, n2, r2):
  (x, y) = ExtendedEuclid(n1, n2)
  return ((r2 * x * n1 + r1 * y * n2) % (n1 * n2) + (n1 * n2)) % (n1 * n2)

## Functions To Generate Large Primes

def isLowPrime(num):
  """Performs Lower Prime Test On Numbers"""
  lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
   67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 
   157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 
   251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313,317, 331, 337, 347, 349, 
   353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 
   457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 
   571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 
   673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 
   797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 
   911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
  for divisor in lowPrimes:
    if num % divisor == 0 and divisor**2 <= num:
      return False
  else: return True
  
def MillerRabin(num):
  """Performs Miller Rabin Test On Possible Prime Numbers"""
  t=num-1
  divby2=0
  while t%2 == 0:
    divby2+=1
    t >>=1
  numOfRounds=20
  for i in range(numOfRounds):
    tester = random.randrange(2, num-1)
    x=pow(tester, t, num)
    if x == 1 or x == num-1:
      return True
    while t != num-1:
        x = (x * x) % num 
        t *= 2
        if x == 1:
          return False 
        if x == num-1:
          return True
    return False
   
def generateLargePrime(n):
  """Generates Large Prime Numbers"""
  while True:
    num=random.randrange(2**(n-1)+1, 2**n - 1)
    if isLowPrime(num) and MillerRabin(num):
        return num
        break
    else:
      continue

## Function For Encryption And Decryption


def Decrypt(ciphertext, p, q, exponent):
  """Decrypt Message Using Private Key"""
  d=InvertModulo(exponent,(p-1)*(q-1))
  return ConvertToStr(PowMod(ciphertext, d, p * q))

def Encrypt(message, modulo, exponent):
  """Encrypt Message Using Public Key"""
  return PowMod(ConvertToInt(message), exponent, modulo)
      
      
      
## Function To Generate Keys

def generateKeys(keySize = 1024 , writeToFile = False):
  """Generates Public And Private Keys For Encryption And Decryption. Set writeToFile Parameter To True, To Write The Keys To Respective Files."""
  p=generateLargePrime(keySize)
  q=generateLargePrime(keySize)
  n=p*q
  while True:
    expo = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
    if GCD(expo, (p - 1) * (q - 1)) == 1:
      break
  if writeToFile:
    file = open("privateKey", 'w')
    file.write("Private Key \np=%s \nq=%s\ne=%s\n" % (p,q,expo))
    file.close()
    file = open("publicKey", 'w')
    file.write("Public Key \nn=%s\ne=%s\n" % (n,expo))
    file.close()
  else:
    print("Public Key ")
    print("n =",n)
    print("e =",expo)
    print()
    print("Private Key ")
    print("p =",p)
    print("q =",q)
    print("e =",expo)


## Functions To Decode Weak Keys

def DecipherPotential(ciphertext, modulo, exponent, potential_messages):
  """If You Know List Of Potential Messages"""
  for message in potential_messages:
    if ciphertext == Encrypt(message, modulo, exponent):
      return message
  return "Encrypted Message not among potential messages"

def DecipherSmallPrime(ciphertext, modulo, exponent):
  """Decodes Message If Any Prime Is Less Than 1,000,000"""
  for x in range(2,1000000):
    if modulo % x == 0:
      small_prime = x
      big_prime = modulo // x
      return Decrypt(ciphertext, small_prime, big_prime, exponent)
  return "Could Not Decrypt!!"

def DecipherSmallDiff(ciphertext, modulo, exponent):
  """Decodes If Difference Between The Primes Is Less Than 10,000"""
  for x in range(IntSqrt(modulo)-10000,IntSqrt(modulo)+1):
    if modulo % x ==0:
      small_prime = x
      big_prime = modulo // small_prime
      return Decrypt(ciphertext, small_prime, big_prime, exponent)
  return "Could Not Decrypt!!"

def DecipherCommonDivisor(first_ciphertext, first_modulo, first_exponent, second_ciphertext, second_modulo, second_exponent):
  """Decodes If We Have 2 Public Key With One Common Prime Among Them"""
  g= GCD(first_modulo,second_modulo)
  if g!=1:
    return (Decrypt(first_ciphertext, g, first_modulo//g, first_exponent), Decrypt(second_ciphertext, g, second_modulo//g, second_exponent))
  return ("Could Not Decrypt!!")

def DecipherHastad(first_ciphertext, first_modulo, second_ciphertext, second_modulo):
  """Decodes If You Have Same Message Encrypted Using Same Exponent But Different Keys"""
  r = ChineseRemainderTheorem(first_modulo, first_ciphertext, second_modulo, second_ciphertext)
  return ConvertToStr(IntSqrt(r))