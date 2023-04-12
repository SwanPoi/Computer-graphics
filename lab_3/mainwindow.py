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
        MainWindow.resize(1121, 791)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.scene_graphicsView = MyGraphicsView(self.centralwidget)
        self.scene_graphicsView.setMinimumSize(QtCore.QSize(944, 834))
        self.scene_graphicsView.setObjectName("scene_graphicsView")
        self.gridLayout.addWidget(self.scene_graphicsView, 0, 2, 4, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.dda_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.dda_pushButton.setGeometry(QtCore.QRect(10, 20, 101, 31))
        self.dda_pushButton.setObjectName("dda_pushButton")
        self.bresenham_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.bresenham_pushButton.setGeometry(QtCore.QRect(120, 20, 141, 28))
        self.bresenham_pushButton.setFlat(False)
        self.bresenham_pushButton.setObjectName("bresenham_pushButton")
        self.integer_bresenham_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.integer_bresenham_pushButton.setGeometry(QtCore.QRect(10, 60, 251, 28))
        self.integer_bresenham_pushButton.setObjectName("integer_bresenham_pushButton")
        self.step_bresenham_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.step_bresenham_pushButton.setGeometry(QtCore.QRect(10, 90, 251, 28))
        self.step_bresenham_pushButton.setObjectName("step_bresenham_pushButton")
        self.vu_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.vu_pushButton.setGeometry(QtCore.QRect(10, 120, 101, 31))
        self.vu_pushButton.setObjectName("vu_pushButton")
        self.library_pushButton = QtWidgets.QPushButton(self.groupBox)
        self.library_pushButton.setGeometry(QtCore.QRect(120, 120, 141, 31))
        self.library_pushButton.setObjectName("library_pushButton")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.x_start_label = QtWidgets.QLabel(self.groupBox_3)
        self.x_start_label.setGeometry(QtCore.QRect(10, 20, 111, 16))
        self.x_start_label.setObjectName("x_start_label")
        self.y_start_label = QtWidgets.QLabel(self.groupBox_3)
        self.y_start_label.setGeometry(QtCore.QRect(130, 20, 131, 16))
        self.y_start_label.setObjectName("y_start_label")
        self.x_start_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.x_start_lineEdit.setGeometry(QtCore.QRect(10, 40, 101, 16))
        self.x_start_lineEdit.setClearButtonEnabled(False)
        self.x_start_lineEdit.setObjectName("x_start_lineEdit")
        self.y_start_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.y_start_lineEdit.setGeometry(QtCore.QRect(130, 40, 121, 16))
        self.y_start_lineEdit.setObjectName("y_start_lineEdit")
        self.x_end_label = QtWidgets.QLabel(self.groupBox_3)
        self.x_end_label.setGeometry(QtCore.QRect(10, 60, 101, 16))
        self.x_end_label.setObjectName("x_end_label")
        self.y_end_label = QtWidgets.QLabel(self.groupBox_3)
        self.y_end_label.setGeometry(QtCore.QRect(130, 60, 121, 16))
        self.y_end_label.setObjectName("y_end_label")
        self.x_end_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.x_end_lineEdit.setGeometry(QtCore.QRect(10, 80, 101, 22))
        self.x_end_lineEdit.setObjectName("x_end_lineEdit")
        self.y_end_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.y_end_lineEdit.setGeometry(QtCore.QRect(120, 80, 121, 22))
        self.y_end_lineEdit.setObjectName("y_end_lineEdit")
        self.angle_label = QtWidgets.QLabel(self.groupBox_3)
        self.angle_label.setGeometry(QtCore.QRect(10, 110, 91, 21))
        self.angle_label.setObjectName("angle_label")
        self.angle_lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.angle_lineEdit.setGeometry(QtCore.QRect(120, 110, 121, 22))
        self.angle_lineEdit.setObjectName("angle_lineEdit")
        self.add_segment_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.add_segment_pushButton.setGeometry(QtCore.QRect(10, 140, 121, 31))
        self.add_segment_pushButton.setObjectName("add_segment_pushButton")
        self.add_spectrum_pushButton = QtWidgets.QPushButton(self.groupBox_3)
        self.add_spectrum_pushButton.setGeometry(QtCore.QRect(130, 140, 121, 31))
        self.add_spectrum_pushButton.setObjectName("add_spectrum_pushButton")
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 2)
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setTitle("")
        self.groupBox_5.setObjectName("groupBox_5")
        self.back_step_pushButton = QtWidgets.QPushButton(self.groupBox_5)
        self.back_step_pushButton.setGeometry(QtCore.QRect(0, 20, 121, 31))
        self.back_step_pushButton.setObjectName("back_step_pushButton")
        self.clear_pushButton = QtWidgets.QPushButton(self.groupBox_5)
        self.clear_pushButton.setGeometry(QtCore.QRect(0, 90, 131, 31))
        self.clear_pushButton.setObjectName("clear_pushButton")
        self.gridLayout.addWidget(self.groupBox_5, 3, 1, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName("groupBox_4")
        self.line_length_label = QtWidgets.QLabel(self.groupBox_4)
        self.line_length_label.setGeometry(QtCore.QRect(10, 30, 101, 16))
        self.line_length_label.setObjectName("line_length_label")
        self.line_length_lineEdit = QtWidgets.QLineEdit(self.groupBox_4)
        self.line_length_lineEdit.setGeometry(QtCore.QRect(120, 30, 111, 22))
        self.line_length_lineEdit.setObjectName("line_length_lineEdit")
        self.compare_steps_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.compare_steps_pushButton.setGeometry(QtCore.QRect(10, 60, 231, 41))
        self.compare_steps_pushButton.setObjectName("compare_steps_pushButton")
        self.compare_time_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.compare_time_pushButton.setGeometry(QtCore.QRect(10, 110, 231, 51))
        self.compare_time_pushButton.setObjectName("compare_time_pushButton")
        self.gridLayout.addWidget(self.groupBox_4, 2, 0, 1, 2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.line_color_label = QtWidgets.QLabel(self.groupBox_2)
        self.line_color_label.setGeometry(QtCore.QRect(10, 60, 111, 21))
        self.line_color_label.setText("")
        self.line_color_label.setObjectName("line_color_label")
        self.line_color_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.line_color_pushButton.setGeometry(QtCore.QRect(10, 20, 111, 28))
        self.line_color_pushButton.setObjectName("line_color_pushButton")
        self.background_color_pushButton = QtWidgets.QPushButton(self.groupBox_2)
        self.background_color_pushButton.setGeometry(QtCore.QRect(10, 90, 111, 31))
        self.background_color_pushButton.setObjectName("background_color_pushButton")
        self.background_color_label = QtWidgets.QLabel(self.groupBox_2)
        self.background_color_label.setGeometry(QtCore.QRect(10, 130, 111, 21))
        self.background_color_label.setText("")
        self.background_color_label.setObjectName("background_color_label")
        self.gridLayout.addWidget(self.groupBox_2, 3, 0, 1, 1)
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
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.program_menu.menuAction())
        self.menubar.addAction(self.author_menu.menuAction())
        self.menubar.addAction(self.exit_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Алгоритмы построения растровых отрезков"))
        self.dda_pushButton.setText(_translate("MainWindow", "ЦДА"))
        self.bresenham_pushButton.setText(_translate("MainWindow", "Алгоритм Брезенхема"))
        self.integer_bresenham_pushButton.setText(_translate("MainWindow", "Алгоритм Брезенхема (целочисленный)"))
        self.step_bresenham_pushButton.setText(_translate("MainWindow", "Брезенхем с устранением ступенчатости"))
        self.vu_pushButton.setText(_translate("MainWindow", "Алгоритм Ву"))
        self.library_pushButton.setText(_translate("MainWindow", "Библиотечный"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Ввод координат точек"))
        self.x_start_label.setText(_translate("MainWindow", "Х начала отрезка"))
        self.y_start_label.setText(_translate("MainWindow", "Y начала отрезка"))
        self.x_end_label.setText(_translate("MainWindow", "X конца отрезка"))
        self.y_end_label.setText(_translate("MainWindow", "Y конца отрезка"))
        self.angle_label.setText(_translate("MainWindow", "Угол поворота "))
        self.add_segment_pushButton.setText(_translate("MainWindow", "Построить отрезок"))
        self.add_spectrum_pushButton.setText(_translate("MainWindow", "Построить спектр"))
        self.back_step_pushButton.setText(_translate("MainWindow", "Шаг назад"))
        self.clear_pushButton.setText(_translate("MainWindow", "Очистить сцену"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Замеры"))
        self.line_length_label.setText(_translate("MainWindow", "Число повторов"))
        self.compare_steps_pushButton.setText(_translate("MainWindow", "Сравнение ступенчатости"))
        self.compare_time_pushButton.setText(_translate("MainWindow", "Сравнение временных характеристик"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Выбор цвета"))
        self.line_color_pushButton.setText(_translate("MainWindow", "Цвет отрезка"))
        self.background_color_pushButton.setText(_translate("MainWindow", "Цвет фона"))
        self.program_menu.setTitle(_translate("MainWindow", "О программе"))
        self.author_menu.setTitle(_translate("MainWindow", "Об авторе"))
        self.exit_menu.setTitle(_translate("MainWindow", "Выход"))
