# --- src/utils.py ---

import os
import uuid
import re # You will need this for validation if you use regex

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def input_non_empty(prompt):
    """Prompt until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value: return value
        print("❌ Input cannot be empty.")

def input_optional_id(prompt):
    """Prompt user for an ID; return None if left empty."""
    value = input(prompt).strip()
    return value if value else str(uuid.uuid4())

def input_number(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit(): return int(value)
        print("❌ Enter a valid number.")

def input_alpha_spaces(prompt):
    """Ensures input only contains letters and spaces."""
    pattern = re.compile(r'^[A-Za-z\s]+$')
    while True:
        value = input(prompt).strip()
        if not value:
            print("❌ Input cannot be empty. Try again!")
        elif not pattern.match(value):
            print("❌ Only letters and spaces allowed!")
        else:
            return value