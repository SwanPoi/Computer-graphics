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

'''
x = a * cos(t)
y = b * sin(t)
'''
def parametric_ellipse(a, b):
    '''Построение эллипса по параметрическим уравнениям'''
    if a > b:
        step = 1 / a
    else:
        step = 1 /b

    ellipse = []
    t = 0
    while t <= step + math.pi / 2:
        x = a * math.cos(t)
        y = b * math.sin(t)

        ellipse.extend([[x, y], [x, -y], [-x, y], [-x, -y]])

        t += step

    return ellipse