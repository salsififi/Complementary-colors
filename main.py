"""
"COULEURS COMPLÉMENTAIRES"
Challenge n°3 on the "Docstring" Discord server
https://discord.com/channels/396825382009044994/1160339200063844356/1160341463759061073
Date: 2024-06-22
Author: Simon Salvaing
Big thanks to @bucdany for his code review and multiple advices!
"""

from colorsys import rgb_to_hls, hls_to_rgb

from check_hex import _check_hex


def convert_hex_to_rvb(hex_value: str) -> tuple:
    """
    Converts a hexadecimal color code to its RGB code (=RVB in French).
    :param hex_value: RGB color code in hexadecimal format (with 6 chars after #)
    :return: list containing the 3 decimal RGB color codes

    >>> convert_hex_to_rvb("#FF0000")
    (255, 0, 0)
    >>> convert_hex_to_rvb("#0000FF")
    (0, 0, 255)
    >>> convert_hex_to_rvb("#800080")
    (128, 0, 128)
    >>> convert_hex_to_rvb("#FFC0CB")
    (255, 192, 203)
    """
    hex_value = _check_hex(hex_value)
    return tuple(int(hex_value[i:i + 2], 16) for i in range(1, len(hex_value), 2))


# region Conversion functions
def convert_rvb_to_hex(rvb: tuple) -> str:
    """
    Converts a rgb color code to hexadecimal code.
    :param rvb: tuple containing the 3 decimal RGB (=RVB in French) color codes
    :return: hexadecimal color code

    >>> convert_rvb_to_hex((255, 255, 255))
    '#ffffff'
    >>> convert_rvb_to_hex((0, 0, 0))
    '#000000'
    """
    return f"#{"".join(f"{rvb[i]:02x}" for i in range(3))}"  # rvb[0]:02x}{rvb[1]:02x}{rvb[2]:02x


# endregion


# region Challenge functions
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
    red, green, blue = convert_hex_to_rvb(hex_value)
    h, l, s = rgb_to_hls(*[color / 255 for color in (red, green, blue)])
    h_norm, s_norm, l_norm = (round(val) for val in (carac * (360 if carac == h else 100)
                                                     for carac in (h, s, l)))

    return {"hex": hex_value,
            "rvb": [red, green, blue],
            "tsl_norm": tuple(f"{carac}{'°' if carac == h_norm else '%'}"
                              for carac in (h_norm, s_norm, l_norm)),
            "tsl": (h, s, l)}


# endregion


def get_complementary(hex_value: str) -> str:
    """
    Finds the complementary color
    :param hex_value: hexadecimal RGB color code
    :return: hexadecimal RGB color code of the complementary color

    >>> get_complementary("#19021e")
    '#071e02'
    """
    h, s, l = get_color_types(hex_value).get("tsl")
    h_complementary = (h + .5) % 1
    rgb_complementary = tuple(int(round(val * 255)) for val in hls_to_rgb(h_complementary, l, s))
    return convert_rvb_to_hex(rgb_complementary)


if __name__ == '__main__':
    from pprint import pprint

    hex_color = "#19021e"
    print(f"Voici le dictionnaire associé à la couleur '{hex_color}':")
    pprint(get_color_types(hex_color))
    print(f"Couleur complémentaire: {get_complementary(hex_color)}.")
