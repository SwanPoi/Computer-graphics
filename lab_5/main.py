from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, QTableWidgetItem, \
    QGraphicsView, QColorDialog, QTableWidget
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint

from cap_algorithm import CAP_algorithm
import time


class GraphicScene(QGraphicsScene):
    point_signal = pyqtSignal(QPoint)
    key_signal = pyqtSignal(QPoint, int)
    end_signal = pyqtSignal()

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


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Лабораторная №5 по компьютерной графике")

        self.draw_view = self.ui.graphicsView

        self.draw_scene = GraphicScene()
        self.draw_view.setScene(self.draw_scene)

        self.draw_scene.point_signal.connect(self.add_point)
        self.draw_scene.key_signal.connect(self.key_line)
        self.draw_scene.end_signal.connect(self.finish_polygon)

        """Координаты точек"""
        self.all_polygons = []
        self.cur_polygon = []

        self.line_color = Qt.red
        self.color = Qt.yellow
        self.can_close = 1
        self.drawn = False

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
        self.color_label.setStyleSheet("background-color: yellow")


        """Кнопки"""
        self.delay_button = self.ui.dekay_pushButton
        self.without_delay_button = self.ui.without_delay_pushButton
        self.set_color_button = self.ui.color_pushButton
        self.add_point_button = self.ui.pushButton_2
        self.close_figure_button = self.ui.pushButton_3
        self.time_button = self.ui.time_pushButton

        """Привязка действий к нажатию кнопок"""
        self.add_point_button.clicked.connect(self.add_point_from_lines)
        self.close_figure_button.clicked.connect(self.finish_polygon)
        self.set_color_button.clicked.connect(self.set_color)
        self.without_delay_button.clicked.connect(self.draw_filling)
        self.delay_button.clicked.connect(lambda: self.draw_filling(delay=True))
        self.time_button.clicked.connect(lambda: self.draw_filling(time_measure=True))

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
        msg.setText("Программа реализует алгоритм с упорядоченным списком ребер со списком активных ребер.\n"
                    "Программа позволяет вводить точки как сочетанием полей ввода и соответствующей кнопки, "
                    "так и щелчком левой кнопкой мыши. Для ввода горизонтального ребра используется сочетание "
                    "Ctrl+левая кнопка мыши, для ввода вертикального ребра - сочетание Alt+левая кнопка мыши. "
                    "Для замыкания фигуры используется правая кнопка мыши или соответствующая кнопка интерфейса.\n"
                    "Закраска возможна с задержкой и без задержки. Закраска производится в случае, если все фигуры "
                    "замкнуты. При вводе после закраски дополнительных фигур "
                    "все введенные объекты считаются единым изображением, предыдущая закраска не учитывается. "
                    "Также программа позволяет произвести замер времени "
                    "закраски без задержки с выводом графического результата закраски и временного значения в "
                    "соответствующее поле.")
        msg.exec()

    def set_color(self):
        '''Выбор цвета'''
        color = QColorDialog.getColor()

        if color.isValid():
            self.color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.color = color

    def draw_point(self, point : QPoint):
        self.draw_scene.addEllipse(point.x(), point.y(), 1, 1, QPen(Qt.black))

    def draw_line(self, first_point : QPoint, second_point : QPoint):
        self.draw_scene.addLine(first_point.x(), first_point.y(), second_point.x(), second_point.y(), pen=QPen(self.line_color, 3))

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
        if not self.drawn:
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

    def key_line(self, point : QPoint, axis : int):
        if not self.drawn:
            if axis == 0:
                self.add_point(QPoint(self.cur_polygon[-1][0], point.y()))
            elif axis == 1:
                self.add_point(QPoint(point.x(), self.cur_polygon[-1][1]))

    def finish_polygon(self):
        if not self.drawn:
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

    def add_point_from_lines(self):
        x = self.get_int(self.x_coordinates_line.text(), 'координата Х точки')

        if x is None:
            return

        y = self.get_int(self.y_coordinates_line.text(), 'координата Y точки')

        if y is None:
            return

        self.add_point(QPoint(x, y))

    """Очистка всей сцены"""
    def clear_all_scene(self):
        self.draw_scene.clear()
        self.all_polygons = []
        self.cur_polygon = []
        self.points_table.setRowCount(0)

    def draw_filling(self, delay=False, time_measure=False):
        if len(self.cur_polygon) != 0:
            self.create_message('Для закраски все фигуры должны быть замкнуты.')
            return

        self.drawn = True
        self.delay_button.setEnabled(False)
        self.without_delay_button.setEnabled(False)
        self.set_color_button.setEnabled(False)
        self.add_point_button.setEnabled(False)
        self.close_figure_button.setEnabled(False)
        self.time_button.setEnabled(False)

        self.draw_scene.clear()
        self.draw_all_polygons()

        if time_measure:
            time_start = time.time()
            CAP_algorithm(self.all_polygons, self.color, self.draw_scene)
            time_end = time.time()

            self.time_line.setText(f'{time_end - time_start:.6f}')
        else:
            CAP_algorithm(self.all_polygons, self.color, self.draw_scene, delay)

        self.delay_button.setEnabled(True)
        self.without_delay_button.setEnabled(True)
        self.set_color_button.setEnabled(True)
        self.add_point_button.setEnabled(True)
        self.close_figure_button.setEnabled(True)
        self.time_button.setEnabled(True)
        self.drawn = False

if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()