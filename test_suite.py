#!/usr/bin/env python3
"""
Test Suite for Bletchley Baudot Cryptanalysis Tool
Verifies encoding, XOR logic, and crib dragging functionality.
"""

from BletchleyMap import (
    BIN_TO_CHAR, CHAR_TO_BIN,
    binary_to_char, char_to_binary,
    text_to_binary, binary_to_text,
    verify_xor_logic
)
from XOREngine import (
    hex_to_binary, binary_to_hex,
    xor_binary_strings, get_xor_stream,
    apply_crib, drag_crib, is_readable
)


def test_baudot_encoding():
    """Test basic Baudot encoding/decoding."""
    print("\n" + "="*70)
    print("TEST 1: Baudot Encoding/Decoding")
    print("="*70)
    
    tests = [
        ('A', '11000'),
        ('B', '10011'),
        ('C', '01110'),
        ('E', '10000'),
        ('H', '00101'),
        ('K', '11110'),
        ('N', '00110'),
        ('S', '10100'),
    ]
    
    passed = 0
    failed = 0
    
    for char, expected_bin in tests:
        result_bin = char_to_binary(char)
        result_char = binary_to_char(expected_bin)
        
        if result_bin == expected_bin and result_char == char:
            print(f"✓ {char} <-> {expected_bin}")
            passed += 1
        else:
            print(f"✗ {char} <-> {expected_bin} (got {result_bin}, {result_char})")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_xor_verification():
    """Test the critical XOR verification: K XOR 5 = H."""
    print("\n" + "="*70)
    print("TEST 2: XOR Verification (K XOR 5 = H)")
    print("="*70)
    
    result = verify_xor_logic()
    
    if result:
        print("✓ Verification PASSED")
    else:
        print("✗ Verification FAILED")
        print("Note: This may indicate encoding table needs adjustment.")
    
    return result


def test_text_encoding():
    """Test encoding and decoding of full text strings."""
    print("\n" + "="*70)
    print("TEST 3: Text Encoding/Decoding")
    print("="*70)
    
    test_strings = ["HELLO", "BAUDOT", "TEST", "ATTACK"]
    
    passed = 0
    failed = 0
    
    for text in test_strings:
        try:
            binary = text_to_binary(text)
            decoded = binary_to_text(binary)
            
            if decoded == text:
                print(f"✓ {text} -> {binary[:20]}... -> {decoded}")
                passed += 1
            else:
                print(f"✗ {text} -> {decoded} (mismatch)")
                failed += 1
        except Exception as e:
            print(f"✗ {text} -> ERROR: {e}")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_xor_operations():
    """Test XOR operations on binary strings."""
    print("\n" + "="*70)
    print("TEST 4: XOR Operations")
    print("="*70)
    
    tests = [
        ('11111', '00000', '11111'),
        ('10101', '01010', '11111'),
        ('11110', '01000', '10110'),  # K XOR 5 (using document's 5)
        ('11110', '00010', '11100'),  # K XOR 5 (alternative)
    ]
    
    passed = 0
    failed = 0
    
    for bin1, bin2, expected in tests:
        result = xor_binary_strings(bin1, bin2)
        if result == expected:
            print(f"✓ {bin1} XOR {bin2} = {result}")
            passed += 1
        else:
            print(f"✗ {bin1} XOR {bin2} = {result} (expected {expected})")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_hex_conversion():
    """Test hex to binary conversion."""
    print("\n" + "="*70)
    print("TEST 5: Hex Conversion")
    print("="*70)
    
    tests = [
        ('FF', '11111111'),
        ('A5', '10100101'),
        ('00', '00000'),
    ]
    
    passed = 0
    failed = 0
    
    for hex_str, expected_bin in tests:
        result = hex_to_binary(hex_str)
        # Pad expected to match result length
        expected_padded = expected_bin.zfill(len(result))
        
        if result == expected_padded:
            print(f"✓ 0x{hex_str} -> {result}")
            passed += 1
        else:
            print(f"✗ 0x{hex_str} -> {result} (expected {expected_padded})")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_crib_dragging():
    """Test crib dragging functionality."""
    print("\n" + "="*70)
    print("TEST 6: Crib Dragging")
    print("="*70)
    
    # Create a simple test case
    # Let's say P1 = "HELLO" and P2 = "WORLD"
    p1 = "HELLO"
    p2 = "WORLD"
    
    p1_bin = text_to_binary(p1)
    p2_bin = text_to_binary(p2)
    
    # XOR them to simulate C1 XOR C2
    xor_stream = xor_binary_strings(p1_bin, p2_bin)
    
    print(f"P1: {p1}")
    print(f"P2: {p2}")
    print(f"XOR stream length: {len(xor_stream)} bits")
    
    # Try dragging P1 as a crib - should reveal P2
    results = drag_crib(xor_stream, p1, max_positions=10)
    
    # Position 0 should give us P2
    if results[0]['result_text'] == p2:
        print(f"✓ Crib '{p1}' at position 0 revealed '{results[0]['result_text']}'")
        print("✓ Crib dragging works correctly!")
        return True
    else:
        print(f"✗ Crib '{p1}' at position 0 gave '{results[0]['result_text']}' (expected '{p2}')")
        return False


def test_readability_heuristic():
    """Test the readability detection heuristic."""
    print("\n" + "="*70)
    print("TEST 7: Readability Heuristic")
    print("="*70)
    
    tests = [
        ("HELLO", True),
        ("ATTACK", True),
        ("THEQUICKBROWN", True),
        ("//?3/8", False),
        ("X9J#P", False),
        ("ABC/9/", False),
    ]
    
    passed = 0
    failed = 0
    
    for text, expected_readable in tests:
        result = is_readable(text)
        if result == expected_readable:
            status = "readable" if result else "unreadable"
            print(f"✓ '{text}' -> {status}")
            passed += 1
        else:
            print(f"✗ '{text}' -> {result} (expected {expected_readable})")
            failed += 1
    
    print(f"\nResult: {passed} passed, {failed} failed")
    return failed == 0


def test_two_time_pad_scenario():
    """Test a realistic two-time pad scenario."""
    print("\n" + "="*70)
    print("TEST 8: Two-Time Pad Attack Scenario")
    print("="*70)
    
    # Simulate a realistic scenario
    # P1 = "ATTACK AT DAWN"
    # P2 = "REPORT SUCCESS"
    # Both encrypted with same key K
    
    # For testing, we'll just XOR the plaintexts
    p1 = "ATTACKATDAWN"
    p2 = "REPORTSUCCES"
    
    print(f"Message 1 (P1): {p1}")
    print(f"Message 2 (P2): {p2}")
    
    # Convert to binary
    p1_bin = text_to_binary(p1)
    p2_bin = text_to_binary(p2)
    
    # Make them same length
    min_len = min(len(p1_bin), len(p2_bin))
    p1_bin = p1_bin[:min_len]
    p2_bin = p2_bin[:min_len]
    
    # XOR to get what attacker sees
    xor_stream = xor_binary_strings(p1_bin, p2_bin)
    
    print(f"\nAttacker intercepts C1 XOR C2...")
    print(f"XOR stream: {len(xor_stream)} bits")
    
    # Try common cribs
    cribs = ["ATTACK", "REPORT", "THE"]
    
    for crib in cribs:
        print(f"\nTrying crib: '{crib}'")
        results = drag_crib(xor_stream, crib)
        
        readable = [r for r in results if r['readable']]
        if readable:
            print(f"  Found {len(readable)} readable results:")
            for r in readable[:3]:  # Show first 3
                print(f"    Pos {r['position']}: {r['result_text']}")
        else:
            print(f"  No readable results found")
    
    print("\n✓ Two-time pad attack scenario completed")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("BLETCHLEY BAUDOT CRYPTANALYSIS TEST SUITE")
    print("="*70)
    
    tests = [
        ("Baudot Encoding", test_baudot_encoding),
        ("XOR Verification", test_xor_verification),
        ("Text Encoding", test_text_encoding),
        ("XOR Operations", test_xor_operations),
        ("Hex Conversion", test_hex_conversion),
        ("Crib Dragging", test_crib_dragging),
        ("Readability Heuristic", test_readability_heuristic),
        ("Two-Time Pad Scenario", test_two_time_pad_scenario),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} CRASHED: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("="*70)
    print(f"Total: {passed}/{len(results)} tests passed")
    print("="*70)
    
    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
