from interface import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene
from PyQt5.QtGui import QPen, QBrush, QPolygonF
from PyQt5.QtCore import Qt, QPointF
import copy
import point_transformations as p_transform
from math import radians

DRAWN = 1
NOT_DRAWN = 0
SET_CENTER = 2
IMAGE_CNANGE = 3

class Cat:
    def __init__(self):
        """Координаты точек"""
        self.points = [[68, 3], [208, 112], [242, 112], [288, 127], [320, 93],
                       [385, 43], [432, 26], [431, 143], [414, 220], [433, 279],
                       [400, 310], [359, 352], [334, 380], [246, 450], [213, 448],
                       [107, 448], [59, 442], [30, 419], [3, 381], [14, 351],
                       [62, 312], [61, 301], [60, 272], [79, 200], [100, 170],
                       [129, 145], [156, 121], [170, 114], [281, 160], [333, 112],
                       [311, 193], [322, 213], [282, 270], [228, 258], [207, 255],
                       [146, 235], [114, 283], [80, 280], [101, 257], [189, 281],
                       [180, 292], [233, 285], [249, 276], [336, 297], [412, 280],
                       [405, 292], [354, 324], [222, 392], [130, 428], [118, 428],
                       [142, 397], [130, 355], [75, 357], [43, 398], [47, 410]]

        """Связи между точками"""
        self.connections = {
            1: [2, 25, 26, 27],
            2: [3, 28],
            3: [4, 29, 36],
            4: [5, 29],
            5: [6, 30],
            6: [7, 30],
            7: [8, 32],
            8: [9, 32],
            9: [10, 32, 44],
            10: [11, 45],
            11: [12, 46],
            12: [13, 47],
            13: [14, 48],
            14: [15],
            15: [16, 48],
            16: [17, 50],
            17: [18],
            18: [19, 55],
            19: [20],
            20: [21, 53, 54],
            21: [22, 37],
            22: [23, 38],
            23: [24, 39],
            24: [25, 39],
            25: [26, 39],
            26: [27, 36],
            27: [28],
            29: [31, 35],
            30: [31],
            31: [32],
            32: [33, 34],
            33: [34, 43, 44, 48],
            34: [35, 40],
            35: [36, 40],
            36: [37, 39],
            37: [38, 39],
            38: [39],
            40: [41],
            41: [42, 48, 52],
            42: [43, 48],
            43: [48],
            44: [45, 47, 48],
            45: [46],
            46: [47],
            47: [48],
            48: [49, 51],
            49: [50],
            50: [51, 55],
            51: [52],
            52: [53],
            53: [54],
            54: [55]
        }

        """Закрашенные области"""
        self.polygon_points = [[20, 53, 54], [10, 11, 45, 46]]

        """Центр для поворота и масштабирования"""
        self.center = [0, 0]

        """Предыдущие позиции точек"""
        self.last_points = []

        """Предыдущий центр"""
        self.last_center = None

class GraphicScene(QGraphicsScene):
    def __init__(self):
        super(GraphicScene, self).__init__()

        self.image = Cat()
        self.drawn = NOT_DRAWN
        self.last_action = None

    """Рисование изображения"""
    def draw_image(self):
        self.clear()
        self.draw_lines()
        self.draw_polygons()
        self.draw_center()

    def draw_lines(self) -> None:
        """Рисование линий"""
        for key in self.image.connections:
            for point in self.image.connections[key]:
                self.addLine(self.image.points[key - 1][0], self.image.points[key - 1][1],
                             self.image.points[point - 1][0], self.image.points[point - 1][1], pen = QPen(Qt.black, 5))

    def draw_polygons(self):
        """Рисование закрашенных областей"""
        for field in self.image.polygon_points:
            polygon = QPolygonF()
            for point in field:
                polygon << QPointF(self.image.points[point - 1][0], self.image.points[point - 1][1])

            self.addPolygon(polygon, pen=QPen(Qt.black, 9), brush=QBrush(Qt.black, 1))

    def draw_center(self):
        """Рисование центра для масштабирования и поворота"""
        self.addEllipse(self.image.center[0], self.image.center[1], 5, 5, pen=QPen(Qt.green, 4), brush=QBrush(Qt.green, 4))

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Лабораторная №2 по компьютерной графике")

        self.draw_view = self.ui.graphicsView

        self.draw_scene = GraphicScene()
        self.draw_view.setScene(self.draw_scene)

        """Выход из программы через меню"""
        self.exit = self.ui.exit_menu
        quit = QAction("Выход", self)
        quit.setShortcut('Ctrl+Q')
        quit.triggered.connect(qApp.quit)
        self.exit.addAction(quit)

        """Очистка экрана через меню"""
        self.clear = self.ui.clear_menu
        clear = QAction("Очистить графическую сцену", self)
        clear.triggered.connect(self.clear_all_scene)
        self.clear.addAction(clear)

        """Вывод информации об авторе"""
        self.author_info = self.ui.author_menu
        author_info = QAction("Информация об авторе", self)
        author_info.triggered.connect(self.author_message)
        self.author_info.addAction(author_info)

        """Вывод информации о программе"""
        self.lab_info = self.ui.program_menu
        lab_info = QAction("Информация о программе", self)
        lab_info.triggered.connect(self.lab_message)
        self.lab_info.addAction(lab_info)

        """Обертки для DoubleSpinBox"""
        self.move_x = self.ui.doubleSpinBox_move_x
        self.move_y = self.ui.doubleSpinBox_move_y
        self.scale_x = self.ui.doubleSpinBox_scale_x
        self.scale_y = self.ui.doubleSpinBox_scale_y
        self.spin = self.ui.doubleSpinBox_spin_x
        self.set_center_x = self.ui.doubleSpinBox_scale_x_2
        self.set_center_y = self.ui.doubleSpinBox_scale_y_2

        """Кнопки"""
        self.load_button = self.ui.load_pushButton
        self.set_center_button = self.ui.pushButton_center_2
        self.reverse_action_button = self.ui.load_pushButton_2
        self.move_button = self.ui.pushButton_move
        self.scale_button = self.ui.pushButton_scale
        self.spin_button = self.ui.pushButton_spin

        """Привязка действий к нажатию кнопок"""
        self.load_button.clicked.connect(self.load_image)
        self.set_center_button.clicked.connect(self.set_new_center)
        self.reverse_action_button.clicked.connect(self.reverse_action)
        self.move_button.clicked.connect(self.move_button_action)
        self.scale_button.clicked.connect(self.scale_button_action)
        self.spin_button.clicked.connect(self.spin_button_action)


    """Создание оповещения"""
    def create_message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setText(text)
        msg.exec()

    """Информация об авторе"""
    def author_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация об авторе")
        msg.setText("Лабораторную работу выполнил студент группы ИУ7-45Б Лебедев Владимир. Вариант 13.")
        msg.exec()

    """Информация о пользователе"""
    def lab_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация о программе")
        msg.setText("Программа решает следующую задачу: Дано исходное изображение. Необходимо реализовать \
        поворот, перенос и масштабирование изображения с возможностью указания координат точки для масштабирования и поворота. \
        Также необходимо реализовать отмену действия на 1 шаг.\n"
        "Коэффициенты масштабирования, переноса, угол поворота, координаты точки задаются числами с максимальной точностью "
        "два знака после запятой. Угол задается в градусах. Начальное положение центра масштабирования и поворота - "
        "начало координат (точка [0, 0]).")
        msg.exec()

    def load_image(self):
        """Загрузка изображения"""
        self.draw_scene.drawn = DRAWN
        self.draw_scene.draw_image()

    def clear_all_scene(self):
        """Очистка графической сцены"""
        self.draw_scene.drawn = NOT_DRAWN
        self.draw_scene.clear()

    def set_new_center(self):
        """Изменение центра масштабирования и поворота"""
        if self.draw_scene.drawn == NOT_DRAWN:
            self.create_message("Изображение не загружено")
        else:
            self.draw_scene.last_action = SET_CENTER
            self.draw_scene.image.last_center = copy.copy(self.draw_scene.image.center)
            self.draw_scene.image.center = [self.set_center_x.value(), self.set_center_y.value()]
            self.draw_scene.draw_image()

    def reverse_action(self):
        """Отмена предыдущего действия"""
        if self.draw_scene.drawn == NOT_DRAWN:
            self.create_message("Изображение не загружено")
        elif self.draw_scene.last_action is None:
            self.create_message("Невозможно отменить более одного действия или несуществующее действие")
        else:
            if self.draw_scene.last_action == SET_CENTER:
                self.draw_scene.image.center = copy.copy(self.draw_scene.image.last_center)
            else:
                self.draw_scene.image.points = copy.deepcopy(self.draw_scene.image.last_points)

            self.draw_scene.last_action = None
            self.draw_scene.draw_image()

    def move_button_action(self):
        """Обработка нажатия кнопки переноса"""
        if self.draw_scene.drawn == NOT_DRAWN:
            self.create_message("Изображение не загружено")
        else:
            self.draw_scene.last_action = IMAGE_CNANGE
            self.draw_scene.image.last_points = copy.deepcopy(self.draw_scene.image.points)
            dx = self.move_x.value()
            dy = self.move_y.value()

            self.move_all_points(dx, dy)
            self.draw_scene.draw_image()

    def move_all_points(self, dx, dy):
        """Перенос всех точек изображения"""
        for point in self.draw_scene.image.points:
            point = p_transform.move_point(point, dx, dy)

    def scale_button_action(self):
        """Обработка нажатия кнопки масштабирования"""
        if self.draw_scene.drawn == NOT_DRAWN:
            self.create_message("Изображение не загружено")
        else:
            kx = self.scale_x.value()
            ky = self.scale_y.value()

            if kx * ky == 0:
                self.create_message("Коэффициенты масштабирования не могут равняться 0")
            else:
                self.draw_scene.last_action = IMAGE_CNANGE
                self.draw_scene.image.last_points = copy.deepcopy(self.draw_scene.image.points)

                self.scale_all_points(kx, ky)
                self.draw_scene.draw_image()

    def scale_all_points(self, kx, ky):
        """Масштабирование всех точек изображения"""
        for point in self.draw_scene.image.points:
            point = p_transform.scale_point(point, self.draw_scene.image.center, kx, ky)

    def spin_button_action(self):
        """Обработка нажатия кнопки поворота"""
        if self.draw_scene.drawn == NOT_DRAWN:
            self.create_message("Изображение не загружено")
        else:
            angle = self.spin.value()

            self.draw_scene.last_action = IMAGE_CNANGE
            self.draw_scene.image.last_points = copy.deepcopy(self.draw_scene.image.points)

            self.spin_all_points(radians(angle))
            self.draw_scene.draw_image()

    def spin_all_points(self, angle):
        """Поворот всех точек изображения"""
        for point in self.draw_scene.image.points:
            point = p_transform.spin_point(point, self.draw_scene.image.center, angle)


if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()