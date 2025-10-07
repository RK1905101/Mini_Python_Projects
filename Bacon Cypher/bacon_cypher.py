"""
Bacon Cipher Implementation with Steganographic Features
=======================================================

The Bacon cipher is a steganographic cipher invented by Francis Bacon in 1605.
It encodes letters using sequences of two different symbols (traditionally A and B).
This implementation includes both traditional and steganographic variants.

Author: Assistant
Date: October 2025
"""

class BaconCipher:
    """
    A comprehensive implementation of the Bacon cipher with multiple encoding methods.
    """
    
    def __init__(self):
        # Traditional Bacon cipher mapping (24-letter alphabet, I/J and U/V combined)
        self.bacon_dict_24 = {
            'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB', 'E': 'AABAA',
            'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB', 'I': 'ABAAA', 'J': 'ABAAA',
            'K': 'ABAAB', 'L': 'ABABA', 'M': 'ABABB', 'N': 'ABBAA', 'O': 'ABBAB',
            'P': 'ABBBA', 'Q': 'ABBBB', 'R': 'BAAAA', 'S': 'BAAAB', 'T': 'BAABA',
            'U': 'BAABB', 'V': 'BAABB', 'W': 'BABAA', 'X': 'BABAB', 'Y': 'BABBA',
            'Z': 'BABBB'
        }
        
        # Modern 26-letter alphabet version
        self.bacon_dict_26 = {
            'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB', 'E': 'AABAA',
            'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB', 'I': 'ABAAA', 'J': 'ABAAB',
            'K': 'ABABA', 'L': 'ABABB', 'M': 'ABBAA', 'N': 'ABBAB', 'O': 'ABBBA',
            'P': 'ABBBB', 'Q': 'BAAAA', 'R': 'BAAAB', 'S': 'BAABA', 'T': 'BAABB',
            'U': 'BABAA', 'V': 'BABAB', 'W': 'BABBA', 'X': 'BABBB', 'Y': 'BBAAA',
            'Z': 'BBAAB'
        }
        
        # Create reverse dictionaries for decoding
        self.reverse_bacon_24 = {v: k for k, v in self.bacon_dict_24.items()}
        self.reverse_bacon_26 = {v: k for k, v in self.bacon_dict_26.items()}
    
    def encode_text(self, text, use_26_letters=True):
        """
        Encode text using the Bacon cipher.
        
        Args:
            text (str): The text to encode
            use_26_letters (bool): Whether to use 26-letter or 24-letter alphabet
            
        Returns:
            str: The encoded text in A/B format
        """
        bacon_dict = self.bacon_dict_26 if use_26_letters else self.bacon_dict_24
        encoded = []
        
        for char in text.upper():
            if char in bacon_dict:
                encoded.append(bacon_dict[char])
            elif char == ' ':
                encoded.append('|')  # Use | to separate words
            # Skip other characters (punctuation, etc.)
        
        return ' '.join(encoded)
    
    def decode_text(self, encoded_text, use_26_letters=True):
        """
        Decode Bacon cipher text.
        
        Args:
            encoded_text (str): The encoded text in A/B format
            use_26_letters (bool): Whether to use 26-letter or 24-letter alphabet
            
        Returns:
            str: The decoded text
        """
        reverse_dict = self.reverse_bacon_26 if use_26_letters else self.reverse_bacon_24
        
        # Split by spaces and decode each group
        groups = encoded_text.split(' ')
        decoded = []
        
        for group in groups:
            if group == '|':
                decoded.append(' ')
            elif group in reverse_dict:
                decoded.append(reverse_dict[group])
            elif len(group) == 5 and all(c in 'AB' for c in group):
                # Try to decode if it's a valid 5-letter A/B sequence
                if group in reverse_dict:
                    decoded.append(reverse_dict[group])
                else:
                    decoded.append('?')  # Unknown sequence
        
        return ''.join(decoded)
    
    def steganographic_encode(self, secret_text, cover_text):
        """
        Hide secret text in cover text using case variations.
        Lowercase = A, Uppercase = B in Bacon cipher.
        
        Args:
            secret_text (str): The secret message to hide
            cover_text (str): The cover text to hide the message in
            
        Returns:
            str: Cover text with hidden message encoded in case variations
        """
        # Encode the secret text
        encoded = self.encode_text(secret_text, use_26_letters=True)
        
        # Convert A/B to binary pattern (A=lowercase, B=uppercase)
        binary_pattern = encoded.replace(' ', '').replace('|', '')
        
        # Filter cover text to only letters
        cover_letters = [c for c in cover_text if c.isalpha()]
        
        if len(binary_pattern) > len(cover_letters):
            raise ValueError(f"Cover text too short. Need {len(binary_pattern)} letters, got {len(cover_letters)}")
        
        # Apply the pattern to cover text
        result = []
        pattern_index = 0
        
        for char in cover_text:
            if char.isalpha() and pattern_index < len(binary_pattern):
                if binary_pattern[pattern_index] == 'A':
                    result.append(char.lower())
                else:  # 'B'
                    result.append(char.upper())
                pattern_index += 1
            else:
                result.append(char)
        
        return ''.join(result)
    
    def steganographic_decode(self, stego_text, message_length=None):
        """
        Extract hidden message from steganographically encoded text.
        
        Args:
            stego_text (str): Text with hidden message in case variations
            message_length (int): Expected length of hidden message (optional)
            
        Returns:
            str: The extracted hidden message
        """
        # Extract the binary pattern from case variations
        pattern = []
        for char in stego_text:
            if char.isalpha():
                pattern.append('A' if char.islower() else 'B')
        
        # Group into 5-character sequences for Bacon decoding
        bacon_groups = []
        for i in range(0, len(pattern), 5):
            if i + 5 <= len(pattern):
                bacon_groups.append(''.join(pattern[i:i+5]))
        
        # Decode each group
        decoded_chars = []
        for group in bacon_groups:
            if group in self.reverse_bacon_26:
                decoded_chars.append(self.reverse_bacon_26[group])
            else:
                decoded_chars.append('?')
        
        result = ''.join(decoded_chars)
        
        # If message length is specified, truncate to that length
        if message_length:
            result = result[:message_length]
        
        return result


def demonstrate_bacon_cipher():
    """
    Comprehensive demonstration of the Bacon cipher with various examples.
    """
    print("🥓 BACON CIPHER DEMONSTRATION 🥓")
    print("=" * 50)
    
    cipher = BaconCipher()
    
    # Example 1: Basic encoding and decoding
    print("\n1. BASIC ENCODING AND DECODING")
    print("-" * 30)
    
    message = "HELLO WORLD"
    print(f"Original message: {message}")
    
    encoded = cipher.encode_text(message)
    print(f"Encoded (26-letter): {encoded}")
    
    decoded = cipher.decode_text(encoded)
    print(f"Decoded: {decoded}")
    
    # Example 2: 24-letter alphabet (traditional)
    print("\n2. TRADITIONAL 24-LETTER ALPHABET")
    print("-" * 35)
    
    message2 = "BACON CIPHER"
    print(f"Original message: {message2}")
    
    encoded_24 = cipher.encode_text(message2, use_26_letters=False)
    print(f"Encoded (24-letter): {encoded_24}")
    
    decoded_24 = cipher.decode_text(encoded_24, use_26_letters=False)
    print(f"Decoded: {decoded_24}")
    
    # Example 3: Steganographic encoding
    print("\n3. STEGANOGRAPHIC ENCODING")
    print("-" * 30)
    
    secret = "SECRET"
    cover = "The quick brown fox jumps over the lazy dog and runs through the forest"
    
    print(f"Secret message: {secret}")
    print(f"Cover text: {cover}")
    
    try:
        stego_text = cipher.steganographic_encode(secret, cover)
        print(f"Steganographic text: {stego_text}")
        
        extracted = cipher.steganographic_decode(stego_text, len(secret))
        print(f"Extracted message: {extracted}")
        
        # Highlight the pattern
        print("\nPattern visualization (lowercase=A, uppercase=B):")
        pattern_viz = ""
        for char in stego_text:
            if char.isalpha():
                pattern_viz += "A" if char.islower() else "B"
        
        # Group by 5s
        grouped_pattern = " ".join([pattern_viz[i:i+5] for i in range(0, len(pattern_viz), 5)])
        print(f"Binary pattern: {grouped_pattern}")
        
    except ValueError as e:
        print(f"Error: {e}")
    
    # Example 4: Interactive demonstration
    print("\n4. CHARACTER MAPPING TABLE")
    print("-" * 25)
    
    print("26-Letter Alphabet Mapping:")
    print("Letter | Bacon Code")
    print("-------|----------")
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        print(f"   {letter}   | {cipher.bacon_dict_26[letter]}")


def interactive_mode():
    """
    Interactive mode for user input and experimentation.
    """
    cipher = BaconCipher()
    
    print("\n🎮 INTERACTIVE BACON CIPHER MODE 🎮")
    print("=" * 40)
    
    while True:
        print("\nChoose an option:")
        print("1. Encode a message")
        print("2. Decode a message")
        print("3. Steganographic encoding")
        print("4. Steganographic decoding")
        print("5. Show character mapping")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            message = input("Enter message to encode: ").strip()
            alphabet = input("Use 26-letter alphabet? (y/n): ").strip().lower()
            use_26 = alphabet != 'n'
            
            encoded = cipher.encode_text(message, use_26_letters=use_26)
            print(f"Encoded: {encoded}")
            
        elif choice == '2':
            encoded = input("Enter encoded message (A/B format): ").strip()
            alphabet = input("Use 26-letter alphabet? (y/n): ").strip().lower()
            use_26 = alphabet != 'n'
            
            decoded = cipher.decode_text(encoded, use_26_letters=use_26)
            print(f"Decoded: {decoded}")
            
        elif choice == '3':
            secret = input("Enter secret message: ").strip()
            cover = input("Enter cover text: ").strip()
            
            try:
                stego = cipher.steganographic_encode(secret, cover)
                print(f"Steganographic text: {stego}")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == '4':
            stego = input("Enter steganographic text: ").strip()
            length = input("Expected message length (or press Enter): ").strip()
            msg_len = int(length) if length.isdigit() else None
            
            extracted = cipher.steganographic_decode(stego, msg_len)
            print(f"Extracted message: {extracted}")
            
        elif choice == '5':
            print("\n26-Letter Alphabet Mapping:")
            print("Letter | Bacon Code")
            print("-------|----------")
            for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                print(f"   {letter}   | {cipher.bacon_dict_26[letter]}")
                
        elif choice == '6':
            print("Thanks for using the Bacon Cipher program! 🥓")
            break
            
        else:
            print("Invalid choice. Please try again.")


def main():
    """
    Main function to run the Bacon cipher demonstration and interactive mode.
    """
    # Run the demonstration
    demonstrate_bacon_cipher()
    
    # Ask if user wants interactive mode
    print("\n" + "=" * 50)
    user_input = input("Would you like to try the interactive mode? (y/n): ").strip().lower()
    
    if user_input == 'y' or user_input == 'yes':
        interactive_mode()
    else:
        print("\nThanks for exploring the Bacon Cipher! 🥓")
        print("The cipher is named after Francis Bacon (1561-1626),")
        print("who used it to hide messages in his works.")


if __name__ == "__main__":
    main()
