import math
import traceback
from functools import partial

from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, QTableWidgetItem, \
    QGraphicsView, QColorDialog, QTableWidget
from PyQt5.QtGui import QPen, QBrush, QPixmap, QImage, QColor, QVector3D
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint
import numpy as np

from functions import function1, function2, function3
from algorithm import hidden_line

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Лабораторная №10 по компьютерной графике")

        self.draw_view = self.ui.graphicsView
        self.draw_scene = QGraphicsScene()
        self.draw_view.setScene(self.draw_scene)

        self.draw_scene.addLine(-100, -100, -90, -90, Qt.white)
        self.draw_scene.addLine(0, 0, 100, 100, Qt.white)

        self.pen = QPen()
        self.color = QColor(Qt.red)

        self.choosen_func = None
        self.all_func = [function1, function2, function3]
        self.x_range = None
        self.z_range = None

        self.transform_function_scale = self.pass_func
        self.transform_function_rotate = self.pass_func

        self.angles = [0, 0, 0]
        self.scale_coef = 1

        """Выход из программы через меню"""
        self.exit = self.ui.menu_3
        quit = QAction("Выход", self)
        quit.setShortcut('Ctrl+Q')
        quit.triggered.connect(qApp.quit)
        self.exit.addAction(quit)

        """Вывод информации об авторе"""
        self.author_info = self.ui.menu_2
        author_info = QAction("Информация об авторе", self)
        author_info.triggered.connect(self.author_message)
        self.author_info.addAction(author_info)

        """Вывод информации об авторе"""
        self.lab_info = self.ui.menu
        lab_info = QAction("Информация о программе", self)
        lab_info.triggered.connect(self.lab_message)
        self.lab_info.addAction(lab_info)

        """Поля ввода"""
        self.start_x_line = self.ui.l_range_start_x
        self.end_x_line = self.ui.l_range_end_x
        self.step_x_line = self.ui.l_range_step
        self.start_z_line = self.ui.l_range_start_z
        self.end_z_line = self.ui.l_range_end_z
        self.step_z_line = self.ui.l_range_step_z

        self.scale_line = self.ui.entry_scale_oy
        self.rotate_x_line = self.ui.entry_rotate_ox
        self.rotate_y_line = self.ui.entry_rotate_oy
        self.rotate_z_line = self.ui.entry_rotate_oz

        self.start_x_line.setText('-10')
        self.end_x_line.setText('10')
        self.step_x_line.setText('0.1')

        self.start_z_line.setText('-10')
        self.end_z_line.setText('10')
        self.step_z_line.setText('0.1')

        self.scale_line.setText('1')
        self.rotate_x_line.setText('0')
        self.rotate_y_line.setText('0')
        self.rotate_z_line.setText('0')

        """Кнопки"""
        self.rotate_button = self.ui.b_rotate
        self.scale_button = self.ui.b_scale
        self.draw_button = self.ui.calc_button
        self.clear_button = self.ui.clear_scene_button

        """Привязка действий к нажатию кнопок"""
        self.rotate_button.clicked.connect(self.user_rotate)
        self.scale_button.clicked.connect(self.user_scale)
        self.draw_button.clicked.connect(self.calculate)
        self.clear_button.clicked.connect(self.clear_all_scene)

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
        msg.setText("Программа реализует алгоритм плавающего горизонта. Предоставляется возможность выбора функции поверхности, "
                    "углов поворота, коэффициента масштабирования, диапазона значений по оси Х и Z.")
        msg.exec()

    def clear_all_scene(self):
        """Очистка всей сцены"""
        self.draw_scene.clear()
        self.transform_function_rotate = self.pass_func
        self.transform_function_scale = self.pass_func
        self.angles = [0, 0, 0]
        self.scale_coef = 1

    def check_range(self, start, end, step):
        start, end, step = float(start), float(end), float(step)
        if start >= end or step <= 0:
            raise ValueError

    def get_range(self, start, end, step):
        return [float(i) for i in list(np.arange(start, end, step))]

    def get_user_range(self):
        self.check_range(self.start_x_line.text(), self.end_x_line.text(), self.step_x_line.text())
        self.check_range(self.start_z_line.text(), self.end_z_line.text(), self.step_z_line.text())
        self.x_range = self.get_range(float(self.start_x_line.text()), float(self.end_x_line.text()),
                                      float(self.step_x_line.text()))
        self.z_range = self.get_range(float(self.start_z_line.text()), float(self.end_z_line.text()),
                                      float(self.step_z_line.text()))

    def get_function(self):
        tmp = self.all_func[self.ui.box_choose_func.currentIndex()]
        if tmp != self.choosen_func:
            self.clear_all_scene()
            self.choosen_func = tmp

    def rotate_point(self, first_coord, second_coord, angle):
        rad_angle = math.radians(angle)
        saved_first = first_coord
        first_coord = first_coord * math.cos(rad_angle) - second_coord * math.sin(rad_angle)
        second_coord = saved_first * math.sin(rad_angle) + second_coord * math.cos(rad_angle)
        return first_coord, second_coord

    def rotate_x(self, point: QVector3D, angle):
        return QVector3D(point.x(), *self.rotate_point(point.y(), point.z(), angle))

    def rotate_y(self, point: QVector3D, angle):
        s = self.rotate_point(point.x(), point.z(), angle)
        return QVector3D(s[0], point.y(), s[1])

    def rotate_z(self, point: QVector3D, angle):
        return QVector3D(*self.rotate_point(point.x(), point.y(), angle), point.z())

    def rotate(self, angle_x, angle_y, angle_z, point: QVector3D) -> QVector3D:
        point = self.rotate_x(point, angle_x)
        point = self.rotate_y(point, angle_y)
        point = self.rotate_z(point, angle_z)
        return point

    def scale(self, a, point: QVector3D) -> QVector3D:
        return QVector3D(point.x() * a, point.y() * a, point.z() * a)

    def complete(self, point: QVector3D):
        return self.transform_function_rotate(self.transform_function_scale(point))

    def pass_func(self, point: QVector3D):
        return point

    def complete(self, point: QVector3D):
        return self.transform_function_rotate(self.transform_function_scale(point))

    def user_rotate(self):
        try:
            if len(''.join(self.rotate_x_line.text().split())) == 0:
                x = 0
            else:
                x = float(self.rotate_x_line.text())

            if len(''.join(self.rotate_y_line.text().split())) == 0:
                y = 0
            else:
                y = float(self.rotate_y_line.text())

            if len(''.join(self.rotate_z_line.text().split())) == 0:
                z = 0
            else:
                z = float(self.rotate_z_line.text())

            arr = [x, y, z]
        except Exception:
            self.create_message("Некорректный ввод углов поворота")
        else:
            self.angles = list(map(lambda x, y: x + y, self.angles, arr))
            self.transform_function_rotate = partial(self.rotate, *self.angles)
            self.calculate()

    def user_scale(self):
        try:
            if len(''.join(self.scale_line.text().split())) == 0:
                s = 1
            else:
                s = float(self.scale_line.text())
            assert (s != 0)
        except Exception:
            self.create_message("Некорректный ввод коэффициента масштабирования")
        else:
            self.scale_coef *= s
            self.transform_function_scale = partial(self.scale, self.scale_coef)
            self.calculate()

    def calculate(self):
        try:
            self.get_user_range()
        except Exception as e:
            print(e)
            self.create_message("Некорректный ввод диапазонов\n")
        else:
            try:
                self.get_function()
                self.draw_scene.clear()
                alg = hidden_line(self.draw_scene, self.choosen_func, self.x_range, self.z_range, self.complete)
                alg.drawFloatingHorizon()
                # self.scene.clear()
                # self.scene.addPixmap(QPixmap.fromImage(self.image))
                self.draw_scene.update()
            except Exception as e:
                print(traceback.format_exc())



if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()