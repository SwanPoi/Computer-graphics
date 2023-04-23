import time
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor, QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QApplication


def lines_seed_filling(scene: QGraphicsScene, image: QImage, border_color: QColor,
                       fill_color: QColor, seed_point: QPoint, delay=False):
    points_stack = [seed_point]

    while points_stack:
        seed_pixel = points_stack.pop()
        x = seed_pixel.x()
        y = seed_pixel.y()
        image.setPixel(x, y, fill_color.rgb())

        buf_x = x
        buf_y = y
        '''Закрашиваем пиксели справа от затравки'''
        x += 1

        while image.pixelColor(x, y).getRgb() != fill_color.getRgb() \
                and image.pixelColor(x, y).getRgb() != border_color.getRgb() and x < image.width():
            image.setPixel(x, y, fill_color.rgb())
            x += 1
        x_right = x - 1

        '''Закрашиваем пиксели слева от затравки'''
        x = buf_x - 1

        while image.pixelColor(x, y).getRgb() != fill_color.getRgb() \
                and image.pixelColor(x, y).getRgb() != border_color.getRgb() and x > 0:
            image.setPixel(x, y, fill_color.rgb())
            x -= 1

        x_left = x + 1

        '''Проходим по верхней строке'''
        x = x_left
        y = buf_y + 1
        while x <= x_right:
            flag = False

            while image.pixelColor(x, y).getRgb() != fill_color.getRgb() \
                        and image.pixelColor(x, y).getRgb() != border_color.getRgb() and x <= x_right:
                flag = True
                x += 1

            '''Помещаем в стек крайний правый пиксель'''
            if flag and y < image.height():
                if x == x_right and image.pixelColor(x, y).getRgb() != fill_color.getRgb() \
                            and image.pixelColor(x, y).getRgb() != border_color.getRgb():
                    points_stack.append(QPoint(x, y))
                else:
                    points_stack.append(QPoint(x - 1, y))

                    flag = False

            '''Продолжаем проверку, если строка была прервана'''
            x_in = x

            while (image.pixelColor(x, y).getRgb() == fill_color.getRgb() or
                       image.pixelColor(x, y).getRgb() == border_color.getRgb()) and x < x_right:
                x += 1

            if x == x_in:
                x += 1

        '''Проходим по нижней строке'''
        x = x_left
        y = buf_y - 1

        while x <= x_right:
            flag = False

            while image.pixelColor(x, y).getRgb() != fill_color.getRgb() and \
                    image.pixelColor(x, y).getRgb() != border_color.getRgb() and x <= x_right:
                flag = True
                x += 1

            '''Помещаем в стек крайний правый пиксель'''
            if flag and y > 0:
                if x == x_right and image.pixelColor(x, y).getRgb() != fill_color.getRgb() and \
                            image.pixelColor(x, y).getRgb() != border_color.getRgb():
                    points_stack.append(QPoint(x, y))
                else:
                    points_stack.append(QPoint(x - 1, y))

                flag = False

            '''Продолжаем проверку, если строка была прервана'''
            x_in = x
            while (image.pixelColor(x, y).getRgb() == fill_color.getRgb() or
                       image.pixelColor(x, y).getRgb() == border_color.getRgb()) and x < x_right:
                x += 1

            if x == x_in:
                x += 1

        if delay:
            scene.clear()
            scene.addPixmap(QPixmap.fromImage(image))
            QApplication.processEvents()
            time.sleep(0.001)


    if not delay:
        scene.clear()
        scene.addPixmap(QPixmap.fromImage(image))


