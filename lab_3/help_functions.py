from PyQt5.QtGui import QColor

def normal_round(digit):
    normal_int = round(digit)

    if len(str(digit)) > 3 and str(digit)[-2] == '.' and str(digit)[-1] == '5' and int(digit) % 2 == 0:
        normal_int += 1

    return normal_int

def sign(digit):
    if digit > 0:
        return 1

    if digit == 0:
        return 0

    return -1

def correct_intensity(color : QColor, intensity):
    c_red = color.red() + intensity
    c_green = color.green() + intensity
    c_blue = color.blue() + intensity
    c_red = 255 if c_red > 255 else c_red
    c_green = 255 if c_green > 255 else c_green
    c_blue = 255 if c_blue > 255 else c_blue

    return QColor(c_red, c_green, c_blue)
