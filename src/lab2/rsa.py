"""
RSA Cryptosystem Implementation Module.
Provides basic functions for prime checking, GCD, multiplicative inverse,
key generation, encryption, and decryption.
"""

# pylint: disable=invalid-name,redefined-outer-name

import random
import typing as tp


def is_prime(n: int) -> bool:
    """
    Tests to see if a number is prime.
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def gcd(a: int, b: int) -> int:
    """
    Euclid's algorithm for determining the greatest common divisor.
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    Euclid's extended algorithm for finding the multiplicative
    inverse of two numbers.
    >>> multiplicative_inverse(7, 40)
    23
    """
    old_r, rem = e, phi
    old_s, coef = 1, 0
    while rem != 0:
        quotient = old_r // rem
        old_r, rem = rem, old_r - quotient * rem
        old_s, coef = coef, old_s - quotient * coef
    return old_s % phi


def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    """
    Generates public and private keypairs using two prime numbers.
    """
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p == q:
        raise ValueError("p and q cannot be equal")

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(2, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are coprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(2, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)

    # Return public and private keypair
    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    """
    Encrypts plaintext using a public key.
    """
    key, n = pk
    # Оптимизировано через встроенный pow для предотвращения переполнения
    cipher = [pow(ord(char), key, n) for char in plaintext]
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    """
    Decrypts a ciphertext using a private key.
    """
    key, n = pk
    plain = [chr(pow(char, key, n)) for char in ciphertext]
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)

    # ИСПРАВЛЕНО: Шифруем ОТКРЫТЫМ ключом (public)
    message = input("Enter a message to encrypt with your public key: ")
    encrypted_msg = encrypt(public, message)
    print("Your encrypted message is: ")
    print("".join(map(str, encrypted_msg)))

    # ИСПРАВЛЕНО: Расшифровываем ЗАКРЫТЫМ ключом (private)
    print("Decrypting message with private key ", private, " . . .")
    print("Your message is:")
    print(decrypt(private, encrypted_msg))
