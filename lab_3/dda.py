from help_functions import normal_round

def dda(x_start, x_end, y_start, y_end, step_mode=False):
    point_list = list()
    steps_count = 0

    if x_start == x_end and y_start == y_end:
        point_list.append([normal_round(x_start), normal_round(y_start)])
    else:

        dx = abs(x_end - x_start)
        dy = abs(y_end - y_start)

        # Определение большего шага
        if dx >= dy:
            length = dx
        else:
            length = dy

        dx = (x_end - x_start) / length # Шаг по х
        dy = (y_end - y_start) / length # Шаг по y

        x = x_start
        y = y_start

        for i in range(0, int(length) + 1):
            if not step_mode:
                point_list.append([normal_round(x), normal_round(y)])
            elif normal_round(x + dx) != normal_round(x) and normal_round(y + dy) != normal_round(y):
                steps_count += 1
            x += dx
            y += dy

    if step_mode:
        return steps_count

    return point_list

