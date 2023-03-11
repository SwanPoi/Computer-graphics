from typing import List
from math import cos, sin

def move_point(point: List, dx: (float, int), dy: (float, int)) -> List:
    """Перенос точки"""
    point[0] += dx
    point[1] += dy

    return point

def scale_point(point: List, center: List, kx: (float, int), ky: (float, int)):
    """Масштабирование точки"""
    point[0] = kx * point[0] + center[0] * (1 - kx)
    point[1] = ky * point[1] + center[1] * (1 - ky)

    return point

def spin_point(point: List, center: List, angle):
    """Поворот точки"""
    point[0] -= center[0]
    point[1] -= center[1]
    saved_x = point[0]

    point[0] = point[0] * cos(angle) - point[1] * sin(angle)
    point[1] = saved_x * sin(angle) + point[1] * cos(angle)

    point[0] += center[0]
    point[1] += center[1]

    return point