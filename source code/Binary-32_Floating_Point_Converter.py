import os
import subprocess
import tkinter as tk

def open_gui1():
    subprocess.Popen(["python", "binary_to_IEEE754.py"])
    root.destroy()  # Close the menu window

def open_gui2():
    subprocess.Popen(["python", "fp_to_IEEE754.py"])
    root.destroy()  # Close the menu window

root = tk.Tk()
root.title("Menu")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the Tk root window
x = (screen_width / 2) - (root.winfo_reqwidth() / 2)
y = (screen_height / 2) - (root.winfo_reqheight() / 2)

# Set the position of the window to the center of the screen
root.geometry("+%d+%d" % (x, y))

label = tk.Label(root, text="Binary-32 Floating Point Converter")
label.pack(pady=10)

button1 = tk.Button(root, text="Binary Floating Point to IEEE-754/1985", command=open_gui1)
button1.pack(padx=30, pady=5)

button2 = tk.Button(root, text="Decimal Floating Point to IEEE-754/1985", command=open_gui2)
button2.pack(padx=10, pady=20)

root.mainloop()