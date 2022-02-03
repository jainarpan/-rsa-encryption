# RSA-module

Program to generate public(Encryption) and private(Decryption) keys for RSA encryption using Miller-Rabin Primality Test of given key size.
Also includes functions to Encrypt and Decrypt messages using these keys.

It also includes function to retrieve the private key from the weak public keys.
Attacks:
- List of potential messages is known.
- Small q (q < 100,000).
- Difference between primes is < 10,000.
- 2 different public keys with one common prime are given.
- Have same message encrypted using same exponent but different keys.

