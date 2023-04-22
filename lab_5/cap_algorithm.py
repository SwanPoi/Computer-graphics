from dataclasses import dataclass
from typing import List
from math import floor
import time

from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QGraphicsScene, QApplication


@dataclass
class Active_Edge:
    x :float
    delta_x : float
    delta_y : float

    def __init__(self, x=0, delta_x=0, delta_y=0):
        self.x = x
        self.delta_x = delta_x
        self.delta_y = delta_y

def sort_by_x(edge : Active_Edge):
    return edge.x

def find_max_and_min_scanning_line(all_polygons : List):
    y_min = all_polygons[0][0][1]
    y_max = all_polygons[0][0][1]

    for polygon in all_polygons:
        for point in polygon:
            if point[1] > y_max:
                y_max = point[1]
            elif point[1] < y_min:
                y_min = point[1]

    return y_max - 1, y_min

def make_y_groups_list(y_max : int, y_min : int, all_polygons : List):
    scan_lines_dict = dict({i : list() for i in range(y_max, y_min - 1, -1)})

    for polygon in all_polygons:
        for i in range(len(polygon) - 1):
            dy = abs(polygon[i + 1][1] - polygon[i][1])

            if (polygon[i][0] - polygon[i + 1][0] == 0):
                x = polygon[i][0]
            elif dy != 0:
                x = get_intersection_point(polygon[i], polygon[i + 1], max(polygon[i + 1][1] - 0.5, polygon[i][1] - 0.5))

            sign = 1
            if polygon[i + 1][1] > polygon[i][1]:
                sign = -1

            if dy != 0:
                dx = sign * (polygon[i + 1][0] - polygon[i][0]) / dy
                scan_lines_dict[max(polygon[i + 1][1] - 1, polygon[i][1] - 1)].append(Active_Edge(x, dx, dy))

        dy = abs(polygon[0][1] - polygon[-1][1])

        if polygon[0][0] - polygon[-1][0] == 0:
            x = polygon[-1][0]
        elif dy != 0:
            x = get_intersection_point(polygon[-1], polygon[0], max(polygon[0][1] - 0.5, polygon[-1][1] - 0.5))

        sign = 1
        if polygon[0][1] > polygon[-1][1]:
            sign = -1

        if dy != 0:
            dx = sign * (polygon[0][0] - polygon[-1][0]) / dy
            scan_lines_dict[max(polygon[0][1] - 1, polygon[-1][1] - 1)].append(Active_Edge(x, dx, dy))

    return scan_lines_dict

def CAP_algorithm(all_polygons : List, color : QColor, scene : QGraphicsScene, delay=False):
    y_max, y_min = find_max_and_min_scanning_line(all_polygons)
    scan_lines_dict = make_y_groups_list(y_max, y_min, all_polygons)
    active_edges_list = []
    current_scan_line = y_max

    while current_scan_line >= y_min:
        '''Добавление новых ребер и сортировка по возрастанию x'''
        active_edges_list.extend(scan_lines_dict[current_scan_line])
        active_edges_list.sort(key=sort_by_x)

        index = 0

        while index < len(active_edges_list):
            if delay:
                QApplication.processEvents()
                time.sleep(0.001)

            scene.addLine(floor(active_edges_list[index].x), current_scan_line, floor(active_edges_list[index + 1].x), current_scan_line, pen=QPen(color, 1))
            index += 2

        index = 0
        '''Корректировка САР'''
        while index < len(active_edges_list):
            active_edges_list[index].x += active_edges_list[index].delta_x
            active_edges_list[index].delta_y -= 1

            if active_edges_list[index].delta_y == 0:
                active_edges_list.pop(index)
            else:
                index += 1

        current_scan_line -= 1

def get_intersection_point(start_point : List, end_point: List, y : int):
    return (y - start_point[1]) * (end_point[0] - start_point[0]) / (
            end_point[1] - start_point[1]) + start_point[0]



