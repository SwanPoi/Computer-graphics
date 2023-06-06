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


def sign(digit):
    if digit > 0:
        return 1

    if digit == 0:
        return 0

    return -1