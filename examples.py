#!/usr/bin/env python3
"""
Example Usage of Bletchley Baudot Cryptanalysis Suite

This demonstrates how to use the core modules programmatically.
"""

from BletchleyMap import text_to_binary, binary_to_text, CHAR_TO_BIN
from XOREngine import (
    xor_binary_strings, 
    get_xor_stream, 
    drag_crib,
    format_results
)


def example_1_basic_encoding():
    """Example 1: Basic Baudot encoding and decoding."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Baudot Encoding/Decoding")
    print("="*70)
    
    message = "HELLO"
    print(f"Original message: {message}")
    
    # Encode to binary
    binary = text_to_binary(message)
    print(f"Binary (5-bit Baudot): {binary}")
    print(f"Length: {len(binary)} bits ({len(binary)//5} characters)")
    
    # Show individual character encodings
    print("\nCharacter breakdown:")
    for char in message:
        bin_rep = CHAR_TO_BIN.get(char)
        print(f"  {char} = {bin_rep}")
    
    # Decode back
    decoded = binary_to_text(binary)
    print(f"\nDecoded message: {decoded}")
    print(f"Match: {decoded == message}")


def example_2_xor_operation():
    """Example 2: XORing two messages."""
    print("\n" + "="*70)
    print("EXAMPLE 2: XOR Operation on Two Messages")
    print("="*70)
    
    message1 = "ATTACK"
    message2 = "DEFEND"
    
    print(f"Message 1: {message1}")
    print(f"Message 2: {message2}")
    
    # Convert to binary
    bin1 = text_to_binary(message1)
    bin2 = text_to_binary(message2)
    
    print(f"\nMessage 1 binary: {bin1}")
    print(f"Message 2 binary: {bin2}")
    
    # XOR them
    xor_result = xor_binary_strings(bin1, bin2)
    print(f"\nXOR result: {xor_result}")
    
    # Try to decode XOR result (will be gibberish)
    try:
        xor_decoded = binary_to_text(xor_result)
        print(f"XOR decoded: {xor_decoded}")
        print("(This is P1 XOR P2 - not meaningful by itself)")
    except Exception as e:
        print(f"Decode error: {e}")


def example_3_crib_dragging():
    """Example 3: Crib dragging attack."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Crib Dragging Attack")
    print("="*70)
    
    # Simulate two messages encrypted with same key
    message1 = "ATTACK AT DAWN"
    message2 = "REPORT SUCCESS"
    
    # Remove spaces (Baudot has limited charset)
    message1 = message1.replace(" ", "")
    message2 = message2.replace(" ", "")
    
    print(f"Secret Message 1: {message1}")
    print(f"Secret Message 2: {message2}")
    print("\n(Both encrypted with same keystream K)")
    
    # Simulate what attacker sees: C1 XOR C2 = P1 XOR P2
    bin1 = text_to_binary(message1)
    bin2 = text_to_binary(message2)
    
    # Make same length
    min_len = min(len(bin1), len(bin2))
    bin1 = bin1[:min_len]
    bin2 = bin2[:min_len]
    
    xor_stream = xor_binary_strings(bin1, bin2)
    
    print(f"\nAttacker intercepts: C1 XOR C2")
    print(f"XOR stream: {xor_stream[:40]}... ({len(xor_stream)} bits)")
    
    # Try crib "ATTACK"
    print("\n" + "-"*70)
    print("ATTACK STRATEGY: Try common word 'ATTACK' as crib")
    print("-"*70)
    
    crib = "ATTACK"
    results = drag_crib(xor_stream, crib)
    
    # Show results
    print(f"\nDragging crib '{crib}' across XOR stream...")
    print(format_results(results, show_all=False))
    
    # The readable result at position 0 should reveal message2
    if results[0]['readable']:
        print(f"\n✓ SUCCESS! Crib '{crib}' at position 0 revealed: '{results[0]['result_text']}'")
        print(f"  This is Message 2: REPORT...")


def example_4_hex_ciphertexts():
    """Example 4: Working with hex ciphertexts."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Working with Hex Ciphertexts")
    print("="*70)
    
    # Simulate hex ciphertexts
    # In reality, these would be actual intercepted ciphertexts
    message1 = "SECRET"
    message2 = "ATTACK"
    
    # Convert to binary then to hex for simulation
    bin1 = text_to_binary(message1)
    bin2 = text_to_binary(message2)
    
    # Simulate as hex (in real scenario, you'd have actual hex ciphertexts)
    hex1 = hex(int(bin1, 2))[2:].upper()
    hex2 = hex(int(bin2, 2))[2:].upper()
    
    print(f"Ciphertext 1 (hex): {hex1}")
    print(f"Ciphertext 2 (hex): {hex2}")
    
    # Use the XOR engine
    xor_stream, chunks = get_xor_stream(hex1, hex2)
    
    print(f"\nComputed XOR stream: {len(xor_stream)} bits")
    print(f"Number of characters: {len(chunks)}")
    
    # Try cribs
    cribs = ["SECRET", "ATTACK", "THE"]
    
    for crib in cribs:
        print(f"\nTrying crib: '{crib}'")
        results = drag_crib(xor_stream, crib, max_positions=5)
        readable = [r for r in results if r['readable']]
        
        if readable:
            print(f"  ✓ Found readable results:")
            for r in readable[:3]:
                print(f"    Pos {r['position']}: {r['result_text']}")
        else:
            print(f"  ✗ No readable results")


def example_5_incremental_recovery():
    """Example 5: Incremental message recovery."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Incremental Message Recovery")
    print("="*70)
    
    # Long messages
    message1 = "MEETATTHENORTHGATEATSUNRISE"
    message2 = "ATTACKTHECASTLEATMIDNIGHT"
    
    # Make same length
    min_len = min(len(message1), len(message2))
    message1 = message1[:min_len]
    message2 = message2[:min_len]
    
    print(f"Message 1: {message1}")
    print(f"Message 2: {message2}")
    print(f"Length: {len(message1)} characters")
    
    # Create XOR stream
    bin1 = text_to_binary(message1)
    bin2 = text_to_binary(message2)
    xor_stream = xor_binary_strings(bin1, bin2)
    
    print("\nRECOVERY PROCESS:")
    print("-"*70)
    
    # Step 1: Try common words
    cribs = ["MEET", "ATTACK", "THE", "AT"]
    discovered = {}
    
    for crib in cribs:
        results = drag_crib(xor_stream, crib)
        readable = [r for r in results if r['readable']]
        
        if readable:
            print(f"\nCrib '{crib}':")
            for r in readable[:2]:
                print(f"  Pos {r['position']:2d}: {r['result_text']} <- Likely part of other message")
                discovered[r['position']] = (crib, r['result_text'])
    
    print("\n" + "-"*70)
    print("RECONSTRUCTION:")
    print("By trying multiple cribs, we can piece together both messages!")


def main():
    """Run all examples."""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║       BLETCHLEY BAUDOT CRYPTANALYSIS SUITE                         ║
║       Usage Examples & Demonstrations                              ║
╚════════════════════════════════════════════════════════════════════╝
    """)
    
    examples = [
        example_1_basic_encoding,
        example_2_xor_operation,
        example_3_crib_dragging,
        example_4_hex_ciphertexts,
        example_5_incremental_recovery,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n✗ Error in {example_func.__name__}: {e}")
    
    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print("1. Run BaudotSolver.py for interactive CLI tool")
    print("2. Run SolverUI.py for graphical interface")
    print("3. See README.md for complete documentation")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
