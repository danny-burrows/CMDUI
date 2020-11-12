import random

_colors = {
    "black"         : 0x0,
    "blue"          : 0x1,
    "green"         : 0x2,
    "aqua"          : 0x3,
    "red"           : 0x4,
    "purple"        : 0x5,
    "yellow"        : 0x6,
    "white"         : 0x7,
    "grey"          : 0x8,
    "light_blue"    : 0x9,
    "light_green"   : 0xa,
    "light_aqua"    : 0xb,
    "light_red"     : 0xc,
    "light_purple"  : 0xd,
    "light_yellow"  : 0xe,
    "bright_white"  : 0xf,
}


def _sanitize_color_name(color_name: str) -> str:
    assert isinstance(color_name, str) 
    return color_name.lower().strip().replace(" ", "_")


def get_bg_code(color_name: str) -> int:
    color_name = _sanitize_color_name(color_name)
    return _colors[color_name] * 16


def get_fg_code(color_name: str) -> int:
    color_name = _sanitize_color_name(color_name)
    return _colors[color_name]


def get_color(fg_color_name: str, bg_color_name: str = "") -> int:
    fg = get_fg_code(fg_color_name)

    if len(bg_color_name):
        bg = get_bg_code(bg_color_name)
        return fg | bg
    else:
        return fg


def get_random_background_color():
    return get_bg_code(random.choice(list(_colors.keys())))


def get_color_hex(fg_color_name: str, bg_color_name: str) -> hex:
    return hex(get_color(fg_color_name, bg_color_name))


""" Really quick example usage...

import os, time

col_code = get_color('Light green', 'Red')
hex_col_code = get_color_hex('Light green', 'Red')

print(col_code)
print(hex_col_code)

os.system(f"color {hex_col_code[2:]}")
"""