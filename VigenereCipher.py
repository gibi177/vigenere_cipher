class VigenereCipher:

  def __init__(self):
    self.key = None

  def set_key(self, key: str):
    """Public method to set the key, which is used for both encoding and decoding"""

    if not key.isalpha():
      raise ValueError("Key must be a string of alphabetic characters")
    self.key = key.lower()

  forward_mapping = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
    'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
    'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
    'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
    'z': 25
}
  reverse_mapping = {v: k for k, v in forward_mapping.items()}
  
  def _get_new_char(self, text_char: str, key_char: str, mode: str) -> str:
    """Helper method to get the new character based on the mode (encode or decode)"""

    text_char_value = self.forward_mapping.get(text_char) # May be the message char or the key char, depending on the mode
    key_char_value = self.forward_mapping.get(key_char)

    if mode == 'encode':
      new_char_value = (text_char_value + key_char_value) % 26 
      new_char = self.reverse_mapping.get(new_char_value)
    elif mode == 'decode':
      new_char_value = (text_char_value - key_char_value) % 26
      new_char = self.reverse_mapping.get(new_char_value)

    return new_char

  def _transform(self, message: str, mode: str) -> str:
    """Main method used to transform the message based on the mode"""

    # Check mode and key before processing
    if mode not in ['encode', 'decode']:
      raise ValueError("Mode must be either 'encode' or 'decode'")
    if self.key is None:
      raise ValueError("Key must be set before encoding")

    result = ""
    key_index = 0
    for ch in message:

      if ch.lower() not in self.forward_mapping:
        result += ch
        continue

      is_upper = ch.isupper()
      if is_upper:
        ch = ch.lower()

      key_char = self.key[key_index]
      new_character = self._get_new_char(ch, key_char, mode)

      key_index += 1
      if key_index >= len(self.key):
        key_index = 0

      if is_upper:
        new_character = new_character.upper()

      result += new_character 

    return result
  
  def encode(self, message: str) -> str:
    """Encodes the message using the Vigenere cipher"""
    return self._transform(message, mode = 'encode')

  def decode(self, message: str) -> str:
    """Decodes the message using the Vigenere cipher"""
    return self._transform(message, mode = 'decode')


if __name__ == "__main__":

  encoder_decoder = VigenereCipher()
  encoder_decoder.set_key("abc")

  message = "Daniel Campos Silva"
  encoded_message = encoder_decoder.encode(message)
  assert (encoded_message == encoded_message)
  print(f"Encoded message: {encoded_message}")

  decoded_message = encoder_decoder.decode(encoded_message)
  assert (decoded_message == message)
  print(f"Decoded message: {decoded_message}")

  assert message == decoded_message


  # Additional test with a longer message

  encoder_decoder.set_key("hello")
  message = """In the early days of modern computing, engineers and scientists faced many challenges related to communication and security. 
As computer networks began to expand, the need for reliable transmission of information became increasingly important. 
Messages traveling across long distances could be intercepted, modified, or completely replaced by attackers. 
For this reason, cryptography became a fundamental tool to protect confidentiality and integrity.

One of the most famous classical encryption methods is the Vigenere cipher. 
Unlike simple substitution ciphers, the Vigenere cipher uses a repeating key to apply different shifts to different letters. 
This technique makes frequency analysis more difficult, because the same letter in the plaintext may be encrypted into different letters in the ciphertext.
However, even though it was once considered secure, the Vigenere cipher can be broken if the attacker has enough ciphertext.

The weakness of the Vigenere cipher comes from the repetition of the key. 
When the key is short, the same pattern of shifts repeats many times throughout the message. 
If the plaintext contains repeated sequences, the ciphertext may also contain repeated sequences at predictable distances.
The Kasiski examination is a well known technique that exploits this property by searching for repeated patterns and measuring the distances between them.
By analyzing the common factors of these distances, it is possible to estimate the most likely key length.

After estimating the key length, the attacker can split the ciphertext into several groups. 
Each group contains characters encrypted with the same key letter, which means each group behaves like a Caesar cipher.
Once the message is separated, the attacker can apply frequency analysis to each group independently.
In English, certain letters such as E, T, A, and O appear much more frequently than others.
By comparing the observed frequencies in each group with the expected frequencies of the English language, the attacker can recover the key one letter at a time.

This process demonstrates an important lesson in cybersecurity. 
Even if an encryption method looks complex, it may still contain weaknesses that can be exploited with mathematics and statistics.
Modern cryptography avoids these problems by using keys that are much larger and by relying on computational hardness assumptions.
Nevertheless, studying classical ciphers remains valuable because it helps students understand the foundations of encryption and the evolution of security techniques.

In conclusion, the Vigenere cipher is an interesting historical algorithm that illustrates both the creativity and the limitations of early cryptographic systems.
While it improves upon monoalphabetic substitution by introducing multiple alphabets, it is not resistant to systematic cryptanalysis when sufficient ciphertext is available.
The combination of Kasiski examination and frequency analysis is usually enough to break the cipher, recover the key, and reveal the original message.
"""

  encoded_message = encoder_decoder.encode(message)
  print(f"Encoded message: {encoded_message}")
  decoded_message = encoder_decoder.decode(encoded_message)
  print(f"Decoded message: {decoded_message}")
  assert message == decoded_message