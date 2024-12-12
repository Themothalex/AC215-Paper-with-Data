def add_numbers(a, b):
    """Adds two numbers."""
    return a + b


def multiply_numbers(a, b):
    """Multiplies two numbers."""
    return a * b


def divide_numbers(a, b):
    """Divides two numbers, handling division by zero."""
    if b == 0:
        return None
    return a / b


def concatenate_strings(s1, s2):
    """Concatenates two strings."""
    return s1 + s2


def reverse_string(s):
    """Reverses a string."""
    return s[::-1]


def is_palindrome(s):
    """Checks if a string is a palindrome."""
    return s == s[::-1]
