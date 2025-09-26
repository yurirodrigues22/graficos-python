import os, sys

def _to_int_safe(v):
    try:
        return int(v)
    except Exception:
        try:
            return int(float(v))
        except Exception:
            return 0

def is_color_dark(hexcolor: str) -> bool:
    if not hexcolor:
        return True
    c = hexcolor.lstrip('#')
    if len(c) != 6:
        return True
    r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
    luminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return luminance < 128

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
