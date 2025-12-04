#!/usr/bin/env python3
"""
Bletchley Baudot Cryptanalysis GUI
Graphical interface for Two-Time Pad attacks on XORed Baudot messages.

Authors: [Your Name] & Smaran
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from XOREngine import get_xor_stream, drag_crib, binary_to_text
from BletchleyMap import verify_xor_logic


class BaudotSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bletchley Baudot Cryptanalysis Suite")
        self.root.geometry("1000x800")
        
        # Data
        self.xor_stream = None
        self.c1_hex = None
        self.c2_hex = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Title
        title_frame = ttk.Frame(self.root, padding="10")
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame, 
            text="BLETCHLEY BAUDOT CRYPTANALYSIS SUITE",
            font=("Courier", 16, "bold")
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Two-Time Pad Attack Tool",
            font=("Courier", 10)
        )
        subtitle_label.pack()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # === INPUT SECTION ===
        input_frame = ttk.LabelFrame(main_frame, text="Ciphertexts (Hex)", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Ciphertext 1
        ttk.Label(input_frame, text="Ciphertext 1:").grid(row=0, column=0, sticky=tk.W)
        self.c1_entry = ttk.Entry(input_frame, width=80)
        self.c1_entry.grid(row=0, column=1, padx=5, pady=2)
        
        # Ciphertext 2
        ttk.Label(input_frame, text="Ciphertext 2:").grid(row=1, column=0, sticky=tk.W)
        self.c2_entry = ttk.Entry(input_frame, width=80)
        self.c2_entry.grid(row=1, column=1, padx=5, pady=2)
        
        # Compute button
        self.compute_btn = ttk.Button(
            input_frame, 
            text="Compute XOR Stream",
            command=self.compute_xor
        )
        self.compute_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # === XOR STREAM DISPLAY ===
        xor_frame = ttk.LabelFrame(main_frame, text="XOR Stream (P1 ⊕ P2)", padding="10")
        xor_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.xor_display = scrolledtext.ScrolledText(
            xor_frame, 
            height=4, 
            width=90,
            font=("Courier", 10),
            state='disabled'
        )
        self.xor_display.pack(fill=tk.BOTH, expand=True)
        
        # === CRIB SECTION ===
        crib_frame = ttk.LabelFrame(main_frame, text="Crib Dragging", padding="10")
        crib_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Crib input
        crib_input_frame = ttk.Frame(crib_frame)
        crib_input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(crib_input_frame, text="Enter Crib:").pack(side=tk.LEFT, padx=5)
        self.crib_entry = ttk.Entry(crib_input_frame, width=30)
        self.crib_entry.pack(side=tk.LEFT, padx=5)
        self.crib_entry.bind('<Return>', lambda e: self.drag_crib())
        
        self.drag_btn = ttk.Button(
            crib_input_frame,
            text="Drag Crib",
            command=self.drag_crib
        )
        self.drag_btn.pack(side=tk.LEFT, padx=5)
        
        self.show_all_var = tk.BooleanVar(value=False)
        self.show_all_check = ttk.Checkbutton(
            crib_input_frame,
            text="Show All Results",
            variable=self.show_all_var
        )
        self.show_all_check.pack(side=tk.LEFT, padx=5)
        
        # Quick cribs
        quick_frame = ttk.Frame(crib_frame)
        quick_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(quick_frame, text="Quick Cribs:").pack(side=tk.LEFT, padx=5)
        
        common_cribs = ["THE", "AND", "REPORT", "MESSAGE", "SECRET", "FROM", "STOP"]
        for crib in common_cribs:
            btn = ttk.Button(
                quick_frame,
                text=crib,
                width=8,
                command=lambda c=crib: self.use_quick_crib(c)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # === RESULTS SECTION ===
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(3, weight=1)
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=20,
            width=90,
            font=("Courier", 10),
            state='disabled'
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for colored output
        self.results_text.tag_configure("readable", foreground="green", font=("Courier", 10, "bold"))
        self.results_text.tag_configure("unreadable", foreground="gray")
        self.results_text.tag_configure("header", foreground="blue", font=("Courier", 10, "bold"))
        
        # === STATUS BAR ===
        status_frame = ttk.Frame(self.root)
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready. Enter ciphertexts to begin.",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=2)
        
        # === MENU ===
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear All", command=self.clear_all)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Verify XOR Logic", command=self.verify_logic)
        help_menu.add_command(label="About", command=self.show_about)
    
    def compute_xor(self):
        """Compute the XOR of the two ciphertexts."""
        # Get inputs
        c1 = self.c1_entry.get().strip()
        c2 = self.c2_entry.get().strip()
        
        if not c1 or not c2:
            messagebox.showerror("Error", "Please enter both ciphertexts.")
            return
        
        # Clean hex strings
        c1 = ''.join(c for c in c1 if c in '0123456789ABCDEFabcdef')
        c2 = ''.join(c for c in c2 if c in '0123456789ABCDEFabcdef')
        
        if not c1 or not c2:
            messagebox.showerror("Error", "Invalid hex strings.")
            return
        
        try:
            # Compute XOR
            self.xor_stream, chunks = get_xor_stream(c1, c2)
            self.c1_hex = c1
            self.c2_hex = c2
            
            # Display XOR stream
            try:
                xor_text = binary_to_text(self.xor_stream)
                display_text = f"Length: {len(chunks)} chars | XOR Stream: {xor_text}"
            except Exception as e:
                display_text = f"Length: {len(chunks)} chars | Binary: {len(self.xor_stream)} bits"
            
            self.xor_display.config(state='normal')
            self.xor_display.delete(1.0, tk.END)
            self.xor_display.insert(1.0, display_text)
            self.xor_display.config(state='disabled')
            
            self.status_label.config(text=f"✓ XOR stream computed: {len(chunks)} characters")
            
            # Enable crib entry
            self.crib_entry.config(state='normal')
            self.drag_btn.config(state='normal')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compute XOR: {e}")
            self.status_label.config(text="✗ Error computing XOR stream")
    
    def drag_crib(self):
        """Drag the entered crib across the XOR stream."""
        if not self.xor_stream:
            messagebox.showwarning("Warning", "Please compute XOR stream first.")
            return
        
        crib = self.crib_entry.get().strip().upper()
        if not crib:
            messagebox.showwarning("Warning", "Please enter a crib.")
            return
        
        try:
            # Perform crib dragging
            results = drag_crib(self.xor_stream, crib)
            
            # Display results
            self.display_results(results, crib)
            
            self.status_label.config(text=f"Dragged crib '{crib}' across {len(results)} positions")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to drag crib: {e}")
            self.status_label.config(text="✗ Error dragging crib")
    
    def display_results(self, results, crib):
        """Display crib drag results."""
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        
        # Header
        header = f"{'='*80}\n"
        header += f"CRIB DRAG RESULTS FOR: '{crib}'\n"
        header += f"{'='*80}\n\n"
        self.results_text.insert(tk.END, header, "header")
        
        show_all = self.show_all_var.get()
        readable_count = 0
        
        for result in results:
            if result['readable']:
                readable_count += 1
            
            if show_all or result['readable']:
                status = "✓ READABLE" if result['readable'] else "✗"
                line = f"Pos {result['position']:3d}: {result['result_text']:30s} {status}\n"
                
                tag = "readable" if result['readable'] else "unreadable"
                self.results_text.insert(tk.END, line, tag)
        
        # Footer
        footer = f"\n{'='*80}\n"
        footer += f"Found {readable_count} readable results out of {len(results)} positions\n"
        footer += f"{'='*80}\n"
        self.results_text.insert(tk.END, footer, "header")
        
        self.results_text.config(state='disabled')
        self.results_text.see(1.0)  # Scroll to top
    
    def use_quick_crib(self, crib):
        """Use a quick crib button."""
        self.crib_entry.delete(0, tk.END)
        self.crib_entry.insert(0, crib)
        self.drag_crib()
    
    def clear_all(self):
        """Clear all inputs and outputs."""
        self.c1_entry.delete(0, tk.END)
        self.c2_entry.delete(0, tk.END)
        self.crib_entry.delete(0, tk.END)
        
        self.xor_display.config(state='normal')
        self.xor_display.delete(1.0, tk.END)
        self.xor_display.config(state='disabled')
        
        self.results_text.config(state='normal')
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state='disabled')
        
        self.xor_stream = None
        self.c1_hex = None
        self.c2_hex = None
        
        self.status_label.config(text="Ready. Enter ciphertexts to begin.")
    
    def verify_logic(self):
        """Verify the XOR logic."""
        result = verify_xor_logic()
        if result:
            messagebox.showinfo("Verification", "✓ XOR logic verified successfully!\n\nK XOR 5 = H test passed.")
        else:
            messagebox.showwarning("Verification", "⚠ XOR logic verification failed.\n\nThe encoding may need adjustment.")
    
    def show_about(self):
        """Show about dialog."""
        about_text = """
Bletchley Baudot Cryptanalysis Suite
Version 1.0

Authors: [Your Name] & Smaran

A tool for breaking Two-Time Pad encryption 
on Baudot-encoded messages using crib dragging.

Subject: Cryptanalysis of XORed Baudot Messages

© 2025
        """
        messagebox.showinfo("About", about_text)


def main():
    """Run the GUI application."""
    root = tk.Tk()
    app = BaudotSolverGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
