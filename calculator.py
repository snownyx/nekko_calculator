import tkinter as tk
from tkinter import ttk
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Calculator")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        # Variable to store current calculation
        self.current = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        # Create display
        self.display = ttk.Entry(root, textvariable=self.result_var, justify="right", font=("Arial", 20))
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        
        # Button layout
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # Create and place buttons
        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            ttk.Button(root, text=button, command=cmd).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Add Clear button
        ttk.Button(root, text="C", command=self.clear).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        
        # Configure grid weights
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
    
    def click(self, key):
        if key == '=':
            try:
                result = eval(self.current)
                self.result_var.set(result)
                self.current = str(result)
            except:
                self.result_var.set("Error")
                self.current = ""
        else:
            self.current += key
            self.result_var.set(self.current)
    
    def clear(self):
        self.current = ""
        self.result_var.set("0")

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop() 