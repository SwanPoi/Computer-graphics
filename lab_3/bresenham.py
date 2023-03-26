from help_functions import sign, correct_intensity, normal_round

def bresenham_for_float(x_start, x_end, y_start, y_end, step_mode=False):
    '''Алгоритм Брезенхема'''
    point_list = list()

    if x_start == x_end and y_start == y_end:
        point_list.append([x_start, y_start])
    else:
        '''Вычисление приращений'''
        dx = x_end - x_start
        dy = y_end - y_start

        '''Вычисление шага изменения'''
        sx = sign(dx)
        sy = sign(dy)

        dx = abs(dx)
        dy = abs(dy)

        if dy > dx:
            dx, dy = dy, dx
            change = 1
        else:
            change = 0

        '''Вычисление модуля тангенса угла наклона'''
        tg = dy / dx

        '''Вычисление начального значения ошибки и начальных координат'''
        error = tg - 0.5
        x = x_start
        y = y_start

        steps_count = 0
        x_prev = x
        y_prev = y

        for i in range(0, int(dx) + 1):
            if not step_mode:
                point_list.append([x, y])

            if error >= 0:
                if change == 1:
                    x += sx
                else:
                    y += sy

                error -= 1

            if error <= 0:
                if change == 1:
                    y += sy
                else:
                    x += sx

                error += tg

            if step_mode:
                if x_prev != x and y_prev != y:
                    steps_count += 1

                x_prev = x
                y_prev = y

    if step_mode:
        return steps_count

    return point_list

def integer_bresenham(x_start, x_end, y_start, y_end, step_mode=False):
    '''Алгоритм Брезенхема с целыми коэффициентами'''
    point_list = list()

    if x_start == x_end and y_start == y_end:
        point_list.append([x_start, y_start])
    else:
        '''Вычисление приращений'''
        dx = x_end - x_start
        dy = y_end - y_start

        '''Вычисление шага изменения'''
        sx = sign(dx)
        sy = sign(dy)

        dx = abs(dx)
        dy = abs(dy)

        if dy > dx:
            dx, dy = dy, dx
            change = 1
        else:
            change = 0

        '''Вычисление начального значения ошибки и начальных координат'''
        error = 2 * dy - dx
        x = x_start
        y = y_start

        steps_count = 0
        x_prev = x
        y_prev = y

        for i in range(0, int(dx) + 1):
            if not step_mode:
                point_list.append([x, y])

            if error >= 0:
                if change == 1:
                    x += sx
                else:
                    y += sy

                error -= 2 * dx

            if error <= 0:
                if change == 1:
                    y += sy
                else:
                    x += sx

                error += 2 * dy

            if step_mode:
                if x_prev != x and y_prev != y:
                    steps_count += 1

                x_prev = x
                y_prev = y

    if step_mode:
        return steps_count

    return point_list

def step_bresenham(x_start, x_end, y_start, y_end, color='black', step_mode=False):
    '''Алгоритм Брезенхема со сглаживанием ступенек'''
    point_list = list()
    intensity = 255

    if x_start == x_end and y_start == y_end:
        point_list.append([x_start, y_start, color])
    else:
        '''Вычисление приращений'''
        dx = x_end - x_start
        dy = y_end - y_start

        '''Вычисление шага изменения'''
        sx = sign(dx)
        sy = sign(dy)

        dx = abs(dx)
        dy = abs(dy)

        if dy > dx:
            dx, dy = dy, dx
            change = 1
        else:
            change = 0

        '''Вычисление модуля тангенса угла наклона'''
        tg = dy / dx

        '''Вычисление начального значения ошибки и коррекция тангенса угла наклона'''
        error = intensity / 2
        tg *= intensity
        w = intensity - tg

        '''Инициализация начальной точки'''
        x = x_start
        y = y_start

        steps_count = 0
        x_prev = x
        y_prev = y

        for i in range(0, int(dx) + 1):
            if not step_mode:
                point_list.append([x, y, correct_intensity(color, normal_round(error))])

            if error < 0:
                if change == 0:
                    x += sx
                else:
                    y += sy

                error += tg
            else:
                y += sy
                x += sx
                error -= w

            if step_mode:
                if x_prev != x and y_prev != y:
                    steps_count += 1

                x_prev = x
                y_prev = y

    if step_mode:
        return steps_count

    return point_list
