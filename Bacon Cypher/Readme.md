# 🥓 Bacon Cipher

A comprehensive Python implementation of the Bacon cipher with traditional encoding/decoding and steganographic features.

## 📖 Table of Contents

- [Overview](#Overview)
- [History](#History)
- [Features](#Features)
- [Installation](#Installation)
- [Usage](#Usage)
  - [Basic Encoding/Decoding](#basic-encodingdecoding)
  - [Steganographic Mode](#steganographic-mode)
  - [Interactive Mode](#interactive-mode)
- [How It Works](#how-It-Works)
- [Examples](#examples)
- [API Reference](#api-reference)
- [Contributing](#contributing)

## 🎯 Overview

The Bacon cipher is a method of steganographic message encoding invented by Francis Bacon in 1605. It encodes letters using sequences of two different symbols (traditionally 'A' and 'B'). This implementation supports both traditional encoding and modern steganographic techniques using text case variations.

## 📜 History

The Bacon cipher was invented by **Francis Bacon (1561-1626)**, an English philosopher, statesman, and scientist. He used this cipher to hide secret messages in his works. The cipher is notable for being one of the earliest forms of steganography—the practice of hiding messages in plain sight.

## ✨ Features

- **Dual Alphabet Support**: Choose between 24-letter (traditional) or 26-letter (modern) alphabet encoding
- **Traditional Encoding**: Convert text to/from A/B binary sequences
- **Steganographic Encoding**: Hide secret messages in cover text using case variations (lowercase = A, uppercase = B)
- **Interactive Mode**: User-friendly command-line interface for experimentation
- **Comprehensive Examples**: Built-in demonstrations showing all features
- **Character Mapping Tables**: Visual reference for encoding patterns

## 🚀 Installation

### Prerequisites

- Python 3.6 or higher

### Setup

1. Clone this repository or download the files:

   ```bash
   git clone <repository-url>
   cd "Bacon Cypher"
   ```

2. No external dependencies required! The implementation uses only Python standard library.

3. Run the program:

   ```bash
   python bacon_cypher.py
   ```

## 💡 Usage

### Basic Encoding/Decoding

```python
from bacon_cypher import BaconCipher

cipher = BaconCipher()

# Encode a message
message = "HELLO"
encoded = cipher.encode_text(message)
print(encoded)  # Output: AABBB AABAA ABABA ABABA ABBBA

# Decode a message
decoded = cipher.decode_text(encoded)
print(decoded)  # Output: HELLO
```

### Steganographic Mode

Hide secret messages in plain text using case variations:

```python
cipher = BaconCipher()

secret = "HELP"
cover = "The quick brown fox jumps over the lazy dog"

# Hide the message
stego_text = cipher.steganographic_encode(secret, cover)
print(stego_text)  # Message hidden in case patterns

# Extract the message
extracted = cipher.steganographic_decode(stego_text, len(secret))
print(extracted)  # Output: HELP
```

### Interactive Mode

Run the program and choose option to enter interactive mode:

```bash
python bacon_cypher.py
```

The interactive mode provides:

1. Encode a message
2. Decode a message
3. Steganographic encoding
4. Steganographic decoding
5. Show character mapping
6. Exit

## 🔍 How-It-Works

### Traditional Bacon Cipher

Each letter is represented by a 5-character sequence of A's and B's:

**26-Letter Alphabet:**

```bash
A = AAAAA    J = ABAAB    S = BAABA
B = AAAAB    K = ABABA    T = BAABB
C = AAABA    L = ABABB    U = BABAA
D = AAABB    M = ABBAA    V = BABAB
E = AABAA    N = ABBAB    W = BABBA
F = AABAB    O = ABBBA    X = BABBB
G = AABBA    P = ABBBB    Y = BBAAA
H = AABBB    Q = BAAAA    Z = BBAAB
I = ABAAA    R = BAAAB
```

### Steganographic Encoding

The steganographic mode uses case variations to hide messages:

- **Lowercase letter** = A
- **Uppercase letter** = B

For example, to hide "HI":

- H = AABBB, I = ABAAA
- Pattern: AABBB ABAAA
- Cover text: "hello world" → "heLLo WOrld"

## 📚 Examples

### Example 1: Basic Message

```python
cipher = BaconCipher()

# Encode
message = "BACON"
encoded = cipher.encode_text(message, use_26_letters=True)
# Output: AAAAB AAAAA AAABA ABBAB ABBBA

# Decode
decoded = cipher.decode_text(encoded, use_26_letters=True)
# Output: BACON
```

### Example 2: Steganographic Message

```python
cipher = BaconCipher()

secret = "SECRET"
cover = "The quick brown fox jumps over the lazy dog and runs through the forest"

# Encode
stego = cipher.steganographic_encode(secret, cover)
# The case pattern hides the message

# Decode
extracted = cipher.steganographic_decode(stego, 6)
# Output: SECRET
```

### Example 3: Using 24-Letter Alphabet (Traditional)

```python
cipher = BaconCipher()

# In 24-letter alphabet, I/J and U/V share codes
message = "JULIUS"
encoded = cipher.encode_text(message, use_26_letters=False)
decoded = cipher.decode_text(encoded, use_26_letters=False)
# Note: J becomes I, U/V are same
```

## 📖 API Reference

### `BaconCipher` Class

#### `__init__()`

Initialize the Bacon cipher with alphabet mappings.

#### `encode_text(text, use_26_letters=True)`

Encode text using Bacon cipher.

**Parameters:**

- `text` (str): The text to encode

- `use_26_letters` (bool): Use 26-letter (True) or 24-letter (False) alphabet

**Returns:**

- str: The encoded text in A/B format

#### `decode_text(encoded_text, use_26_letters=True)`

Decode Bacon cipher text.

**Parameters:**

- `encoded_text` (str): The encoded text in A/B format
- `use_26_letters` (bool): Use 26-letter (True) or 24-letter (False) alphabet

**Returns:**

- str: The decoded text

#### `steganographic_encode(secret_text, cover_text)`

Hide secret text in cover text using case variations.

**Parameters:**

- `secret_text` (str): The secret message to hide
- `cover_text` (str): The cover text to hide the message in

**Returns:**

- str: Cover text with hidden message encoded in case variations

**Raises:**

- `ValueError`: If cover text is too short to hide the message

#### `steganographic_decode(stego_text, message_length=None)`

Extract hidden message from steganographically encoded text.

**Parameters:**

- `stego_text` (str): Text with hidden message in case variations
- `message_length` (int, optional): Expected length of hidden message

**Returns:**

- str: The extracted hidden message

## 🎨 Features Showcase

### Demonstration Mode

Run the program to see:

- Basic encoding/decoding examples
- Traditional 24-letter alphabet usage
- Steganographic encoding demonstration
- Complete character mapping table

### Interactive Mode

Experiment with:

- Custom message encoding
- Custom message decoding
- Creating steganographic messages
- Extracting hidden messages
- Viewing alphabet mappings

## 🛠️ Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (uses only standard library)
- **Encoding**: Supports both 24-letter and 26-letter alphabets
- **Steganography**: Case-based hiding (lowercase/uppercase)
- **Error Handling**: Validates input and provides helpful error messages

## 🙏 Acknowledgments

- Francis Bacon (1561-1626) for inventing this ingenious cipher

**Made with 🥓 and Python**
