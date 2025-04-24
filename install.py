import subprocess
import sys

def install_sympy():
    try:
        # Try importing SymPy to check if it's installed
        import sympy
        print("SymPy is already installed.")
    except ImportError:
        # If SymPy is not installed, install it using pip
        print("SymPy is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "sympy"])
        print("SymPy has been successfully installed.")
def intsall_pymunk():
    try:
        # Try importing Pymunk to check if it's installed
        import pymunk
        print("Pymunk is already installed.")
    except ImportError:
        # If Pymunk is not installed, install it using pip
        print("Pymunk is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pymunk"])
        print("Pymunk has been successfully installed.")
def install_pygame():
    try:
        # Try importing Pygame to check if it's installed
        import pygame
        print("Pygame is already installed.")
    except ImportError:
        # If Pygame is not installed, install it using pip
        print("Pygame is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Pygame has been successfully installed.")
if __name__ == "__main__":
    install_sympy()
    intsall_pymunk()
    install_pygame()
    # This script checks if the required libraries are installed and installs them if they are not.