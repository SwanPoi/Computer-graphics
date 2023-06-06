def bresenham_circle(radius):
    x = 0
    y = radius
    diagonal_step = 2 * (1 - radius)
    circle = [[x, y], [x, -y], [y, x], [-y, x]]
    delta = 0
    while y >= x:
        if diagonal_step < 0:
            delta = 2 * (diagonal_step + y) - 1

            if delta <= 0:
                x += 1
                diagonal_step += 2 * x + 1
            else:
                x += 1
                y -= 1
                diagonal_step += 2 * (x - y + 1)
        elif diagonal_step > 0:
            delta = 2 * (diagonal_step - x) - 1

            if delta <= 0:
                x += 1
                y -= 1
                diagonal_step += 2 * (x - y + 1)
            else:
                y -= 1
                diagonal_step = diagonal_step - 2 * y + 1
        else:
            x += 1
            y -= 1
            diagonal_step += 2 * (x - y + 1)

        circle.extend([[x, y], [-x, y], [x, -y], [-x, -y], [y, x], [-y, x], [y, -x], [-y, -x]])

    return circle

def bresenham_ellipse(a, b):
    x = 0
    y = b

    sqr_a = a * a
    sqr_b = b * b

    ellipse = [[x, y], [x, -y]]

    delta = sqr_b - sqr_a * (2 * b + 1)

    while y >= 0:
        if delta < 0:
            delta_streak = 2 * (delta + y) - 1

            x += 1
            if delta_streak <= 0:
                delta += sqr_b * (2 * x + 1)
            else:
                y -= 1
                delta += sqr_b * (2 * x + 1) + sqr_a * (1 - 2 * y)
        elif delta > 0:
            delta_streak = 2 * delta + sqr_b * (2 - 2 * x)

            y -= 1
            if delta_streak <= 0:
                x += 1
                delta += sqr_b * (2 * x + 1) + sqr_a * (1 - 2 * y)
            else:
                delta += sqr_a * (1 - 2 * y)
        else:
            x += 1
            y -= 1
            delta += sqr_b * (2 * x + 1) + sqr_a * (1 - 2 * y)

        ellipse.extend([[x, y], [x, -y], [-x, y], [-x, -y]])

    return ellipse