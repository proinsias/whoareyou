# -*- coding: utf-8 -*-

import io
import typing

import numpy as np
import PIL.Image


DEFAULT_HEIGHT = 100


def get_ansi_color_code(
    r: int,
    g: int,
    b: int,
) -> int:
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)


def get_color(
    r: int,
    g: int,
    b: int,
) -> str:
    ansi_color_code = int(get_ansi_color_code(r, g, b))
    return f'\x1b[48;5;{ansi_color_code}m \x1b[0m'


def getAnsiColorsFromPhotoData(
    photo_data: bytes,
) -> typing.List[typing.List[str]]:
    """
    Convert photo data from bytes to ANSI colors.

    Credit to <https://github.com/nikhilkumarsingh/terminal-image-viewer>.
    """

    img = PIL.Image.open(io.BytesIO(photo_data))

    h = DEFAULT_HEIGHT
    w = int((img.width / img.height) * h)

    img = img.resize((w, h), PIL.Image.ANTIALIAS)
    img_arr = np.asarray(img)
    h, w, _ = img_arr.shape

    return [
        [
            get_color(img_arr[x][y][0], img_arr[x][y][1], img_arr[x][y][2])
            for y in range(w)
        ]
        for x in range(h)
    ]
