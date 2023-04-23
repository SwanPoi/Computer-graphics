from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, QTableWidgetItem, \
    QGraphicsView, QColorDialog, QTableWidget
from PyQt5.QtGui import QPen, QBrush, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint

import time
from brezenham import integer_bresenham
from seed_algorithm import lines_seed_filling


class GraphicScene(QGraphicsScene):
    point_signal = pyqtSignal(QPoint)
    key_signal = pyqtSignal(QPoint, int)
    end_signal = pyqtSignal()
    seed_signal = pyqtSignal(QPoint)

    def __init__(self):
        super(GraphicScene, self).__init__()

    def mousePressEvent(self, event) -> None:
        modifiers = QApplication.keyboardModifiers()
        if event.button() == Qt.LeftButton:
            if modifiers == Qt.AltModifier:
                self.key_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 0)
            elif modifiers == Qt.ControlModifier:
                self.key_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 1)
            else:
                self.point_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())))
        elif event.button() == Qt.RightButton:
            self.end_signal.emit()
        elif event.button() == Qt.MiddleButton:
            self.seed_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())))

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        modifiers = QApplication.keyboardModifiers()

        if modifiers == Qt.ShiftModifier:
            self.point_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())))


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Лабораторная №6 по компьютерной графике")

        self.draw_view = self.ui.graphicsView

        self.draw_scene = GraphicScene()
        self.draw_view.setScene(self.draw_scene)

        self.image = self.draw_view.image
        self.image.fill(Qt.white)
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))

        self.draw_scene.point_signal.connect(self.add_point)
        self.draw_scene.key_signal.connect(self.key_line)
        self.draw_scene.end_signal.connect(self.finish_polygon)
        self.draw_scene.seed_signal.connect(self.add_seed_point)


        """Координаты точек"""
        self.all_polygons = []
        self.cur_polygon = []
        self.seed_point = []

        self.line_color = Qt.black
        self.color = Qt.darkGreen
        self.can_close = 1

        """Таблицы"""
        self.points_table = self.ui.points_tableWidget

        self.points_table.setColumnCount(2)
        self.points_table.setRowCount(0)
        self.points_table.setHorizontalHeaderLabels(['x', 'y'])
        self.points_table.setEditTriggers(QTableWidget.NoEditTriggers)


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

        """Вывод информации об авторе"""
        self.lab_info = self.ui.program_menu
        lab_info = QAction("Информация о программе", self)
        lab_info.triggered.connect(self.lab_message)
        self.lab_info.addAction(lab_info)

        """Поля ввода координат точки"""
        self.x_coordinates_line = self.ui.x_lineEdit
        self.y_coordinates_line = self.ui.y_lineEdit

        self.time_line = self.ui.lineEdit

        self.color_label = self.ui.color_label
        self.color_label.setStyleSheet("background-color: darkGreen")


        """Кнопки"""
        self.delay_button = self.ui.dekay_pushButton
        self.without_delay_button = self.ui.without_delay_pushButton
        self.set_color_button = self.ui.color_pushButton
        self.add_point_button = self.ui.pushButton_2
        self.close_figure_button = self.ui.pushButton_3
        self.time_button = self.ui.time_pushButton
        self.seed_button = self.ui.seed_pushButton

        """Привязка действий к нажатию кнопок"""
        self.add_point_button.clicked.connect(self.add_point_from_lines)
        self.close_figure_button.clicked.connect(self.finish_polygon)
        self.set_color_button.clicked.connect(self.set_color)
        self.without_delay_button.clicked.connect(self.draw_filling)
        self.delay_button.clicked.connect(lambda: self.draw_filling(delay=True))
        self.time_button.clicked.connect(lambda: self.draw_filling(time_measure=True))
        self.seed_button.clicked.connect(lambda: self.add_point_from_lines(seed=True))

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
        msg.setText("Программа реализует алгоритм затравочного заполнения.\n"
                    "Программа позволяет вводить точки как сочетанием полей ввода и соответствующей кнопки, "
                    "так и щелчком левой кнопкой мыши. Для ввода горизонтального ребра используется сочетание "
                    "Ctrl+левая кнопка мыши, для ввода вертикального ребра - сочетание Alt+левая кнопка мыши. "
                    "Для замыкания фигуры используется правая кнопка мыши или соответствующая кнопка интерфейса. "
                    "Сочетание Shift+зажать ЛКМ позволяет вводить произвольную кривую. Добавление "
                    "затравочной точки производится средней кнопкой мыши (при заполнении учитывается только"
                    "последняя добавленная затравочная точка.\n"
                    "Затравочное заполнение возможно с задержкой и без задержки. Затравка производится в случае, если хотя бы "
                    "одна фигура замкнута. "
                    "Также программа позволяет произвести замер времени "
                    "затравочного заполнения без задержки с выводом графического результата затравки и временного значения в "
                    "соответствующее поле.")
        msg.exec()

    def set_color(self):
        '''Выбор цвета'''
        color = QColorDialog.getColor()

        if color == self.line_color:
            self.create_message('Невозможно выбрать цвет затравки, совпадающий с цветом линий')
            return

        if color.isValid():
            self.color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.color = color

    def draw_point(self, point : QPoint):
        self.image.setPixel(point.x(), point.y(), QColor(self.line_color).rgb())
        self.draw_scene.clear()
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))
        #self.draw_scene.addEllipse(point.x(), point.y(), 1, 1, QPen(Qt.black))

    def draw_line(self, first_point : QPoint, second_point : QPoint):
        points = integer_bresenham(first_point.x(), second_point.x(), first_point.y(), second_point.y())

        for point in points:
            self.image.setPixel(point[0], point[1], QColor(self.line_color).rgb())

        self.draw_scene.clear()
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))
        #self.draw_scene.addLine(first_point.x(), first_point.y(), second_point.x(), second_point.y(), pen=QPen(self.line_color))

    def draw_polygon(self, polygon):
        for i in range(len(polygon) - 1):
            self.draw_point(QPoint(polygon[i][0], polygon[i][1]))
            self.draw_line(QPoint(polygon[i][0], polygon[i][1]), QPoint(polygon[i + 1][0], polygon[i + 1][1]))

        self.draw_point(QPoint(polygon[-1][0], polygon[-1][1]))
        self.draw_line(QPoint(polygon[0][0], polygon[0][1]), QPoint(polygon[-1][0], polygon[-1][1]))

    def draw_all_polygons(self):
        for polygon in self.all_polygons:
            self.draw_polygon(polygon)

    def add_row_to_table(self, first_value, second_value):
        self.points_table.insertRow(self.points_table.rowCount())
        self.points_table.setItem(self.points_table.rowCount() - 1, 0, QTableWidgetItem(str(first_value)))
        self.points_table.setItem(self.points_table.rowCount() - 1, 1, QTableWidgetItem(str(second_value)))

    def add_point(self, point : QPoint):
        if len(self.cur_polygon) == 0:
            self.add_row_to_table('Многоугольник №' + str(len(self.all_polygons) + 1), '')
            self.points_table.setSpan(self.points_table.rowCount() - 1, 0, 1, 2)

        if [point.x(), point.y()] in self.cur_polygon:
            self.create_message('Точки в одной и той же фигуре не могут повторяться.')
            return

        self.cur_polygon.append([point.x(), point.y()])
        self.add_row_to_table(point.x(), point.y())
        self.draw_point(point)

        if len(self.cur_polygon) > 1:
            self.draw_line(QPoint(self.cur_polygon[-2][0], self.cur_polygon[-2][1]), point)

    def add_seed_point(self, point : QPoint):
        self.seed_point.append(point)
        self.image.setPixel(point.x(), point.y(), QColor(self.color).rgb())
        self.draw_scene.clear()
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))

    def key_line(self, point : QPoint, axis : int):
        if axis == 0:
            self.add_point(QPoint(self.cur_polygon[-1][0], point.y()))
        elif axis == 1:
            self.add_point(QPoint(point.x(), self.cur_polygon[-1][1]))

    def finish_polygon(self):
        if len(self.cur_polygon) <= 2:
            self.create_message('Для замыкания фигура должна содержать хотя бы 3 точки')
        else:
            self.draw_line(QPoint(self.cur_polygon[0][0], self.cur_polygon[0][1]),
                           QPoint(self.cur_polygon[-1][0], self.cur_polygon[-1][1]))
            self.all_polygons.append(self.cur_polygon)
            self.cur_polygon = []

    def get_int(self, text, string):
        '''Ввод из поля'''
        result = None
        try:
            result = int(text)
        except:
            self.create_message(f'Ошибка: {string} - нецелое число')

        return result

    def add_point_from_lines(self, seed=False):
        x = self.get_int(self.x_coordinates_line.text(), 'координата Х точки')

        if x is None:
            return

        if x < 0 or x > self.image.width():
            self.create_message(f'Координата х может быть в диапазоне {0, self.image.width()}')
            return

        y = self.get_int(self.y_coordinates_line.text(), 'координата Y точки')

        if y is None:
            return

        if y < 0 or y > self.image.height():
            self.create_message(f'Координата y может быть в диапазоне {0, self.image.height()}')
            return

        if seed:
            self.add_seed_point(QPoint(x, y))
        else:
            self.add_point(QPoint(x, y))


    """Очистка всей сцены"""
    def clear_all_scene(self):
        self.draw_scene.clear()
        self.all_polygons = []
        self.cur_polygon = []
        self.seed_point = []
        self.points_table.setRowCount(0)
        self.image = QImage(5000, 5000, QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))


    def draw_filling(self, delay=False, time_measure=False):
        if len(self.all_polygons) == 0:
            self.create_message('Для закраски должна быть добавлена хотя бы одна замкнутая фигура.')
            return

        if len(self.seed_point) == 0:
            self.create_message('Отсутствует затравочная точка')
            return

        self.draw_scene.clear()
        self.draw_all_polygons()

        if time_measure:
            time_start = time.time()
            lines_seed_filling(self.draw_scene, self.image, QColor(self.line_color), QColor(self.color),
                               self.seed_point[-1])
            time_end = time.time()

            self.time_line.setText(f'{time_end - time_start:.6f}')
        else:
            lines_seed_filling(self.draw_scene, self.image, QColor(self.line_color), QColor(self.color),
                               self.seed_point[-1], delay)




if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()