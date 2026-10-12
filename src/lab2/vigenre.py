"""
Модуль для шифрования и дешифрования текста с помощью шифра Виженера.
"""
def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_index = 0  # Отдельный счетчик для позиции в ключевом слове

    for char in plaintext:
        if "A" <= char <= "Z":
            shift = ord(keyword[key_index % len(keyword)].lower()) - ord("a")
            ciphertext += chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
            key_index += 1
        elif "a" <= char <= "z":
            shift = ord(keyword[key_index % len(keyword)].lower()) - ord("a")
            ciphertext += chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            key_index += 1
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_index = 0

    for char in ciphertext:
        if "A" <= char <= "Z":
            shift = ord(keyword[key_index % len(keyword)].lower()) - ord("a")
            plaintext += chr((ord(char) - ord("A") - shift) % 26 + ord("A"))
            key_index += 1
        elif "a" <= char <= "z":
            shift = ord(keyword[key_index % len(keyword)].lower()) - ord("a")
            plaintext += chr((ord(char) - ord("a") - shift) % 26 + ord("a"))
            key_index += 1
        else:
            plaintext += char
    return plaintext
