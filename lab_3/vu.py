from PyQt5.QtGui import QColor
from math import floor
from help_functions import correct_intensity, normal_round

def vu(x_start, x_end, y_start, y_end, color : QColor, step_mode=False):
    '''Алгоритм Ву построения отрезка'''
    points_list = list()
    intensity = 255
    steps_count = 0

    if x_start == x_end and y_start == y_end:
        points_list.append([x_start, y_start, color])
    else:
        dx = x_end - x_start
        dy = y_end - y_start

        step = 1

        if abs(dy) > abs(dx):
            tg = dx /dy

            if y_start > y_end:
                tg *= -1
                step *= -1

            if dy < dx:
                y_new_end = normal_round(y_end) - 1
            else:
                y_new_end = normal_round(y_end) + 1

            x = x_start

            for y in range(normal_round(y_start), y_new_end, step):
                d1 = x - floor(x)
                d2 = 1 - d1

                first_point = [int(x) + 1, y, correct_intensity(color, normal_round(abs(d2) * intensity))]
                second_point = [int(x), y, correct_intensity(color, normal_round(abs(d1) * intensity))]

                if step_mode and y < y_end:
                    if int(x) != int(x + tg):
                        steps_count += 1

                if not step_mode:
                    points_list.append(first_point)
                    points_list.append(second_point)

                x += tg
        else:
            tg = dy / dx

            if x_start > x_end:
                step *= -1
                tg *= -1

            x_new_end = normal_round(x_end) - 1 if dy > dx else normal_round(x_end) + 1

            y = y_start

            for x in range(normal_round(x_start), x_new_end, step):
                d1 = y - floor(y)
                d2 = 1 - d1

                first_point = [x, int(y) + 1, correct_intensity(color, normal_round(abs(d2) * intensity))]
                second_point = [x, int(y), correct_intensity(color, normal_round(abs(d1) * intensity))]

                if step_mode and x < x_end:
                    if int(y) != int(y + tg):
                        steps_count += 1

                if not step_mode:
                    points_list.append(first_point)
                    points_list.append(second_point)

                y += tg


        if step_mode:
            return steps_count

    return points_list