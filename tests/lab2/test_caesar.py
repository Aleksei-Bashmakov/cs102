import unittest

from src.lab2.caesar import decrypt_caesar, encrypt_caesar


class CaesarTestCase(unittest.TestCase):

    # ---------- шифрование ----------
    def test_encrypt_examples_from_task(self):
        self.assertEqual(encrypt_caesar("PYTHON"), "SBWKRQ")
        self.assertEqual(encrypt_caesar("python"), "sbwkrq")
        self.assertEqual(encrypt_caesar("Python3.6"), "Sbwkrq3.6")
        self.assertEqual(encrypt_caesar(""), "")

    def test_encrypt_default_shift_is_3(self):
        self.assertEqual(encrypt_caesar("ABC"), encrypt_caesar("ABC", 3))

    def test_encrypt_full_alphabet(self):
        self.assertEqual(
            encrypt_caesar("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "DEFGHIJKLMNOPQRSTUVWXYZABC",
        )
        self.assertEqual(
            encrypt_caesar("abcdefghijklmnopqrstuvwxyz"),
            "defghijklmnopqrstuvwxyzabc",
        )

    def test_encrypt_wraparound(self):
        self.assertEqual(encrypt_caesar("XYZ"), "ABC")
        self.assertEqual(encrypt_caesar("xyz"), "abc")

    def test_encrypt_alphabet_boundaries(self):
        self.assertEqual(encrypt_caesar("AZaz"), "DCdc")

    def test_encrypt_zero_shift(self):
        self.assertEqual(encrypt_caesar("Hello, World!", 0), "Hello, World!")

    def test_encrypt_custom_shifts(self):
        self.assertEqual(encrypt_caesar("ABC", 1), "BCD")
        self.assertEqual(encrypt_caesar("HELLO", 13), "URYYB")

    def test_encrypt_shift_larger_than_alphabet(self):
        self.assertEqual(encrypt_caesar("ABC", 26), "ABC")
        self.assertEqual(encrypt_caesar("ABC", 29), "DEF")
        self.assertEqual(encrypt_caesar("ABC", 52), "ABC")

    def test_encrypt_negative_shift(self):
        self.assertEqual(encrypt_caesar("DEF", -3), "ABC")
        self.assertEqual(encrypt_caesar("ABC", -3), "XYZ")

    def test_encrypt_keeps_case(self):
        self.assertEqual(encrypt_caesar("aBcXyZ"), "dEfAbC")

    def test_encrypt_non_letters_unchanged(self):
        self.assertEqual(encrypt_caesar("123 !?.,"), "123 !?.,")
        self.assertEqual(encrypt_caesar("Hello, World! 123"), "Khoor, Zruog! 123")
        self.assertEqual(encrypt_caesar("a\nb\tc"), "d\ne\tf")

    def test_encrypt_symbols_next_to_letter_ranges_unchanged(self):
        # символы, стоящие в таблице сразу до и после букв: @ [ ` {
        self.assertEqual(encrypt_caesar("@[`{"), "@[`{")

    def test_encrypt_non_latin_letters_unchanged(self):
        self.assertEqual(encrypt_caesar("Привет"), "Привет")

    def test_encrypt_returns_string(self):
        self.assertIsInstance(encrypt_caesar("abc"), str)

    # ---------- расшифровка ----------
    def test_decrypt_examples_from_task(self):
        self.assertEqual(decrypt_caesar("SBWKRQ"), "PYTHON")
        self.assertEqual(decrypt_caesar("sbwkrq"), "python")
        self.assertEqual(decrypt_caesar("Sbwkrq3.6"), "Python3.6")
        self.assertEqual(decrypt_caesar(""), "")

    def test_decrypt_wraparound(self):
        self.assertEqual(decrypt_caesar("ABC"), "XYZ")
        self.assertEqual(decrypt_caesar("abc"), "xyz")

    def test_decrypt_zero_and_custom_shifts(self):
        self.assertEqual(decrypt_caesar("Hello, World!", 0), "Hello, World!")
        self.assertEqual(decrypt_caesar("URYYB", 13), "HELLO")
        self.assertEqual(decrypt_caesar("BCD", 1), "ABC")

    def test_decrypt_shift_larger_than_alphabet(self):
        self.assertEqual(decrypt_caesar("DEF", 29), "ABC")

    def test_decrypt_negative_shift(self):
        self.assertEqual(decrypt_caesar("ABC", -3), "DEF")

    def test_decrypt_non_letters_and_non_latin_unchanged(self):
        self.assertEqual(decrypt_caesar("Khoor, Zruog! 123"), "Hello, World! 123")
        self.assertEqual(decrypt_caesar("Привет"), "Привет")

    # ---------- связь шифрования и расшифровки ----------
    def test_decrypt_reverses_encrypt_for_many_shifts(self):
        text = "Hello, World! 123 xyz XYZ Привет\n"
        for shift in range(-30, 60):
            with self.subTest(shift=shift):
                self.assertEqual(decrypt_caesar(encrypt_caesar(text, shift), shift), text)

    def test_rot13_applied_twice_gives_original(self):
        self.assertEqual(encrypt_caesar(encrypt_caesar("Python", 13), 13), "Python")


if __name__ == "__main__":
    unittest.main()