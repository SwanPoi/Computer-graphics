from interface import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene
from PyQt5.QtGui import QPen, QBrush, QPolygonF
from PyQt5.QtCore import Qt, QObject, QPointF

class Cat:
    def __init__(self):
        '''Координаты точек'''
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

        '''Связи между точками'''
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

        '''Закрашенные области'''
        self.polygon_points = [[20, 53, 54], [10, 11, 45, 46]]

        '''Предыдущие позиции точек'''
        self.last_points = []

class GraphicScene(QGraphicsScene):
    def __init__(self):
        super(GraphicScene, self).__init__()

        self.image = Cat()

    '''Рисование изображения'''
    def draw_image(self):
        self.clear()
        self.draw_lines()
        self.draw_polygons()

    '''Рисование линий'''
    def draw_lines(self) -> None:
        for key in self.image.connections:
            for point in self.image.connections[key]:
                self.addLine(self.image.points[key - 1][0], self.image.points[key - 1][1],
                             self.image.points[point - 1][0], self.image.points[point - 1][1], pen = QPen(Qt.black, 5))

    '''Рисование закрашенных областей'''
    def draw_polygons(self):
        for field in self.image.polygon_points:
            polygon = QPolygonF()
            for point in field:
                polygon << QPointF(self.image.points[point - 1][0], self.image.points[point - 1][1])

            self.addPolygon(polygon, pen=QPen(Qt.black, 9), brush=QBrush(Qt.black, 1))

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



        """Кнопки"""
        self.load_button = self.ui.load_pushButton

        """Привязка действий к нажатию кнопок"""
        self.load_button.clicked.connect(self.load_image)

    """Создание оповещения"""
    def create_message(self, text):
        msg = QMessageBox()
        msg.setWindowTitle("Информация")
        msg.setText(text)
        msg.exec()

    '''Информация об авторе'''
    def author_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация об авторе")
        msg.setText("Лабораторную работу выполнил студент группы ИУ7-45Б Лебедев Владимир. Вариант 13.")
        msg.exec()

    '''Информация о пользователе'''
    def lab_message(self):
        msg = QMessageBox()
        msg.setWindowTitle("Информация о программе")
        msg.setText("Программа решает следующую задачу:Дано исходное изображение. Необходимо реализовать \
        поворот, перенос и масштабирование изображения с возможностью указания центра (для масштабирования и поворота. \
        Также необходимо реализовать отмену действия на 1 шаг.\n"
        "Коэффициенты масштабирования, переноса, угол поворота задаются числами с максимальной точностью "
        "два знака после запятой. Угол задается в градусах.")
        msg.exec()

    '''Загрузка изображения'''
    def load_image(self):
        self.draw_scene.draw_image()

    '''Очистка графической сцены'''
    def clear_all_scene(self):
        self.draw_scene.clear()

if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()