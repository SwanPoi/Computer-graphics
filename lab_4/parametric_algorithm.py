import math

'''
x = radius * cos(t)
y = radius * sin(t)
'''
def parametric_circle(radius):
    '''Построение окружности по параметрическому уравнению'''
    step = 1 / radius
    circle = []
    t = 0

    while t <= step + math.pi / 4:
        x = radius * math.cos(t)
        y = radius * math.sin(t)
        circle.extend([[x, y], [-x, y], [x, -y], [-x, -y], [y, x], [-y, x], [y, -x], [-y, -x]])
        t += step

    return circle