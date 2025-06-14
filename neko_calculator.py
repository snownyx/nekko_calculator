import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk
import os
import sys
from threading import Thread

class NekoCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Neko Calculator ✧˖°")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Get the correct base path for resources
        if getattr(sys, 'frozen', False):
            # If the application is run as a bundle
            self.base_path = sys._MEIPASS
        else:
            # If the application is run from a Python interpreter
            self.base_path = os.path.dirname(os.path.abspath(__file__))
        
        # Set window icon
        try:
            paw_path = os.path.join(self.base_path, 'images', 'paw.jpg')
            paw_img = Image.open(paw_path)
            paw_img = paw_img.resize((32, 32))  # Resize for icon
            self.paw_icon = ImageTk.PhotoImage(paw_img)
            self.root.iconphoto(True, self.paw_icon)
        except Exception as e:
            print(f"Warning: Could not set window icon: {str(e)}")
        
        # Kawaii theme colors
        self.bg_color = "#FFE6F3"  # Light pink
        self.button_color = "#FFB6C1"  # Pastel pink
        self.button_hover = "#FFC0CB"  # Lighter pink
        self.text_color = "#FF69B4"  # Hot pink
        self.display_bg = "#FFFFFF"  # White
        
        # Configure root background
        self.root.configure(bg=self.bg_color)
        
        # Load cat images
        self.load_cat_images()
        
        # Variable to store current calculation
        self.current = ""
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        self.is_calculating = False
        
        # Create main frame
        self.main_frame = tk.Frame(root, bg=self.bg_color)
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Create display with kawaii theme
        self.display_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.display_frame.pack(fill="x", pady=(0, 20))
        
        self.display = tk.Entry(self.display_frame, 
                              textvariable=self.result_var,
                              justify="right",
                              font=("Comic Sans MS", 24),
                              bg=self.display_bg,
                              fg=self.text_color,
                              bd=0,
                              relief="flat")
        self.display.pack(fill="x", ipady=10)
        
        # Cat image label
        self.cat_label = tk.Label(self.display_frame, bg=self.bg_color)
        self.cat_label.pack(pady=10)
        
        # Button layout
        buttons = [
            '7', '8', '9', '÷',
            '4', '5', '6', '×',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]
        
        # Create button frame
        self.button_frame = tk.Frame(self.main_frame, bg=self.bg_color)
        self.button_frame.pack(expand=True, fill="both")
        
        # Create and place buttons
        row = 0
        col = 0
        for button in buttons:
            self.create_button(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # Add Clear button with direct clear function
        clear_btn = tk.Button(self.button_frame,
                            text='C',
                            font=("Comic Sans MS", 16, "bold"),
                            bg=self.button_color,
                            fg=self.text_color,
                            activebackground=self.button_hover,
                            activeforeground=self.text_color,
                            relief="raised",
                            bd=3,
                            command=self.clear)
        
        # Add 3D effect to clear button
        clear_btn.bind("<Enter>", lambda e: clear_btn.configure(relief="sunken"))
        clear_btn.bind("<Leave>", lambda e: clear_btn.configure(relief="raised"))
        
        clear_btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Configure grid weights
        for i in range(4):
            self.button_frame.grid_rowconfigure(i, weight=1)
            self.button_frame.grid_columnconfigure(i, weight=1)
        
        # Show happy cat initially
        self.show_cat_image('happy')
    
    def load_cat_images(self):
        # Load and resize cat images
        self.cat_images = {}
        image_files = {
            'happy': 'happy_cat.jpg',
            'processing': 'processing_cat.jpg',
            'error': 'error_cat.jpg',
            'thankyou': 'thankyou_cat.jpg'
        }
        
        for state, filename in image_files.items():
            try:
                image_path = os.path.join(self.base_path, 'images', filename)
                img = Image.open(image_path)
                img = img.resize((100, 100))  # Resize to a reasonable size
                self.cat_images[state] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image {filename}: {str(e)}")
                # Create a blank image as fallback
                blank_img = Image.new('RGB', (100, 100), self.bg_color)
                self.cat_images[state] = ImageTk.PhotoImage(blank_img)
    
    def create_button(self, text, row, col):
        btn = tk.Button(self.button_frame,
                       text=text,
                       font=("Comic Sans MS", 16, "bold"),
                       bg=self.button_color,
                       fg=self.text_color,
                       activebackground=self.button_hover,
                       activeforeground=self.text_color,
                       relief="raised",
                       bd=3,
                       command=lambda: self.button_click(text))
        
        # Add 3D effect
        btn.bind("<Enter>", lambda e: btn.configure(relief="sunken"))
        btn.bind("<Leave>", lambda e: btn.configure(relief="raised"))
        
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    def show_cat_image(self, state):
        self.cat_label.configure(image=self.cat_images[state])
    
    def button_click(self, key):
        if key == '=':
            self.is_calculating = True
            self.show_cat_image('processing')
            # Simulate calculation delay
            Thread(target=self.calculate_result).start()
        else:
            self.current += key
            self.result_var.set(self.current)
            self.show_cat_image('happy')
    
    def calculate_result(self):
        try:
            # Replace symbols for calculation
            calculation = self.current.replace('×', '*').replace('÷', '/')
            result = eval(calculation)
            self.result_var.set(result)
            self.current = str(result)
            self.show_cat_image('thankyou')
        except:
            self.result_var.set("Error")
            self.current = ""
            self.show_cat_image('error')
        
        self.is_calculating = False
    
    def clear(self):
        self.current = ""
        self.result_var.set("0")
        self.show_cat_image('happy')

if __name__ == "__main__":
    root = tk.Tk()
    calculator = NekoCalculator(root)
    root.mainloop() 