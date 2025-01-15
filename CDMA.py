import numpy as np

def generate_walsh_codes(size):
    if size & (size - 1) != 0:
        raise ValueError("Size must be a power of 2.")
    walsh_matrix = np.array([[1]])
    while walsh_matrix.shape[0] < size:
        walsh_matrix = np.block([
            [walsh_matrix, walsh_matrix],
            [walsh_matrix, -walsh_matrix]
        ])
    return walsh_matrix

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    chars = [chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)]
    return ''.join(chars)

def encode_signal(word, walsh_code):
    binary_word = text_to_binary(word)
    signal = []
    for bit in binary_word:
        signal.extend(walsh_code if bit == '1' else -walsh_code)
    return np.array(signal)

def decode_signal(received_signal, walsh_code):
    chunk_size = len(walsh_code)
    num_chunks = len(received_signal) // chunk_size
    binary_word = ''
    for i in range(num_chunks):
        chunk = received_signal[i * chunk_size:(i + 1) * chunk_size]
        correlation = np.dot(chunk, walsh_code)
        binary_word += '1' if correlation > 0 else '0'
    return binary_to_text(binary_word)

# Parameters
num_stations = 4
walsh_size = 8
words = {
    "A": "GOD",
    "B": "CAT",
    "C": "HAM",
    "D": "SUN"
}

walsh_codes = generate_walsh_codes(walsh_size)

encoded_signals = {}
for station, word in words.items():
    walsh_code = walsh_codes[list(words.keys()).index(station)]
    encoded_signals[station] = encode_signal(word, walsh_code)

combined_signal = sum(encoded_signals.values())

decoded_words = {}
for station, walsh_code in zip(words.keys(), walsh_codes):
    decoded_words[station] = decode_signal(combined_signal, walsh_code)

for station, original_word in words.items():
    decoded_word = decoded_words[station]
    assert decoded_word == original_word, f"Mismatch for {station}: {decoded_word} != {original_word}"
    print(f"Station {station}: {decoded_word}")
