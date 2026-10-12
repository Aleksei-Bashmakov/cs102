"""
Unit tests for the RSA cryptosystem implementation.
"""

# pylint: disable=invalid-name,import-error

import unittest
from src.lab2.rsa import is_prime, gcd, multiplicative_inverse, generate_keypair, encrypt, decrypt


class TestRSACryptosystem(unittest.TestCase):
    """Набор тестов для проверки корректности работы криптосистемы RSA."""

    def test_is_prime(self):
        """Проверка функции определения простых чисел."""
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(11))
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(0))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(15))

    def test_gcd(self):
        """Проверка алгоритма Евклида для поиска НОД."""
        self.assertEqual(gcd(12, 15), 3)
        self.assertEqual(gcd(3, 7), 1)
        self.assertEqual(gcd(0, 5), 5)
        self.assertEqual(gcd(100, 10), 10)

    def test_multiplicative_inverse(self):
        """Проверка расширенного алгоритма Евклида (поиск d)."""
        self.assertEqual(multiplicative_inverse(7, 40), 23)
        self.assertEqual(multiplicative_inverse(3, 11), 4)

    def test_generate_keypair_valid(self):
        """Проверка успешной генерации пары ключей."""
        p, q = 61, 53
        public, private = generate_keypair(p, q)

        # Разворачиваем ключи
        e, n_pub = public
        d, n_priv = private

        # Модуль n должен быть равен p * q
        self.assertEqual(n_pub, p * q)
        self.assertEqual(n_priv, p * q)

        # Проверяем математическую связь: (e * d) % phi == 1
        phi = (p - 1) * (q - 1)
        self.assertEqual((e * d) % phi, 1)

    def test_generate_keypair_exceptions(self):
        """Проверка генерации исключений (ошибок) при неверных p и q."""
        # p и q должны быть простыми числами
        with self.assertRaises(ValueError):
            generate_keypair(4, 11)

        # p и q не должны быть равны
        with self.assertRaises(ValueError):
            generate_keypair(11, 11)

    def test_encrypt_and_decrypt_cycle(self):
        """Сквозной тест: шифрование и последующая успешная расшифровка."""
        public, private = generate_keypair(61, 53)
        message = "Hello, World! 2026"

        # Шифруем открытым, расшифровываем закрытым
        encrypted = encrypt(public, message)
        decrypted = decrypt(private, encrypted)

        # Исходное сообщение должно совпадать с расшифрованным
        self.assertEqual(message, decrypted)

    def test_encrypt_output_type(self):
        """Проверка того, что на выходе шифрования получается список чисел."""
        public, _ = generate_keypair(17, 19)
        encrypted = encrypt(public, "ABC")

        self.assertIsInstance(encrypted, list)
        self.assertTrue(all(isinstance(x, int) for x in encrypted))


if __name__ == "__main__":
    unittest.main()
