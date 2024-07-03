"""
Functions needed in main.py to:
- check the validity of hexadecimal color codes
- convert 3-digits to 6-dits hexadecimal color codes
"""

from re import compile, IGNORECASE
from typing import NoReturn

VALID_HEX = compile(r"^#[a-f\d]+$", IGNORECASE)


def check_hex(hex_value: str) -> str | NoReturn:
    """
    Check if a hexadecimal value is valid for a color.
    If it's a 3 hex digit code, converts it to 6 hex digit code

    >>> check_hex("#012")
    '#001122'
    >>> check_hex("#a0f")
    '#aa00ff'
    >>> check_hex("#00AAff")
    '#00AAff'
    >>> check_hex("0AF")
    Traceback (most recent call last):
        ...
    ValueError: le code couleur saisi n'est pas valide
    """
    if not is_a_valid_hex(hex_value):
        raise ValueError("le code couleur saisi n'est pas valide")

    if len(hex_value) == 4:
        hex_value = convert_3_to_6_digits_hex(hex_value)

    return hex_value


def is_a_valid_hex(hex_value: str) -> bool:
    """
    Checks if a hexadecimal rgb value has a valid format.
    :param hex_value: RGB color code in hexadecimal format (3 or 6 hex digits)
    :return: True if valid, False if not.

    >>> is_a_valid_hex("#000000")
    True
    >>> is_a_valid_hex("#FFFFFF")
    True
    >>> is_a_valid_hex("#0123AF")
    True
    >>> is_a_valid_hex("#1234af")
    True
    >>> is_a_valid_hex("FFFFFF")
    False
    >>> is_a_valid_hex("#12345")
    False
    >>> is_a_valid_hex("#0000GG")
    False
    >>> is_a_valid_hex("#123456789")
    False
    >>> is_a_valid_hex("#ABCDEFA")
    False
    >>> is_a_valid_hex("FF0000#")
    False
    >>> is_a_valid_hex("#00F")
    True
    >>> is_a_valid_hex("#abc")
    True
    >>> is_a_valid_hex("#0F")
    False
    >>> is_a_valid_hex("#1234")
    False
    """
    return bool(VALID_HEX.match(hex_value) and len(hex_value) in (4, 7))


def convert_3_to_6_digits_hex(hex_value: str) -> str:
    """
    Converts an 3-chars hexadecimal color code to 6-chars hexadecimal color code.
    :param hex_value: hexadecimal color code with 3 chars after #, such as "#00f"
    :return: string where each alphanumeric char of hex_value is duplicated
    >>> convert_3_to_6_digits_hex("#012")
    '#001122'
    >>> convert_3_to_6_digits_hex("#a0f")
    '#aa00ff'
    """
    return f"#{"".join(char * 2 for char in hex_value[1:])}"
