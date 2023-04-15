import math

'''(x - x_center)^2 + (y - y_center)^2 = radius^2
y = y_center + sqrt(radius^2 - (x - x_center)^2)'''
def canonical_circle(radius):
    '''Каноническое уравнение окружности'''
    circle = []
    border = round(radius / math.sqrt(2))
    r_square = radius ** 2
    for x in range(border + 1):
        y = math.sqrt(r_square - (x) ** 2)
        circle.extend([[x, y], [-x, y], [x, -y], [-x, -y], [y, x], [-y, x], [y, -x], [-y, -x]])

    return circle

