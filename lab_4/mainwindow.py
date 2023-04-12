# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsView

class MyGraphicsView(QGraphicsView):
    cnt_calls_resizeEvent = 0
    cnt_zoom = 0

    def __init__(self, parent):
        super().__init__(parent)
        self.cnt_calls_resizeEvent = 0
        self.cnt_zoom = 0

    def resizeEvent(self, event) -> None:
        if self.cnt_calls_resizeEvent == 0:
            self.cnt_calls_resizeEvent += 1
        else:
            self.scene().draw_axises(self.width(), self.height())

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        scale_factor = 1.5

        if event.angleDelta().y() > 0:
            self.scale(scale_factor, scale_factor)
            self.cnt_zoom += 1
        elif self.cnt_zoom != 0:
            self.scale(1 / scale_factor, 1 / scale_factor)
            self.cnt_zoom -= 1


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1121, 813)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scene_graphicsView = MyGraphicsView(self.centralwidget)
        self.scene_graphicsView.setMinimumSize(QtCore.QSize(944, 834))
        self.scene_graphicsView.setObjectName("scene_graphicsView")
        self.gridLayout.addWidget(self.scene_graphicsView, 0, 2, 4, 1)
        self.gridLayout.addWidget(self.scene_graphicsView, 0, 3, 3, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.canon_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.canon_pushButton.setGeometry(QtCore.QRect(10, 20, 271, 31))
        self.canon_pushButton.setObjectName("canon_pushButton")
        self.param_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.param_pushButton.setGeometry(QtCore.QRect(10, 57, 271, 31))
        self.param_pushButton.setObjectName("param_pushButton")
        self.bresenham_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.bresenham_pushButton.setGeometry(QtCore.QRect(10, 90, 271, 31))
        self.bresenham_pushButton.setObjectName("bresenham_pushButton")
        self.miidle_point_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.miidle_point_pushButton.setGeometry(QtCore.QRect(10, 130, 271, 31))
        self.miidle_point_pushButton.setObjectName("miidle_point_pushButton")
        self.library_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.library_pushButton.setGeometry(QtCore.QRect(10, 170, 271, 31))
        self.library_pushButton.setObjectName("library_pushButton")
        self.line_color_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.line_color_pushButton.setGeometry(QtCore.QRect(10, 240, 111, 31))
        self.line_color_pushButton.setObjectName("line_color_pushButton")
        self.background_color_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.background_color_pushButton.setGeometry(QtCore.QRect(140, 240, 131, 31))
        self.background_color_pushButton.setObjectName("background_color_pushButton")
        self.line_color_label = QtWidgets.QLabel(self.groupBox)
        self.line_color_label.setGeometry(QtCore.QRect(10, 280, 111, 21))
        self.line_color_label.setText("")
        self.line_color_label.setObjectName("line_color_label")
        self.background_color_label = QtWidgets.QLabel(self.groupBox)
        self.background_color_label.setGeometry(QtCore.QRect(140, 280, 131, 21))
        self.background_color_label.setText("")
        self.background_color_label.setObjectName("background_color_label")
        self.color_label = QtWidgets.QLabel(self.groupBox)
        self.color_label.setGeometry(QtCore.QRect(10, 210, 261, 21))
        self.color_label.setObjectName("color_label")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setGeometry(QtCore.QRect(0, 310, 295, 431))
        self.groupBox_3.setObjectName("groupBox_3")
        self.x_center_label = QtWidgets.QLabel(self.groupBox_3)
        self.x_center_label.setGeometry(QtCore.QRect(10, 20, 111, 16))
        self.x_center_label.setObjectName("x_center_label")
        self.y_center_label = QtWidgets.QLabel(self.groupBox_3)
        self.y_center_label.setGeometry(QtCore.QRect(130, 20, 131, 16))
        self.y_center_label.setObjectName("y_center_label")
        self.x_center_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.x_center_lineEdit.setGeometry(QtCore.QRect(10, 40, 101, 16))
        self.x_center_lineEdit.setClearButtonEnabled(False)
        self.x_center_lineEdit.setObjectName("x_center_lineEdit")
        self.y_center_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.y_center_lineEdit.setGeometry(QtCore.QRect(130, 40, 121, 16))
        self.y_center_lineEdit.setObjectName("y_center_lineEdit")
        self.circle_radius_label = QtWidgets.QLabel(self.groupBox_3)
        self.circle_radius_label.setGeometry(QtCore.QRect(10, 60, 101, 16))
        self.circle_radius_label.setObjectName("circle_radius_label")
        self.width_label = QtWidgets.QLabel(self.groupBox_3)
        self.width_label.setGeometry(QtCore.QRect(10, 90, 121, 16))
        self.width_label.setObjectName("width_label")
        self.circle_radius_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.circle_radius_lineEdit.setGeometry(QtCore.QRect(140, 60, 131, 16))
        self.circle_radius_lineEdit.setObjectName("circle_radius_lineEdit")
        self.width_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.width_lineEdit.setGeometry(QtCore.QRect(140, 90, 131, 16))
        self.width_lineEdit.setObjectName("width_lineEdit")
        self.height_label = QtWidgets.QLabel(self.groupBox_3)
        self.height_label.setGeometry(QtCore.QRect(10, 110, 121, 21))
        self.height_label.setObjectName("height_label")
        self.height_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.height_lineEdit.setGeometry(QtCore.QRect(140, 110, 131, 16))
        self.height_lineEdit.setObjectName("height_lineEdit")
        self.add_circle_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.add_circle_pushButton.setGeometry(QtCore.QRect(10, 140, 141, 31))
        self.add_circle_pushButton.setObjectName("add_circle_pushButton")
        self.add_ellipse_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.add_ellipse_pushButton.setGeometry(QtCore.QRect(160, 140, 121, 31))
        self.add_ellipse_pushButton.setObjectName("add_ellipse_pushButton")
        self.start_radius_label = QtWidgets.QLabel(self.groupBox_3)
        self.start_radius_label.setGeometry(QtCore.QRect(10, 190, 121, 16))
        self.start_radius_label.setObjectName("start_radius_label")
        self.end_radius_label = QtWidgets.QLabel(self.groupBox_3)
        self.end_radius_label.setGeometry(QtCore.QRect(10, 230, 111, 16))
        self.end_radius_label.setObjectName("end_radius_label")
        self.start_radius_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.start_radius_lineEdit.setGeometry(QtCore.QRect(10, 210, 101, 16))
        self.start_radius_lineEdit.setObjectName("start_radius_lineEdit")
        self.end_radius_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.end_radius_lineEdit.setGeometry(QtCore.QRect(10, 250, 101, 16))
        self.end_radius_lineEdit.setObjectName("end_radius_lineEdit")
        self.step_circle_label = QtWidgets.QLabel(self.groupBox_3)
        self.step_circle_label.setGeometry(QtCore.QRect(10, 270, 101, 16))
        self.step_circle_label.setObjectName("step_circle_label")
        self.step_circle_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.step_circle_lineEdit.setGeometry(QtCore.QRect(10, 290, 101, 16))
        self.step_circle_lineEdit.setObjectName("step_circle_lineEdit")
        self.count_circles_label = QtWidgets.QLabel(self.groupBox_3)
        self.count_circles_label.setGeometry(QtCore.QRect(10, 310, 121, 16))
        self.count_circles_label.setObjectName("count_circles_label")
        self.count_circles_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.count_circles_lineEdit.setGeometry(QtCore.QRect(10, 330, 101, 21))
        self.count_circles_lineEdit.setObjectName("count_circles_lineEdit")
        self.circle_spectrum_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.circle_spectrum_pushButton.setGeometry(QtCore.QRect(0, 390, 131, 31))
        self.circle_spectrum_pushButton.setObjectName("circle_spectrum_pushButton")
        self.start_width_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.start_width_lineEdit.setGeometry(QtCore.QRect(150, 210, 121, 16))
        self.start_width_lineEdit.setObjectName("start_width_lineEdit")
        self.start_width_label = QtWidgets.QLabel(self.groupBox_3)
        self.start_width_label.setGeometry(QtCore.QRect(150, 190, 141, 16))
        self.start_width_label.setObjectName("start_width_label")
        self.start_height_label = QtWidgets.QLabel(self.groupBox_3)
        self.start_height_label.setGeometry(QtCore.QRect(150, 230, 131, 16))
        self.start_height_label.setObjectName("start_height_label")
        self.start_height_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.start_height_lineEdit.setGeometry(QtCore.QRect(150, 250, 121, 16))
        self.start_height_lineEdit.setObjectName("start_height_lineEdit")
        self.step_ellipse_label = QtWidgets.QLabel(self.groupBox_3)
        self.step_ellipse_label.setGeometry(QtCore.QRect(140, 270, 141, 20))
        self.step_ellipse_label.setObjectName("step_ellipse_label")
        self.step_ellipse_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.step_ellipse_lineEdit.setGeometry(QtCore.QRect(150, 290, 121, 16))
        self.step_ellipse_lineEdit.setObjectName("step_ellipse_lineEdit")
        self.count_ellipse_label = QtWidgets.QLabel(self.groupBox_3)
        self.count_ellipse_label.setGeometry(QtCore.QRect(150, 340, 121, 16))
        self.count_ellipse_label.setObjectName("count_ellipse_label")
        self.count_ellipse_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.count_ellipse_lineEdit.setGeometry(QtCore.QRect(140, 360, 131, 16))
        self.count_ellipse_lineEdit.setObjectName("count_ellipse_lineEdit")
        self.ellipse_spectrum_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.ellipse_spectrum_pushButton.setGeometry(QtCore.QRect(140, 390, 141, 31))
        self.ellipse_spectrum_pushButton.setObjectName("ellipse_spectrum_pushButton")
        self.rx_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.rx_pushButton.setGeometry(QtCore.QRect(140, 310, 71, 28))
        self.rx_pushButton.setObjectName("rx_pushButton")
        self.ry_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.ry_pushButton.setGeometry(QtCore.QRect(220, 310, 61, 28))
        self.ry_pushButton.setObjectName("ry_pushButton")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 3, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1121, 26))
        self.menubar.setObjectName("menubar")
        self.program_menu = QtWidgets.QMenu(self.menubar)
        self.program_menu.setObjectName("program_menu")
        self.author_menu = QtWidgets.QMenu(self.menubar)
        self.author_menu.setObjectName("author_menu")
        self.exit_menu = QtWidgets.QMenu(self.menubar)
        self.exit_menu.setObjectName("exit_menu")
        self.clear_menu = QtWidgets.QMenu(self.menubar)
        self.clear_menu.setObjectName("clear_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.program_menu.menuAction())
        self.menubar.addAction(self.author_menu.menuAction())
        self.menubar.addAction(self.exit_menu.menuAction())
        self.menubar.addAction(self.clear_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Алгоритмы построения окружностей/эллипсов"))
        self.canon_pushButton.setText(_translate("MainWindow", "Каноническое уравнение"))
        self.param_pushButton.setText(_translate("MainWindow", "Параметрическое уравнение"))
        self.bresenham_pushButton.setText(_translate("MainWindow", "Алгоритм Брезенхема"))
        self.miidle_point_pushButton.setText(_translate("MainWindow", "Алгоритм средней точки"))
        self.library_pushButton.setText(_translate("MainWindow", "Библиотечный"))
        self.line_color_pushButton.setText(_translate("MainWindow", "Цвет линии"))
        self.background_color_pushButton.setText(_translate("MainWindow", "Цвет фона"))
        self.color_label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">Выбор цвета</p></body></html>"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Ввод параметров окружности/эллипса"))
        self.x_center_label.setText(_translate("MainWindow", "Х центра"))
        self.y_center_label.setText(_translate("MainWindow", "Y центра"))
        self.circle_radius_label.setText(_translate("MainWindow", "R окружности"))
        self.width_label.setText(_translate("MainWindow", "Ширина эллипса Rx"))
        self.height_label.setText(_translate("MainWindow", "Высота эллипса Ry"))
        self.add_circle_pushButton.setText(_translate("MainWindow", "Построить окружность"))
        self.add_ellipse_pushButton.setText(_translate("MainWindow", "Построить эллипс"))
        self.start_radius_label.setText(_translate("MainWindow", "Начальный радиус"))
        self.end_radius_label.setText(_translate("MainWindow", "Конечный радиус"))
        self.step_circle_label.setText(_translate("MainWindow", "Шаг радиуса"))
        self.count_circles_label.setText(_translate("MainWindow", "Число окружностей"))
        self.circle_spectrum_pushButton.setText(_translate("MainWindow", "Спектр окружностей"))
        self.start_width_label.setText(_translate("MainWindow", "Начальная ширина Rx"))
        self.start_height_label.setText(_translate("MainWindow", "Начальная высота Ry"))
        self.step_ellipse_label.setText(_translate("MainWindow", "Шаг изменения полуоси"))
        self.count_ellipse_label.setText(_translate("MainWindow", "Число эллипсов"))
        self.ellipse_spectrum_pushButton.setText(_translate("MainWindow", "Спектр эллипсов"))
        self.rx_pushButton.setText(_translate("MainWindow", "Rx"))
        self.ry_pushButton.setText(_translate("MainWindow", "Ry"))
        self.program_menu.setTitle(_translate("MainWindow", "О программе"))
        self.author_menu.setTitle(_translate("MainWindow", "Об авторе"))
        self.exit_menu.setTitle(_translate("MainWindow", "Выход"))
        self.clear_menu.setTitle(_translate("MainWindow", "Очистка экрана"))
