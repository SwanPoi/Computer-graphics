from mainwindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QAction, qApp, QGraphicsScene, QTableWidgetItem
from PyQt5.QtGui import QPen, QBrush
from PyQt5.QtCore import Qt, QObject

MOUSE_ADD = 0
ADD = 1
DELETE = 2
EDIT = 3

class GraphicScene(QGraphicsScene):
    def __init__(self):
        super(GraphicScene, self).__init__()
        """Массивы с координатами точек"""
        self.all_polygons = []
        self.cur_polygon = []
        self.table_coordinates = []
        self.buffer_coordinates= []

        self.color = Qt.red
        self.can_close = 1

        # self.setScene(self.scene)

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        modifiers = QApplication.keyboardModifiers()
        if event.button() == Qt.LeftButton:
            self.can_close = 1
            if len(self.cur_polygon) and modifiers == Qt.AltModifier:
                self.cur_polygon.append([self.cur_polygon[-1][0], event.scenePos().y()])
            elif len(self.cur_polygon) and modifiers == Qt.ControlModifier:
                self.cur_polygon.append([event.scenePos().x(), self.cur_polygon[-1][1]])
            else:
                self.cur_polygon.append([event.scenePos().x(), event.scenePos().y()])

            self.addEllipse(self.cur_polygon[-1][0], self.cur_polygon[-1][1], 5, 5)



            if len(self.cur_polygon) > 1:
                self.addLine(self.cur_polygon[-2][0], self.cur_polygon[-2][1], self.cur_polygon[-1][0],
                             self.cur_polygon[-1][1], pen=QPen(self.color, 3))
        elif event.button() == Qt.RightButton:
            if len(self.cur_polygon) > 2:
                self.addLine(self.cur_polygon[-1][0],
                                 self.cur_polygon[-1][1], self.cur_polygon[0][0], self.cur_polygon[0][1], pen=QPen(self.color, 3))
                self.all_polygons.append(self.cur_polygon)
                self.cur_polygon = []
            else:
                self.can_close = 0
        # self.update()



class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Лабораторная №1 по компьютерной графике")

        self.draw_view = self.ui.graphicsView

        self.draw_scene = GraphicScene()
        self.draw_view.setScene(self.draw_scene)
        """Словарь координат для таблиц"""
        self.first_dict = {'X:': [],
                           'Y:': []}
        self.second_dict = {'X:': [],
                            'Y:': []}

        """Таблицы"""
        self.points_table = self.ui.points_tableWidget
        '''
        self.first_table.setColumnCount(2)
        self.first_table.setHorizontalHeaderLabels([x for x in self.first_dict.keys()])
        self.first_table.viewport().installEventFilter(self)

        self.second_table.setColumnCount(2)
        self.second_table.setHorizontalHeaderLabels([x for x in self.second_dict.keys()])
        self.second_table.viewport().installEventFilter(self)
        '''
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

        """Кнопки"""
        self.delay_button = self.ui.dekay_pushButton
        self.without_delay_button = self.ui.without_delay_pushButton
        self.set_color_button = self.ui.color_pushButton
        self.add_point_button = self.ui.pushButton_2
        self.close_figure_button = self.ui.pushButton_3
        self.time_button = self.ui.time_pushButton

        """Привязка действий к нажатию кнопок"""


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
        msg.setText("")
        msg.exec()


    """Добавление точки в таблицу"""
    '''def set_data_to_table(self, dict, table):
        table.setRowCount(len(dict['X:']))
        for n, key in enumerate(dict.keys()):
            for m, item in enumerate(dict[key]):
                newitem = QTableWidgetItem(str(item))
                newitem.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                table.setItem(m, n, newitem)'''

    """Очистка всей сцены"""
    def clear_all_scene(self):
        self.draw_scene.clear()



if __name__ == '__main__':
    """Запуск приложения"""
    app = QApplication([])

    window = MyWindow()
    window.show()

    app.exec()