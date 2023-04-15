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