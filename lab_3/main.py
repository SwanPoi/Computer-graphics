from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, QTableWidgetItem, \
    QColorDialog
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QObject
from dda import dda
from bresenham import *

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

        self.clear_button.clicked.connect(self.clear_scene)

        self.used_algorithm = None

    """Создание оповещения"""
    def create_message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setText(text)
        msg.exec()

    def author_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация об авторе")
        msg.setText("Лабораторную работу выполнил студент группы ИУ7-45Б Лебедев Владимир. Вариант 13.")
        msg.exec()

    def lab_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация о программе")
        msg.setText("Программа решает следующую задачу:\"Даны два множества точек на плоскости. Из первого множества "
                    "выбрать три различные точки так, чтобы треугольник с вершинами в этих точках содержал "
                    "(строго внутри себя) равное количество точек первого и второго множеств\"\n"
                    "Задача решается с помощью оценки векторных произведений для трех точек треугольника и одной "
                    "выбранной точки. Если все псевдоскалярные произведения отличны от нуля и одного знака, то "
                    "выбранная точка лежит внутри треугольника.\nПользователю предоставляется возможность добавлять "
                    "точки в множества (первое множество выделяется красным цветом, второе множество выделяется "
                    "зеленым цветом). Возможно добавление путем ввода координат и нажатия соответсвующей кнопки или "
                    "путем постановки точки кликом мыши на графической сцене (появляется точка, обведенная черным "
                    "кругом) и нажатием соответсвующей кнопки. Если была нажата не кнопка добавления в какое-либо "
                    "множество, то точка исчезнет с холста. Также пользователь может удалить или редактировать точки, "
                    "введя их координаты или выделив строку с необходимой точкой в таблице точек - при этом координаты "
                    "точки появятся в поле для ввода координат, а точка подсветится фиолетовым цветом.")
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

    def set_dda(self):
        '''Выбор ЦДА'''
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

        self.used_algorithm = DDA
        self.dda_button.setStyleSheet("background-color: yellow")

    def set_bresenham(self):
        '''Выбор алгоритма Брезенхема'''
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

        self.used_algorithm = BRESENHAM
        self.bresenham_button.setStyleSheet("background-color: yellow")

    def set_integer_bresenham(self):
        '''Выбор целочисленного алгоритма Брезенхема'''
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

        self.used_algorithm = INTEGER_BRESENHAM
        self.integer_bresenham_button.setStyleSheet("background-color: yellow")

    def set_step_bresenham(self):
        '''Выбор алгоритма Брезенхема со сглаживанием'''
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

        self.used_algorithm = STEP_BRESENHAM
        self.step_bresenham_button.setStyleSheet("background-color: yellow")

    def set_vu(self):
        '''Выбор алгоритма Ву'''
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

        self.used_algorithm = VU
        self.vu_button.setStyleSheet("background-color: yellow")

    def set_library(self):
        '''Выбор библиотечного алгоритма'''
        for button in self.algorithm_buttons:
            button.setStyleSheet("background-color: white")

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
                x_start, y_start, x_end, y_end = coordinates

                if algorithm_index == DDA:
                    points_list = dda(x_start, x_end, y_start, y_end)
                elif algorithm_index == BRESENHAM:
                    points_list = bresenham_for_float(x_start, x_end, y_start, y_end)
                elif algorithm_index == INTEGER_BRESENHAM:
                    points_list = integer_bresenham(x_start, x_end, y_start, y_end)
                elif algorithm_index == STEP_BRESENHAM:
                    points_list = step_bresenham(x_start, x_end, y_start, y_end, self.draw_scene.line_color)
                elif algorithm_index == LIBRARY:
                    self.draw_scene.addLine(x_start, y_start, x_end, y_end, QPen(self.draw_scene.line_color))

                if algorithm_index != LIBRARY and is_drawn:
                    self.draw_line_by_algorithm(points_list)




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



if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()