import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import struct

# Counter for output files
file_counter = 1

def float_to_IEEE754(float_num, exponent):
    # Multiply the floating point number by 10 raised to the power of the exponent
    float_num *= 10 ** exponent

    # Convert the floating point number to IEEE 754/1985 Single Precision Floating Point
    ieee754_bin = ''.join(bin(c).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', float_num))
    ieee754_hex = ''.join(hex(c).replace('0x', '').rjust(2, '0') for c in struct.pack('!f', float_num))

    # Separate the binary output into the sign bit, exponent bits, and mantissa bits
    sign_bit = ieee754_bin[0]
    exponent_bits = ieee754_bin[1:9]
    mantissa_bits = ieee754_bin[9:]
    e_prime = int(exponent_bits, 2)

    # Return the binary and hexadecimal IEEE 754 representations
    return sign_bit, exponent_bits, mantissa_bits, ieee754_hex, e_prime

def convert_and_display():
    try:
        # Attempt to convert user input to float and int
        float_num = float(float_num_entry.get())
        exponent = int(exponent_entry.get())

        # Perform the conversion and update the GUI with the results
        sign_bit, exponent_bits, mantissa_bits, ieee754_hex, e_prime = float_to_IEEE754(float_num, exponent)
        
        # Update the GUI elements with the conversion results
        sign_bit_var.set(sign_bit)
        exponent_bits_var.set(exponent_bits)
        mantissa_bits_var.set(mantissa_bits)
        ieee754_hex_var.set(ieee754_hex)

        # Determine and display the type of the number based on IEEE 754 analysis
        update_number_type(sign_bit, exponent_bits, mantissa_bits, e_prime)

    except ValueError as e:
        # Show error message for invalid input values
        messagebox.showerror("Input error", str(e))
    except OverflowError:
        # Handle the case where the float number is too large for the format
        messagebox.showerror("Overflow error", "The floating-point number is too large.")
    except Exception as e:
        # General error handling for any other unexpected issues
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def update_number_type(sign_bit, exponent_bits, mantissa_bits, e_prime):
    # Logic to determine the number type based on the IEEE 754 standard
    if sign_bit == '0' and exponent_bits == '00000000' and mantissa_bits == '00000000000000000000000':
        number_type_var.set('Zero')
    elif sign_bit == '0' and e_prime >= 255:
        number_type_var.set('Positive Infinity')
    elif sign_bit == '1' and e_prime >= 255:
        number_type_var.set('Negative Infinity')
    elif e_prime == 0 and mantissa_bits != '00000000000000000000000':
        number_type_var.set('Denormalized')
    else:
        number_type_var.set('Finite')

def output_to_file():
    global file_counter
    try:
        filename = f"FP_to_IEEE754_Output_{file_counter}.txt"
        with open(filename, "w") as file:
            file.write("Floating Point to IEEE-754\n\n")
            file.write("User Input:\n")
            file.write("Floating Point Number: {}\n".format(float_num_entry.get()))
            file.write("Exponent: {}\n\n".format(exponent_entry.get()))
            file.write("Output:\n")
            file.write("Sign Bit: {}\n".format(sign_bit_var.get()))
            file.write("Exponent Bits: {}\n".format(exponent_bits_var.get()))
            file.write("Mantissa Bits: {}\n".format(mantissa_bits_var.get()))
            file.write("IEEE 754 (Hex): {}\n".format(ieee754_hex_var.get()))
            file.write("Type: {}\n".format(number_type_var.get()))
        messagebox.showinfo("File Output", "Results have been saved to {}".format(filename))
        file_counter += 1
    except Exception as e:
        messagebox.showerror("File Output Error", f"An error occurred while saving the file: {str(e)}")

def back_to_menu(): # Goes back to the Menu 
    subprocess.Popen(["python", "Binary-32_Floating_Point_Converter.py"])
    root.destroy()  # Close this window
    
# Set up the main window.
root = tk.Tk()
root.title("Floating Point to IEEE-754 Converter")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the Tk root window
x = (screen_width / 2) - (root.winfo_reqwidth() / 2)
y = (screen_height / 2) - (root.winfo_reqheight() / 2)

# Set the position of the window to the center of the screen
root.geometry("+%d+%d" % (x, y))

# Create input fields.
tk.Label(root, text="Floating Point Number:").grid(row=0)
tk.Label(root, text="Exponent:").grid(row=1)

float_num_entry = tk.Entry(root, width=30)
exponent_entry = tk.Entry(root, width=30)

float_num_entry.grid(row=0, column=1, padx=20)
exponent_entry.grid(row=1, column=1)

# Set up variables for output labels.
sign_bit_var = tk.StringVar()
exponent_bits_var = tk.StringVar()
mantissa_bits_var = tk.StringVar()
ieee754_hex_var = tk.StringVar()
number_type_var = tk.StringVar()

# Buttons and Outputs.
convert_button = tk.Button(root, text="Convert", command=convert_and_display)
convert_button.grid(row=2, column=1, pady = 10)

tk.Label(root).grid(row=3) # space

tk.Label(root, text="Sign Bit:").grid(row=4)
tk.Label(root, textvariable=sign_bit_var).grid(row=4, column=1)

tk.Label(root, text="Exponent Bits:").grid(row=5)
tk.Label(root, textvariable=exponent_bits_var).grid(row=5, column=1)

tk.Label(root, text="Mantissa Bits:").grid(row=6)
tk.Label(root, textvariable=mantissa_bits_var).grid(row=6, column=1)

tk.Label(root, text="IEEE 754 (Hex):").grid(row=7)
tk.Label(root, textvariable=ieee754_hex_var).grid(row=7, column=1)

tk.Label(root, text="Type:").grid(row=8)
tk.Label(root, textvariable=number_type_var).grid(row=8, column=1)

tk.Label(root).grid(row=9) # space

output_button = tk.Button(root, text="Output to Text File", command=output_to_file)
output_button.grid(row=10, column=1)

menu_button = tk.Button(root, text="Back To Menu", command=back_to_menu)
menu_button.grid(row=11, column=1, pady=10)

# Start the GUI loop.
root.mainloop()