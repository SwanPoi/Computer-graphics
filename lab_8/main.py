from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, QTableWidgetItem, \
    QGraphicsView, QColorDialog, QTableWidget
from PyQt5.QtGui import QPen, QBrush, QPixmap, QImage, QColor
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QPoint

import cut_algorithm as cut
from brezenham import integer_bresenham

class GraphicScene(QGraphicsScene):
    point_signal = pyqtSignal(QPoint)
    key_signal = pyqtSignal(QPoint, int, int)
    cutter_signal = pyqtSignal(QPoint, int)

    def __init__(self):
        super(GraphicScene, self).__init__()

    def mousePressEvent(self, event) -> None:
        modifiers = QApplication.keyboardModifiers()
        if event.button() == Qt.LeftButton:
            if modifiers == Qt.ShiftModifier:
                self.cutter_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 1)
            elif modifiers == Qt.AltModifier:
                self.key_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 0, 1)
            elif modifiers == Qt.ControlModifier:
                self.key_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 1, 1)
            else:
                self.cutter_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 0)
        elif event.button() == Qt.RightButton:
            if modifiers == Qt.AltModifier:
                self.key_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 0, 0)
            elif modifiers == Qt.ControlModifier:
                self.key_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())), 1, 0)
            else:
                self.point_signal.emit(QPoint(int(event.scenePos().x()), int(event.scenePos().y())))


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Лабораторная №8 по компьютерной графике")

        self.draw_view = self.ui.graphicsView

        self.draw_scene = GraphicScene()
        self.draw_view.setScene(self.draw_scene)

        self.image = self.draw_view.image
        self.image.fill(Qt.white)
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))

        self.draw_scene.point_signal.connect(self.add_point)
        self.draw_scene.key_signal.connect(self.key_line)
        self.draw_scene.cutter_signal.connect(self.add_cutter)

        self.drawn = False
        """Координаты точек"""
        self.all_segments = []
        self.cur_segment = []
        self.cutter = []
        self.is_close = False

        self.line_color = Qt.black
        self.cutter_color = Qt.darkGreen
        self.cut_color = Qt.red
        self.scene_color = Qt.white
        self.can_close = 1

        """Таблицы"""
        self.points_table = self.ui.points_tableWidget

        self.points_table.setColumnCount(2)
        self.points_table.setRowCount(0)
        self.points_table.setHorizontalHeaderLabels(['x', 'y'])
        self.points_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.points_table.setColumnWidth(0, 5)
        self.points_table.setColumnWidth(1, 20)
        self.points_table.setColumnWidth(2, 20)

        self.cutter_table = self.ui.cut_tableWidget

        self.cutter_table.setColumnCount(2)
        self.cutter_table.setRowCount(0)
        self.cutter_table.setHorizontalHeaderLabels(['x', 'y'])
        self.cutter_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cutter_table.setColumnWidth(0, 5)
        self.cutter_table.setColumnWidth(1, 20)
        self.cutter_table.setColumnWidth(2, 20)

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
        self.x_left_line = self.ui.x_left_lineEdit
        self.y_left_line = self.ui.y_left_lineEdit
        self.x_right_line = self.ui.x_right_lineEdit
        self.y_right_line = self.ui.y_right_lineEdit

        self.line_color_label = self.ui.color_segment_label
        self.cutter_color_label = self.ui.color_cut_label
        self.cut_color_label = self.ui.color_final_label
        self.cutter_color_label.setStyleSheet("background-color: darkGreen")
        self.line_color_label.setStyleSheet("background-color: black")
        self.cut_color_label.setStyleSheet("background-color: red")

        self.ui.xr_label.hide()
        self.ui.yr_label.hide()
        self.x_right_line.hide()
        self.y_right_line.hide()

        """Кнопки"""
        self.add_point_button = self.ui.add_point_pushButton
        self.add_cutter_button = self.ui.add_cut_pushButton
        self.close_figure_button = self.ui.final_cut_pushButton
        self.do_cut_button = self.ui.cut_pushButton
        self.set_line_color_button = self.ui.color_segment_pushButton
        self.set_cutter_color_button = self.ui.color_cut_pushButton
        self.set_cut_color_button = self.ui.color_final_pushButton

        """Привязка действий к нажатию кнопок"""
        self.add_point_button.clicked.connect(self.add_point_from_lines)
        self.add_cutter_button.clicked.connect(self.add_cutter_from_lines)
        self.close_figure_button.clicked.connect(self.close_cutter)
        self.set_line_color_button.clicked.connect(self.set_line_color)
        self.set_cutter_color_button.clicked.connect(self.set_cutter_color)
        self.set_cut_color_button.clicked.connect(self.set_cut_color)
        self.do_cut_button.clicked.connect(self.do_cut)

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
        msg.setText("Программа реализует алгоритм Кируса-Бека отсечения отрезка произвольным выпуклого отсекателем.\n"
                    "Программа позволяет вводить точки отрезков и отсекатель как сочетанием полей ввода и соответствующей кнопки, "
                    "так и щелчком левой кнопкой мыши (для отсекателя обычный щелчок левой кнопки мыши - добавление точки отсекателя, "
                    "щелчок левой кнопкой мыши+Shift - замыкание отсекателя). "
                    "Для ввода горизонтального отрезка (ребра отсекателя) используется сочетание кнопки мыши с "
                    "Ctrl, для ввода вертикального ребра - сочетание с Alt. "
                    "Отсекатель может быть только один (при построении нового отсекателя предыдущий стирается), "
                    "отрезков по заданию - не более 10. При построении не выпуклого отсекателя, отсекатель стирается\n"
                    "Можно выбирать цвет отрезков, отсекателя и частей отрезков, полученных в результате работы алгоритма "
                    "(он не может совпадать с цветом изначального отрезка, так как изначальные отрезки не стираются).")
        msg.exec()

    def set_line_color(self):
        '''Выбор цвета'''
        color = QColorDialog.getColor()

        if color == self.cut_color:
            self.create_message('Невозможно выбрать цвет отрезков, совпадающий с отсекающим цветом')
            return

        if color.isValid():
            self.line_color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.line_color = color

    def set_cutter_color(self):
        '''Выбор цвета'''
        color = QColorDialog.getColor()

        if color.isValid():
            self.cutter_color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.cutter_color = color

    def set_cut_color(self):
        '''Выбор цвета'''
        color = QColorDialog.getColor()

        if color == self.line_color:
            self.create_message('Невозможно выбрать отсекающий цвет, совпадающий с цветом отрезков')
            return

        if color.isValid():
            self.cut_color_label.setStyleSheet("background-color: {}".format(color.name()))
            self.cut_color = color

    def draw_point(self, point : QPoint, color):
        self.image.setPixel(point.x(), point.y(), QColor(color).rgb())
        self.draw_scene.clear()
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))

    def draw_line(self, first_point : QPoint, second_point : QPoint, color):
        points = integer_bresenham(first_point.x(), second_point.x(), first_point.y(), second_point.y())

        for point in points:
            self.image.setPixel(point[0], point[1], QColor(color).rgb())

        self.draw_scene.clear()
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))

    def draw_cutter(self, polygon, color):
        for i in range(len(polygon) - 1):
            self.draw_point(QPoint(polygon[i][0], polygon[i][1]), color)
            self.draw_line(QPoint(polygon[i][0], polygon[i][1]), QPoint(polygon[i + 1][0], polygon[i + 1][1]), color)

        self.draw_point(QPoint(polygon[-1][0], polygon[-1][1]), color)
        self.draw_line(QPoint(polygon[0][0], polygon[0][1]), QPoint(polygon[-1][0], polygon[-1][1]), color)

    def draw_all_segments(self):
        for segment in self.all_segments:
            self.draw_line(QPoint(segment[0][0], segment[0][1]), QPoint(segment[1][0], segment[1][1]), self.line_color)

    def add_row_to_table(self, table, first_value, second_value):
        table.insertRow(table.rowCount())
        table.setItem(table.rowCount() - 1, 0, QTableWidgetItem(str(first_value)))
        table.setItem(table.rowCount() - 1, 1, QTableWidgetItem(str(second_value)))

    def add_point(self, point : QPoint):
        if len(self.all_segments) == 10:
            self.create_message('По заданию необходим ввод до 10 отрезков')
            return

        if not self.drawn:
            if len(self.cur_segment) == 0:
                self.add_row_to_table(self.points_table, 'Отрезок №' + str(len(self.all_segments) + 1), '')
                self.points_table.setSpan(self.points_table.rowCount() - 1, 0, 1, 2)

            if [point.x(), point.y()] in self.cur_segment:
                self.create_message('Точки отрезка не могут совпадать.')
                return

            self.cur_segment.append([point.x(), point.y()])
            self.add_row_to_table(self.points_table, point.x(), point.y())
            self.draw_point(point, self.line_color)

            if len(self.cur_segment) > 1:
                self.draw_line(QPoint(self.cur_segment[0][0], self.cur_segment[0][1]), point, self.line_color)
                self.all_segments.append(self.cur_segment)
                self.cur_segment = []

    def key_line(self, point : QPoint, axis : int, func : int):
        if not self.drawn:
            if func == 0:
                if len(self.cur_segment) == 0:
                    self.add_point(point)
                elif axis == 0:
                    self.add_point(QPoint(self.cur_segment[-1][0], point.y()))
                elif axis == 1:
                    self.add_point(QPoint(point.x(), self.cur_segment[-1][1]))
            else:
                if len(self.cutter) == 0:
                    self.add_cutter(point)
                elif axis == 0:
                    self.add_cutter(QPoint(self.cutter[-1][0], point.y()))
                elif axis == 1:
                    self.add_cutter(QPoint(point.x(), self.cutter[-1][1]))

    def add_cutter(self, point : QPoint, func=0):
        if not self.drawn:
            if self.is_close == True:
                self.draw_cutter(self.cutter, Qt.white)
                self.cutter = []
                self.cutter_table.setRowCount(0)
                self.cutter_table.setSpan(self.cutter_table.rowCount() - 1, 0, 1, 2)
                self.is_close = False

            if func == 0:
                self.cutter.append([point.x(), point.y()])
                self.draw_point(point, self.cutter_color)
                self.add_row_to_table(self.cutter_table, point.x(), point.y())

                if len(self.cutter) >= 2:
                    self.draw_line(QPoint(self.cutter[-2][0], self.cutter[-2][1]),
                                       QPoint(self.cutter[-1][0], self.cutter[-1][1]), self.cutter_color)

            else:
                if len(self.cutter) < 3:
                    self.create_message('Для замыкания отсекателя необходимо минимум 3 точки')
                else:
                    if cut.check_correct_polygon(self.cutter):
                        self.is_close = True
                        self.draw_line(QPoint(self.cutter[0][0], self.cutter[0][1]),
                                           QPoint(self.cutter[-1][0], self.cutter[-1][1]), self.cutter_color)
                    else:
                        self.draw_cutter(self.cutter, Qt.white)
                        self.create_message('Отсекатель должен быть выпуклым многоугольником')
                        self.cutter = []
                        self.cutter_table.setRowCount(0)
                        self.cutter_table.setSpan(self.cutter_table.rowCount() - 1, 0, 1, 2)

    def get_int(self, text, string):
        '''Ввод из поля'''
        result = None
        try:
            result = int(text)
        except:
            self.create_message(f'Ошибка: {string} - нецелое число')

        return result

    def add_point_from_lines(self):
        if len(self.all_segments) == 10:
            self.create_message('По заданию необходим ввод до 10 отрезков')
            return

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

        self.add_point(QPoint(x, y))

    def add_cutter_from_lines(self):
        xl = self.get_int(self.x_left_line.text(), 'координата Х точки отсекателя')

        if xl is None:
            return

        if xl < 0 or xl > self.image.width():
            self.create_message(f'Координата х может быть в диапазоне {0, self.image.width()}')
            return

        yl = self.get_int(self.y_left_line.text(), 'координата Y точки отсекателя')

        if yl is None:
            return

        if yl < 0 or yl > self.image.height():
            self.create_message(f'Координата y может быть в диапазоне {0, self.image.height()}')
            return

        self.add_cutter(QPoint(xl, yl), 0)

    def close_cutter(self):
        self.add_cutter(QPoint(0, 0), 1)

    """Очистка всей сцены"""
    def clear_all_scene(self):
        self.draw_scene.clear()
        self.all_segments = []
        self.cur_segment = []
        self.cutter = []
        self.is_close = False
        self.points_table.setRowCount(0)
        self.cutter_table.setRowCount(0)
        self.image = QImage(5000, 5000, QImage.Format_ARGB32)
        self.image.fill(Qt.white)
        self.draw_scene.addPixmap(QPixmap.fromImage(self.image))


    def do_cut(self):
        if len(self.all_segments) == 0:
            self.create_message('Должен быть добавлен хотя бы один отрезок.')
            return

        if len(self.cutter) <= 1:
            self.create_message('Отсутствует отсекатель')
            return

        if not self.is_close:
            self.create_message('Отсекатель не замкнут')
            return

        self.drawn = True
        self.add_point_button.setEnabled(False)
        self.add_cutter_button.setEnabled(False)
        self.set_line_color_button.setEnabled(False)
        self.set_cutter_color_button.setEnabled(False)
        self.set_cut_color_button.setEnabled(False)
        self.do_cut_button.setEnabled(False)

        for segment in self.all_segments:
            result = cut.cut_cyrus_beck(self.cutter, segment)

            if not (result is None):
                self.draw_line(QPoint(segment[0][0], segment[0][1]), QPoint(segment[1][0], segment[1][1]), Qt.white)
                self.draw_line(QPoint(segment[0][0], segment[0][1]), QPoint(result[0][0], result[0][1]), self.line_color)
                self.draw_line(QPoint(result[1][0], result[1][1]), QPoint(segment[1][0], segment[1][1]), self.line_color)
                self.draw_line(QPoint(result[0][0], result[0][1]), QPoint(result[1][0], result[1][1]), self.cut_color)

        self.add_point_button.setEnabled(True)
        self.add_cutter_button.setEnabled(True)
        self.set_line_color_button.setEnabled(True)
        self.set_cutter_color_button.setEnabled(True)
        self.set_cut_color_button.setEnabled(True)
        self.do_cut_button.setEnabled(True)
        self.drawn = False



if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()