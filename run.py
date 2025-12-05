#!/usr/bin/env python3
"""
Master Script for Bletchley Baudot Cryptanalysis Suite
Quick access to all tools and features.
"""

import sys
import subprocess
import os


def print_banner():
    """Display the main banner."""
    banner = """
╔════════════════════════════════════════════════════════════════════╗
║       BLETCHLEY BAUDOT CRYPTANALYSIS SUITE                         ║
║       Master Control Interface                                     ║
║       Version 1.0.0                                                ║
╚════════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """Display the main menu."""
    menu = """
═══════════════════════════════════════════════════════════════════════
                           AVAILABLE TOOLS
═══════════════════════════════════════════════════════════════════════

  1. 🖥️  Launch CLI Tool          (BaudotSolver.py)
  2. 🎨 Launch GUI Tool          (SolverUI.py)
  3. 🧪 Run Test Suite           (test_suite.py)
  4. 📚 View Examples            (examples.py)
  5. ✓  Verify Encoding          (BletchleyMap.py)
  6. ⚙️  Test XOR Engine         (XOREngine.py)
  7. 📖 Open Documentation       (README.md)
  8. 📊 View Project Summary     (PROJECT_SUMMARY.md)
  9. 🌐 Open Web Interface       (index.html)
  0. ❌ Exit
  
  ?. Show Quick Reference

═══════════════════════════════════════════════════════════════════════
    """
    print(menu)


def run_tool(script_name, description):
    """Run a Python script."""
    print(f"\n{'='*70}")
    print(f"Starting: {description}")
    print(f"{'='*70}\n")
    
    try:
        subprocess.run([sys.executable, script_name])
    except KeyboardInterrupt:
        print("\n\nTool interrupted by user.")
    except Exception as e:
        print(f"\n✗ Error running {script_name}: {e}")
    
    input("\nPress Enter to return to main menu...")


def open_file(filename):
    """Open a file with the default system application."""
    try:
        if sys.platform == 'darwin':  # macOS
            subprocess.run(['open', filename])
        elif sys.platform == 'win32':  # Windows
            os.startfile(filename)
        else:  # Linux
            subprocess.run(['xdg-open', filename])
        print(f"✓ Opening {filename}...")
    except Exception as e:
        print(f"✗ Could not open {filename}: {e}")
    
    input("\nPress Enter to return to main menu...")


def show_quick_info():
    """Display quick information."""
    info = """
╔════════════════════════════════════════════════════════════════════╗
║                         QUICK REFERENCE                            ║
╚════════════════════════════════════════════════════════════════════╝

📁 PROJECT STRUCTURE:
   BletchleyMap.py     - Baudot encoding dictionary
   XOREngine.py        - XOR operations & crib dragging
   BaudotSolver.py     - Command-line interface
   SolverUI.py         - Graphical interface
   test_suite.py       - Comprehensive tests
   examples.py         - Usage demonstrations

🎯 QUICK START:
   1. Run tests to verify: python3 test_suite.py
   2. View examples: python3 examples.py
   3. Launch tool: python3 BaudotSolver.py (CLI) or SolverUI.py (GUI)

📊 TEST STATUS:
   ✓ 8/8 tests passing
   ✓ XOR verification passing (K ⊕ 5 = H)
   ✓ All modules functional

🔬 THE ATTACK:
   When two messages P₁ and P₂ are encrypted with same key K:
   C₁ ⊕ C₂ = (P₁ ⊕ K) ⊕ (P₂ ⊕ K) = P₁ ⊕ P₂
   
   Use crib dragging to recover both plaintexts!

📚 DOCUMENTATION:
   README.md           - Complete user guide
   PROJECT_SUMMARY.md  - Project overview
   CHANGELOG.md        - Version history

═══════════════════════════════════════════════════════════════════════
    """
    print(info)
    input("\nPress Enter to return to menu...")


def main():
    """Main program loop."""
    while True:
        os.system('clear' if os.name == 'posix' else 'cls')
        print_banner()
        print_menu()
        
        try:
            choice = input("Enter your choice (0-9, ? for help): ").strip()
            
            if choice == '1':
                run_tool('BaudotSolver.py', 'CLI Cryptanalysis Tool')
            
            elif choice == '2':
                run_tool('SolverUI.py', 'GUI Cryptanalysis Tool')
            
            elif choice == '3':
                run_tool('test_suite.py', 'Test Suite')
            
            elif choice == '4':
                run_tool('examples.py', 'Examples & Demonstrations')
            
            elif choice == '5':
                run_tool('BletchleyMap.py', 'Encoding Verification')
            
            elif choice == '6':
                run_tool('XOREngine.py', 'XOR Engine Test')
            
            elif choice == '7':
                open_file('README.md')
            
            elif choice == '8':
                open_file('PROJECT_SUMMARY.md')
            
            elif choice == '9':
                open_file('index.html')
            
            elif choice == '0':
                print("\n" + "="*70)
                print("Thank you for using Bletchley Baudot Cryptanalysis Suite!")
                print("="*70 + "\n")
                sys.exit(0)
            
            elif choice == '?':
                os.system('clear' if os.name == 'posix' else 'cls')
                show_quick_info()
            
            else:
                print("\n✗ Invalid choice. Please enter 0-9 or ? for help.")
                input("Press Enter to continue...")
        
        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("Program interrupted. Goodbye!")
            print("="*70 + "\n")
            sys.exit(0)
        except Exception as e:
            print(f"\n✗ Error: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()