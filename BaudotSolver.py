#!/usr/bin/env python3
"""
Bletchley Baudot Cryptanalysis CLI
Command-line interface for Two-Time Pad attacks on XORed Baudot messages.

Authors: [Your Name] & Smaran
Subject: Cryptanalysis of XORed Baudot Messages
"""

import sys
from XOREngine import (
    get_xor_stream, 
    drag_crib, 
    format_results, 
    binary_to_text,
    hex_to_binary
)
from BletchleyMap import verify_xor_logic


def print_banner():
    """Display the program banner."""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║       BLETCHLEY BAUDOT CRYPTANALYSIS SUITE                         ║
║       Two-Time Pad Attack Tool                                     ║
║       Authors: [Your Name] & Smaran                                ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def display_help():
    """Display help information."""
    help_text = """
USAGE:
    python3 BaudotSolver.py

DESCRIPTION:
    This tool helps break Two-Time Pad encryption on Baudot-encoded messages.
    When two messages (P1 and P2) are encrypted with the same keystream (K):
    
    C1 = P1 XOR K
    C2 = P2 XOR K
    C1 XOR C2 = P1 XOR P2
    
    By dragging known words (cribs) across C1 XOR C2, we can recover both
    plaintext messages.

PROCESS:
    1. Enter two hex ciphertexts (C1 and C2)
    2. The tool computes C1 XOR C2
    3. Enter a crib (guessed word) like "THE", "REPORT", etc.
    4. The tool tries the crib at every position
    5. Look for readable English text in the results
    6. Repeat with new cribs to build the complete plaintext

TIPS:
    - Common cribs: THE, AND, REPORT, MESSAGE, SECRET, FROM, STOP
    - Look for results marked as "✓ READABLE"
    - Build your plaintext incrementally
    - Use discovered fragments as new cribs

COMMANDS:
    help    - Show this help message
    verify  - Verify XOR logic (K XOR 5 = H test)
    new     - Enter new ciphertexts
    quit    - Exit the program
    """
    print(help_text)


def get_multiline_hex(prompt):
    """
    Get hex input from user, allowing multi-line paste.
    
    Args:
        prompt (str): Prompt to display
    
    Returns:
        str: Cleaned hex string
    """
    print(prompt)
    print("(Paste hex string, can be multi-line. Press Enter twice when done)")
    
    lines = []
    empty_count = 0
    
    while True:
        line = input().strip()
        if not line:
            empty_count += 1
            if empty_count >= 2 or (empty_count >= 1 and lines):
                break
        else:
            empty_count = 0
            lines.append(line)
    
    # Combine all lines and clean
    hex_string = ''.join(lines)
    hex_string = ''.join(c for c in hex_string if c in '0123456789ABCDEFabcdef')
    
    return hex_string


def interactive_mode(c1_hex, c2_hex, xor_stream):
    """
    Interactive crib dragging mode.
    
    Args:
        c1_hex (str): First ciphertext in hex
        c2_hex (str): Second ciphertext in hex
        xor_stream (str): Binary XOR stream
    """
    print("\n" + "=" * 70)
    print("INTERACTIVE CRIB DRAGGING MODE")
    print("=" * 70)
    
    # Try to decode and display the XOR stream
    try:
        xor_decoded = binary_to_text(xor_stream)
        print(f"\nXOR Stream (P1 XOR P2): {xor_decoded}")
        print(f"Length: {len(xor_decoded)} characters")
    except Exception as e:
        print(f"XOR Stream length: {len(xor_stream)} bits ({len(xor_stream)//5} characters)")
    
    print("\nEnter cribs to drag across the XOR stream.")
    print("Type 'help' for commands, 'quit' to exit, 'new' for new ciphertexts.\n")
    
    while True:
        try:
            crib = input("\nEnter crib (or command): ").strip()
            
            if not crib:
                continue
            
            crib_lower = crib.lower()
            
            if crib_lower == 'quit' or crib_lower == 'exit' or crib_lower == 'q':
                print("Exiting...")
                break
            
            elif crib_lower == 'help' or crib_lower == 'h':
                display_help()
                continue
            
            elif crib_lower == 'new':
                return 'new'
            
            elif crib_lower == 'verify':
                print("\n" + "=" * 70)
                verify_xor_logic()
                print("=" * 70)
                continue
            
            elif crib_lower == 'show':
                # Show the XOR stream again
                try:
                    xor_decoded = binary_to_text(xor_stream)
                    print(f"\nXOR Stream: {xor_decoded}")
                except:
                    pass
                continue
            
            # It's a crib - drag it!
            print(f"\nDragging crib '{crib.upper()}' across XOR stream...")
            
            results = drag_crib(xor_stream, crib)
            
            # First show only readable results
            readable_results = [r for r in results if r['readable']]
            
            if readable_results:
                print("\n" + "=" * 70)
                print(f"READABLE RESULTS FOR CRIB: '{crib.upper()}'")
                print("=" * 70)
                for result in readable_results:
                    print(f"Pos {result['position']:3d}: {result['result_text']}")
                print("=" * 70)
            else:
                print("\nNo readable results found.")
            
            # Ask if user wants to see all results
            show_all = input("\nShow all results? (y/n): ").strip().lower()
            if show_all == 'y' or show_all == 'yes':
                print(format_results(results, show_all=True))
        
        except KeyboardInterrupt:
            print("\n\nInterrupted. Type 'quit' to exit.")
            continue
        except EOFError:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return 'quit'


def main():
    """Main program loop."""
    print_banner()
    
    # Verify the encoding logic
    print("Verifying Baudot encoding...")
    if not verify_xor_logic():
        print("\n⚠ WARNING: XOR verification failed!")
        print("The encoding may need adjustment. Check BletchleyMap.py")
        print("Continuing anyway...\n")
    else:
        print("✓ XOR logic verified successfully!\n")
    
    display_help()
    
    while True:
        # Get ciphertexts
        print("\n" + "=" * 70)
        print("ENTER CIPHERTEXTS")
        print("=" * 70)
        
        c1_hex = get_multiline_hex("\n[1] Enter Ciphertext 1 (hex):")
        if not c1_hex:
            print("No ciphertext entered. Exiting.")
            break
        
        c2_hex = get_multiline_hex("\n[2] Enter Ciphertext 2 (hex):")
        if not c2_hex:
            print("No ciphertext entered. Exiting.")
            break
        
        print(f"\nC1 length: {len(c1_hex)} hex chars ({len(c1_hex)*4} bits)")
        print(f"C2 length: {len(c2_hex)} hex chars ({len(c2_hex)*4} bits)")
        
        # Compute XOR stream
        print("\nComputing XOR stream (C1 XOR C2)...")
        try:
            xor_stream, chunks = get_xor_stream(c1_hex, c2_hex)
            print(f"✓ XOR stream computed: {len(xor_stream)} bits ({len(chunks)} Baudot characters)")
        except Exception as e:
            print(f"✗ Error computing XOR stream: {e}")
            continue
        
        # Enter interactive mode
        result = interactive_mode(c1_hex, c2_hex, xor_stream)
        
        if result == 'quit':
            break
        elif result == 'new':
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
