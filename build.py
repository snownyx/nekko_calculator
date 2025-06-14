import os
import platform
import subprocess
import shutil
import sys
from PIL import Image

def create_icon():
    try:
        # Open the paw image
        img = Image.open('images/paw.jpg')
        
        # Convert to RGBA if not already
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # Resize to standard icon sizes
        sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
        img.save('icon.ico', sizes=sizes)
        
        # Create PNG version for Linux
        img.save('icon.png')
        return True
    except Exception as e:
        print(f"Warning: Could not create icon: {str(e)}")
        return False

def create_linux_desktop_entry():
    desktop_entry = '''[Desktop Entry]
Version=1.0
Type=Application
Name=Neko Calculator
Comment=A kawaii cat-themed calculator
Exec={}
Icon={}
Terminal=false
Categories=Utility;Calculator;
'''.format(
    os.path.abspath('dist/NekoCalculator'),
    os.path.abspath('dist/icon.png')
)
    
    with open('dist/neko-calculator.desktop', 'w') as f:
        f.write(desktop_entry)

def build_application():
    try:
        # Create dist directory if it doesn't exist
        if not os.path.exists('dist'):
            os.makedirs('dist')
        
        # Install required packages
        print("Installing required packages...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        
        # Create icon
        has_icon = create_icon()
        
        # Create spec file
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Get the absolute path to the images directory
import os
images_path = os.path.abspath('images')

a = Analysis(
    ['neko_calculator.py'],
    pathex=[],
    binaries=[],
    datas=[(images_path, 'images')],  # Use absolute path for images
    hiddenimports=['PIL._tkinter_finder', 'tkinter', 'tkinter.ttk'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NekoCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True temporarily for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
        
        with open('neko_calculator.spec', 'w') as f:
            f.write(spec_content)
        
        # Build the application using python -m pyinstaller
        print("Building application...")
        subprocess.run([sys.executable, '-m', 'PyInstaller', 'neko_calculator.spec'])
        
        # Copy icon to dist folder
        if os.path.exists('icon.png'):
            shutil.copy('icon.png', 'dist/')
        
        # Create Linux desktop entry
        if platform.system() == 'Linux':
            create_linux_desktop_entry()
            print("\nTo install the application on Linux:")
            print("1. Copy the desktop entry to applications directory:")
            print("   sudo cp dist/neko-calculator.desktop /usr/share/applications/")
            print("2. Make the application executable:")
            print("   chmod +x dist/NekoCalculator")
        
        # Create a README file
        readme_content = '''Neko Calculator
==============

A kawaii cat-themed calculator application!

How to Run:
-----------
1. For Windows:
   - Double-click NekoCalculator.exe in the dist folder

2. For Linux:
   - Open terminal in the dist folder
   - Run: ./NekoCalculator
   - Or install desktop entry:
     sudo cp neko-calculator.desktop /usr/share/applications/
     chmod +x NekoCalculator

Features:
---------
- Cute cat-themed interface
- Basic arithmetic operations
- Visual feedback with cat images
- 3D button effects

Created with ❤️ using Python and Tkinter
'''
        
        with open('dist/README.txt', 'w') as f:
            f.write(readme_content)
        
        # Clean up icon files
        if os.path.exists('icon.ico'):
            os.remove('icon.ico')
        if os.path.exists('icon.png'):
            os.remove('icon.png')
        
        print("\nBuild completed successfully!")
        print("You can find your application in the 'dist' folder")
        print("For Windows: Look for NekoCalculator.exe")
        print("For Linux: Look for NekoCalculator")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure Python is installed correctly")
        print("2. Try running: pip3 install pyinstaller")
        print("3. Try running: python3 -m pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_application() 