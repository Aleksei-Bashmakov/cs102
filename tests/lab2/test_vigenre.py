import unittest
from src.lab2.vigenre import encrypt_vigenere, decrypt_vigenere


class TestEncryptVigenere(unittest.TestCase):

    def test_basic_encryption(self):
        self.assertEqual(
            encrypt_vigenere("ATTACKATDAWN", "LEMON"),
            "LXFOPVEFRNHR",
        )

    def test_lowercase_encryption(self):
        self.assertEqual(
            encrypt_vigenere("python", "a"),
            "python",
        )

    def test_uppercase_encryption(self):
        self.assertEqual(
            encrypt_vigenere("PYTHON", "A"),
            "PYTHON",
        )

    def test_mixed_case_encryption(self):
        self.assertEqual(
            encrypt_vigenere("AttackAtDawn", "LEMON"),
            "LxfopvEfRnhr",
        )

    def test_keyword_case_does_not_matter(self):
        self.assertEqual(
            encrypt_vigenere("ATTACKATDAWN", "lemon"),
            encrypt_vigenere("ATTACKATDAWN", "LEMON"),
        )

    def test_spaces_and_punctuation(self):
        self.assertEqual(
            encrypt_vigenere("HELLO, WORLD!", "KEY"),
            "RIJVS, UYVJN!",
        )

    def test_digits_and_special_characters(self):
        self.assertEqual(
            encrypt_vigenere("A1-B2 C3!", "BC"),
            "B1-D2 D3!",
        )

    def test_non_letters_advance_keyword(self):
        self.assertEqual(
            encrypt_vigenere("A-A", "BC"),
            "B-C",
        )

    def test_empty_plaintext(self):
        self.assertEqual(encrypt_vigenere("", "KEY"), "")

    def test_single_character_keyword(self):
        self.assertEqual(
            encrypt_vigenere("ABCXYZ", "B"),
            "BCDYZA",
        )

    def test_keyword_repeats(self):
        self.assertEqual(
            encrypt_vigenere("AAAAAA", "BC"),
            "BCBCBC",
        )

    def test_keyword_longer_than_text(self):
        self.assertEqual(
            encrypt_vigenere("ABC", "LEMON"),
            "LFO",
        )

    def test_wraps_around_alphabet(self):
        self.assertEqual(
            encrypt_vigenere("XYZ", "BCD"),
            "YAC",
        )

    def test_zero_shift(self):
        self.assertEqual(
            encrypt_vigenere("AbCz", "AAAA"),
            "AbCz",
        )

    def test_empty_keyword_with_empty_text(self):
        self.assertEqual(encrypt_vigenere("", ""), "")

    def test_empty_keyword_with_nonempty_text(self):
        with self.assertRaises(ZeroDivisionError):
            encrypt_vigenere("HELLO", "")


class TestDecryptVigenere(unittest.TestCase):

    def test_basic_decryption(self):
        self.assertEqual(
            decrypt_vigenere("LXFOPVEFRNHR", "LEMON"),
            "ATTACKATDAWN",
        )

    def test_uppercase_decryption_with_a(self):
        self.assertEqual(
            decrypt_vigenere("PYTHON", "A"),
            "PYTHON",
        )

    def test_lowercase_decryption_with_a(self):
        self.assertEqual(
            decrypt_vigenere("python", "a"),
            "python",
        )

    def test_mixed_case_decryption(self):
        self.assertEqual(
            decrypt_vigenere("LxfopvEfRnhr", "LEMON"),
            "AttackAtDawn",
        )

    def test_spaces_and_punctuation(self):
        self.assertEqual(
            decrypt_vigenere("RIJVS, UYVJN!", "KEY"),
            "HELLO, WORLD!",
        )

    def test_digits_and_special_characters(self):
        self.assertEqual(
            decrypt_vigenere("B1-D2 D3!", "BC"),
            "A1-B2 C3!",
        )

    def test_non_letters_advance_keyword(self):
        self.assertEqual(
            decrypt_vigenere("B-C", "BC"),
            "A-A",
        )

    def test_empty_ciphertext(self):
        self.assertEqual(decrypt_vigenere("", "KEY"), "")

    def test_single_character_keyword(self):
        self.assertEqual(
            decrypt_vigenere("BCDYZA", "B"),
            "ABCXYZ",
        )

    def test_keyword_repeats(self):
        self.assertEqual(
            decrypt_vigenere("BCBCBC", "BC"),
            "AAAAAA",
        )

    def test_keyword_longer_than_text(self):
        self.assertEqual(
            decrypt_vigenere("LFO", "LEMON"),
            "ABC",
        )

    def test_wraps_around_alphabet(self):
        self.assertEqual(
            decrypt_vigenere("YAC", "BCD"),
            "XYZ",
        )

    def test_zero_shift(self):
        self.assertEqual(
            decrypt_vigenere("AbCz", "AAAA"),
            "AbCz",
        )

    def test_empty_keyword_with_empty_text(self):
        self.assertEqual(decrypt_vigenere("", ""), "")

    def test_empty_keyword_with_nonempty_text(self):
        with self.assertRaises(ZeroDivisionError):
            decrypt_vigenere("HELLO", "")


if __name__ == "__main__":
    unittest.main()