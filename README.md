# Bletchley Baudot Cryptanalysis Suite

**Live Demo:** https://kryptmancer.github.io/Crypt

**Authors:** Aryan & Smaran  
**Subject:** Cryptanalysis of XORed Baudot Messages (Two-Time Pad Attack)

## 📋 Overview

This toolkit facilitates the recovery of two distinct plaintext messages ($P_1$ and $P_2$) that have been encrypted using the same keystream ($K$) - a classic cryptographic vulnerability known as a **Two-Time Pad**.

### The Mathematics

When two messages are encrypted with the same one-time pad key:

$$C_1 = P_1 \oplus K$$
$$C_2 = P_2 \oplus K$$

By XORing the ciphertexts together:

$$C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2$$

The keystream cancels out, leaving only the XOR of the two plaintexts. Using **crib dragging** (trying known words at different positions), we can recover both messages.

## 🚀 Quick Start

### Installation

No external dependencies required for CLI mode. For GUI mode, ensure Tkinter is installed (comes with most Python installations).

```bash
cd /path/to/Crypt
```

### Running the Tools

**Command Line Interface (Recommended for beginners):**
```bash
python3 BaudotSolver.py
```

**Graphical User Interface:**
```bash
python3 SolverUI.py
```

**Run Tests:**
```bash
python3 test_suite.py
```

## 📁 Project Structure

```
Crypt/
├── BletchleyMap.py      # Baudot encoding dictionary (ITA2/Bletchley Park)
├── XOREngine.py         # XOR operations and crib dragging logic
├── BaudotSolver.py      # Command-line interface
├── SolverUI.py          # Graphical interface (Tkinter)
├── test_suite.py        # Comprehensive test suite
├── README.md            # This file
└── css/
    └── style.css        # (Optional styling for web components)
```

## 🔧 Module Details

### BletchleyMap.py

Handles the **5-bit Baudot encoding** based on ITA2 (International Telegraph Alphabet No. 2) with Bletchley Park variations.

**Key Features:**
- `BIN_TO_CHAR`: Dictionary mapping 5-bit binary to characters
- `CHAR_TO_BIN`: Reverse mapping for encoding
- `text_to_binary()`: Convert text to concatenated 5-bit binary
- `binary_to_text()`: Decode 5-bit binary back to text
- `verify_xor_logic()`: Verifies that $K \oplus 5 = H$ per Bletchley specifications

**Sample Encoding:**
```
A = 11000    N = 00110
B = 10011    S = 10100
E = 10000    K = 11110
H = 00101    5 = 01000
```

### XOREngine.py

The cryptanalysis engine that performs XOR operations and crib dragging.

**Key Functions:**
- `get_xor_stream(hex_c1, hex_c2)`: XORs two hex ciphertexts
- `apply_crib(xor_stream, crib_text, position)`: Tests a crib at a specific position
- `drag_crib(xor_stream, crib_text)`: Tries crib at all possible positions
- `is_readable(text)`: Heuristic to identify readable English text

**Crib Dragging Algorithm:**
1. Convert crib to 5-bit Baudot binary
2. XOR crib with XOR stream at each position
3. Decode result back to text
4. Filter for readable results

### BaudotSolver.py

Interactive command-line interface for cryptanalysis.

**Usage:**
1. Enter two hex ciphertexts (C1 and C2)
2. Program computes C1 ⊕ C2
3. Enter cribs (guessed words) like "THE", "REPORT", "MESSAGE"
4. Review results - look for readable English text
5. Use discovered fragments as new cribs

**Commands:**
- `help` - Show help information
- `verify` - Verify XOR logic
- `new` - Enter new ciphertexts
- `quit` - Exit program

### SolverUI.py

Graphical interface built with Tkinter for visual crib dragging.

**Features:**
- Input fields for both ciphertexts
- Real-time XOR stream display
- Quick-access buttons for common cribs
- Color-coded results (green = readable, gray = unreadable)
- Toggle to show all results or just readable ones

## 🎯 Usage Guide

### Step-by-Step Attack

1. **Enter Ciphertexts**
   ```
   Ciphertext 1 (hex): A1B2C3D4E5F6...
   Ciphertext 2 (hex): 1A2B3C4D5E6F...
   ```

2. **Start with Common Cribs**
   - THE, AND, REPORT, MESSAGE, SECRET, ATTACK, FROM, STOP
   - Try short words (3-6 letters) first

3. **Analyze Results**
   - Look for readable English text
   - Note the position where cribs produce readable output
   - Build a mental map of where words might be

4. **Build on Success**
   - Use discovered fragments as new cribs
   - Try variants: "REPORT" → "REPORTS", "REPORTED"
   - Cross-reference positions between different cribs

5. **Reconstruct Messages**
   - Once you find several matching positions
   - Piece together the full plaintext
   - Verify consistency across different cribs

### Example Session

```
Enter Ciphertext 1: 9A7B3C8D4E5F6A1B2C3D
Enter Ciphertext 2: 2B3C4D5E6F7A8B9C0D1E

Computing XOR Stream...
✓ XOR stream computed: 32 characters

Enter crib: REPORT
Dragging crib 'REPORT' across XOR stream...

READABLE RESULTS FOR CRIB: 'REPORT'
====================================
Pos   3: ATTACK
Pos  12: SECRET
====================================

Enter crib: ATTACK
...
```

## 🧪 Testing

Run the comprehensive test suite to verify all components:

```bash
python3 test_suite.py
```

**Tests Include:**
- ✓ Baudot encoding/decoding
- ✓ XOR verification (K ⊕ 5 = H)
- ✓ Text encoding/decoding
- ✓ XOR operations
- ✓ Hex conversion
- ✓ Crib dragging
- ✓ Readability heuristic
- ✓ Two-time pad attack scenario

## 📚 Technical Notes

### Baudot Encoding Specifics

The tool uses **5-bit Baudot encoding** which differs from modern 8-bit ASCII:
- Each character is exactly 5 bits
- Special handling for `00000` (NULL/Blank, displayed as `/`)
- Limited character set: A-Z, and select numbers/symbols

### Hex Alignment Challenge

Standard hex uses 4-bit nibbles, but Baudot uses 5-bit characters. The tool handles this by:
1. Converting hex to full binary string
2. Padding to ensure length is multiple of 5
3. Splitting into 5-bit chunks

### Readability Heuristic

The `is_readable()` function uses these criteria:
- At least 70% of characters must be letters (not special chars)
- At least 40% must be common English letters (E, T, A, O, I, N, S, H, R, D, L, U)
- Minimum length of 3 characters

### Known Limitations

1. **State-less Operation**: Does not track Baudot "Figures/Letters" shift states
2. **English-Only**: Readability heuristic optimized for English text
3. **Manual Process**: Requires human judgment to piece together fragments

## 🔍 Troubleshooting

### "XOR verification failed" warning

The tool tests whether $K \oplus 5 = H$ based on your encoding table. If this fails:
- Check `BletchleyMap.py` for correct 5-bit assignments
- Verify against your specific Baudot variant
- The tool will continue to work, but encoding may need adjustment

### "No readable results found"

Try these strategies:
- Use shorter cribs (3-4 letters)
- Try common words: THE, AND, FOR, WITH
- The messages may use uncommon words
- Check that ciphertexts are entered correctly

### Invalid hex strings

- Remove all spaces, newlines, and formatting
- Ensure only hex characters (0-9, A-F)
- Both ciphertexts should be similar length

## 📖 References

- **ITA2 (Baudot Code)**: International Telegraph Alphabet No. 2
- **Two-Time Pad Attack**: Classic cryptanalysis technique
- **Crib Dragging**: Known-plaintext attack method
- **Bletchley Park**: Historic WWII codebreaking center

## 🎓 Educational Notes

This tool demonstrates several important cryptographic principles:

1. **Never Reuse One-Time Pads**: The security of OTP depends on using each key exactly once
2. **XOR Properties**: $A \oplus B \oplus B = A$ (self-inverse property)
3. **Known-Plaintext Attacks**: If attacker knows part of the plaintext, they can recover more
4. **Frequency Analysis**: Common words appear frequently in natural language

## 🛠️ Future Enhancements

Potential improvements for future versions:
- [ ] Implement Figures/Letters shift state tracking
- [ ] Add frequency analysis visualization
- [ ] Support for multiple language models
- [ ] Automated crib suggestion based on n-gram analysis
- [ ] Export functionality for results
- [ ] Load ciphertexts from file
- [ ] Batch processing mode

## 📝 License

Educational use only. Part of Cryptology coursework.

## 👥 Authors

- **[Your Name]** - Implementation & Testing
- **Smaran** - Design & Analysis

---

**Course:** Cryptology  
**Institution:** [Your Institution]  
**Date:** December 2025

---

## Quick Command Reference

```bash
# Run CLI tool
python3 BaudotSolver.py

# Run GUI tool
python3 SolverUI.py

# Run tests
python3 test_suite.py

# Verify encoding only
python3 BletchleyMap.py

# Test XOR engine
python3 XOREngine.py
```

---

*"The price of reliability is the pursuit of the utmost simplicity."* - Tony Hoare
