def middle_point_circle(radius):
    '''Построение окружности алгоритмом срединной точки'''
    x = radius
    y = 0
    delta = 5 / 4 - radius # (x - 0.5)^2 + (y + 1)^2 - r^2
    circle = [[x, y], [x, -y], [y, x], [-y, x]]

    while x >= y:
        if delta < 0:
            y += 1
            delta += 2 * y + 1
        else:
            y += 1
            x -= 1
            delta += 2 * y + 1 - 2 * x

        circle.extend([[x, y], [-x, y], [x, -y], [-x, -y], [y, x], [-y, x], [y, -x], [-y, -x]])

    return circle
