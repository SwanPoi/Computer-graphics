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

def middle_point_ellipse(a, b):
    sqr_a = a * a
    sqr_b = b * b

    x = 0
    y = b

    ellipse = [[x, y], [x, -y]]

    delta = sqr_b - sqr_a * (b - 0.25)

    while x * sqr_b <= y * sqr_a:
        x += 1

        if delta <= 0:
            delta += 2 * sqr_b * x + sqr_b
        else:
            y -= 1
            delta += 2 * sqr_b * x + sqr_b - 2 * y * sqr_a

        ellipse.extend([[x, y], [x, -y], [-x, y], [-x, -y]])

    delta = sqr_b * ((x + 0.5) ** 2) + sqr_a * ((y - 1) ** 2) - sqr_a * sqr_b

    while y >= 0:
        y -= 1

        if delta <= 0:
            x += 1
            delta += 2 * x * sqr_b - 2 * y * sqr_a + sqr_a
        else:
            delta += - 2 * y * sqr_a + sqr_a

        ellipse.extend([[x, y], [x, -y], [-x, y], [-x, -y]])

    return ellipse
