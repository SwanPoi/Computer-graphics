from Lab_4.canonical_algorithm import canonical_circle
from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, \
    QColorDialog
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt

from canonical_algorithm import *
from parametric_algorithm import *
from bresenham import *
from middle_point import *
from point_transform import *

CANONICAL = 1
PARAMETRIC = 2
BRESENHAM = 3
MIDDLE_POINT = 4
LIBRARY = 5

X = 10
Y = 20

class MyGraphicScene(QGraphicsScene):
    def __init__(self, width, height):
        super(MyGraphicScene, self).__init__()
        self.line_color = QColor(Qt.black)
        self.background_color = QColor(Qt.white)
        self.list_for_axises = []
        self.draw_axises(width, height)

    def draw_axises(self, width, height):
        '''Рисование осей'''
        self.setSceneRect(0, 0, width - 5, height - 5)

        '''Удаление предыдущих осей'''
        if self.list_for_axises:
            for object in self.list_for_axises:
                self.removeItem(object)

        '''Рисование оси Х'''
        self.list_for_axises.append(
            self.addLine(0, 0, width, 0, QPen(Qt.black if self.background_color != Qt.black else Qt.white)))
        '''Добавление засечек'''
        for i in range(50, width, 50):
            self.list_for_axises.append(
                self.addLine(i, 0, i, 10, QPen(Qt.black if self.background_color != Qt.black else Qt.white)))
            self.list_for_axises.append(self.addText(str(i)))
            self.list_for_axises[-1].setPos(i - 10, 6)
            if self.background_color == Qt.black:
                self.list_for_axises[-1].setDefaultTextColor(Qt.white)

        '''Рисование оси Y'''
        self.list_for_axises.append(
            self.addLine(0, 0, 0, height, QPen(Qt.black if self.background_color != Qt.black else Qt.white)))
        '''Добавление засечек'''
        for i in range(50, height, 50):
            self.list_for_axises.append(
                self.addLine(0, i, 5, i, QPen(Qt.black if self.background_color != Qt.black else Qt.white)))
            self.list_for_axises.append(self.addText(str(i)))
            self.list_for_axises[-1].setPos(5, i - 10)
            if self.background_color == Qt.black:
                self.list_for_axises[-1].setDefaultTextColor(Qt.white)

    def change_line_color(self, color):
        '''Замена цвета линии'''
        temp_color = QColor(color)

        if temp_color != self.line_color:
            self.line_color = temp_color

    def change_background_color(self, color):
        '''Замена цвета фона'''
        temp_color = QColor(color)
        if temp_color != self.background_color:
            self.background_color = temp_color
            self.setBackgroundBrush(QBrush(self.background_color))

            if self.background_color == Qt.black or self.background_color == Qt.white:
                self.draw_axises(int(self.width() + 5), int(self.height() + 5))

class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Лабораторная №3 по компьютерной графике")

        self.draw_scene = MyGraphicScene(self.ui.scene_graphicsView.width(), self.ui.scene_graphicsView.height())
        self.ui.scene_graphicsView.setScene(self.draw_scene)
        """Выход из программы через меню"""
        self.exit = self.ui.exit_menu
        quit = QAction("Выход", self)
        quit.setShortcut('Ctrl+Q')
        quit.triggered.connect(qApp.quit)
        self.exit.addAction(quit)

        """Вывод информации об авторе"""
        self.author_info = self.ui.author_menu
        author_info = QAction("Информация об авторе", self)
        author_info.triggered.connect(self.author_message)
        self.author_info.addAction(author_info)

        """Вывод информации об авторе"""
        self.lab_info = self.ui.program_menu
        lab_info = QAction("Информация о программе", self)
        lab_info.triggered.connect(self.lab_message)
        self.lab_info.addAction(lab_info)

        """Очистка сцены"""
        self.clear = self.ui.clear_menu
        clear = QAction("Очистка сцены", self)
        clear.triggered.connect(self.clear_scene)
        self.lab_info.addAction(clear)

        """Поля для отображения цвета"""
        self.line_color_label = self.ui.line_color_label
        self.line_color_label.setStyleSheet("background-color: black")
        self.background_color_label = self.ui.background_color_label

        """Поля ввода"""
        self.x_center_line = self.ui.x_center_lineEdit
        self.y_center_line = self.ui.y_center_lineEdit

        self.circle_radius_line = self.ui.circle_radius_lineEdit
        self.ellipse_width_line = self.ui.width_lineEdit
        self.ellipse_height_line = self.ui.height_lineEdit

        self.start_radius_line = self.ui.start_radius_lineEdit
        self.end_radius_line = self.ui.end_radius_lineEdit
        self.step_radius_line = self.ui.step_circle_lineEdit
        self.count_circles_line = self.ui.count_circles_lineEdit

        self.start_width_line = self.ui.start_width_lineEdit
        self.start_heigth_line = self.ui.start_height_lineEdit
        self.step_ellipse_line = self.ui.step_ellipse_lineEdit
        self.count_ellipses_line = self.ui.count_ellipse_lineEdit

        """Кнопки"""
        self.canonical_button = self.ui.canon_pushButton
        self.parametrical_button = self.ui.param_pushButton
        self.bresenham_button = self.ui.bresenham_pushButton
        self.middle_point_button = self.ui.miidle_point_pushButton
        self.library_button = self.ui.library_pushButton

        self.algorithm_buttons = [self.canonical_button, self.parametrical_button, self.bresenham_button,
                                   self.middle_point_button, self.library_button]

        self.change_line_color_button = self.ui.line_color_pushButton
        self.change_background_color_button = self.ui.background_color_pushButton

        self.add_circle_button = self.ui.add_circle_pushButton
        self.add_ellipse_button = self.ui.add_ellipse_pushButton

        self.circle_spectrum_button = self.ui.circle_spectrum_pushButton
        self.ellipse_spectrum_button = self.ui.ellipse_spectrum_pushButton

        self.rx_step_button = self.ui.rx_pushButton
        self.ry_step_button = self.ui.ry_pushButton

        """Привязка действий к нажатию кнопок"""
        self.change_line_color_button.clicked.connect(self.set_line_color)
        self.change_background_color_button.clicked.connect(self.set_background_color)

        self.canonical_button.clicked.connect(self.set_canonical)
        self.parametrical_button.clicked.connect(self.set_parametric)
        self.bresenham_button.clicked.connect(self.set_bresenham)
        self.middle_point_button.clicked.connect(self.set_middle_point)
        self.library_button.clicked.connect(self.set_library)

        self.rx_step_button.clicked.connect(self.set_rx)
        self.ry_step_button.clicked.connect(self.set_ry)

        self.add_circle_button.clicked.connect(lambda: self.circles_algoritms(self.used_algorithm))
        self.add_ellipse_button.clicked.connect(lambda: self.ellipses_algoritms(self.used_algorithm))

        self.circle_spectrum_button.clicked.connect(lambda: self.circle_spectrum(self.used_algorithm))

        self.used_algorithm = None
        self.used_axis = None

    """Создание оповещения"""
    def create_message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setText(text)
        msg.exec()

    def author_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация об авторе")
        msg.setText("Лабораторную работу выполнил студент группы ИУ7-45Б Лебедев Владимир.")
        msg.exec()

    def lab_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация о программе")
        msg.setText("")
        msg.exec()

    def set_line_color(self):
        '''Выбор цвета линии'''
        color = QColorDialog.getColor()

        if color.isValid():
            self.line_color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.draw_scene.change_line_color(color.name())

    def set_background_color(self):
        '''Выбор цвета фона'''
        color = QColorDialog.getColor()

        if color.isValid():
            self.background_color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.draw_scene.change_background_color(color.name())

    def draw_line_by_algorithm(self, list_points):
        '''Рисование точек'''
        for point in list_points:
            self.draw_scene.addRect(point[0], point[1], 1, 1,
                                  QPen(self.draw_scene.line_color if len(point) == 2 else point[2]))

    def clear_algorithm_buttons(self):
        '''Сброс цвета кнопок'''
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

    def set_canonical(self):
        '''Выбор канонического уравнения'''
        self.clear_algorithm_buttons()
        self.used_algorithm = CANONICAL
        self.canonical_button.setStyleSheet("background-color: yellow")

    def set_parametric(self):
        '''Выбор параметрического уравнения'''
        self.clear_algorithm_buttons()
        self.used_algorithm = PARAMETRIC
        self.parametrical_button.setStyleSheet("background-color: yellow")

    def set_bresenham(self):
        '''Выбор алгоритма Брезенхема'''
        self.clear_algorithm_buttons()
        self.used_algorithm = BRESENHAM
        self.bresenham_button.setStyleSheet("background-color: yellow")

    def set_middle_point(self):
        '''Выбор алгоритма средней точки'''
        self.clear_algorithm_buttons()
        self.used_algorithm = MIDDLE_POINT
        self.middle_point_button.setStyleSheet("background-color: yellow")

    def set_library(self):
        '''Выбор библиотечного алгоритма'''
        self.clear_algorithm_buttons()
        self.used_algorithm = LIBRARY
        self.library_button.setStyleSheet("background-color: yellow")

    def clear_axis_buttons(self):
        '''Очистка кнопок выбора полуоси'''
        self.rx_step_button.setStyleSheet("background-color: white")
        self.ry_step_button.setStyleSheet("background-color: white")

    def set_rx(self):
        '''Выбор приращения по оси Х'''
        self.clear_axis_buttons()
        self.used_axis = X
        self.rx_step_button.setStyleSheet("background-color: yellow")

    def set_ry(self):
        '''Выбор приращения по оси Y'''
        self.clear_axis_buttons()
        self.used_axis = Y
        self.ry_step_button.setStyleSheet("background-color: yellow")

    def clear_scene(self):
        '''Очистка сцены'''
        self.draw_scene.clear()
        self.draw_scene.list_for_axises = []
        self.draw_scene.draw_axises(self.ui.scene_graphicsView.width(), self.ui.scene_graphicsView.height())

    def get_int(self, text, string):
        '''Ввод из поля'''
        result = None

        try:
            result = int(text)
        except:
            self.create_message(f'Ошибка: {string} - нецелое число')

        return result

    def draw_points_by_algorithm(self, list_points):
        '''Рисование точек'''
        for point in list_points:
            self.draw_scene.addRect(point[0], point[1], 1, 1,
                                  QPen(self.draw_scene.line_color if len(point) == 2 else point[2]))

    def circles_algoritms(self, algorithm):
        '''Построение окружности'''
        if not algorithm:
            self.create_message('Не выбран алгоритм построения')
            return

        radius = self.get_int(self.circle_radius_line.text(), 'радиус')
        x_center = self.get_int(self.x_center_line.text(), 'координата x центра')
        y_center = self.get_int(self.y_center_line.text(), 'координата y центра')

        if radius is None or x_center is None or y_center is None:
            return
        elif radius == 0:
            self.create_message('Радиус окружности не может равняться нулю')
            return

        self.clear_circle_algorithms(algorithm, radius, x_center, y_center)

    def clear_circle_algorithms(self, algorithm, radius, x_center, y_center):
        if algorithm == CANONICAL:
            circle_points = canonical_circle(radius)
        elif algorithm == PARAMETRIC:
            circle_points = parametric_circle(radius)
        elif algorithm == BRESENHAM:
            circle_points = bresenham_circle(radius)
        elif algorithm == MIDDLE_POINT:
            circle_points = middle_point_circle(radius)

        point_transform_to_center(circle_points, x_center, y_center)
        self.draw_points_by_algorithm(circle_points)

    def ellipses_algoritms(self, algorithm):
        '''Построение эллипса'''
        if not algorithm:
            self.create_message('Не выбран алгоритм построения')
            return

        x_center = self.get_int(self.x_center_line.text(), 'координата x центра')
        y_center = self.get_int(self.y_center_line.text(), 'координата y центра')
        a = self.get_int(self.ellipse_width_line.text(), 'полуось a')
        b = self.get_int(self.ellipse_height_line.text(), 'полуось b')

        if x_center is None or y_center is None or a is None or b is None:
            return
        elif a == 0:
            self.create_message('Ширина эллипса не может равняться нулю')
            return
        elif b == 0:
            self.create_message('Высота эллипса не может равняться нулю')
            return

        self.clear_ellipse_algorithms(algorithm, a, b, x_center, y_center)

    def clear_ellipse_algorithms(self, algorithm, a, b, x_center, y_center):
        if algorithm == CANONICAL:
            ellipse_points = canonical_ellipse(a, b)
        elif algorithm == PARAMETRIC:
            ellipse_points = parametric_ellipse(a, b)
        elif algorithm == BRESENHAM:
            ellipse_points = bresenham_ellipse(a, b)

        point_transform_to_center(ellipse_points, x_center, y_center)
        self.draw_points_by_algorithm(ellipse_points)

    def circle_spectrum(self, algorithm):
        '''Построение спектра окружностей'''
        if not algorithm:
            self.create_message('Не выбран алгоритм построения')
            return

        start_radius = self.get_int(self.start_radius_line.text(), 'начальное значение радиуса')
        end_radius = self.get_int(self.end_radius_line.text(), 'конечное значение радиуса')
        count_circles = self.get_int(self.count_circles_line.text(), 'количество окружностей')
        radius_step = self.get_int(self.step_radius_line.text(), 'шаг изменения радиуса')
        x_center = self.get_int(self.x_center_line.text(), 'координата x центра')
        y_center = self.get_int(self.y_center_line.text(), 'координата y центра')

        if x_center is None or y_center is None or start_radius is None or end_radius is None or (count_circles is None and radius_step is None):
            return
        elif start_radius == 0 or end_radius == 0:
            self.create_message('Радиус окружности не может равняться нулю')
            return
        elif count_circles is not None and count_circles <= 0:
            self.create_message('Количество окружностей должно быть больше нуля')
            return
        elif radius_step is not None and radius_step == 0:
            self.create_message('Шаг изменения радиуса не может равняться нулю')
            return
        elif count_circles is None and start_radius > end_radius and radius_step > 0:
            self.create_message('Шаг изменения радиуса больше нуля, а радиус должен уменьшаться')
            return
        elif count_circles is None and start_radius < end_radius and radius_step < 0:
            self.create_message('Шаг изменения радиуса меньше нуля, а радиус должен увеличиваться')
            return

        if radius_step is not None:
            if start_radius <= end_radius:
                while start_radius < end_radius:
                    self.clear_circle_algorithms(algorithm, start_radius, x_center, y_center)
                    start_radius += radius_step
            elif start_radius > end_radius:
                while start_radius >= end_radius:
                    self.clear_circle_algorithms(algorithm, start_radius, x_center, y_center)
                    start_radius += radius_step
            else:
                self.clear_circle_algorithms(algorithm, start_radius, x_center, y_center)
        elif count_circles is not None:

            step = round(abs(start_radius - end_radius) / count_circles)

            if start_radius > end_radius:
                step *= -1
                end_radius -= 2
            
            for i_radius in range(start_radius, end_radius + 1, step):
                self.clear_circle_algorithms(algorithm, i_radius, x_center, y_center)





if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()