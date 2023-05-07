from sympy import Point, Polygon
from typing import List

def check_correct_polygon(polygon : List):
    poly = Polygon(*polygon)
    return poly.is_convex()

def get_vector(first_point, second_point):
    return [second_point[0] - first_point[0], second_point[1] - first_point[1]]

def scalar_mul(first_vector, second_vector):
    return first_vector[0] * second_vector[0] + first_vector[1] * second_vector[1]

def get_normal(first_point, second_point, third_point):
    vector = get_vector(first_point, second_point)

    if vector[1]:
        normal = [1, -vector[0] / vector[1]]
    else:
        normal = [0, 1]

    if scalar_mul(get_vector(second_point, third_point), normal) < 0:
        normal[0] *= -1
        normal[1] *= -1

    return normal

def cut_cyrus_beck(cutter, segment):
    t_beg = 0
    t_end = 1

    first_point = segment[0]
    second_point = segment[1]

    d = get_vector(first_point, second_point)

    for i in range(-2, len(cutter) - 2):
        normal = get_normal(cutter[i], cutter[i + 1], cutter[i + 2])

        w = get_vector(cutter[i], first_point)
        d_scalar = scalar_mul(d, normal)
        w_scalar = scalar_mul(w, normal)

        if d_scalar == 0:
            if w_scalar < 0:
                return None
            else:
                continue

        t = - w_scalar / d_scalar

        if d_scalar > 0:
            if t <= 1:
                t_beg = max(t, t_beg)
            else:
                return None
        elif d_scalar < 0:
            if t >= 0:
                t_end = min(t, t_end)
            else:
                return None

        if t_beg > t_end:
            return None

    if t_beg <= t_end:
        first_result = [round(first_point[0] + d[0] * t_beg), round(first_point[1] + d[1] * t_beg)]
        second_result = [round(first_point[0] + d[0] * t_end), round(first_point[1] + d[1] * t_end)]

        return first_result, second_result

    return None





