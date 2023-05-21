from sympy import Point, Polygon
from typing import List

def check_correct_polygon(polygon : List):
    poly = Polygon(*polygon)
    return poly.is_convex()

def sutherland_hodgman(polygon : List, cutter : List):
    for i in range(len(cutter)):
        next_i = (i + 1) % len(cutter)
        polygon = cut_polygon_by_edge([cutter[i], cutter[next_i]], polygon)
        if len(polygon) < 3:
            return []

    return polygon

def cut_polygon_by_edge(segment : List, polygon : List) -> List:
    new_polygon = []

    for j in range(1, len(polygon) + 1):
        cur_point = polygon[j % len(polygon)]

        if check_intersection([polygon[j - 1], cur_point], segment):
            new_polygon.append(get_intersection_point(segment[0], segment[1], polygon[j - 1], cur_point))

        if is_visible(segment, cur_point) <= 0:
            new_polygon.append(cur_point)

    return new_polygon

def check_intersection(vector : List, cutter_side : List):
    first_visible = is_visible(cutter_side, vector[0])
    second_visible = is_visible(cutter_side, vector[1])

    return first_visible * second_visible < 0

def is_visible(side_cutter : List, point : List):
    vector = [side_cutter[1][0] - side_cutter[0][0], side_cutter[1][1] - side_cutter[0][1]]
    vec_point = [point[0] - side_cutter[0][0], point[1] - side_cutter[0][1]]
    result = vec_point[0] * vector[1] - vec_point[1] * vector[0]

    if abs(result) < 1e-7:
        result = 0

    return sign(result)

def sign(number):
    result = 0

    if number > 0:
        result = 1
    elif number < 1:
        result = -1

    return result

def get_intersection_point(p1, p2, w1, w2):
    a11 = p2[0] - p1[0]
    a21 = p2[1] - p1[1]
    a12 = w1[0] - w2[0]
    a22 = w1[1] - w2[1]

    r1 = w1[0] - p1[0]
    r2 = w1[1] - p1[1]

    d = a11 * a22 - a12 * a21

    A11 = a22 / d
    A12 = -a12 / d

    t = A11 * r1 + A12 * r2

    x = p1[0] + (p2[0] - p1[0]) * t
    y = p1[1] + (p2[1] - p1[1]) * t

    return [round(x), round(y)]


