"""
Bletchley Baudot Encoding Map
Based on ITA2 (International Telegraph Alphabet No. 2) with Bletchley Park variations.

This module handles the encoding/decoding between 5-bit Baudot binary and characters.
"""

# Bletchley Park / ITA2 Baudot 5-bit encoding (Letters mode)
# Based on the provided samples: A=11000, B=10011, C=01110, D=10010, E=10000, etc.
BIN_TO_CHAR = {
    '00000': '/',    # NULL/Blank - using / as per Bletchley notation
    '11000': 'A',
    '10011': 'B',
    '01110': 'C',
    '10010': 'D',
    '10000': 'E',
    '10110': 'F',
    '01011': 'G',
    '00101': 'H',
    '01100': 'I',
    '11010': 'J',
    '11110': 'K',
    '01001': 'L',
    '00111': 'M',
    '00110': 'N',
    '00011': 'O',
    '01101': 'P',
    '11101': 'Q',
    '01010': 'R',
    '10100': 'S',
    '00001': 'T',
    '11100': 'U',
    '01111': 'V',
    '11001': 'W',
    '10111': 'X',
    '10101': 'Y',
    '10001': 'Z',
    # Figures mode characters (subset)
    # Note: Bletchley variant has specific mappings for numbers
    '01000': '3',
    '00010': '4',
    '11011': '5',    # Bletchley-specific: Satisfies K(11110) XOR 5(11011) = H(00101)
    '10110': '8',
    '11111': '9',
}

# Reverse mapping for encoding
CHAR_TO_BIN = {v: k for k, v in BIN_TO_CHAR.items()}

# Note on Bletchley Variant:
# The encoding satisfies K XOR 5 = H as per Bletchley specifications
# K = 11110, 5 = 11011, H = 00101
# Verification: 11110 XOR 11011 = 00101 ✓


def binary_to_char(binary_str):
    """
    Convert a 5-bit binary string to its corresponding character.
    
    Args:
        binary_str (str): 5-bit binary string
    
    Returns:
        str: Corresponding character, or '?' if unknown
    """
    if len(binary_str) != 5:
        return '?'
    return BIN_TO_CHAR.get(binary_str, '?')


def char_to_binary(char):
    """
    Convert a character to its 5-bit binary representation.
    
    Args:
        char (str): Single character
    
    Returns:
        str: 5-bit binary string, or None if character not in map
    """
    return CHAR_TO_BIN.get(char.upper())


def text_to_binary(text):
    """
    Convert a text string to concatenated 5-bit binary.
    
    Args:
        text (str): Text to encode
    
    Returns:
        str: Concatenated binary string (5 bits per character)
    """
    binary = ''
    for char in text.upper():
        char_bin = char_to_binary(char)
        if char_bin:
            binary += char_bin
        else:
            # Unknown character - use null
            binary += '00000'
    return binary


def binary_to_text(binary_str):
    """
    Convert concatenated 5-bit binary to text.
    
    Args:
        binary_str (str): Binary string (length must be multiple of 5)
    
    Returns:
        str: Decoded text
    """
    if len(binary_str) % 5 != 0:
        raise ValueError(f"Binary string length must be multiple of 5, got {len(binary_str)}")
    
    text = ''
    for i in range(0, len(binary_str), 5):
        chunk = binary_str[i:i+5]
        text += binary_to_char(chunk)
    return text


def verify_xor_logic():
    """
    Verify that the XOR logic matches Bletchley requirements.
    Tests: K XOR 5 = H
    
    Returns:
        bool: True if verification passes
    """
    k_bin = CHAR_TO_BIN.get('K')
    five_bin = CHAR_TO_BIN.get('5')
    h_bin = CHAR_TO_BIN.get('H')
    
    if not all([k_bin, five_bin, h_bin]):
        print("Warning: Not all test characters found in map")
        return False
    
    # Perform XOR
    k_int = int(k_bin, 2)
    five_int = int(five_bin, 2)
    result_int = k_int ^ five_int
    result_bin = format(result_int, '05b')
    
    print(f"Verification Test: K XOR 5 = H")
    print(f"K = {k_bin} ({k_int})")
    print(f"5 = {five_bin} ({five_int})")
    print(f"K XOR 5 = {result_bin} ({result_int})")
    print(f"H = {h_bin} ({int(h_bin, 2)})")
    print(f"Match: {result_bin == h_bin}")
    
    return result_bin == h_bin


if __name__ == "__main__":
    print("Bletchley Baudot Encoding Map")
    print("=" * 50)
    print("\nCharacter to Binary Mapping:")
    for char in sorted(CHAR_TO_BIN.keys()):
        print(f"{char}: {CHAR_TO_BIN[char]}")
    
    print("\n" + "=" * 50)
    verify_xor_logic()
    
    # Test encoding/decoding
    print("\n" + "=" * 50)
    print("Test Encoding/Decoding:")
    test_text = "HELLO"
    binary = text_to_binary(test_text)
    decoded = binary_to_text(binary)
    print(f"Text: {test_text}")
    print(f"Binary: {binary}")
    print(f"Decoded: {decoded}")
