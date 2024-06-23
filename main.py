"""
COULEURS COMPLÉMENTAIRES
Challenge on the "Docstring" Discord server
Date: 2024-06-22
"""

import re
import colorsys
from functools import wraps
from typing import Callable, Any

# region Checking constants and functions
VALID_HEX_3 = r"^#[0-9A-Fa-f]{3}$"
VALID_HEX_6 = r"^#[0-9A-Fa-f]{6}$"
VALID_HEX = fr"^{VALID_HEX_3}|{VALID_HEX_6}$"


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
    return True if re.match(VALID_HEX, hex_value) else False


def convert_3_to_6_digits_hex(hex_value: str) -> str:
    """
    Converts an 3-chars hexadecimal color code to 6-chars hexadecimal color code.
    :param hex_value: hexadecimal color code with 3 chars after #, such as "#00F"
    :return: string where each alphanumeric char of hexa-rgb_3 is duplicated

    >>> convert_3_to_6_digits_hex("#012")
    '#001122'
    >>> convert_3_to_6_digits_hex("#a0f")
    '#aa00ff'
    >>> convert_3_to_6_digits_hex("#00AAff")
    '#00AAff'
    >>> convert_3_to_6_digits_hex("0AF")
    Traceback (most recent call last):
        ...
    ValueError: le code couleur saisi n'est pas valide
    """
    if re.match(VALID_HEX_6, hex_value):
        return hex_value

    if not re.match(VALID_HEX_3, hex_value):
        raise ValueError("le code couleur saisi n'est pas valide")

    return "#" + "".join(char * 2 for char in hex_value[1:])


def check_hex(f: Callable) -> Callable:
    """Check if a hexadecimal value is valid for a color.
    If it's a 3 hex digit code, converts it to 6 hex digit code"""
    @wraps(f)
    def wrapper(hex_value: str) -> Any:
        if not is_a_valid_hex(hex_value):
            raise ValueError("le code couleur saisi n'est pas valide")
        if len(hex_value) == 4:
            hex_value = convert_3_to_6_digits_hex(hex_value)
        res = f(hex_value)
        return res
    return wrapper
# endregion


# region Converting functions
@check_hex
def convert_hex_to_rvb(hex_value: str) -> list:
    """
    Converts a hexadecimal color code to its RGB code (=RVB in French).
    :param hex_value: RGB color code in hexadecimal format (with 6 chars after #)
    :return: list containing the 3 decimal RGB color codes

    >>> convert_hex_to_rvb("#FF0000")
    [255, 0, 0]
    >>> convert_hex_to_rvb("#0000FF")
    [0, 0, 255]
    >>> convert_hex_to_rvb("#800080")
    [128, 0, 128]
    >>> convert_hex_to_rvb("#FFC0CB")
    [255, 192, 203]
    """
    return [int(hex_value[i:i + 2], 16) for i in (1, 3, 5)]


def convert_rvb_to_hex(rvb: tuple[int, int, int]) -> str:
    """
    Converts a rgb color code to hexadecimal code.
    :param rvb: tuple containing the 3 decimal RGB (=RVB in French) color codes
    :return: hexadecimal color code

    >>> convert_rvb_to_hex((255, 255, 255))
    '#ffffff'
    >>> convert_rvb_to_hex((0, 0, 0))
    '#000000'
    """
    return f"#{rvb[0]:02x}{rvb[1]:02x}{rvb[2]:02x}"
# endregion


# region Challenge functions
@check_hex
def get_color_types(hex_value: str) -> dict:
    """
    Converts hexadecimal RGB format to decimal RGB and TSL formats
    :param hex_value: RGB color code in hexadecimal format
    :return: dictionary with those keys:
    - 'hex': [str] hexadecimal value of the color passed as an argument
    - 'rvb': [list] decimal values of RGB elements
    - 'tsl_norm': [tuple] values of HSL (=TSL in French) elements
    (color in 360° hue, saturation in %, and luminosity in %)
    - 'tsl': [tuple] values of HSV elements
    (hue, saturation and luminosity in [0 - 1] format)

    >>> get_color_types("#19021e")
    {'hex': '#19021e', 'rvb': [25, 2, 30], 'tsl_norm': ('289°', '88%', '6%'), 'tsl': (0.8035714285714285, 0.875, 0.06274509803921569)}
    """
    hex_value = hex_value.lower()
    red, green, blue = convert_hex_to_rvb(hex_value)
    hue, luminosity, saturation = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
    h_norm, s_norm, l_norm = tuple(round(val) for val in
                                   (hue * 360, saturation * 100, luminosity * 100))
    tsl_norm = (f"{h_norm}°", f"{s_norm}%", f"{l_norm}%")

    return {"hex": hex_value,
            "rvb": convert_hex_to_rvb(hex_value),
            "tsl_norm": tsl_norm,
            "tsl": (hue, saturation, luminosity)}


@check_hex
def get_complementary(hex_value: str) -> str:
    """
    Finds the complementary color
    :param hex_value: hexadecimal RGB color code
    :return: hexadecimal RGB color code of the complementary color

    >>> get_complementary("#19021e")
    '#071e02'
    """
    red, green, blue = convert_hex_to_rvb(hex_value)
    h, l, s = colorsys.rgb_to_hls(red / 255, green / 255, blue / 255)
    h_complementary = (h + 0.5) - 1
    rgb_complementary = tuple(int(val * 255) for val in colorsys.hls_to_rgb(h_complementary, l, s))
    return convert_rvb_to_hex(rgb_complementary)
# endregion


if __name__ == '__main__':
    import doctest
    if doctest.testmod().failed == 0:
        print("👍🏼 OK! 👍🏼")
