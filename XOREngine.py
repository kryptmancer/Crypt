"""
XOR Engine for Baudot Cryptanalysis
Handles XOR operations on ciphertexts and crib dragging.
"""

from BletchleyMap import text_to_binary, binary_to_text, binary_to_char


def hex_to_binary(hex_string):
    """
    Convert hex string to binary string.
    
    Args:
        hex_string (str): Hexadecimal string (can have spaces or 0x prefix)
    
    Returns:
        str: Binary string
    """
    # Clean the hex string
    hex_string = hex_string.replace(' ', '').replace('0x', '').replace('0X', '')
    
    # Convert to binary
    binary = bin(int(hex_string, 16))[2:]  # [2:] removes '0b' prefix
    
    # Ensure it's a multiple of 5 bits by padding with leading zeros if needed
    remainder = len(binary) % 5
    if remainder != 0:
        binary = '0' * (5 - remainder) + binary
    
    return binary


def binary_to_hex(binary_string):
    """
    Convert binary string to hex string.
    
    Args:
        binary_string (str): Binary string
    
    Returns:
        str: Hexadecimal string
    """
    # Convert to integer then to hex
    hex_val = hex(int(binary_string, 2))[2:].upper()
    return hex_val


def xor_binary_strings(bin1, bin2):
    """
    XOR two binary strings of equal length.
    
    Args:
        bin1 (str): First binary string
        bin2 (str): Second binary string
    
    Returns:
        str: XOR result as binary string
    """
    # Ensure equal length by padding the shorter one
    max_len = max(len(bin1), len(bin2))
    bin1 = bin1.zfill(max_len)
    bin2 = bin2.zfill(max_len)
    
    # XOR bit by bit
    result = ''
    for b1, b2 in zip(bin1, bin2):
        result += '1' if b1 != b2 else '0'
    
    return result


def get_xor_stream(hex_c1, hex_c2):
    """
    Convert two hex ciphertexts to binary and XOR them.
    Returns the XOR sum broken into 5-bit chunks.
    
    Args:
        hex_c1 (str): First ciphertext in hex
        hex_c2 (str): Second ciphertext in hex
    
    Returns:
        tuple: (binary_xor_string, list_of_5bit_chunks)
    """
    # Convert hex to binary
    bin_c1 = hex_to_binary(hex_c1)
    bin_c2 = hex_to_binary(hex_c2)
    
    # XOR them
    xor_result = xor_binary_strings(bin_c1, bin_c2)
    
    # Break into 5-bit chunks
    chunks = []
    for i in range(0, len(xor_result), 5):
        chunk = xor_result[i:i+5]
        if len(chunk) == 5:
            chunks.append(chunk)
        elif len(chunk) > 0:
            # Pad the last chunk if needed
            chunks.append(chunk.ljust(5, '0'))
    
    return xor_result, chunks


def apply_crib(xor_stream, crib_text, position):
    """
    Apply a crib (known plaintext guess) at a specific position in the XOR stream.
    This reveals what the other plaintext would be at that position.
    
    Formula: (P1 XOR P2) XOR P1_guess = P2_revealed
    
    Args:
        xor_stream (str): Binary string of XORed ciphertexts (C1 XOR C2 = P1 XOR P2)
        crib_text (str): The guessed plaintext (crib)
        position (int): Character position to start the crib (0-indexed)
    
    Returns:
        dict: {
            'crib': crib_text,
            'position': position,
            'crib_binary': binary representation of crib,
            'result_binary': XOR result,
            'result_text': decoded result,
            'readable': boolean indicating if result looks readable
        }
    """
    # Convert crib to binary
    crib_binary = text_to_binary(crib_text)
    crib_length = len(crib_binary)
    
    # Calculate bit position (position * 5 since each char is 5 bits)
    bit_position = position * 5
    
    # Check if crib fits
    if bit_position + crib_length > len(xor_stream):
        return {
            'crib': crib_text,
            'position': position,
            'crib_binary': crib_binary,
            'result_binary': '',
            'result_text': '[OUT OF BOUNDS]',
            'readable': False
        }
    
    # Extract the relevant portion of XOR stream
    xor_portion = xor_stream[bit_position:bit_position + crib_length]
    
    # XOR the crib with the XOR stream portion
    result_binary = xor_binary_strings(xor_portion, crib_binary)
    
    # Decode the result
    try:
        result_text = binary_to_text(result_binary)
        # Check if result is "readable" (mostly letters, not special chars)
        readable = is_readable(result_text)
    except Exception as e:
        result_text = f"[DECODE ERROR: {e}]"
        readable = False
    
    return {
        'crib': crib_text,
        'position': position,
        'crib_binary': crib_binary,
        'result_binary': result_binary,
        'result_text': result_text,
        'readable': readable
    }


def is_readable(text):
    """
    Heuristic to determine if text looks like readable English.
    Checks for high frequency of common letters.
    
    Args:
        text (str): Text to check
    
    Returns:
        bool: True if text appears readable
    """
    if not text or len(text) < 3:
        return False
    
    # Count letters vs special characters
    letters = sum(1 for c in text if c.isalpha())
    special = sum(1 for c in text if c in ['/', '?', '3', '4', '5', '8', '9'])
    
    # At least 70% should be letters
    if letters / len(text) < 0.7:
        return False
    
    # Check for common English letters
    common_letters = 'ETAOINSHRDLU'
    common_count = sum(1 for c in text.upper() if c in common_letters)
    
    # At least 40% should be common letters
    if letters > 0 and common_count / letters < 0.4:
        return False
    
    return True


def drag_crib(xor_stream, crib_text, max_positions=None):
    """
    Drag a crib across all positions in the XOR stream.
    
    Args:
        xor_stream (str): Binary XOR stream
        crib_text (str): The crib to drag
        max_positions (int, optional): Maximum positions to try. If None, tries all.
    
    Returns:
        list: List of result dictionaries from apply_crib
    """
    # Calculate maximum number of positions
    crib_binary = text_to_binary(crib_text)
    crib_length = len(crib_binary)
    max_pos = (len(xor_stream) - crib_length) // 5 + 1
    
    if max_positions:
        max_pos = min(max_pos, max_positions)
    
    results = []
    for pos in range(max_pos):
        result = apply_crib(xor_stream, crib_text, pos)
        results.append(result)
    
    return results


def format_results(results, show_all=False):
    """
    Format crib drag results for display.
    
    Args:
        results (list): List of result dictionaries
        show_all (bool): If False, only show readable results
    
    Returns:
        str: Formatted results string
    """
    output = []
    output.append("=" * 80)
    output.append(f"CRIB DRAG RESULTS FOR: '{results[0]['crib']}'")
    output.append("=" * 80)
    
    readable_count = 0
    for result in results:
        if result['readable']:
            readable_count += 1
        
        if show_all or result['readable']:
            status = "✓ READABLE" if result['readable'] else "✗"
            output.append(f"Pos {result['position']:3d}: {result['result_text']:30s} {status}")
    
    output.append("=" * 80)
    output.append(f"Found {readable_count} readable results out of {len(results)} positions")
    output.append("=" * 80)
    
    return '\n'.join(output)


if __name__ == "__main__":
    print("XOR Engine Test")
    print("=" * 50)
    
    # Test XOR operations
    test_hex1 = "A1B2C3"
    test_hex2 = "D4E5F6"
    
    print(f"Test Hex 1: {test_hex1}")
    print(f"Test Hex 2: {test_hex2}")
    
    xor_stream, chunks = get_xor_stream(test_hex1, test_hex2)
    print(f"\nXOR Stream (binary): {xor_stream}")
    print(f"Number of 5-bit chunks: {len(chunks)}")
    
    # Try to decode the XOR stream
    try:
        decoded = binary_to_text(xor_stream)
        print(f"Decoded XOR stream: {decoded}")
    except Exception as e:
        print(f"Decode error: {e}")
    
    # Test crib dragging
    print("\n" + "=" * 50)
    print("Test Crib Dragging:")
    test_crib = "THE"
    print(f"Crib: {test_crib}")
    
    results = drag_crib(xor_stream, test_crib, max_positions=10)
    print(format_results(results, show_all=True))
