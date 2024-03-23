import os
import subprocess
import tkinter as tk
from tkinter import messagebox

# Counter for output files
file_counter = 1

def binary_to_IEEE754(new_significand, new_exponent):
    # Initial Variables
    sign_bit = '0' if not new_significand.startswith('-') else '1'
    # Remove the sign for processing
    adjusted_significand = new_significand.lstrip('-')

    # Handling zero as a special case
    if adjusted_significand == '0' or adjusted_significand == '0.0':
        return sign_bit, '00000000', '0' * 23, '00000000', "Zero"

    # Ensure the significand has both parts for processing
    if '.' not in adjusted_significand:
        adjusted_significand += '.0'

    # Convert to binary scientific notation for normalization
    normalized_binary, offset = normalize_binary(adjusted_significand)
    new_exponent += offset  # Adjust exponent based on normalization

    # Initialize IEEE 754 binary parts
    e_prime = '00000000'  # Default for denormalized numbers (all bits 0)
    mantissa = ''

    # Handling based on the exponent value
    if new_exponent < -126:
        # Handling for Denormalized numbers
        shift_bits = -126 - new_exponent
        # Ensure the shifting does not remove all significant bits
        if shift_bits > 0:
            # Correctly calculate mantissa for denormalized numbers
            # Using logic from your provided code to adjust the mantissa
            mantissa = '0' * (shift_bits - 1) + '1' + normalized_binary.split('.')[1]
            mantissa = mantissa[:23].ljust(23, '0')
            print_type = "Denormalized"
        else:
            mantissa = '0' * 23
            print_type = "Zero"
    elif new_exponent >= 128:
        # Handling for Infinity (overflow)
        e_prime = '11111111'
        mantissa = '0' * 23
        if sign_bit=='0':
            print_type = "Positive Infinity"
        else:
            print_type = "Negative Infinity"
    else:
        # Handling for Normalized numbers
        e_prime = format(127 + new_exponent, '08b')
        mantissa = normalized_binary.split('.')[1].ljust(23, '0')[:23]
        print_type = "Finite"

    # Construct full IEEE 754 binary string
    ieee_binary = sign_bit + e_prime + mantissa

    # Convert full IEEE 754 binary string to hexadecimal
    hexadecimal_value = format(int(ieee_binary, 2), '08x')

    return sign_bit, e_prime, mantissa, hexadecimal_value, print_type

def round_half_to_even(mantissa):
    # If the 24th bit is 1
    if mantissa[23] == '1':
        # If any of the bits after the 24th bit is 1 or the 23rd bit is 1
        if any(bit == '1' for bit in mantissa[24:]) or mantissa[22] == '1':
            # Round up
            return bin(int(mantissa[:23], 2) + 1)[2:].zfill(23)
    # Otherwise, just take the first 23 bits
    return mantissa[:23]

def normalize_binary(binary_str):
    # Ensure there's a decimal part for splitting
    if '.' not in binary_str:
        binary_str += '.0'
    
    integer_part, fractional_part = binary_str.split('.')

    # Handle normalization differently based on the integer part
    if integer_part == '0':
        # Find the first '1' in the fractional part and calculate shift
        shift_index = fractional_part.find('1')
        if shift_index != -1:
            shift = -(shift_index + 1)  # Adjust for position after decimal
            normalized = '1.' + fractional_part[shift_index + 1:]
        else:
            return '0.0', 0  # Case for binary zero
    else:
        # Normalize numbers with non-zero integer part
        shift = len(integer_part) - 1
        normalized = '1.' + integer_part[1:] + fractional_part

    return normalized, shift

def convert_and_display():
    significand = significand_entry.get()
    exponent = exponent_entry.get()

    try:
        exponent = int(exponent)  # Convert exponent to integer.
        sign_bit, e_prime, fractional_part, hexadecimal_value, print_type = binary_to_IEEE754(significand, exponent)
        
        # Display results in the GUI.
        sign_bit_var.set(sign_bit)
        e_prime_var.set(e_prime)
        fractional_part_var.set(fractional_part)
        hex_value_var.set(hexadecimal_value)
        print_type_STR.set(print_type)

    except ValueError as e:
        messagebox.showerror("Input error", str(e))

def output_to_file():
    global file_counter
    try:
        filename = f"Binary_to_IEEE754_Output_{file_counter}.txt"
        with open(filename, "w") as file:
            file.write("Binary to IEEE-754\n\n")
            file.write("User Input:\n")
            file.write("Significand: {}\n".format(significand_entry.get()))
            file.write("Exponent: {}\n\n".format(exponent_entry.get()))
            file.write("Output:\n")
            file.write("Sign Bit: {}\n".format(sign_bit_var.get()))
            file.write("Exponent Bits: {}\n".format(e_prime_var.get()))
            file.write("Mantissa Bits: {}\n".format(fractional_part_var.get()))
            file.write("IEEE 754 (Hex): {}\n".format(hex_value_var.get()))
            file.write("Type: {}\n".format(print_type_STR.get()))
        messagebox.showinfo("File Output", "Results have been saved to {}".format(filename))
        file_counter += 1
    except Exception as e:
        messagebox.showerror("File Output Error", f"An error occurred while saving the file: {str(e)}")

def back_to_menu(): # Goes back to the Menu 
    subprocess.Popen(["python", "Binary-32_Floating_Point_Converter.py"])
    root.destroy()  # Close this window

# Set up the main window.
root = tk.Tk()
root.title("Binary to IEEE-754 Converter")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the Tk root window
x = (screen_width / 2) - (root.winfo_reqwidth() / 2)
y = (screen_height / 2) - (root.winfo_reqheight() / 2)

# Set the position of the window to the center of the screen
root.geometry("+%d+%d" % (x, y))

# Create input fields.
tk.Label(root, text="Significand:").grid(row=0)
tk.Label(root, text="Exponent:").grid(row=1)

significand_entry = tk.Entry(root, width=30)
exponent_entry = tk.Entry(root, width=30)

significand_entry.grid(row=0, column=1, padx=20)
exponent_entry.grid(row=1, column=1)

# Set up variables for output labels.
sign_bit_var = tk.StringVar()
e_prime_var = tk.StringVar()
fractional_part_var = tk.StringVar()
hex_value_var = tk.StringVar()
print_type_STR = tk.StringVar()

# Buttons and Outputs.
convert_button = tk.Button(root, text="Convert", command=convert_and_display)
convert_button.grid(row=2, column=1, pady=10)

tk.Label(root).grid(row=3) # space

tk.Label(root, text="Sign Bit:").grid(row=4)
tk.Label(root, textvariable=sign_bit_var).grid(row=4, column=1)

tk.Label(root, text="Exponent Bits:").grid(row=5)
tk.Label(root, textvariable=e_prime_var).grid(row=5, column=1)

tk.Label(root, text="Mantissa Bits:").grid(row=6)
tk.Label(root, textvariable=fractional_part_var).grid(row=6, column=1)

tk.Label(root, text="IEEE 754 (Hex):").grid(row=7)
tk.Label(root, textvariable=hex_value_var).grid(row=7, column=1)

tk.Label(root, text="Type:").grid(row=8)
tk.Label(root, textvariable=print_type_STR).grid(row=8, column=1)

tk.Label(root).grid(row=9) # space

output_button = tk.Button(root, text="Output to Text File", command=output_to_file)
output_button.grid(row=10, column=1)

menu_button = tk.Button(root, text="Back To Menu", command=back_to_menu)
menu_button.grid(row=11, column=1, pady=10)

# Start the GUI loop.
root.mainloop()