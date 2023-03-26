from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, QTableWidgetItem
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QObject

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

    def change_bg_color(self, color):
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

        """Очистка экрана через меню"""
        self.clear = self.ui.exit_menu
        clear = QAction("Очистить графическую сцену", self)
        #clear.triggered.connect(self.clear_all_scene)
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


        """Кнопки"""
        self.dda_button = self.ui.dda_pushButton
        self.bresenham_button = self.ui.bresenham_pushButton
        self.integer_bresenham_button = self.ui.integer_bresenham_pushButton
        self.step_bresenham_button = self.ui.step_bresenham_pushButton
        self.vu_button = self.ui.vu_pushButton
        self.library_button = self.ui.library_pushButton

        self.change_line_color_button = self.ui.line_color_pushButton
        self.change_background_color_button = self.ui.background_color_pushButton

        self.add_line_button = self.ui.add_segment_pushButton
        self.add_spectrum_button = self.ui.add_spectrum_pushButton

        self.time_compare_button = self.ui.compare_time_pushButton
        self.step_compare_button = self.ui.compare_steps_pushButton

        self.step_back = self.ui.back_step_pushButton
        self.clear_button = self.ui.clear_pushButton

        """Привязка действий к нажатию кнопок"""
        #self.add_point_to_first_button.clicked.connect(self.add_point_to_first)


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



if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()