from dataclasses import dataclass
from typing import List

@dataclass
class Cutter:
    x_l : int
    x_r : int
    y_up : int
    y_down : int

    def __init__(self, x_l=0, x_r=0, y_up=0, y_down=0):
        self.x_l = x_l
        self.x_r = x_r
        self.y_up = y_up
        self.y_down = y_down


def get_code(point : List, cutter : Cutter):
    code = ''
    x = point[0]
    y = point[1]

    if x < cutter.x_l:
        code = '1' + code
    else:
        code = '0' + code

    if x > cutter.x_r:
        code = '1' + code
    else:
        code = '0' + code

    if y < cutter.y_down:
        code = '1' + code
    else:
        code = '0' + code

    if y > cutter.y_up:
        code = '1' + code
    else:
        code = '0' + code

    return code

def cut_algorithm(segment : List, cutter : Cutter):
    '''Простой алгоритм отсечения'''

    '''Вычисление кодов концов отрезка'''
    first_code = get_code(segment[0], cutter)
    second_code = get_code(segment[1], cutter)

    '''Вычисление сумм концов отрезка'''
    first_sum = sum([int(i) for i in first_code])
    second_sum = sum([int(i) for i in second_code])

    '''Установка признака видимости и начального значения тангенса угла наклона'''
    is_visible = 1
    m = 10 ** 30

    final_flag = False
    cur_flag = False
    draw = [[], []]
    buf_draw = []

    '''Проверка полной видимости отрезка'''
    if first_sum == 0 and second_sum == 0:
        draw[0] = segment[0]
        draw[1] = segment[1]
        final_flag = True

    '''Вычисление логического произведения кодов концов отрезка'''
    if not final_flag:
        pl = 0
        for i in range(len(first_code)):
            pl += int(first_code[i]) * int(second_code[i])

        if pl != 0:
            is_visible = -1
            final_flag = True

    i = 0
    '''Проверка видимости первого конца отрезка'''
    if not final_flag:
        if first_sum == 0:
            draw[0] = segment[0]
            buf_draw = segment[1]
            i = 2
            cur_flag = True

    '''Проверка видимости второго конца отрезка'''
    if not final_flag and not cur_flag:
        if second_sum == 0:
            draw[0] = segment[1]
            buf_draw = segment[0]
            i = 2
            cur_flag = True

    end_flag = False
    if not final_flag:
        while not end_flag:
            if not cur_flag:
                i += 1

            if i <= 2:
                if not cur_flag:
                    buf_draw = segment[i - 1]

                cur_flag = False
                if segment[0][0] != segment[1][0]:
                    m = (segment[1][1] - segment[0][1]) / (segment[1][0] - segment[0][0])

                    if buf_draw[0] <= cutter.x_l:
                        y_intersection = m * (cutter.x_l - buf_draw[0]) + buf_draw[1]

                        if y_intersection >= cutter.y_down and y_intersection <= cutter.y_up:
                            draw[i - 1].extend([cutter.x_l, y_intersection])
                            continue

                    if buf_draw[0] >= cutter.x_r:
                        y_intersection = m * (cutter.x_r - buf_draw[0]) + buf_draw[1]

                        if (y_intersection >= cutter.y_down) and (y_intersection <= cutter.y_up):
                            draw[i - 1].extend([cutter.x_r, y_intersection])
                            continue

                if m == 0:
                    continue

                if buf_draw[1] >= cutter.y_up:
                    x_intersection = (cutter.y_up - buf_draw[1]) / m + buf_draw[0]

                    if (x_intersection >= cutter.x_l) and (x_intersection <= cutter.x_r):
                        draw[i - 1].extend([x_intersection, cutter.y_up])
                        continue

                if buf_draw[1] > cutter.y_down:
                    is_visible = -1
                    break

                x_intersection = (cutter.y_down - buf_draw[1]) / m + buf_draw[0]

                if (x_intersection >= cutter.x_l) and (x_intersection <= cutter.x_r):
                    draw[i - 1].extend([x_intersection, cutter.y_down])
                else:
                    is_visible = -1
                    break
            else:
                end_flag = True


    if is_visible == 1:
        return draw
    else:
        return []






