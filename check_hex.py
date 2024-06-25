"""
Functions needed in main.py to:
- check the validity of hexadecimal color codes
- convert 3-digits to 6-dits hexadecimal color codes
"""

from re import compile, IGNORECASE

VALID_HEX = [compile(rf"^#[a-f\d]{{{n}}}$", IGNORECASE) for n in (3, 6)]


def _check_hex(hex_value: str) -> str:
    """
    Check if a hexadecimal value is valid for a color.
    If it's a 3 hex digit code, converts it to 6 hex digit code

    >>> _check_hex("#012")
    '#001122'
    >>> _check_hex("#a0f")
    '#aa00ff'
    >>> _check_hex("#00AAff")
    '#00AAff'
    >>> _check_hex("0AF")
    Traceback (most recent call last):
        ...
    ValueError: le code couleur saisi n'est pas valide
    """

    if not _is_a_valid_hex(hex_value):
        raise ValueError("le code couleur saisi n'est pas valide")

    if len(hex_value) == 4:
        hex_value = _convert_3_to_6_digits_hex(hex_value)

    return hex_value


def _is_a_valid_hex(hex_value: str) -> bool:
    """
    Checks if a hexadecimal rgb value has a valid format.
    :param hex_value: RGB color code in hexadecimal format (3 or 6 hex digits)
    :return: True if valid, False if not.

    >>> _is_a_valid_hex("#000000")
    True
    >>> _is_a_valid_hex("#FFFFFF")
    True
    >>> _is_a_valid_hex("#0123AF")
    True
    >>> _is_a_valid_hex("#1234af")
    True
    >>> _is_a_valid_hex("FFFFFF")
    False
    >>> _is_a_valid_hex("#12345")
    False
    >>> _is_a_valid_hex("#0000GG")
    False
    >>> _is_a_valid_hex("#123456789")
    False
    >>> _is_a_valid_hex("#ABCDEFA")
    False
    >>> _is_a_valid_hex("FF0000#")
    False
    >>> _is_a_valid_hex("#00F")
    True
    >>> _is_a_valid_hex("#abc")
    True
    >>> _is_a_valid_hex("#0F")
    False
    >>> _is_a_valid_hex("#1234")
    False
    """
    return any(regex.match(hex_value) for regex in VALID_HEX)


def _convert_3_to_6_digits_hex(hex_value: str) -> str:
    """
    Converts an 3-chars hexadecimal color code to 6-chars hexadecimal color code.
    :param hex_value: hexadecimal color code with 3 chars after #, such as "#00f"
    :return: string where each alphanumeric char of hex_value is duplicated
    >>> _convert_3_to_6_digits_hex("#012")
    '#001122'
    >>> _convert_3_to_6_digits_hex("#a0f")
    '#aa00ff'
    """
    return f"#{"".join(char * 2 for char in hex_value[1:])}"


if __name__ == '__main__':
    from doctest import testmod
    if testmod().failed == 0:
        print("Tests passés avec succès ")
        print("👍🏼 OK! 👍🏼")
