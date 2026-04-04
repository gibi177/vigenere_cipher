import string
from collections import Counter
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from VigenereCipher import VigenereCipher
# Frequências aproximadas (em porcentagem)
FREQ_EN = {
    'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702,
    'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966, 'j': 0.153,
    'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507,
    'p': 1.929, 'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056,
    'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150, 'y': 1.974,
    'z': 0.074
}




def clean_text(text: str) -> str:
    """Keep only letters A-Z and convert to lowercase."""
    return ''.join([c.lower() for c in text if c.isalpha()])


def shift_char(c: str, shift: int) -> str:
    """Shift a character backwards (Caesar decode) by shift."""
    return chr((ord(c) - ord('a') - shift) % 26 + ord('a'))


def caesar_decode(text: str, shift: int) -> str:
    """Decode a Caesar cipher with given shift."""
    return ''.join(shift_char(c, shift) for c in text)


def chi_square_score(text: str, expected_freq: dict) -> float:
    """
    Chi-square test comparing observed frequencies vs expected frequencies.
    Lower score means better match.
    """
    n = len(text)
    if n == 0:
        return float("inf")

    observed = Counter(text)
    score = 0.0

    for letter in string.ascii_lowercase:
        observed_count = observed.get(letter, 0)
        expected_count = expected_freq[letter] * n / 100.0
        score += ((observed_count - expected_count) ** 2) / expected_count

    return score


def split_into_columns(ciphertext: str, key_length: int) -> list[str]:
    """
    Split ciphertext into key_length groups.
    Group i contains letters at positions i, i+key_length, i+2*key_length...
    """
    columns = ['' for _ in range(key_length)]
    index = 0

    for ch in ciphertext:
        if ch.isalpha():
            columns[index % key_length] += ch.lower()
            index += 1

    return columns


def recover_key(ciphertext: str, key_length: int) -> str:
    """
    Recover Vigenere key using chi-square frequency analysis.
    language: "pt" or "en"
    """
    ciphertext_clean = clean_text(ciphertext)

    
    expected = FREQ_EN
   

    columns = split_into_columns(ciphertext_clean, key_length)

    recovered_key = ""

    for col in columns:
        best_shift = 0
        best_score = float("inf")

        for shift in range(26):
            decoded_col = caesar_decode(col, shift)
            score = chi_square_score(decoded_col, expected)

            if score < best_score:
                best_score = score
                best_shift = shift

        # shift 0 = 'a', shift 1 = 'b', ...
        recovered_key += chr(best_shift + ord('a'))

    return recovered_key


def break_vigenere(ciphertext: str, key_length: int):
    """
    Recover key and decrypt ciphertext.
    """
    key = recover_key(ciphertext, key_length)

    v = VigenereCipher()
    v.set_key(key)

    plaintext = v.decode(ciphertext)
    return key, plaintext

def english_word_score(text: str) -> int:
    common_words = [" the ", " and ", " of ", " to ", " in ", " is ", " that ", " it "]
    t = text.lower()
    return sum(t.count(w) for w in common_words)


def improve_key_by_word_score(ciphertext: str, key: str):
    from VigenereCipher import VigenereCipher

    best_key = key
    best_score = -1

    for i in range(len(key)):
        for c in string.ascii_lowercase:
            test_key = key[:i] + c + key[i+1:]

            v = VigenereCipher()
            v.set_key(test_key)
            plaintext = v.decode(ciphertext)

            score = english_word_score(plaintext)

            if score > best_score:
                best_score = score
                best_key = test_key

    return best_key, best_score


if __name__ == "__main__":
    # Exemplo de uso
    cipher = """Pr ess xytph cmwwoni zq Sshpykvso, evl xzhbztpzdsi rlhoicpr lzpcm lzpywuk
                ez goecp gasctsz fj evl jtcs..."""

    key_length = 5
    key, message = break_vigenere(cipher, key_length)

    print("Recovered key:", key)
    print("Decrypted message:\n", message)

print("ok")