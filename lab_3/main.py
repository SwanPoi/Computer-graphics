from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, \
    QColorDialog
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
import time
from math import radians
from dda import dda
from vu import vu
from bresenham import *
from help_functions import spin_point
import matplotlib.pyplot as plt
import numpy as np

DDA = 1
BRESENHAM = 2
INTEGER_BRESENHAM = 3
STEP_BRESENHAM = 4
VU = 5
LIBRARY = 6

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

        """Поля для отображения цвета"""
        self.line_color_label = self.ui.line_color_label
        self.line_color_label.setStyleSheet("background-color: black")
        self.background_color_label = self.ui.background_color_label

        """Поля ввода"""
        self.x_start_line = self.ui.x_start_lineEdit
        self.x_end_line = self.ui.x_end_lineEdit
        self.y_start_line = self.ui.y_start_lineEdit
        self.y_end_line = self.ui.y_end_lineEdit

        self.angle_line = self.ui.angle_lineEdit
        self.repeats_line = self.ui.line_length_lineEdit

        """Кнопки"""
        self.dda_button = self.ui.dda_pushButton
        self.bresenham_button = self.ui.bresenham_pushButton
        self.integer_bresenham_button = self.ui.integer_bresenham_pushButton
        self.step_bresenham_button = self.ui.step_bresenham_pushButton
        self.vu_button = self.ui.vu_pushButton
        self.library_button = self.ui.library_pushButton

        self.algorithm_buttons = [self.dda_button, self.bresenham_button, self.integer_bresenham_button,
                                  self.step_bresenham_button, self.vu_button, self.library_button]

        self.change_line_color_button = self.ui.line_color_pushButton
        self.change_background_color_button = self.ui.background_color_pushButton

        self.add_line_button = self.ui.add_segment_pushButton
        self.add_spectrum_button = self.ui.add_spectrum_pushButton

        self.time_compare_button = self.ui.compare_time_pushButton
        self.step_compare_button = self.ui.compare_steps_pushButton

        self.step_back = self.ui.back_step_pushButton
        self.clear_button = self.ui.clear_pushButton

        """Привязка действий к нажатию кнопок"""
        self.change_line_color_button.clicked.connect(self.set_line_color)
        self.change_background_color_button.clicked.connect(self.set_background_color)

        self.dda_button.clicked.connect(self.set_dda)
        self.bresenham_button.clicked.connect(self.set_bresenham)
        self.integer_bresenham_button.clicked.connect(self.set_integer_bresenham)
        self.step_bresenham_button.clicked.connect(self.set_step_bresenham)
        self.vu_button.clicked.connect(self.set_vu)
        self.library_button.clicked.connect(self.set_library)

        self.add_line_button.clicked.connect(lambda: self.choose_algorithm(self.used_algorithm))
        self.add_spectrum_button.clicked.connect(lambda: self.draw_spectrum(self.used_algorithm))

        self.clear_button.clicked.connect(self.clear_scene)
        self.step_back.clicked.connect(self.reverse_last_action)

        self.time_compare_button.clicked.connect(self.time_characteristics)
        self.step_compare_button.clicked.connect(self.step_characteristics)

        self.used_algorithm = None
        self.last_action = list()

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
        msg.setText("Программа строит растровые способы с помощью следующих алгоритмов:\n"
                    "1) Цифровой дифференциальный анализатор\n"
                    "2) Алгоритм Брезенхема с действительными коэффициентами\n"
                    "3) Алгоритм Брезенхема с целыми коэффициентами\n"
                    "4) Алгоритм Брезенхема с устранением ступенчатости\n"
                    "5) Алгоритм Ву\n"
                    "6) Средствами Qt\n"
                    "Программа предоставляет возможность выбирать цвет отрезка, а также цвет фона.\n"
                    "Ввод координат, угла и числа повторов замера времени построения осуществляется в соответствующие поля. "
                    "Координаты могут задаваться целыми числами или вещественными числами с точкой (не запятой). "
                    "Угол задается целым числом градусов, число повторов - целым положительным числом.\n"
                    "Исследование времени построения происходит для конкретного введенного отрезка, суммарное время, "
                    "затраченное на алгоритм, делится на число повторений.\n"
                    "Исследование ступенчатости также происходит для конкретного введенного отрезка. "
                    "Поворот производится на 90 градусов относительно текущего местоположения отрезка.")
        msg.exec()

    def set_line_color(self):
        '''Выбор цвета линии'''
        color = QColorDialog.getColor()

        if color.isValid():
            self.last_action = ['change_line_color', self.draw_scene.line_color.name()]
            self.line_color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.draw_scene.change_line_color(color.name())

    def set_background_color(self):
        '''Выбор цвета фона'''
        color = QColorDialog.getColor()

        if color.isValid():
            self.last_action = ['change_background_color', self.draw_scene.background_color.name()]
            self.background_color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.draw_scene.change_background_color(color.name())

    def draw_line_by_algorithm(self, list_points):
        '''Рисование точек'''
        for point in list_points:
            self.draw_scene.addRect(point[0], point[1], 1, 1,
                                  QPen(self.draw_scene.line_color if len(point) == 2 else point[2]))

    def clear_algorithm_buttons(self):
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

    def set_dda(self):
        '''Выбор ЦДА'''
        self.clear_algorithm_buttons()
        self.last_action = ['choose_algorithm', self.used_algorithm]

        self.used_algorithm = DDA
        self.dda_button.setStyleSheet("background-color: yellow")

    def set_bresenham(self):
        '''Выбор алгоритма Брезенхема'''
        self.clear_algorithm_buttons()
        self.last_action = ['choose_algorithm', self.used_algorithm]

        self.used_algorithm = BRESENHAM
        self.bresenham_button.setStyleSheet("background-color: yellow")

    def set_integer_bresenham(self):
        '''Выбор целочисленного алгоритма Брезенхема'''
        self.clear_algorithm_buttons()
        self.last_action = ['choose_algorithm', self.used_algorithm]

        self.used_algorithm = INTEGER_BRESENHAM
        self.integer_bresenham_button.setStyleSheet("background-color: yellow")

    def set_step_bresenham(self):
        '''Выбор алгоритма Брезенхема со сглаживанием'''
        self.clear_algorithm_buttons()
        self.last_action = ['choose_algorithm', self.used_algorithm]

        self.used_algorithm = STEP_BRESENHAM
        self.step_bresenham_button.setStyleSheet("background-color: yellow")

    def set_vu(self):
        '''Выбор алгоритма Ву'''
        self.clear_algorithm_buttons()
        self.last_action = ['choose_algorithm', self.used_algorithm]

        self.used_algorithm = VU
        self.vu_button.setStyleSheet("background-color: yellow")

    def set_library(self):
        '''Выбор библиотечного алгоритма'''
        self.clear_algorithm_buttons()
        self.last_action = ['choose_algorithm', self.used_algorithm]

        self.used_algorithm = LIBRARY
        self.library_button.setStyleSheet("background-color: yellow")

    def choose_algorithm(self, algorithm_index, coordinates=None, is_drawn=True):
        points_list = list()

        if not algorithm_index:
            self.create_message('Не выбран алгоритм построения')
        else:
            if not coordinates:
                coordinates = self.get_coordinates()

            if coordinates:
                if is_drawn:
                    self.last_action = ['use_algorithm', len(self.draw_scene.items())]
                x_start, y_start, x_end, y_end = coordinates

                time_start = time.time()
                if algorithm_index == DDA:
                    points_list = dda(x_start, x_end, y_start, y_end)
                elif algorithm_index == BRESENHAM:
                    points_list = bresenham_for_float(x_start, x_end, y_start, y_end)
                elif algorithm_index == INTEGER_BRESENHAM:
                    points_list = integer_bresenham(x_start, x_end, y_start, y_end)
                elif algorithm_index == STEP_BRESENHAM:
                    points_list = step_bresenham(x_start, x_end, y_start, y_end, self.draw_scene.line_color)
                elif algorithm_index == VU:
                    points_list = vu(x_start, x_end, y_start, y_end, self.draw_scene.line_color)
                elif algorithm_index == LIBRARY:
                    self.draw_scene.addLine(x_start, y_start, x_end, y_end, QPen(self.draw_scene.line_color))

                if algorithm_index != LIBRARY and is_drawn:
                    self.draw_line_by_algorithm(points_list)

                time_end = time.time()

                return time_end - time_start

    def draw_spectrum(self, algorithm_index, coordinates=None, angle=None, is_drawn=True):
        '''Построение спектра'''
        if not algorithm_index:
            self.create_message('Не выбран алгоритм построения')
        else:
            if not coordinates:
                coordinates = self.get_coordinates()

            if coordinates:
                if not angle:
                    angle = self.get_angle()

                if angle:
                    if is_drawn:
                        count_items = len(self.draw_scene.items())

                    for i in range(int(360 // angle)):
                        self.choose_algorithm(algorithm_index, coordinates, is_drawn)
                        coordinates[2], coordinates[3] = spin_point([coordinates[2], coordinates[3]], [coordinates[0],
                                                                      coordinates[1]], radians(angle))


                    self.last_action = ['draw_spectrum', count_items]


    def get_angle(self):
        '''Ввод угла поворота'''
        result = None

        try:
            result = int(self.angle_line.text())
        except:
            self.create_message('Угол задается целым числом градусов')

        return result

    def get_count_of_repeats(self):
        '''Ввод числа повторов'''
        result = None

        try:
            result = int(self.repeats_line.text())
        except:
            self.create_message('Число повторений задается целым положительным числом')
        else:
            if result <= 0:
                self.create_message('Число повторений задается целым положительным числом')
                result = None

        return result

    def get_coordinates(self):
        '''Ввод координат отрезка'''
        result = None
        max_value_x = self.ui.scene_graphicsView.width()
        max_value_y = self.ui.scene_graphicsView.height()

        try:
            x_start = float(self.x_start_line.text())
            x_end = float(self.x_end_line.text())
            y_start = float(self.y_start_line.text())
            y_end = float(self.y_end_line.text())
        except:
            self.create_message("Вы ввели неверные координаты. Координаты должны быть числовыми")
        else:
            if 0 <= x_start < max_value_x and 0 <= x_end < max_value_x and 0 <= y_start < max_value_y and 0 <= y_end < max_value_y:
                result = [x_start, y_start, x_end, y_end]
            else:
                self.create_message('Введенные координаты находятся вне холста')

        return result

    def clear_scene(self):
        '''Очистка сцены'''
        self.draw_scene.clear()
        self.draw_scene.list_for_axises = []
        self.draw_scene.draw_axises(self.ui.scene_graphicsView.width(), self.ui.scene_graphicsView.height())

    def reverse_last_action(self):
        '''Отмена последнего действия'''
        if len(self.last_action) == 0:
            self.create_message('Невозможно отменить более одного или еще не совершенные действия.')
        elif self.last_action[0] == 'change_line_color':
            '''Отмена выбора цвета линии'''
            self.draw_scene.change_line_color(self.last_action[1])
            self.line_color_label.setStyleSheet("background-color: {}".format(self.last_action[1]))
        elif self.last_action[0] == 'change_background_color':
            '''Отмена выбора цвета фона'''
            self.draw_scene.change_background_color(self.last_action[1])
            self.background_color_label.setStyleSheet("background-color: {}".format(self.last_action[1]))
        elif self.last_action[0] == 'use_algorithm':
            '''Отмена рисования линии'''
            for i in range(len(self.draw_scene.items()) - self.last_action[1]):
                self.draw_scene.removeItem((self.draw_scene.items())[0])
        elif self.last_action[0] == 'draw_spectrum':
            '''Отмена рисования спектра'''
            for i in range(len(self.draw_scene.items()) - self.last_action[1]):
                self.draw_scene.removeItem((self.draw_scene.items())[0])
        elif self.last_action[0] == 'choose_algorithm':
            '''Отмена выбора алгоритма'''
            if self.last_action[1] == None:
                self.clear_algorithm_buttons()
            elif self.last_action[1] == DDA:
                self.set_dda()
            elif self.last_action[1] == BRESENHAM:
                self.set_bresenham()
            elif self.last_action[1] == INTEGER_BRESENHAM:
                self.set_integer_bresenham()
            elif self.last_action[1] == STEP_BRESENHAM:
                self.set_step_bresenham()
            elif self.last_action[1] == VU:
                self.set_vu()
            elif self.last_action[1] == LIBRARY:
                self.set_library()

            self.used_algorithm = self.last_action[1]

        self.last_action = []

    def time_characteristics(self):
        plt.figure('Временные характеристики работы алгоритмов построения отрезков', figsize=(9, 7))
        list_times = [[], [], [], [], []]

        coordinates = self.get_coordinates()

        if coordinates:
            repeats = self.get_count_of_repeats()

            if repeats:
                for i in range(repeats):
                    list_times[0].append(self.choose_algorithm(DDA, coordinates, False))
                    list_times[1].append(self.choose_algorithm(BRESENHAM, coordinates, False))
                    list_times[2].append(self.choose_algorithm(INTEGER_BRESENHAM, coordinates, False))
                    list_times[3].append(self.choose_algorithm(STEP_BRESENHAM, coordinates, False))
                    list_times[4].append(self.choose_algorithm(VU, coordinates, False))

                tuple_labers = ('ЦДА', 'Алгоритм \nБрезенхема с\nдействительными\nкоэффицентами',
                                'Алгоритм \nБрезенхема с\nцелыми\nкоэффицентами',
                                'Алгоритм \nБрезенхема с\n устранением\nступенчатости', 'Ву')

                final_times = []

                for i in range(len(list_times)):
                    sum = 0
                    for j in range(len(list_times[i])):
                        sum += list_times[i][j]
                    final_times.append(sum / repeats)

                all_alg = range(len(final_times))

                plt.bar(all_alg, final_times, align='center')
                plt.xticks(all_alg, tuple_labers)
                plt.ylabel('Секунды')
                plt.show()

    def step_characteristics(self):
        coordinates = self.get_coordinates()

        if coordinates:
            x_start, y_start, x_end, y_end = coordinates
            step = 2
            angle = 0
            angles = list()
            dda_steps = list()
            bresenham_steps = list()
            int_bresenham_steps = list()
            smooth_bresenham_steps = list()
            vu_steps = list()

            for i in range(90 // step):
                dda_steps.append(dda(x_start, x_end, y_start, y_end, step_mode=True))
                bresenham_steps.append(bresenham_for_float(x_start, x_end, y_start, y_end, step_mode=True))
                int_bresenham_steps.append(integer_bresenham(x_start, x_end, y_start, y_end, step_mode=True))
                smooth_bresenham_steps.append(step_bresenham(x_start, x_end, y_start, y_end, color=self.draw_scene.line_color, step_mode=True))
                vu_steps.append(vu(x_start, x_end, y_start, y_end, color=self.draw_scene.line_color, step_mode=True))
                x_end, y_end = spin_point([x_end, y_end], [x_start, y_start], radians(step))

                angles.append(angle)
                angle += step

            plt.figure("Характеристика ступенчатости алгоритмов построения.", figsize=(18, 10))

            plt.subplot(2, 3, 1)
            plt.title("ЦДА")
            plt.plot(angles, dda_steps)
            plt.xticks(np.arange(91, step=5))
            plt.ylabel("Число ступенек")
            plt.xlabel("Угол (в градусах)")

            plt.subplot(2, 3, 2)
            plt.title("Алгоритм Брензенхема с действительными коэффицентами")
            plt.plot(angles, bresenham_steps)
            plt.xticks(np.arange(91, step=5))
            plt.ylabel("Число ступенек")
            plt.xlabel("Угол (в градусах)")

            plt.subplot(2, 3, 3)
            plt.title("Алгоритм Брензенхема с целыми коэффицентами")
            plt.plot(angles, int_bresenham_steps)
            plt.xticks(np.arange(91, step=5))
            plt.ylabel("Число ступенек")
            plt.xlabel("Угол (в градусах)")

            plt.subplot(2, 3, 4)
            plt.title("Алгоритм Брензенхема с устранением ступенчатости")
            plt.plot(angles, smooth_bresenham_steps)
            plt.xticks(np.arange(91, step=5))
            plt.ylabel("Число ступенек")
            plt.xlabel("Угол (в градусах)")

            plt.subplot(2, 3, 5)
            plt.title("Алгоритм Ву")
            plt.plot(angles, vu_steps)
            plt.xticks(np.arange(91, step=5))
            plt.ylabel("Число ступенек")
            plt.xlabel("Угол (в градусах)")

            plt.subplot(2, 3, 6)
            plt.plot(angles, dda_steps, label="ЦДА")
            plt.plot(angles, bresenham_steps, '-*', label="Брензенхем с \nдействительными коэффицентами")
            plt.plot(angles, int_bresenham_steps, '-.', label="Брензенхем с целыми \n коэффицентами")
            plt.plot(angles, smooth_bresenham_steps, '.', label="Брензенхем с\n устранением\nступенчатости")
            plt.plot(angles, vu_steps, '--', label="By")
            plt.title("Исследование ступенчатости.")
            plt.xticks(np.arange(91, step=5))
            plt.legend()
            plt.ylabel("Число ступенек")
            plt.xlabel("Угол (в градусах)")

            plt.show()

if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()