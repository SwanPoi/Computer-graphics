import math

'''
(x - x_center)^2 + (y - y_center)^2 = radius^2
y = y_center + sqrt(radius^2 - (x - x_center)^2)
'''
def canonical_circle(radius):
    '''Каноническое уравнение окружности'''
    circle = []
    border = round(radius / math.sqrt(2))
    r_square = radius * radius
    for x in range(border + 1):
        y = math.sqrt(r_square - (x) ** 2)
        circle.extend([[x, y], [-x, y], [x, -y], [-x, -y], [y, x], [-y, x], [y, -x], [-y, -x]])

    return circle

'''
x^2/a^2 + y^2/b^2 = 1
y = sqrt(b^2 * (1 - x^2/a^2))
'''
def canonical_ellipse(a, b):
    '''Построение эллипса по каноническому уравнению'''
    ellipse =[]
    sqr_a = a * a
    sqr_b = b * b

    border_x = round(a / math.sqrt(1 + sqr_b / sqr_a))
    border_y = round(b / math.sqrt(1 + sqr_a / sqr_b))

    for x in range(border_x + 1):
        y = math.sqrt(sqr_a * sqr_b - x ** 2 * sqr_b) / a
        ellipse.extend([[x, y], [x, -y], [-x, y], [-x, -y]])

    for y in range(border_y, - 1, -1):
        x = math.sqrt(sqr_a * sqr_b - y ** 2 * sqr_a) / b
        ellipse.extend([[x, y], [x, -y], [-x, y], [-x, -y]])

    return ellipse



