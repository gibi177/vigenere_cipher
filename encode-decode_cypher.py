class VigenereCipher:

  def __init__(self, key: str):
    self.key = key
    
  forward_mapping = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4,
    'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9,
    'k': 10, 'l': 11, 'm': 12, 'n': 13, 'o': 14,
    'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19,
    'u': 20, 'v': 21, 'w': 22, 'x': 23, 'y': 24,
    'z': 25
}
  reverse_mapping = {v: k for k, v in forward_mapping.items()}
  
  def get_new_char(self, text_char: str, key_char: str) -> str:
    new_char_value = (self.forward_mapping[text_char] + self.forward_mapping[key_char]) % 26
    new_char = self.reverse_mapping.get(new_char_value)
    return new_char

  def transform(self, message: str) -> str:
    result = ""

    key_index = 0
    for ch in message:

      if ch.lower() not in self.forward_mapping:
        result += ch
        continue

      isUpper = ch.isupper()
      if isUpper:
        ch = ch.lower()

      key_char = self.key[key_index]
      new_character = self.get_new_char(ch, key_char) 

      key_index += 1
      if key_index >= len(self.key):
        key_index = 0

      if isUpper:
        new_character = new_character.upper()

      result += new_character 

    return result
  
  def encode(self, word: str) -> str:
    return self.transform(word)



encoder = VigenereCipher('abc')
message = "abczz"
encoded_message = encoder.encode(message)

assert (encoded_message == "aceza")
print(f"Encoded message: {encoded_message}")